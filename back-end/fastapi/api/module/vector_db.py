from langchain.schema import Document
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client.models import Distance, VectorParams
from api.module.preprocessing import morpheme
from langchain.retrievers import BM25Retriever
from typing import Any


def text_to_documents(text_list: list, metadata: dict) -> list:
    return [
        Document(page_content=data, metadata=metadata | {"nth": i})
        for i, data in enumerate(text_list)
    ]


def load_qdrant(
    collection_name: str, host: str = "vector-store", port: int = 6333
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
    Qdrant.from_documents(
        documents,
        embeddings,
        host=host,
        port=port,
        collection_name=collection_name,
    )


def bm25_search(collection_name: str, client: QdrantClient) -> BM25Retriever:
    count = client.count(collection_name).count
    record_list = client.scroll(
        collection_name, limit=count, with_vectors=True
    )[0]
    corpus = [
        record.payload["page_content"]
        for record in record_list
        if record.payload is not None and "page_content" in record.payload
    ]

    def preprocess_func(text: str) -> list[str]:
        _, text_list = morpheme(text, neologd=True)
        return text_list

    retriever = BM25Retriever.from_texts(
        corpus, preprocess_func=preprocess_func
    )
    return retriever
