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
def create_prompt_template_for_compose(relate_data):
    system_template = """あなたは人間と友好的に会話するAIです。
AIは以下に示される番号付きのドキュメント情報を使って、質問に対して詳細かつ正確な回答を提供します。
AIは回答に使用したドキュメントの番号を、該当する箇所に引用の形式で示します。例：[0-1],[2-5],[4-0]
AIはドキュメント情報を使って質問に回答できない場合、「わかりません」と回答します。
ドキュメントはデータベースに保存されており、ドキュメント情報グループの先頭にはそのファイル名とグループ番号が与えられるので考慮に入れてください。
"""
    # ファイル名順に並び替え
    relate_info = sorted(relate_data, key=lambda x:x.metadata["filename"])

    # ドキュメント情報をファイル名ごとにグルーピングして列挙
    current_file = ""
    group_num = -1
    item_num = 0
    for info in relate_info:
        if info.metadata["filename"] != current_file:
            group_num += 1
            item_num = 0
            current_file = info.metadata["filename"]
            system_template += f"- [{group_num}] {current_file}\n"
        system_template += f"  - [{group_num}-{item_num}] {info.page_content}\n"
        item_num += 1

    system_message_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=[],
            template=system_template
        )
    )
    prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        HumanMessagePromptTemplate.from_template("{query}")
    ])
    return prompt, relate_info

def chunk_split(text_data,chunk_num=6):
    text_splitter = RecursiveCharacterTextSplitter(
        separators = ["\n\n","\n","。","．",".","、","，",","],
        keep_separator = True,
        chunk_size = chunk_num,
        chunk_overlap = 0
    )
    return text_splitter.split_text(text_data)

# select(LLMを使った参考情報の選択)部分のプロンプトテンプレートを作成
# 引数：ドキュメントの一部のリスト(要素として，ドキュメント情報とメタデータを含む)
def create_prompt_template_for_select():
#     system_template = """あなたは回答を生成するのに必要な情報を選択するだけのAIです。
# AIは以下に示される番号付きのドキュメント情報から、質問に対する回答を生成するときに必要と思われる文章の番号を全て選択します。
# 選んだ情報の番号は、カンマで区切って列挙します。角括弧で囲う必要はありません。例：0,3,4
# AIはドキュメント情報から使えそうな文章が見つからない場合、カンマを1つだけ出力します。
# {info}
# """
# AIは質問に対する回答生成に必要だと思われる文章の番号だけを全て出力し、それ以外の言葉を話しません。
#     system_template = """あなたは質問に対して数字とカンマのみで応答するAIです。
# AIは以下に示される番号付きのドキュメント情報から、質問に対する回答を生成するときに必要と思われる文章の番号を全て選択します。
# ドキュメント情報は、ファイル名のグループ毎に分けられています。
# グループ内の番号付き文章それぞれは、元は先頭から結合された1つの文書です。
# 選んだ情報の番号は、カンマで区切って列挙します。角括弧で囲う必要はありません。例：0,3,4
# AIはドキュメント情報から使えそうな文章が見つからない場合、カンマを1つだけ出力します。
# AIは質問に対する回答生成に必要だと思われるドキュメント番号だけを出力し、それ以外の言葉を話しません。
# また、必要のない番号も出力しません。
# {info}
# """
# ドキュメントはデータベースに保存されており、ドキュメント情報グループの先頭にはそのファイル名が与えられます。
#     system_template = """あなたは質問に対して番号の列挙のみで応答するAIです。
# AIは以下に示される番号付きのドキュメント情報から、質問に対する回答を生成するときに必要と思われる文章の番号を全て選択します。
# ドキュメント情報は、ファイル名のグループ毎に分けられています。
# グループ内の番号付き文章それぞれは、元は先頭から結合された1つの文書です。
# 選んだ情報の番号は、カンマで区切って列挙します。角括弧で囲う必要はありません。例：0,3,4,5,8,21,44
# AIはドキュメント情報から使えそうな文章が見つからない場合、カンマを1つだけ出力します。
# AIは質問に対する回答生成に必要だと思われるドキュメント番号だけを出力し、それ以外の言葉を話しません。
# {info}
# """
#     system_template = """Humanからの質問と、その回答として利用できるかわかっていないドキュメントがあります。
# ドキュメントからHumanの質問に対する回答に使用できそうな文章の番号を全て取り出してください。
# ドキュメントはデータベースに保存されており、そのファイル名が与えられるので考慮にいれてください。
# 同一ファイル内の番号付き文章それぞれは、元は先頭から結合された1つの文書でした。
# それを適当な長さ毎に区切って番号を振ってあります。
# Humanの質問に対する回答に使用できそうな文章の番号を若い順に列挙してください。
# また、番号を列挙した後、なぜそれを選んだのかの理由を簡単に述べてください。

