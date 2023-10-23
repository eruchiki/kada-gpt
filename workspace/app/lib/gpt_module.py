from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain import LLMChain
from lib.vector_module import documents_search
from langchain.callbacks import get_openai_callback
import os
import json
import tiktoken
from lib.const import *
import re
import asyncio

# compose(最終的な出力回答)部分のプロンプトテンプレートを作成
# 引数：ドキュメントのリスト(要素として，ドキュメント情報とメタデータを含む)
def create_prompt_template_for_compose():
    system_template = """あなたは人間と友好的に会話するAIです。
AIは以下に示される番号付きのドキュメント情報を使って、質問に対して詳細かつ正確な回答を提供します。
AIは回答に使用したドキュメントの番号を、該当する箇所に引用の形式で示します。
引用例：これは引用です[0-1]。これも引用です[2-5]。これは複数の引用を使っています[4-0][2-2]。この文書には引用が必要ありません。
AIはドキュメント情報を使って質問に回答できない場合、「わかりません」と回答します。
ドキュメントはデータベースに保存されており、ドキュメント情報グループの先頭にはそのファイル名とグループ番号が与えられるので考慮に入れてください。
グループ内のドキュメント情報は文章の塊ごとに改行で区切られています。情報は塊同士で分けて考えてください。

# ドキュメント情報
{info}
"""
    system_message_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["info"],
            template=system_template
        )
    )
    prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        HumanMessagePromptTemplate.from_template("{query}")
    ])
    return prompt

def create_prompt_info_for_compose(info_list):
    selected_info_list = [info for info in info_list if info != []]
    selected_info_list = sorted(selected_info_list, key=lambda x:x[0][0].metadata["filename"])

    file_list = []
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
                system_template_info += f"  - [{file_num}-{item_num}] {info.page_content}\n"
                item_num += 1
            system_template_info += "\n"
    return system_template_info, file_list

def chunk_split(text_data,chunk_num=6):
    text_splitter = RecursiveCharacterTextSplitter(
        separators = ["\n\n","\n","。","．","."],
        keep_separator = True,
        chunk_size = chunk_num,
        chunk_overlap = 0
    )
    split_text = text_splitter.split_text(text_data)
    for i in range(1, len(split_text)):
        split_text[i-1] += split_text[i][0]
        split_text[i] = split_text[i][1:]
    return split_text

# select(LLMを使った参考情報の選択)部分のプロンプトテンプレートを作成
# 引数：ドキュメントの一部のリスト(要素として，ドキュメント情報とメタデータを含む)
def create_prompt_template_for_select():
    system_template = """質問文と、その回答として利用できるかわかっていないドキュメントがあります。
質問文に対して回答を考えるときに参考になりそうなドキュメントの番号を取り出してください。
番号付きドキュメントそれぞれは、元は先頭から結合された1つの文書でした。
ドキュメントのファイル名が与えられるので考慮してください。

# 制約
- 番号について詳細かつ正確に回答してください
- 参考になりそうな文章の番号を全て取り出してください
- 参考になりそうな情報が複数ある場合は、必ずすべて答えてください
- 参考になりそうな情報は広めに取ってください
- 番号に該当する文章は出力しないでください
- ドキュメント全ての番号を選択するのはコスパが悪いので、絶対に避けてください
- 参考になりそうな情報がない場合や、質問文とドキュメントの内容に関係が無いと思われる場合は、必ず出力の例に沿って「回答の生成に使えそうな情報がありません」と回答してください
- 回答に矛盾が生じるときは出力の例に沿って「回答の生成に使えそうな情報がありません」と回答してください
- 出力の例を参考に回答してください。それ以外の形式で回答しないでください

# 出力の例
- 回答の生成にはドキュメントの[1101]から[1124]の情報が使えそうです
- 回答の生成にはドキュメントの[892]から[901]、[1023]から[1028]の情報が使えそうです
- 回答の生成にはドキュメントの[97]の情報が使えそうです
- 回答の生成にはドキュメントの[425]、[644]から[656]、[700]の情報が使えそうです
- 回答の生成には使えそうな情報がありません

# ドキュメントのファイル名
{filename}

# ドキュメントの内容
{info}
# 質問文
{query}
"""
    prompt=PromptTemplate(
        input_variables=["filename", "info", "query"],
        template=system_template
    )
    return prompt

