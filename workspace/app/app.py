import streamlit as st
from langchain.llms import OpenAI
from lib.pdf_module import *
from lib.vector_module import *
from lib.store_module import *
from lib.gpt_module import *
from langchain.memory import ConversationBufferWindowMemory,VectorStoreRetrieverMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from lib.const import *


HOST = "qdrant"
PORT = 6333
COLLECTION_NAME = "document4"
# memory = ConversationBufferWindowMemory(memory_key="chat_history",k=3)

def init_page():
    st.set_page_config(
        page_title="組織内文書へ質問",
        page_icon="🧠",
        layout="wide"
    )
    st.sidebar.title("メニュー")
    if 'costs' not in st.session_state:
        st.session_state.costs = []
    if StSession.CHAT_MESSAGES not in st.session_state:
        st.session_state[StSession.CHAT_MESSAGES] = []

def select_model():
    if StSession.MODEL_RADIO not in st.session_state:
        st.session_state[StSession.MODEL_RADIO] = list(StSession.MODEL_OPTIONS.keys())[2]
        index = 2
    elif StSession.MODEL_RADIO_TMP not in st.session_state:
        index = list(StSession.MODEL_OPTIONS.keys()).index(st.session_state[StSession.MODEL_RADIO])
    else:
        index = list(StSession.MODEL_OPTIONS.keys()).index(st.session_state[StSession.MODEL_RADIO_TMP])
    
    model_help = "モデル毎の最大トークン数は以下の通りです．"
    for key, value in StSession.MODEL_OPTIONS.items():
        model_help += f"\n\n{key} : {OpenAI.modelname_to_contextsize(value)}"
    
    st.session_state[StSession.MODEL_RADIO] = st.selectbox("モデルを選んでください",
                     options=list(StSession.MODEL_OPTIONS.keys()),
                     help=model_help,
                     key=StSession.MODEL_RADIO_TMP,
                     index=index)
    st.session_state[StSession.MODEL_NAME] = StSession.MODEL_OPTIONS[st.session_state[StSession.MODEL_RADIO]]

def input_num_of_reference():
    if StSession.CHAT_REFERENCE_NUMS not in st.session_state:
        st.session_state[StSession.CHAT_REFERENCE_NUMS] = index = 4
    elif StSession.CHAT_REFERENCE_NUMS_TMP not in st.session_state:
        index = st.session_state[StSession.CHAT_REFERENCE_NUMS]
    else:
        index = st.session_state[StSession.CHAT_REFERENCE_NUMS_TMP]
    st.session_state[StSession.CHAT_REFERENCE_NUMS] = st.number_input('質問ごとに取得する参考情報数(既定値:4)',
                    min_value=1,
                    max_value=10,
                    value=index,
                    step=1,
                    key=StSession.CHAT_REFERENCE_NUMS_TMP)


def input_query_text():
    if StSession.CHAT_QUERY not in st.session_state:
        st.session_state[StSession.CHAT_QUERY] = index = None
    elif StSession.CHAT_QUERY_TMP not in st.session_state:
        index = st.session_state[StSession.CHAT_QUERY]
    else:
        index = st.session_state[StSession.CHAT_QUERY_TMP]

    st.session_state[StSession.CHAT_QUERY] = st.text_area("質問: ", key=StSession.CHAT_QUERY_TMP, value=index, height=122)

def setting_page():
    split_option = st.radio("文書分割方法", ("chunk", "sentence"),horizontal=True)
    st.session_state.split_option = split_option
    if split_option == "sentence":
        st.session_state.sentence_length = st.number_input('1vectorにおける文章数',1,10,1,step=1)
        st.session_state.split_string = st.text_input("split_word ", key="input",value="。.．")
    elif split_option == "chunk":
        st.session_state.chunk_num = st.number_input('1vectorにおけるchunk数',100,2000,1000,step=100)
        st.session_state.split_string = st.text_input("split_word ", key="input",value="。.．")

def get_pdf_text():
    uploaded_file = st.file_uploader(
        label='PDFをアップロードしてください．',
        type='pdf'
    )
    setting_page()
    if uploaded_file:
        if not os.path.exists("./reference_data"):
            os.mkdir("./reference_data")
        if not os.path.exists("./data"):
            os.mkdir("./data")
        if not os.path.exists("./process_data"):
            os.mkdir("./process_data")
        file_path = f"./reference_data/{uploaded_file.name}"
        if file_path in glob("./reference_data/*.pdf"):
            return -1
        with open(file_path,mode="wb") as f:
            f.write(uploaded_file.read())
        text = pdf_reader(file_path)
        clean_text = normalize_text(text,remove_str="[\u3000 ]")
        skipped_text = skip_text(clean_text,skip_pattern=r"^\d+")
        st.write([skipped_text])
        with open("./process_data/"+str(os.path.splitext(os.path.basename(file_path))[0])+".txt",mode="w",encoding="utf-8") as f:
            f.write(skipped_text)
        if st.session_state.split_option == "sentence":
            split_text = sentence_split(skipped_text,split_str=st.session_state.split_string).split("\n")
        elif st.session_state.split_option == "chunk":
            split_text = chunk_split(skipped_text,chunk_num=st.session_state.chunk_num)    
        documents = text_to_documents(split_text,
                                      metadata={"type":"related","filename":uploaded_file.name})
        st.write(documents)
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
    st.header("組織内文書へ質問")
    db = load_qdrant(host=HOST,port=PORT,collection_name=COLLECTION_NAME)
    form_container = st.empty()
    response_container = st.container()


    with form_container.container():
        with st.form("question_form", clear_on_submit=False):
            col1, col2 = st.columns((2, 1))
            with col1:
                input_query_text()
            with col2:
                select_model()
                input_num_of_reference()
            submitted = st.form_submit_button("質問する")

    if submitted:
        # form_container.empty()
        with st.spinner("ChatGPTが入力中 ..."):
            answer, file_list, cost = chat(st.session_state[StSession.CHAT_QUERY],st.session_state[StSession.MODEL_NAME],db,st.session_state[StSession.CHAT_REFERENCE_NUMS])
        st.session_state.costs.append(cost)
        st.session_state[StSession.CHAT_MESSAGES].append({
            "query": st.session_state[StSession.CHAT_QUERY],
            "response": answer,
            "reference": file_list,
        })

    if st.session_state[StSession.CHAT_MESSAGES] != []:
        for i, message in enumerate(reversed(st.session_state[StSession.CHAT_MESSAGES])):
            with st.chat_message('user'):
                st.markdown(message['query'])
            with st.chat_message('assistant'):
                st.markdown(message['response'])
                for j, relate in enumerate(message['reference']):
                    string = f"[{relate['number']}] {relate['file_name']}"
                    with open(f"./reference_data/{relate['file_name']}", 'rb') as f:
                        data = f.read()
                    st.download_button(label=string, data=data, file_name=relate['file_name'], key=f"{i}-{j}-chat_dl_bt")
            st.markdown("---")

def main():
    init_page() 
    selection = st.sidebar.radio("モード", ["PDFをアップロード","組織内文書へ質問"])
    if selection == "PDFをアップロード":
        page_pdf_upload_and_build_vector_db()
    elif selection == "組織内文書へ質問":
        page_ask_my_pdf()
    st.sidebar.markdown("---")
    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## コスト")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


if __name__ == '__main__':
    main()