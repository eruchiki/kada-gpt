from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models import models
from fastapi import HTTPException
from typing import List
from fastapi import UploadFile
import os
import asyncio
import mimetypes
import api.module.document_reader as doc_reader
import api.module.preprocessing as preprocess
from langchain.schema import Document
import datetime as dt
from typing import Optional


class VectorStore:

    def __init__(self, collection_id: str, client: QdrantClient) -> None:
        self.client = client
        self.collection_id = collection_id
        self.embeddings = OpenAIEmbeddings()

    def set_qdrant(self) -> None:
        self.qdrant = Qdrant(
            client=self.client,
            collection_name=self.collection_id,
            embeddings=self.embeddings,
        )

    def get_all_collection(self) -> List[models.CollectionDescription]:
        return self.client.get_collections().collections

    def check_exist_collection(self) -> bool:
        collections = self.get_all_collection()
        collection_ids = [collection.name for collection in collections]
        return self.collection_id in collection_ids

    def create_collection(self) -> None:
        if not self.check_exist_collection():
            try:
                self.client.create_collection(
                    collection_name=self.collection_id,
                    vectors_config=VectorParams(
                        size=1536, distance=Distance.COSINE
                    ),
                )
            except NotImplementedError as e:
                raise HTTPException(status_code=500, detail=e)

    def delete_collection(self) -> None:
        if self.check_exist_collection():
            try:
                self.client.delete_collection(
                    collection_name=self.collection_id,
                    timeout=30,
                )
            except NotImplementedError as e:
                raise HTTPException(status_code=500, detail=e)

    async def insert_documents(
        self,
        files: List[UploadFile],
        file_paths: List[str],
        ids: List[int],
    ) -> None:
        self.token_num = 0
        for file, id, file_path in zip(files, ids, file_paths):
            text = doc_reader.pdf_reader(file)
            normalized_text = preprocess.normalize_text(text)
            self.token_num += preprocess.num_tokens_from_string(
                normalized_text, "text-embedding-ada-002"
            )
            split_text = preprocess.chunk_split(normalized_text)
            documents = [
                Document(
                    page_content=data,
                    metadata={
                        "type": "related",
                        "fileid": str(id),
                        "filename": str(file_path),
                    }
                    | {"nth": i},
                )
                for i, data in enumerate(split_text)
            ]
            self.qdrant.add_documents(documents)
            await file.seek(0)
        await self.save_pdf(files, file_paths)

    def define_path(self, files: List[UploadFile]) -> List[str]:
        self.collection_path = os.path.join("pdf_files", self.collection_id)
        if not os.path.isdir(self.collection_path):
            os.makedirs(self.collection_path)
        file_paths = []
        for file in files:
            non_extension = os.path.splitext(str(file.filename))[0]
            file_name = os.path.basename(non_extension)
            extension = os.path.splitext(str(file.filename))[1]
            if extension == "":
                extension = ".pdf"
            guessed_extension = mimetypes.guess_extension(str(file.filename))
            if guessed_extension is not None:
                extension = "." + guessed_extension
            date_string = dt.datetime.now().strftime("%Y%m%d%H%M%S%f")
            file_name = date_string + "_" + file_name + extension
            file_path = os.path.join(self.collection_path, file_name)
            file_paths.append(file_path)
        return file_paths

    async def save_pdf(
        self, files: List[UploadFile], file_paths: List[str]
    ) -> None:
        if not os.path.isdir(self.collection_path):
            os.makedirs(self.collection_path)
        await asyncio.gather(
            *[
                doc_reader.async_create_file_with_data(path, file)
                for path, file in zip(file_paths, files)
            ]
        )

    async def load_pdf(self) -> None:
        pass

    def seach_docs(
        self,
        query: str,
        top_k: int = 3,
        filter: Optional[dict] = None,
        border: float = 0.7,
    ) -> tuple[list, list]:
        docs = self.qdrant.similarity_search_with_score(
            query=query, k=top_k, filter=filter
        )
        related_data = [doc for doc, score in docs if score > border]
        score_data = [score for doc, score in docs if score > border]
        for i, item in enumerate(related_data):
            item.metadata["rank"] = i
        return related_data, score_data

    def delete_document(self, document_id: str) -> None:
        condition = models.FieldCondition(
            key="metadata.fileid", match=models.MatchValue(value=document_id)
        )
        point_filter = models.Filter(must=[condition])
        try:
            self.client.delete(
                collection_name=self.collection_id,
                points_selector=point_filter,
            )
        except NotImplementedError as e:
            raise HTTPException(status_code=500, detail=e)