# # 制約
# - 使用できそうな文章の番号だけを取り出してください
# - 出力はJSON形式で、Numberのリストで回答してください
# - 使用できそうな情報がない場合は空のリスト"[]"を出力してください

# # ドキュメントの内容
# {info}
# """

# 機械学習のデータ圧縮方法とサーバ管理演習について教えて
# 機械学習のデータ圧縮手法の評価項目はどのようになっていますか？
    system_template = """Humanからの質問と、その回答として利用できるかわかっていないドキュメントがあります。
ドキュメントからHumanの質問に対する回答に使用できそうな文章の番号を取り出してください。
ドキュメントはデータベースに保存されており、そのファイル名が与えられるので考慮にいれてください。
同一ファイル内の番号付き文章それぞれは、元は先頭から結合された1つの文書でした。
それを適当な長さ毎に区切って番号を振ってあります。

# 制約
- 使用できそうな文章の番号だけを取り出してください
- その番号に該当する文章は出力しないでください
- 使用できそうな情報がない場合は「使えそうな文章がありません」と回答してください

# 出力の例1
"明日の天気を教えて"という質問の回答には「明日の天気.pdf」の1102から1124までの情報が使えそうです。

# 出力の例2
"日本の文化を学びたい"という質問の回答には「日本の文化.pdf」の892から901および「我が国の歴史.pdf」の1023から1028までの情報が使えそうです。

# ドキュメントの内容
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
        # HumanMessagePromptTemplate.from_template("{query}\n\nAI: 以下の番号の文章が回答に使用できそうです。\n[")
        HumanMessagePromptTemplate.from_template("{query}")
    ])
    return prompt

#     system_template = """
# あなたは優秀なオフィスワーカー。
# あなたは友人からこのような質問「'{query}'」がありました。また、その回答として利用できるかわかっていないドキュメントがあります。
# ドキュメントから質問に対する回答を考える際に参考になりそうな文章の番号を取り出してください。
# ドキュメントはデータベースに保存されており、そのファイル名が与えられるので考慮にいれてください。
# 同一ファイル内の番号付き文章それぞれは、元は先頭から結合された1つの文書でした。
# それを適当な長さ毎に区切って番号を振ってあります。

# # 制約
# - 参考になりそうな文章の番号だけを取り出してください
# - その番号に該当する文章は出力しないでください
# - 使用できそうな情報がない場合は「使えそうな文章がありません」と回答してください

# # 出力の例1
# 「明日の天気を教えて」という質問には「明日の天気.pdf」の1102から1124までの情報が使えそうです。

# # 出力の例2
# 「日本の文化を学びたい」という質問には「日本の文化.pdf」の892から901および「我が国の歴史.pdf」の1023から1028までの情報が使えそうです。

