from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.users as schema
import api.cruds.users as cruds


router = APIRouter()


# ユーザリスト取得
@router.get("/chat/users", response_model=List[schema.DisplayResponseUser])
async def get_user_list(
    db: AsyncSession = Depends(get_db),
) -> List[schema.DisplayResponseUser]:
    user_list = await cruds.get_all_user(db)
    return user_list


# ユーザ登録
@router.post("/chat/users", response_model=schema.CreateResponseUser)
async def create_user(
    user_body: schema.CreateUser, db: AsyncSession = Depends(get_db)
) -> schema.CreateResponseUser:
    return await cruds.create_user(db, user_body)


# ユーザ情報変更
@router.patch(
    "/chat/users/{user_id}", response_model=schema.UpdateResponseUser
)
async def update_user_info(
    user_id: int,
    user_body: schema.UpdateUser,
    db: AsyncSession = Depends(get_db),
) -> schema.UpdateResponseUser:
    before_data = await cruds.get_user(db, user_id)
    if before_data is None:
        raise HTTPException(status_code=404, detail=f"{user_id} not Found")
    user_info = await cruds.update_user(db, user_body, original=before_data)
    return user_info


# ユーザ削除
@router.delete(
    "/chat/users/{user_id}", response_model=schema.DeleteResponseUser
)
async def delate_user(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> schema.ResponseUser:
    before_data = await cruds.get_user(db, user_id)
    if before_data is None:
        raise HTTPException(status_code=404, detail=f"{user_id} not Found")
    user_info = await cruds.delete_user(db, original=before_data)
    return user_info


# ユーザ情報取得
@router.get("/chat/users/{user_id}", response_model=schema.GertResponseUser)
async def get_user_info(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> schema.GertResponseUser:
    user_info = await cruds.get_user_and_group_name(db, user_id)
    print(user_info)
    if user_info is None:
        raise HTTPException(status_code=404, detail=f"{user_id} not Found")
    return user_info
