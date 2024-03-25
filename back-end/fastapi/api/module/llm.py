from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from template import CHAT_TEMPLATE, SYSTEM_TEMPLATE
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain import LLMChain
from langchain.callbacks import get_openai_callback
import tiktoken
import re
import asyncio
import time


def create_prompt_info_for_compose(info_list: list) -> tuple[str, list, list]:
    selected_info_list = [info for info in info_list if info != []]
    selected_info_list = sorted(
        selected_info_list, key=lambda x: x[0][0].metadata["filename"]
    )
    for_log_quote_lines, file_list = [], []
    system_template_info = ""
    current_file = ""
    file_num = -1
    item_num = 0
    for info_group in selected_info_list:
        if current_file != info_group[0][0].metadata["filename"]:
            file_num += 1
            item_num = 0
            current_file = info_group[0][0].metadata["filename"]
            file_list.append(info_group[0][0].metadata["filename"])
            system_template_info += f"- [{file_num}] {current_file}\n"
        for info_set in info_group:
            for info in info_set:
                system_template_info += (
                    f"  - [{file_num}-{item_num}] {info.page_content}\n"
                )
                for_log_quote_lines.append(
                    [f"{file_num}-{item_num}", info.page_content]
                )
                item_num += 1
            system_template_info += "\n"
    return system_template_info, file_list, for_log_quote_lines


def chunk_split(text_data: str, chunk_num: int = 6) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "．", "."],
        keep_separator=True,
        chunk_size=chunk_num,
        chunk_overlap=0,
    )
    split_text = text_splitter.split_text(text_data)
    for i in range(1, len(split_text)):
        split_text[i - 1] += split_text[i][0]
        split_text[i] = split_text[i][1:]
    return split_text


# selectionのプロンプトでGPT3.5に問い合わせ
async def get_answer(
    llm_chain: Any, _filename: str, _info: Any, _query: str, sem: Any
) -> list:
    async with sem:
        try:
            with get_openai_callback() as cb:
                resp = await asyncio.wait_for(
                    llm_chain.arun(
                        {"query": _query, "info": _info, "filename": _filename}
                    ),
                    65,
                )
            resp = re.sub(r"\s", "", resp)
            cost = cb.total_cost
        except Exception as e:
            print(e)
            resp = "エラー: " + str(e)
            cost = 0
        return [resp, cost]


# selectionを並列処理
async def generate_concurrently(
    info_list: list,
    filename_list: list,
    query: str,
    prompt: str,
    model: str = "gpt-3.5-turbo",
) -> None:
    # モデル定義
    llm = ChatOpenAI(temperature=0, model_name=model, request_timeout=12)
    # プロンプト設定
    llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    sem = asyncio.Semaphore(10)  # セマフォ
    # 並列処理
    tasks = [
        get_answer(llm_chain, _filename, _info, query, sem)
        for _info, _filename in zip(info_list, filename_list)
    ]
    return await asyncio.gather(*tasks)


def compose(selected_info_list: list, query: str, llm: Any):
    system_message_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["info"],
            template=CHAT_TEMPLATE
        )
    )
    prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        HumanMessagePromptTemplate.from_template("{query}")
    ])
    string_info, file_list, for_log_quote_lines = create_prompt_info_for_compose(selected_info_list)
    prompt_str = prompt.format(query=query, info=string_info)
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
    )
    try:
        with get_openai_callback() as cb:
            response = llm_chain.run({"query":query,"info":string_info})
    except Exception as e:
        print(e)
        response = "エラー: " + str(e)
    cost = cb.total_cost
    print(response)
    ret = re.findall(r"\[([0-9]+)\-[0-9]+\]", response)
    ret += re.findall(r"\[([0-9]+)\]", response)
    ret_lines = re.findall(r"\[([0-9]+\-[0-9]+)\]", response)
    nums_ref = sorted(list(set(map(int, ret))))

    res_quote_lines = [{"number":i,"sentence":line} for i, line in for_log_quote_lines if i in ret_lines]
    res_quote_files = [{"number":i,"file_name":file} for i, file in enumerate(file_list) if i in nums_ref]

    for_log_compose_data = [prompt_str, response, cost, res_quote_lines, res_quote_files]
    return response,res_quote_files,cost,for_log_compose_data,

def chat_default(query: str, model: Any, db: Any, relate_num: int = 4, filter: dict = None) -> :
    start_time = time.time()
    llm = ChatOpenAI(temperature=0, model_name=model, request_timeout=300)
    input_data = [query, model, relate_num]

    related_data, score_data = documents_search(
        db, query, top_k=relate_num, filter=filter
    )
    for i, item in enumerate(related_data):
        item.metadata["rank"] = i
    related_info = []
    for relate in related_data:
        group = []
        split_text = chunk_split(relate.page_content)
        for i, text in enumerate(split_text):
            info = Document(
                page_content=text,
                metadata={
                    "filename": relate.metadata["filename"],
                    "rank": relate.metadata["rank"],
                    "item_number": i,
                },
            )
            group.append(info)
        related_info.append([group])

    retriever_data = [related_data, score_data]
    db_time = time.time()

    final_response, file_list, total_cost, for_log_compose_data = compose(
        related_info, query, llm
    )

    compose_time = time.time()
    system_data = [start_time, db_time, db_time, compose_time, "default"]
    # save_chat_log(
    #     input_data, retriever_data, [], for_log_compose_data, system_data
    # )
    return final_response, file_list, total_cost, start_time
