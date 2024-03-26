from langchain.schema import Document
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
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


def insert_data(
    documents: str, embeddings: Any, host: str, port: int, collection_name: str
) -> None:
    qdrant = Qdrant.from_documents(
        documents,
        embeddings,
        host=host,
        port=port,
        collection_name=collection_name,
    )
