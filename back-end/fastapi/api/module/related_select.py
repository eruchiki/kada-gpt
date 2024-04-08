from langchain.prompts import (
    PromptTemplate,
)
from template import SYSTEM_TEMPLATE
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain import LLMChain
from api.module.preprocessing import chunk_split
from langchain.callbacks import get_openai_callback
from typing import Any
import re
import asyncio


def create_prompt_info_for_select(
    relate_info: Document,
) -> tuple[str, str, list]:
    # ドキュメントを更に分割しつつ，元のチャンクグループで列挙
    system_template_info = ""
    relate_info_cut = []
    un_num = 0
    system_template_filename = f"{relate_info.metadata['filename']}"
    split_text = chunk_split(relate_info.page_content)
    for i, text in enumerate(split_text):
        info = Document(
            page_content=text,
            metadata={
                "filename": relate_info.metadata["filename"],
                "rank": relate_info.metadata["rank"],
                "item_number": i,
            },
        )
        relate_info_cut.append(info)
        system_template_info += f"[{un_num}] {info.page_content}\n"
        un_num += 1
    return system_template_info, system_template_filename, relate_info_cut


# Qdrantから取ってきた文書に対し，情報の取捨選択をGPTに行わせる
def select(related_data: list, query: str) -> tuple[list, int, list]:
    prompt = PromptTemplate(
        input_variables=["filename", "info", "query"], template=SYSTEM_TEMPLATE
    )
    string_info_list = []
    info_list = []
    filename_list = []

    select_data_format = []
    for data in related_data:
        string_info, filename, info = create_prompt_info_for_select(data)
        select_data_format.append(
            prompt.format(query=query, info=string_info, filename=filename)
        )
        string_info_list.append(string_info)
        info_list.append(info)
        filename_list.append(filename)
    tmp_list = asyncio.run(
        generate_concurrently(string_info_list, filename_list, query, prompt)
    )
    each_cost = [cost for resp, cost in tmp_list]
    total_cost = sum(each_cost)
    response = [resp for resp, cost in tmp_list]
    selected_info_list, number_list = selection_extraction(info_list, response)

    for_log_select_data = []
    for prompt_str, response, cost, res_format, select_lines in zip(
        select_data_format,
        response,
        each_cost,
        number_list,
        selected_info_list,
    ):
        for_log_select_data.append(
            [prompt_str, response, cost, res_format, select_lines]
        )

    return selected_info_list, total_cost, for_log_select_data


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
    prompt: PromptTemplate,
    model: str = "gpt-3.5-turbo",
) -> Any:
    # モデル定義
    llm = ChatOpenAI(temperature=0, model=model, timeout=12)
    # プロンプト設定
    llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    sem = asyncio.Semaphore(10)  # セマフォ
    # 並列処理
    tasks = [
        get_answer(llm_chain, _filename, _info, query, sem)
        for _info, _filename in zip(info_list, filename_list)
    ]
    return await asyncio.gather(*tasks)


# selectのformat
def selection_format(response_list: list) -> list:
    number_list = []
    for response in response_list:
        range_list = []
        range_tuples = re.findall(r"\[(\d+)\]から\[(\d+)\]", response)
        for range_tuple in range_tuples:
            range_list = sorted([int(range_tuple[0]), int(range_tuple[1])])
            range_list = list(range(range_list[0], range_list[1]))
        one_num_list = re.findall(r"\[(\d+)\]", response)
        one_num_list = [int(s) for s in one_num_list]
        number_list.append(sorted(list(set(one_num_list + range_list))))
    return number_list


def selection_extraction(
    info_list: list, response_list: list
) -> tuple[list, list]:
    selected_info_list = []
    number_list = selection_format(response_list)

    for infos, nums in zip(info_list, number_list):
        info_group = []
        dst_info = []
        for info in infos:
            if info.metadata["item_number"] in nums:
                info_group.append(info)
            else:
                if len(info_group) > 0:
                    dst_info.append(info_group)
                info_group = []
        if len(info_group) > 0:
            dst_info.append(info_group)
        selected_info_list.append(dst_info)
    return selected_info_list, number_list
