from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_community.vectorstores import Qdrant

VS_URL = "vector-store"
VS_PORT = 6333

client = QdrantClient(host=VS_URL, port=VS_PORT)

collections = client.get_collections().collections
collection_names = [collection.name for collection in collections]

condition = models.FieldCondition(
    key="metadata.fileid", match=models.MatchValue(value="15")
)
scroll_filter = models.Filter(must=[condition])
results = client.scroll(
    collection_name="30", scroll_filter=scroll_filter,
    limit=1000
)

print(collection_names)
print(client.get_collection(collection_name="28"))
print(results)
