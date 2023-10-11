from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client.models import Distance, VectorParams
from langchain.callbacks import get_openai_callback

def load_qdrant(collection_name,host='qdrant',port=6333):
    client = QdrantClient(host=host, port=port)

    # すべてのコレクション名を取得
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]

    # コレクションが存在しなければ作成
    if collection_name not in collection_names:
        # コレクションが存在しない場合、新しく作成します
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
    return Qdrant(
        client=client,
        collection_name=collection_name, 
        embeddings=OpenAIEmbeddings()
    )

def insert_data(documents,embeddings,host,port,collection_name):
    with get_openai_callback() as cb:
        qdrant = Qdrant.from_documents(documents, embeddings,host=host,port=port, collection_name= collection_name)
    cost = cb.total_cost
    return cost
