from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import users
import api.cruds.users as cruds


router = APIRouter()


# ユーザリスト取得
@router.get("/chat/users", response_model=List[users.UserInfo])
async def get_user_list(
    db: AsyncSession = Depends(get_db),
) -> List[users.UserInfo]:
    user_list = await cruds.get_all_user(db)
    return user_list


# ユーザ登録
@router.post("/chat/users", response_model=users.ResponseUser)
async def create_user(
    db: AsyncSession, user_body: users.CreateUser
) -> users.ResponseUser:
    return await cruds.create_user(db, user_body)


# ユーザ情報変更
@router.patch("/chat/users/{user_id}", response_model=users.ResponseUser)
async def update_user_info(
    user_id: int, db: AsyncSession, user_body: users.UpdateUser
) -> users.ResponseUser:
    user_info = await cruds.update_user(db, user_id, user_body)
    if user_info is None:
        raise HTTPException(status_code=404, detail=f"{user_id} not Found")
    return user_info


# ユーザ削除
@router.delete(
    "/chat/users/{user_id}", response_model=users.ResponseUser
)
async def delate_user(
    user_id: int, db: AsyncSession
) -> users.ResponseUser:
    user_info = await cruds.delete_user(db, user_id)
    if user_info is None:
        raise HTTPException(status_code=404, detail=f"{user_id} not Found")
    return user_info


# ユーザ情報取得
@router.get("/chat/users/{user_id}", response_model=users.ResponseUser)
async def get_user_info(
    user_id: int, db: AsyncSession
) -> users.ResponseUser:
    user_info = await cruds.get_user(db, user_id)
    if user_info is None:
        raise HTTPException(status_code=404, detail=f"{user_id} not Found")
    return user_info
