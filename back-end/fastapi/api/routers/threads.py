from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
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
    "/chat/users/{user_id}/thread",
    response_model=List[schema.DisplayResponseThread],
)
async def get_thread_all(
    db: AsyncSession = Depends(get_db),
) -> schema.DisplayResponseThread:
    return await cruds.get_all_thread(db)


# スレッド削除
@router.delete(
    "/chat/users/{user_id}/thread/{thread_id}",
    response_model=schema.DeleteResponseThread,
)
async def delate_thread(
    thread_id: int, db: AsyncSession = Depends(get_db)
) -> Optional[schema.DeleteResponseThread]:
    before_data = await cruds.get_thread(db, thread_id)
    if before_data is None:
        raise HTTPException(status_code=404, detail=f"{thread_id} not Found")
    thread_info = await cruds.delete_thread(db, thread_id, original=before_data)
    return thread_info


# スレッド内のチャット履歴取得
@router.get("/chat/users/{user_id}/thread/{thread_id}",
            response_model=schema.DeleteResponseThread)
async def get_thraed_chat() -> dict:
    return {}


# チャット送受信
@router.post("/chat/users/{user_id}/thread/{thread_id}")
async def get_user_info() -> dict:
    return {}
