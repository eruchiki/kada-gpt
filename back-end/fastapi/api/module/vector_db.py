from langchain.schema import Document
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import MeCab
import pykakasi
from typing import Optional
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client.models import Distance, VectorParams
from langchain.callbacks import get_openai_callback


def text_to_documents(text_list: list, metadata: dict) -> list:
    return [
        Document(page_content=data, metadata=metadata | {"nth": i})
        for i, data in enumerate(text_list)
    ]


def documents_search(
    db: Any,
    query: str,
    top_k: int = 3,
    filter: Optional[dict] = None,
    border: float = 0.7,
) -> tuple[list, list]:
    docs = db.similarity_search_with_score(query=query, k=top_k, filter=filter)
    # print([(doc.page_content,score) for doc,score in docs])
    return [doc for doc, score in docs if score > border], [
        score for doc, score in docs if score > border
    ]


def load_qdrant(
    collection_name: str, host: str = "qdrant", port: int = 6333
) -> Qdrant:
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
        embeddings=OpenAIEmbeddings(),
    )


def insert_data(documents: str, embeddings: Any, host: str, port: int, collection_name: str) -> :
    qdrant = Qdrant.from_documents(
        documents,
        embeddings,
        host=host,
        port=port,
        collection_name=collection_name,
    )
