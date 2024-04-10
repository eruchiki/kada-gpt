from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from api.db import get_db
from api.vs import get_vs
import api.schemas.threads as schema
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.threads as cruds
from qdrant_client import QdrantClient


router = APIRouter()


# スレッド作成
@router.post(
    "/chat/users/{user_id}/thread", response_model=schema.CreateResponseThread
)
async def create_thread(
    thread_body: schema.CreateThread, db: AsyncSession = Depends(get_db)
) -> schema.CreateResponseThread:
    return await cruds.create_thread(db, thread_body)


# スレッド取得
@router.get(
    "/chat/users/{user_id}/thread/{thread_id}",
    response_model=Optional[schema.ChatHistoryResponseThread],
)
async def get_thread(
    user_id: int,
    thread_id: int,
    db: AsyncSession = Depends(get_db),
) -> schema.ChatHistoryResponseThread:
    thread_data = await cruds.get_thread(db, user_id, thread_id)
    if thread_data is None:
        raise HTTPException(status_code=404, detail=f"{thread_id} not Found")
    return thread_data


# スレッド一覧取得
@router.get(
    "/chat/users/{user_id}/thread",
    response_model=List[schema.DisplayResponseThread],
)
async def get_thread_all(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> schema.DisplayResponseThread:
    return await cruds.get_all_thread(db, user_id)


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
    thread_info = await cruds.delete_thread(
        db, thread_id, original=before_data
    )
    return thread_info


# チャット送受信
@router.post(
    "/chat/users/{user_id}/thread/{thread_id}",
    response_model=schema.DesplayResponseMessage,
)
async def send_message(
    message_body: schema.SendMessage,
    db: AsyncSession = Depends(get_db),
    vs: QdrantClient = Depends(get_vs),
) -> schema.DesplayResponseMessage:
    return await cruds.send_message(db, vs, message_body)


# チャット履歴取得
@router.get(
    "/chat/users/{user_id}/thread/{thread_id}",
    response_model=List[schema.DesplayResponseMessage],
)
async def get_all_messages(
    user_id: int, thread_id: int, db: AsyncSession = Depends(get_db)
) -> List[schema.DesplayResponseMessage]:
    return await cruds.get_all_messages(db, user_id, thread_id)
