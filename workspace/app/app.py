import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from lib.pdf_module import *
from lib.vector_module import *
from lib.store_module import *
from lib.gpt_module import *
from langchain.memory import ConversationBufferWindowMemory,VectorStoreRetrieverMemory
from langchain.embeddings.openai import OpenAIEmbeddings


HOST = "qdrant"
PORT = 6333
COLLECTION_NAME = "document3"
memory = ConversationBufferWindowMemory(memory_key="chat_history",k=3)

def init_page():
    st.set_page_config(
        page_title="組織内文書へ質問",
        page_icon="🤗"
    )
    st.sidebar.title("メニュー")
    if 'costs' not in st.session_state:
        st.session_state.costs = []


def select_model():
    model = st.sidebar.radio("モデルを選んでください:", ("GPT-3.5", "GPT-3.5-16k", "GPT-4"))
    if model == "GPT-3.5":
        st.session_state.model_name = "gpt-3.5-turbo"
    elif model == "GPT-3.5":
        st.session_state.model_name = "gpt-3.5-turbo-16k"
    else:
        st.session_state.model_name = "gpt-4"
    
    # 300: 本文以外の指示のトークン数 (以下同じ)
    st.session_state.max_token = OpenAI.modelname_to_contextsize(st.session_state.model_name) - 300
    return ChatOpenAI(temperature=0, model_name=st.session_state.model_name)

def setting_page():
    split_option = st.radio("文書分割方法", ("chunk", "sentence"),horizontal=True)
    st.session_state.split_option = split_option
    if split_option == "sentence":
        st.session_state.sentence_length = st.number_input('1vectorにおける文章数',1,10,1,step=1)
        st.session_state.split_string = st.text_input("split_word ", key="input",value="。")
    elif split_option == "chunk":
        st.session_state.chunk_num = st.number_input('1vectorにおけるchunk数',100,2000,100,step=100)
        st.session_state.split_string = st.text_input("split_word ", key="input",value="。")

def get_pdf_text():
    uploaded_file = st.file_uploader(
        label='PDFをアップロードしてください．',
        type='pdf'
    )
    setting_page()
    if uploaded_file:
        file_path = f"./reference_data/{uploaded_file.name}"
        if file_path in glob("./reference_data/*.pdf"):
            return -1
        with open(file_path,mode="wb") as f:
            f.write(uploaded_file.read())
        text = pdf_reader(file_path)
        clean_text = normalize_text(text,remove_str="[\u3000 ]")
        skiped_text = skip_text(clean_text,skip_pattern=r"^\d+")
        with open("./process_data/"+str(os.path.splitext(os.path.basename(file_path))[0])+".txt",mode="w",encoding="utf-8") as f:
            f.write(skiped_text)
        if st.session_state.split_option == "sentence":
            split_text = sentence_split(skiped_text,split_str=st.session_state.split_string).split("\n")
        elif st.session_state.split_option == "chunk":
            split_text = chunk_split(skiped_text,chunk_num=st.session_state.chunk_num,split_str=st.session_state.split_string)    
        documents = text_to_documents(split_text,
                                      metadata={"type":"related","filename":uploaded_file.name})
        st.write("".join(split_text))
        return documents
    else:
        return None

def page_pdf_upload_and_build_vector_db():
    st.title("PDFをアップロード")
    container = st.container()
    with container:
        pdf_text = get_pdf_text()
        if pdf_text == -1:
            st.warning('その文献は既にベクトル化されています')
        elif pdf_text:
            with st.spinner("Loading PDF ..."):
                cost = insert_data(pdf_text,
                            embeddings = OpenAIEmbeddings(),
                            host=HOST,
                            port=PORT,
                            collection_name=COLLECTION_NAME)
            st.session_state.costs.append(cost)

def page_ask_my_pdf():
    st.title("組織内文書へ質問")
    llm = select_model()
    db = load_qdrant(host=HOST,port=PORT,collection_name=COLLECTION_NAME)
    container = st.container()
    response_container = st.container()

    with container:
        with st.form("question_form", clear_on_submit=False):
            answer = None
            st.session_state.ralate_num = st.number_input('1queryに置ける参考情報数',1,10,1,step=1)
            query = st.text_input("質問: ", key="input")
            submitted = st.form_submit_button("質問する")
        if submitted:
            with st.spinner("ChatGPTが入力中 ..."):
                answer, relate_data,cost = chat(query,llm,memory,db,st.session_state.ralate_num)
            st.session_state.costs.append(cost)

        if answer:
            with response_container:
                st.markdown("## 質問")
                st.write(query)
                st.markdown("## 回答")
                st.write(answer)
                st.markdown("## 参照情報")
                for relate in relate_data:
                    st.write(relate)

def main():
    init_page() 
    selection = st.sidebar.radio("モード", ["PDFをアップロード","組織内文書へ質問"])
    if selection == "PDFをアップロード":
        page_pdf_upload_and_build_vector_db()
    elif selection == "組織内文書へ質問":
        page_ask_my_pdf()
    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## コスト")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


if __name__ == '__main__':
    main()