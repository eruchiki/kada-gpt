from sqlalchemy.ext.asyncio import AsyncSession
import api.models.model as model
import api.models.qdrant as qdrant
import api.schemas.collections as collection_schema
from sqlalchemy import select
from typing import Optional, List, Tuple
from sqlalchemy.engine import Result
from qdrant_client import QdrantClient
from datetime import datetime
from fastapi import UploadFile


# コレクション作成
async def create_collection(
    db: AsyncSession,
    vs: QdrantClient,
    collection_create: collection_schema.CreateCollection,
) -> model.Collections:
    collection = model.Collections(**collection_create.model_dump())
    db.add(collection)
    await db.commit()
    await db.refresh(collection)
    collection_id = str(collection.__dict__["id"])
    vs_client = qdrant.VectorStore(collection_id=collection_id, client=vs)
    vs_client.create_collection()
    return collection


# 全コレクション取得
async def get_all_collection(
    db: AsyncSession,
    group_id: int
) -> Optional[List[Tuple[int, int, str, datetime, datetime]]]:
    result: Result = await db.execute(
        select(
            model.Collections.id,
            model.Collections.group_id,
            model.Collections.create_user_id,
            model.Collections.name,
            model.Collections.created_at,
            model.Collections.update_at,
        ).filter(model.Collections.publish,
                 model.Collections.group_id == group_id)
    )
    return result.all()


# 特定のコレクション取得
async def get_collection(
    db: AsyncSession, collection_id: int
) -> Optional[model.Collections]:
    result: Result = await db.execute(
        select(model.Collections).filter(
            model.Collections.id == collection_id, model.Collections.publish
        )
    )
    collection_data = result.first()
    return collection_data[0] if collection_data is not None else None


# コレクション削除
async def delete_collection(
    db: AsyncSession,
    vs: QdrantClient,
    original: model.Collections,
) -> Optional[model.Collections]:
    original.publish = False
    await db.commit()
    await db.refresh(original)
    collection_id = str(original.id)
    vs_client = qdrant.VectorStore(collection_id=collection_id, client=vs)
    vs_client.delete_collection()
    return original


# ドキュメント登録
async def add_documents(
    db: AsyncSession,
    vs: QdrantClient,
    files: List[UploadFile],
    collection_id: int,
    create_user_id: int,
) -> List[model.Documents]:
    vs_client = qdrant.VectorStore(collection_id=str(collection_id), client=vs)
    vs_client.set_qdrant()
    file_paths = vs_client.define_path(files)
    document_list = []
    document = None
    for file_path in file_paths:
        document = model.Documents(
            create_user_id=create_user_id,
            collection_id=collection_id,
            uri=file_path,
        )
        db.add(document)
        await db.commit()
        await db.refresh(document)
        document_list.append(document)
    await vs_client.insert_documents(
        files,
        file_paths,
        [document.__dict__["id"] for document in document_list],
    )
    return document_list


# 任意のコレクション中の全ドキュメント取得
async def get_all_documents(
    db: AsyncSession, collection_id: int
) -> Optional[List[Tuple[int, int, int, str, datetime, datetime]]]:
    result: Result = await db.execute(
        select(
            model.Documents.id,
            model.Documents.collection_id,
            model.Documents.create_user_id,
            model.Documents.uri,
            model.Documents.created_at,
            model.Documents.update_at,
        ).filter(
            model.Documents.publish,
            model.Documents.collection_id == collection_id,
        )
    )
    return result.all()


# 特定のドキュメント取得
async def get_document(
    db: AsyncSession, collection_id: int, document_id: int
) -> Optional[model.Documents]:
    result: Result = await db.execute(
        select(model.Documents).filter(
            model.Documents.id == document_id,
            model.Documents.collection_id == collection_id,
            model.Documents.publish,
        )
    )
    document_data = result.first()
    return document_data[0] if document_data is not None else None


# ドキュメント削除
async def delete_document(
    db: AsyncSession,
    vs: QdrantClient,
    original: model.Documents,
) -> Optional[model.Documents]:
    original.publish = False
    await db.commit()
    await db.refresh(original)
    document_id = str(original.id)
    collection_id = str(original.collection_id)
    vs_client = qdrant.VectorStore(collection_id=collection_id, client=vs)
    vs_client.delete_document(document_id)
    return original