def create_prompt_info_for_select(relate_info):
    # ドキュメントを更に分割しつつ，元のチャンクグループで列挙
    system_template_info = ""
    relate_info_cut = []
    un_num = 0
    system_template_filename = f"{relate_info.metadata['filename']}"
    split_text = chunk_split(relate_info.page_content)
    for i, text in enumerate(split_text):
        info = Document(
            page_content=text,
            metadata={"filename":relate_info.metadata["filename"], "rank":relate_info.metadata["rank"], "item_number":i}
        )
        relate_info_cut.append(info)
        system_template_info += f"[{un_num}] {info.page_content}\n"
        un_num += 1

    return system_template_info, system_template_filename, relate_info_cut

def save_memory(memory,query,response):
    memory.chat_memory.add_user_message(query)
    memory.chat_memory.add_ai_message(response)

def save_log(query,response,related_data,score_data):
    log_file = "./log.json"
    new_data = {"query":query,"response":response,"relate":related_data,"score":score_data}
    if os.path.exists(log_file):
        with open(log_file,mode="r",encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = []
    log_data.append(new_data)
    with open(log_file, mode='w',encoding="utf-8") as f:
        json.dump(log_data, f,ensure_ascii=False)

# selectionのプロンプトでGPT3.5に問い合わせ
async def get_answer(llm_chain, _filename, _info, _query):
    try:
        with get_openai_callback() as cb:
            resp = await asyncio.wait_for(llm_chain.arun({"query":_query,"info":_info,"filename":_filename}), 240)
        resp = re.sub(r'\s', '', resp)
        cost = cb.total_cost
    except Exception as e:
        print(e)
        resp = None
        cost = 0
    return [resp, cost]

# selectionを並列処理
async def generate_concurrently(info_list, filename_list, query, prompt, model="gpt-3.5-turbo"):
    # モデル定義
    llm = ChatOpenAI(temperature=0, model_name=model, request_timeout=240)
    # プロンプト設定
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True
    )
    # 並列処理
    tasks = [get_answer(llm_chain, _filename, _info, query) for _info, _filename in zip(info_list, filename_list)]
    return await asyncio.gather(*tasks)

def selection_format(response_list):
    number_list = []
    for response in response_list:
        range_list = []
        range_tuples = re.findall(r'\[(\d+)\]から\[(\d+)\]', response)
        for range_tuple in range_tuples:
            range_list = sorted([int(range_tuple[0]), int(range_tuple[1])])
            range_list = list(range(range_list[0], range_list[1]))
        one_num_list = re.findall(r'\[(\d+)\]', response)
        one_num_list = [int(s) for s in one_num_list]
        number_list.append(sorted(list(set(one_num_list + range_list))))
    return number_list

def selection_extraction(info_list, response_list):
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
    return selected_info_list

# select処理を行う
# Qdrantから取ってきた文書に対し，情報の取捨選択をGPTに行わせる
def select(related_data, query):
    prompt = create_prompt_template_for_select()
    string_info_list = []
    info_list = []
    filename_list = []
    for data in related_data:
        string_info, filename, info = create_prompt_info_for_select(data)
        string_info_list.append(string_info)
        info_list.append(info)
        filename_list.append(filename)
    tmp_list =  asyncio.run(generate_concurrently(string_info_list, filename_list, query, prompt))
    total_cost = sum([cost for resp, cost in tmp_list])
    response = [resp for resp, cost in tmp_list]
    selected_info_list = selection_extraction(info_list, response)
    return selected_info_list, response, total_cost

def compose(selected_info_list, query, llm, max_token):
    prompt = create_prompt_template_for_compose()
    string_info, file_list = create_prompt_info_for_compose(selected_info_list)
    input_token_size = llm.get_num_tokens(prompt.format(query=query, info=string_info))
    if input_token_size > max_token:
        response = "トークンサイズが制限を超えています"
        return response,file_list,0,0
    llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    )
    with get_openai_callback() as cb:
        response = llm_chain.run({"query":query,"info":string_info})
    cost = cb.total_cost
    # save_memory(memory,query,response)
    # save_log(query,response,[data.page_content for data in related_data],score_data)
    ret = re.findall(r"\[([0-9]+)", response)
    nums_ref = sorted(list(set(map(int, ret))))
    print(response)
    return response,file_list,cost,nums_ref

def chat(query,llm,memory,db,relate_num=3,filter=None, max_token=4000):
    related_data,score_data = documents_search(db,query,top_k=relate_num,filter=filter)
    for i, item in enumerate(related_data):
        item.metadata["rank"] = i

    print(related_data)
    
    selected_info_list, response, cost = select(related_data, query)
    print(response)
    print(cost)
    final_response, file_list, compose_cost, nums_ref = compose(selected_info_list, query, llm, max_token)
    print(compose_cost)

    total_cost = cost + compose_cost
    return final_response, file_list, total_cost, nums_ref
