from fastapi import APIRouter
from typing import List
from api.schemas import users


router = APIRouter()


# ユーザリスト取得
@router.get("/chat/users", response_model=List[users.UserInfo])
async def get_user_list() -> List:
    return []


# ユーザ登録
@router.post("/chat/users", response_model=users.ResponseCreateUser)
async def create_user(user_body: users.CreateUser) -> users.ResponseCreateUser:
    return users.ResponseCreateUser(id=1, **user_body.dict())


# ユーザ情報変更
@router.patch("/chat/users/{user_id}")
async def update_user_info() -> dict:
    return {}


# ユーザ削除
@router.delete("/chat/users/{user_id}", response_model=users.DeleteUser)
async def delate_user() -> users.DeleteUser:
    return {}


# ユーザ情報取得
@router.get("/chat/users/{user_id}", response_model=users.UserInfo)
async def get_user_info() -> users.UserInfo:
    return {}
