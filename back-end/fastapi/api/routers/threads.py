from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from api.db import get_db
from api.vs import get_vs
import api.schemas.threads as schema
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.threads as cruds
from qdrant_client import QdrantClient
from fastapi.responses import FileResponse


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


# スレッド一覧取得(group id条件)
@router.get(
    "/chat/users/{user_id}/{group_id}/thread",
    response_model=List[schema.DisplayResponseThread],
)
async def get_thread_all_group(
    user_id: int,
    group_id: int,
    db: AsyncSession = Depends(get_db),
) -> schema.DisplayResponseThread:
    return await cruds.get_all_thread_group(db, group_id)


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
    response_model=schema.ResponseMessage,
)
async def send_message(
    message_body: schema.SendMessage,
    db: AsyncSession = Depends(get_db),
    vs: QdrantClient = Depends(get_vs),
) -> schema.ResponseMessage:
    return await cruds.send_message(db, vs, message_body)


# チャット履歴取得
@router.get(
    "/chat/users/{user_id}/thread/{thread_id}/history",
    response_model=List[schema.DesplayResponseMessage],
)
async def get_history(
    user_id: int, thread_id: int, db: AsyncSession = Depends(get_db)
) -> List[schema.DesplayResponseMessage]:
    return await cruds.get_history(db, user_id, thread_id)
