from sqlalchemy.ext.asyncio import AsyncSession
import api.models.users as user_model
import api.schemas.users as user_schema
from sqlalchemy import select
from typing import Tuple, Optional, List
from sqlalchemy.engine import Result, Row


# ユーザ作成
async def create_user(
    db: AsyncSession, user_create: user_schema.CreateUser
) -> user_model.Users:
    user = user_model.Users(**user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# 全ユーザ取得
async def get_all_user(
    db: AsyncSession,
) -> Optional[List[Tuple[user_schema.UserInfo]]]:
    result: Result[Tuple[user_schema.UserInfo]] = await db.execute(
        select(
            user_model.Users.id,
            user_model.Users.name,
            user_model.Users.email,
            user_model.Groups.name,
        ).outerjoin(user_model.Groups)
    )
    return result.all()


# 特定のユーザ取得
async def get_user(
    db: AsyncSession, user_id: int
) -> Optional[user_schema.ResponseUser]:
    result: Result[Tuple[user_schema.ResponseUser]] = await db.execute(
        select(
            user_model.Users.id,
            user_model.Users.group_id,
            user_model.Users.name,
            user_model.Users.email,
            user_model.Users.created_at,
            user_model.Users.update_at,
            user_model.Users.admin,
            user_model.Groups.name,
        )
        .outerjoin(user_model.Groups)
        .filter(user_model.Users.id == user_id)
    )
    user_data: Optional[Row[Tuple[user_schema.ResponseUser]]] = result.first()
    return user_data[0]


# ユーザ情報更新
async def update_user(
    db: AsyncSession, user_id: int, update_data: user_schema.UpdateUser
) -> Optional[user_schema.ResponseUser]:
    before_data = await get_user(db, user_id)
    if before_data is not None:
        before_data.name = update_data.name
        before_data.password = update_data.password
        before_data.group_id = update_data.group_id
        before_data.email = update_data.email
    else:
        return None
    await db.commit()
    await db.refresh(before_data)
    return before_data


# ユーザ削除
async def delete_user(
    db: AsyncSession,
    user_id: int,
) -> Optional[user_schema.ResponseUser]:
    update_data = await get_user(db, user_id)
    if update_data is not None:
        update_data.publish = False
    else:
        return None
    await db.commit()
    await db.refresh(update_data)
    return update_data
