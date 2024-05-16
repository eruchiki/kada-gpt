from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from api.db import get_db
from api.vs import get_vs
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.collections as schemas
import api.cruds.collection as cruds
from qdrant_client import QdrantClient
from fastapi import UploadFile
from fastapi.responses import FileResponse
import os


router = APIRouter()


# コレクション作成
@router.post(
    "/chat/collections", response_model=schemas.CreateResponseCollection
)
async def create_collection(
    collection_body: schemas.CreateCollection,
    db: AsyncSession = Depends(get_db),
    vs: QdrantClient = Depends(get_vs),
) -> schemas.CreateResponseCollection:
    return await cruds.create_collection(db, vs, collection_body)


# コレクション一覧取得
@router.get(
    "/chat/collections/{group_id}",
    response_model=List[schemas.ResponseCollectionBase]
)
async def get_collection(
    group_id: int,
    db: AsyncSession = Depends(get_db)
) -> List[schemas.ResponseCollectionBase]:
    colection_list = await cruds.get_all_collection(db, group_id)
    return colection_list


# コレクション削除
@router.delete(
    "/chat/collections/{collection_id}",
    response_model=schemas.DelateResponseCollection,
)
async def delate_collections(
    collection_id: int,
    db: AsyncSession = Depends(get_db),
    vs: QdrantClient = Depends(get_vs),
) -> schemas.DelateResponseCollection:
    before_data = await cruds.get_collection(db, collection_id)
    if before_data is None:
        raise HTTPException(
            status_code=404, detail=f"{collection_id} not Found"
        )
    collection_info = await cruds.delete_collection(
        db, vs, original=before_data
    )
    return collection_info


# ドキュメント登録
@router.post(
    "/chat/collections/{collection_id}",
    response_model=List[schemas.AddResponseDocument],
)
async def add_documents(
    collection_id: int,
    create_user_id: int,
    files: List[UploadFile],
    db: AsyncSession = Depends(get_db),
    vs: QdrantClient = Depends(get_vs),
) -> List[schemas.AddResponseDocument]:
    return await cruds.add_documents(
        db, vs, files, collection_id, create_user_id
    )


# ドキュメント一覧取得
@router.get(
    "/chat/collections/{collection_id}",
    response_model=List[schemas.ResponseDocuments],
)
async def get_documents(
    collection_id: int,
    db: AsyncSession = Depends(get_db),
) -> List[schemas.ResponseDocuments]:
    document_list = await cruds.get_all_documents(db, collection_id)
    return document_list


# 特定のドキュメント取得
@router.get(
    "/chat/collections/{collection_id}/{document_id}",
    response_model=FileResponse,
)
async def get_document(
    collection_id: int,
    document_id: int,
    db: AsyncSession = Depends(get_db),
) -> List[Any]:
    document_info = await cruds.get_document(db, collection_id, document_id)
    if not os.path.exists(document_info.uri):
        raise HTTPException(
            status_code=404, detail=f"{document_info.uri} not found"
        )
    responsefile = FileResponse(
        path=document_info.uri,
        filename=os.path.basename(document_info.uri),
    )
    return responsefile


# ドキュメント削除
@router.delete(
    "/chat/collections/{collection_id}/{document_id}",
    response_model=schemas.DelateResponseDocument,
)
async def delate_documents(
    collection_id: int,
    document_id: int,
    db: AsyncSession = Depends(get_db),
    vs: QdrantClient = Depends(get_vs),
) -> schemas.DelateResponseDocument:
    before_data = await cruds.get_document(db, collection_id, document_id)
    if before_data is None:
        raise HTTPException(status_code=404, detail=f"{document_id} not Found")
    document_info = await cruds.delete_document(
        db, vs, original=before_data
    )
    return document_info
