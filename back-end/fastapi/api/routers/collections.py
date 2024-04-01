from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.collections as schemas
import api.cruds.collection as cruds


router = APIRouter()


# コレクション作成
@router.post(
    "/chat/collections", response_model=schemas.CreateResponseCollection
)
async def create_collection(
    collection_body: schemas.CreateCollection,
    db: AsyncSession = Depends(get_db),
) -> schemas.CreateResponseCollection:
    return await cruds.create_collection(db, collection_body)


# コレクション一覧取得
@router.get(
    "/chat/collections", response_model=List[schemas.ResponseCollectionBase]
)
async def get_collection(
    db: AsyncSession = Depends(get_db),
) -> List[schemas.ResponseCollectionBase]:
    colection_list = await cruds.get_all_collection(db)
    return colection_list


# コレクション削除
@router.delete(
    "/chat/collections/{collection_id}",
    response_model=schemas.DelateResponseCollection,
)
async def delate_collections(
    collection_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.DelateResponseCollection:
    before_data = await cruds.get_collection(db, collection_id)
    if before_data is None:
        raise HTTPException(
            status_code=404, detail=f"{collection_id} not Found"
        )
    collection_info = await cruds.delete_collection(db, original=before_data)
    return collection_info


# ドキュメント登録
@router.get("/chat/collections/{collection_id}")
async def add_documents() -> dict:
    return {}


# ドキュメント削除
@router.delete("/chat/collections/{collection_id}/{documents_id}")
async def delate_documents() -> dict:
    return {}