# # ドキュメントの内容
# {info}
# """
#     # system_message_prompt = SystemMessagePromptTemplate(
#     #     prompt=PromptTemplate(
#     #         input_variables=["info"],
#     #         template=system_template
#     #     )
#     # )
#     prompt = PromptTemplate(
#         input_variables=["info", "query"],
#         template=system_template
#     )
#     # prompt = ChatPromptTemplate.from_messages([
#     #     system_message_prompt,
#     #     # HumanMessagePromptTemplate.from_template("{query}\n\nAI: 以下の番号の文章が回答に使用できそうです。\n[")
#     #     # HumanMessagePromptTemplate.from_template("{query}")
#     # ])
#     return prompt

def create_prompt_info_for_select(relate_data):
    # ファイル名順に並び替え
    relate_info = sorted(relate_data, key=lambda x:x.metadata["filename"])
    # ドキュメントを更に分割しつつ，元のチャンクグループで列挙
    system_template_info = ""
    relate_info_cut = []
    un_num = 0
    for doc in relate_info:
        system_template_info += f"- {doc.metadata['filename']}\n"
        split_text = chunk_split(doc.page_content)
        for i, text in enumerate(split_text):
            info = Document(
                page_content=text,
                metadata={"filename":doc.metadata["filename"], "rank":doc.metadata["rank"], "item_number":i}
            )
            relate_info_cut.append(info)
            system_template_info += f"  - [{un_num}] {info.page_content}\n"
            un_num += 1

    return system_template_info, relate_info_cut

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

async def get_answer(llm_chain, _info, _query):
    print("start_selection")
    try: 
        with get_openai_callback() as cb:
            resp = llm_chain({"query":_query,"info":_info})["text"]
        cost = cb.total_cost
    except Exception as e: # 念のための例外処理
        print(e)
        resp = None
        cost = 0
        
    print("get_selection_answer")
    return [resp, cost]

async def generate_concurrently(info_list, query, prompt, model="gpt-3.5-turbo"):
    """非同期関数"""
    # モデル定義
    llm = ChatOpenAI(temperature=0, model_name=model, request_timeout=60)
    
    # プロンプト設定
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True
    )

    # 並列処理
    tasks = [get_answer(llm_chain, _info, query) for _info in info_list]
    return await asyncio.gather(*tasks)

async def select(related_data, query, select_llm_relate_num=3):
    prompt = create_prompt_template_for_select()
    string_info_list = []
    info_list = []
    for i in range(0, len(related_data), select_llm_relate_num):
        string_info, info = create_prompt_info_for_select(related_data[i:i+select_llm_relate_num])
        string_info_list.append(string_info)
        info_list.append(info)
    print(info_list)
    print(string_info_list)
    tmp_list = await generate_concurrently(string_info_list, query, prompt)
    total_cost = sum([cost for resp, cost in tmp_list])
    response = [resp for resp, cost in tmp_list]
    return response, total_cost

def chat(query,llm,memory,db,relate_num=3,filter=None, max_token=4000):
    related_data,score_data = documents_search(db,query,top_k=relate_num,filter=filter)
    for i, item in enumerate(related_data):
        item.metadata["rank"] = i
    
    response, cost = asyncio.run(select(related_data, query))
    print(response)

    # prompt, related_info = create_prompt_template_for_compose(related_data)
    # input_token_size = llm.get_num_tokens(prompt.format(query=query))
    # if related_data == [] or input_token_size > max_token:
    #     response = "すみません。答えられません。"
    #     return response,related_data,0,None,0
    # llm_chain = LLMChain(
    # llm=llm,
    # prompt=prompt,
    # memory=memory,
    # verbose=True,
    # )
    # with get_openai_callback() as cb:
    #     response = llm_chain(query)["text"]
    # cost = cb.total_cost
    # save_memory(memory,query,response)
    # save_log(query,response,[data.page_content for data in related_data],score_data)
    # ret = re.findall(r"\[([0-9]+)\]", response)
    # print(ret)
    # nums_ref = sorted(list(set(map(int, ret))))
    # print(nums_ref)
    # # return response,related_data,cost,template,input_token,output_token
    # return response,related_info,cost,llm_chain,nums_ref,input_token_size
