from sqlalchemy.ext.asyncio import AsyncSession
import api.models.model as model
import api.schemas.users as user_schema
from sqlalchemy import select
from typing import Tuple, Optional, List
from datetime import datetime
from sqlalchemy.engine import Result


# ユーザ作成
async def create_user(
    db: AsyncSession, user_create: user_schema.CreateUser
) -> model.Users:
    user = model.Users(**user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# 全ユーザ取得
async def get_all_user(
    db: AsyncSession,
) -> Optional[List[Tuple[int, int, str, str, str, datetime, datetime, bool]]]:
    result: Result = await db.execute(
        select(
            model.Users.id,
            model.Users.group_id,
            model.Users.name,
            model.Groups.name.label("group_name"),
            model.Users.email,
            model.Users.created_at,
            model.Users.update_at,
            model.Users.admin,
        )
        .outerjoin(model.Groups)
        .filter(model.Users.publish)
    )
    return result.all()


# 特定のユーザ取得
async def get_user(db: AsyncSession, user_id: int) -> Optional[model.Users]:
    result: Result = await db.execute(
        select(model.Users).filter(
            model.Users.id == user_id, model.Users.publish
        )
    )
    user_data = result.first()
    return user_data[0] if user_data is not None else None


# 特定のユーザ取得
async def get_user_and_group_name(
    db: AsyncSession, user_id: int
) -> Tuple[int, int, str, str, str, str, datetime, datetime, bool]:
    result: Result = await db.execute(
        select(
            model.Users.id,
            model.Users.group_id,
            model.Users.name,
            model.Users.password,
            model.Groups.name.label("group_name"),
            model.Users.email,
            model.Users.created_at,
            model.Users.update_at,
            model.Users.admin,
        )
        .filter(model.Users.id == user_id, model.Users.publish == True)
        .outerjoin(model.Groups)
    )
    user_data = result.first()
    return user_data if user_data is not None else None


# ユーザ情報更新
async def update_user(
    db: AsyncSession,
    update_data: user_schema.UpdateUser,
    original: model.Users,
) -> model.Users:
    original.name = update_data.name
    original.password = update_data.password
    original.group_id = update_data.group_id
    original.email = update_data.email
    await db.commit()
    await db.refresh(original)
    return original


# ユーザ削除
async def delete_user(
    db: AsyncSession,
    original: model.Users,
) -> Optional[model.Users]:
    original.publish = False
    await db.commit()
    await db.refresh(original)
    return original
