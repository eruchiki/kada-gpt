from sqlalchemy import create_engine
from qdrant_client import QdrantClient
from api.models.model import Base
import shutil

DB_URL = "mysql+pymysql://root@db:3306/api?charset=utf8"
engine = create_engine(DB_URL, echo=True)

VS_URL = "vector-store"
VS_PORT = 6333
client = QdrantClient(host=VS_URL, port=VS_PORT)


def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def reset_vectore_store() -> None:
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    for collection_name in collection_names:
        print("delete collection: ", collection_name)
        result = client.delete_collection(collection_name)
        print(result)


def reset_file_store() -> None:
    shutil.rmtree("/src/pdf_files")


if __name__ == "__main__":
    reset_database()
    reset_vectore_store()
    reset_file_store()
