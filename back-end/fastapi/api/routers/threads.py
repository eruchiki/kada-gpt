from fastapi import APIRouter
from typing import List
from api.schemas import threads

router = APIRouter()


# スレッド作成
@router.post("/chat/users/{user_id}/thread",
             response_model=threads.Thread)
async def create_thread() -> dict:
    return {}


# スレッド一覧取得
@router.get("/chat/users/{user_id}/thread",
            response_model=List[threads.Thread])
async def add_user() -> dict:
    return {}


# スレッド内のチャット履歴取得
@router.get("/chat/users/{user_id}/thread/{thread_id}")
async def get_thraed_chat() -> dict:
    return {}


# スレッド削除
@router.delete("/chat/users/{user_id}/thread/{thread_id}")
async def delate_thread() -> dict:
    return {}


# チャット送信
@router.post("/chat/users/{user_id}/thread/{thread_id}")
async def get_user_info() -> dict:
    return {}
