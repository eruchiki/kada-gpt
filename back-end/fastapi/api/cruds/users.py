from sqlalchemy.ext.asyncio import AsyncSession
import api.models.users as user_model
import api.schemas.users as user_schema
from sqlalchemy import select
from typing import List, Tuple, Optional
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
async def get_all_user(db: AsyncSession) -> List[Tuple[str]]:
    result: Result = await db.execute(
        select(
            user_model.Users.name,
            user_model.Users.email,
            user_model.Groups.name,
        ).outerjoin(user_model.Groups)
    )
    return result.all()


# 特定のユーザ取得
async def get_user(
    db: AsyncSession, user_id: int
) -> List[Tuple[str, str, str]]:
    result = await db.execute(
        select(
            user_model.Users.name,
            user_model.Users.email,
            user_model.Groups.name,
        )
        .outerjoin(user_model.Groups)
        .filter(user_model.Users.id == user_id)
    )
    return result.first()


# ユーザ削除
async def delete_user(
    db: AsyncSession,
    user_id: int,
) -> Optional[user_model.Users]:
    result: Result = await db.execute(
        select(user_model.Users).filter(user_model.Users.id == user_id)
    )
    update_data: Optional[Tuple[user_model.Users]] = result.first()
    if update_data is not None:
        update_data[0].exsited = False
    else:
        return None
    await db.commit()
    await db.refresh(update_data[0])
    return update_data
