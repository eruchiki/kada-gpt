import streamlit as st
from langchain.llms import OpenAI
from lib.pdf_module import *
from lib.vector_module import *
from lib.store_module import *
from lib.gpt_module import *
from langchain.memory import ConversationBufferWindowMemory,VectorStoreRetrieverMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from lib.const import *
from lib.log_module import *


HOST = "qdrant"
PORT = 6333
COLLECTION_NAME = "kadagpt_1"
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
    if StSession.UPLOADER_KEY not in st.session_state:
        st.session_state[StSession.UPLOADER_KEY] = 'uploader' + str(time.time())

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
    
    st.session_state[StSession.MODEL_RADIO] = st.selectbox("chatGPTモデル(既定値\:GPT-4)",
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

def input_size_of_chunk():
    if StSession.DOC_CHUNK_SIZE not in st.session_state:
        st.session_state[StSession.DOC_CHUNK_SIZE] = index = 1000
    elif StSession.DOC_CHUNK_SIZE_TMP not in st.session_state:
        index = st.session_state[StSession.DOC_CHUNK_SIZE]
    else:
        index = st.session_state[StSession.DOC_CHUNK_SIZE_TMP]
    st.session_state[StSession.DOC_CHUNK_SIZE] = st.number_input('分割時のchunkサイズ(既定値:1000)',
                    min_value=100,
                    max_value=2500,
                    value=index,
                    step=100,
                    key=StSession.DOC_CHUNK_SIZE_TMP)

def get_pdf_text():
    col1, col2 = st.columns((2, 1))
    with col1:
        uploaded_files = st.file_uploader(
            label='PDFファイルをアップロードできます(複数選択可)',
            type='pdf',
            accept_multiple_files=True,
            key=st.session_state[StSession.UPLOADER_KEY]
        )
    with col2:
        input_size_of_chunk()

    return uploaded_files

def change_uploader_key():
    st.session_state[StSession.UPLOADER_KEY] = 'uploader' + str(time.time())

def get_file_docs(uploaded_files, chunk_num):
    document_list = []
    total_token = 0
    os.makedirs("./reference_files", exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = f"./reference_files/{uploaded_file.name}"
        if file_path in glob("./reference_files/*.pdf"):
            document_list.append([])
            st.markdown("- `" + uploaded_file.name + "` は処理済みのためスキップしました")
            continue
        with open(file_path,mode="wb") as f:
            f.write(uploaded_file.read())
        uploaded_file.seek(0)
        text = pdf_reader(uploaded_file)
        clean_text = normalize_text(text)
        total_token += num_tokens_from_string(clean_text, "text-embedding-ada-002")
        split_text = chunk_split(clean_text,chunk_num=chunk_num)
        save_emb_log(split_text, total_token)
        documents = text_to_documents(split_text,
                                    metadata={"type":"related","filename":uploaded_file.name})
        document_list.append(documents)
    return document_list, total_token

def text_embedding(document_list):
    for documents in document_list:
        if documents == []:
            continue
        insert_data(documents,
            embeddings = OpenAIEmbeddings(),
            host=HOST,
            port=PORT,
            collection_name=COLLECTION_NAME)

def page_pdf_upload_and_build_vector_db():
    st.header("PDFをアップロード")
    container = st.container()
    emb_container = st.empty()
    with container:
        st.session_state[StSession.DOC_FILE_DATA] = get_pdf_text()
        if st.session_state[StSession.DOC_FILE_DATA]:
            uploaded_files = st.session_state[StSession.DOC_FILE_DATA]
            with emb_container.container():
                do_embedding = st.button('前処理開始',type='primary')
            if do_embedding:
                emb_container.empty()
                with st.spinner("処理中...画面を閉じないでください"):
                    document_list, total_token = get_file_docs(uploaded_files, st.session_state[StSession.DOC_CHUNK_SIZE])
                    text_embedding(document_list)
                    cost = 0.0001 * (total_token / 1000)
                    st.session_state.costs.append(cost)

                st.success(f'✅  処理が完了しました．')
                st.button('OK', on_click=change_uploader_key,type='primary')

def page_ask_my_pdf():
    st.header("組織内文書へ質問")
    db = load_qdrant(host=HOST,port=PORT,collection_name=COLLECTION_NAME)
    form_container = st.empty()


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
                    with open(f"./reference_files/{relate['file_name']}", 'rb') as f:
                        data = f.read()
                    st.download_button(label=string, data=data, file_name=relate['file_name'], key=f"{i}-{j}-chat_dl_bt")
            st.markdown("---")

def main():
    init_page() 
    selection = st.sidebar.radio("モード", ["PDFをアップロード","組織内文書へ質問"], index=1)
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