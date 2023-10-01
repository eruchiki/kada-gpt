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
COLLECTION_NAME = "document"
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
    st.session_state.sentence_length = st.number_input('1vectorにおける文章数',1,10,1,step=1)
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
        split_text = sentence_split(skip_text(clean_text,skip_pattern=r"^\d+"))
        with open("./process_data/"+str(os.path.splitext(os.path.basename(file_path))[0])+".txt",mode="w",encoding="utf-8") as f:
            f.write(split_text)
        st.write(split_text)
        documents = text_to_documents(split_text.split("\n"),
                                      metadata={"type":"related","filename":uploaded_file.name})
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
        query = st.text_input("質問: ", key="input")
        if not query:
            answer = None
        else:
            with st.spinner("ChatGPTが入力中 ..."):
                answer, relate_data,cost = chat(query,llm,memory,db)
            st.session_state.costs.append(cost)

        if answer:
            with response_container:
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