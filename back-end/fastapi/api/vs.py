from qdrant_client import QdrantClient

VS_URL = "vector-store"
VS_PORT = 6333

client = QdrantClient(host=VS_URL, port=VS_PORT)


def get_vs() -> QdrantClient:
    return client
