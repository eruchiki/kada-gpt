from langchain.prompts import PromptTemplate
from langchain import LLMChain
from lib.vector_module import documents_search
from langchain.callbacks import get_openai_callback

def create_template(relate_info):
    input_val = ["chat_history","query"]
    template = "{chat_history}\n質問：{query}\n関連情報\n"
    for i,info in enumerate(relate_info):
        template += f"{i+1}.{info}\n"
    template += "解答："
    return PromptTemplate(input_variables=input_val,template=template)

def save_memory(memory,query,response):
    memory.chat_memory.add_user_message(query)
    memory.chat_memory.add_ai_message(response)

def chat(query,llm,memory,db):
    related_data = documents_search(db,query,top_k=10)
    if related_data == []:
        response = "すみません。答えられません。"
        return response,related_data,0
    template = create_template(related_data)
    llm_chain = LLMChain(
    llm=llm,
    prompt=template,
    memory=memory,
    verbose=True,
    )
    with get_openai_callback() as cb:
        response = llm_chain(query)["text"]
    cost = cb.total_cost
    save_memory(memory,query,response)
    return response,related_data,cost
