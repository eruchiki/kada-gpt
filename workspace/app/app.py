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
    
    st.session_state[StSession.MODEL_RADIO] = st.selectbox("chatGPTモデル(既定\:GPT-4)",
                     options=list(StSession.MODEL_OPTIONS.keys()),
                     help=model_help,
                     key=StSession.MODEL_RADIO_TMP,
                     index=index)
    st.session_state[StSession.MODEL_NAME] = StSession.MODEL_OPTIONS[st.session_state[StSession.MODEL_RADIO]]

def select_method():
    if StSession.METHOD_SELECT not in st.session_state:
        st.session_state[StSession.METHOD_SELECT] = list(StSession.METHOD_OPTIONS.keys())[1]
        index = 1
    elif StSession.METHOD_SELECT_TMP not in st.session_state:
        index = list(StSession.METHOD_OPTIONS.keys()).index(st.session_state[StSession.METHOD_SELECT])
    else:
        index = list(StSession.METHOD_OPTIONS.keys()).index(st.session_state[StSession.METHOD_SELECT_TMP])
    
    st.session_state[StSession.METHOD_SELECT] = st.selectbox("適応手法(既定\:検討手法)",
                     options=list(StSession.METHOD_OPTIONS.keys()),
                     help="従来手法は一般的なRAG．検討手法は従来手法に加えて，retrieveの後にselectを行う．",
                     key=StSession.METHOD_SELECT_TMP,
                     index=index)
    st.session_state[StSession.METHOD_NAME] = StSession.METHOD_OPTIONS[st.session_state[StSession.METHOD_SELECT]]

def input_num_of_reference():
    if StSession.CHAT_REFERENCE_NUMS not in st.session_state:
        st.session_state[StSession.CHAT_REFERENCE_NUMS] = index = 4
    elif StSession.CHAT_REFERENCE_NUMS_TMP not in st.session_state:
        index = st.session_state[StSession.CHAT_REFERENCE_NUMS]
    else:
        index = st.session_state[StSession.CHAT_REFERENCE_NUMS_TMP]
    st.session_state[StSession.CHAT_REFERENCE_NUMS] = st.number_input('取得する参考情報数(既定:4)',
                    min_value=1,
                    max_value=10,
                    value=index,
                    step=1,
                    key=StSession.CHAT_REFERENCE_NUMS_TMP,
                    help="参考情報数によってはモデルのトークン上限に到達する可能性があります．\n\nエラーが発生した場合は数値を小さくしてください．"
                    )


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
    st.session_state[StSession.DOC_CHUNK_SIZE] = st.number_input('分割時のchunkサイズ(既定:1000)',
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
            col1, col2, col3 = st.columns((2, 1, 1), gap="medium")
            with col1:
                input_query_text()
            with col2:
                select_model()
                input_num_of_reference()
            with col3:
                select_method()
            submitted = st.form_submit_button("質問する")

    if submitted:
        with st.spinner("ChatGPTが入力中 ..."):
            if st.session_state[StSession.METHOD_NAME] == "default":
                answer, file_list, cost, start_time = chat_default(st.session_state[StSession.CHAT_QUERY],st.session_state[StSession.MODEL_NAME],db,st.session_state[StSession.CHAT_REFERENCE_NUMS])
            elif st.session_state[StSession.METHOD_NAME] == "select":
                answer, file_list, cost, start_time = chat(st.session_state[StSession.CHAT_QUERY],st.session_state[StSession.MODEL_NAME],db,st.session_state[StSession.CHAT_REFERENCE_NUMS])
        st.session_state.costs.append(cost)
        st.session_state[StSession.CHAT_MESSAGES].insert(0, {
            "time": start_time,
            "query": st.session_state[StSession.CHAT_QUERY],
            "response": answer,
            "reference": file_list,
            "feedback": {"reference_level": None, "accuracy": None},
        })

    for i, message in enumerate(st.session_state[StSession.CHAT_MESSAGES]):
        h_col1, h_col2 = st.columns((3, 1), gap="medium")
        with h_col1:
            with st.chat_message('user'):
                st.markdown(message['query'])
            with st.chat_message('assistant'):
                st.markdown(message['response'])
                for j, relate in enumerate(message['reference']):
                    string = f"[{relate['number']}] {relate['file_name']}"
                    with open(f"./reference_files/{relate['file_name']}", 'rb') as f:
                        data = f.read()
                    st.download_button(label=string, data=data, file_name=relate['file_name'], key=f"{i}-{j}-chat_dl_bt")
        with h_col2:
            h_container = st.empty()
            with h_container.container():
                feedback_tmp = st.slider(label="参考度を%で教えてください", min_value=0, max_value=100, value=50, step=1, key=f"{i}-chat_fb_sld", help="情報を探す時に，どの程度参考になったかを回答してください．だいたいの数値で大丈夫です．")
                feedback_tmp2 = st.selectbox("回答の正確性を教えてください",
                     options=[
                         "わからない",
                         "極めて正確",
                         "正確だが情報不足",
                         "一部情報が間違い",
                         "全情報が間違い",
                         "質問と関係なし"
                         ],
                     help="参考情報を元々知っている場合は答えてください．アップロードしたPDFの内容に基づいて選択してください．",
                     key=f"{i}-chat_fb_select",
                     )
                ok_bt = st.button("アンケート保存", type='primary', key=f"{i}-chat_fb_bt", use_container_width=True)
            if ok_bt:
                message["feedback"]["reference_level"] = feedback_tmp
                message["feedback"]["accuracy"] = feedback_tmp2
                save_feedback(message)
            if message["feedback"]["reference_level"] != None:
                h_container.empty()
                st.markdown(f"[アンケート回答済]  \n- 参考度: {message['feedback']['reference_level']}%  \n- 正確性: {message['feedback']['accuracy']}")
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
    for i, cost in enumerate(reversed(costs)):
        if i == 0:
            st.sidebar.markdown(f"- ${cost:.5f} (最新の履歴)")
        else:
            st.sidebar.markdown(f"- ${cost:.5f}")


if __name__ == '__main__':
    main()