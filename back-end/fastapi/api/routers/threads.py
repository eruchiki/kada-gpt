from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.db import get_db
import api.schemas.threads as schema
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.threads as cruds


router = APIRouter()


# スレッド作成
@router.post(
    "/chat/users/{user_id}/thread", response_model=schema.CreateResponseThread
)
async def create_thread(
    thread_body: schema.CreateThread, db: AsyncSession = Depends(get_db)
) -> schema.CreateResponseThread:
    return await cruds.create_thread(db, thread_body)


# スレッド一覧取得
@router.get(
    "/chat/users/{user_id}/thread", response_model=List[schema.DisplayThread]
)
async def add_user(
    db: AsyncSession = Depends(get_db),
) -> schema.ResponseMessage:
    return await cruds.get_all_thread(db)


# スレッド削除
@router.delete(
    "/chat/users/{user_id}/thread/{thread_id}",
    response_model=schema.ThreadInfo,
)
async def delate_thread(
    thread_id: int, db: AsyncSession = Depends(get_db)
) -> schema.ThreadInfo:
    before_data = await cruds.get_thread(db, thread_id)
    if before_data is None:
        raise HTTPException(status_code=404, detail=f"{thread_id} not Found")
    user_info = await cruds.delete_thread(db, original=before_data)
    return user_info


# スレッド内のチャット履歴取得
@router.get("/chat/users/{user_id}/thread/{thread_id}")
async def get_thraed_chat() -> dict:
    return {}


# チャット送信
@router.post("/chat/users/{user_id}/thread/{thread_id}")
async def get_user_info() -> dict:
    return {}
