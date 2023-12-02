from sqlalchemy.ext.asyncio import AsyncSession
import api.models.model as model
import api.schemas.groups as group_schema
from sqlalchemy import select
from typing import Tuple, Optional, List
from datetime import datetime
from sqlalchemy.engine import Result


# グループ作成
async def create_group(
    db: AsyncSession, group_create: group_schema.CreateGroup
) -> model.Groups:
    group = model.Groups(**group_create.dict())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


# 全グループ取得
async def get_all_group(
    db: AsyncSession,
) -> Optional[List[Tuple[int, str, datetime, datetime]]]:
    result: Result = await db.execute(
        select(
            model.Groups.id,
            model.Groups.name,
            model.Groups.created_at,
            model.Groups.update_at,
        ).filter(model.Groups.publish == True)
    )
    return result.all()


# 特定のグループ取得
async def get_group(
    db: AsyncSession, group_id: int
) -> Optional[model.Groups]:
    result: Result[Tuple[model.Groups]] = await db.execute(
        select(model.Groups).filter(
            model.Groups.id == group_id, model.Groups.publish == True
        )
    )
    group_data = result.first()
    return group_data[0] if group_data is not None else None


# グループ情報更新
async def update_group(
    db: AsyncSession,
    update_data: group_schema.UpdateGroup,
    original: model.Groups,
) -> model.Groups:
    original.name = update_data.name
    await db.commit()
    await db.refresh(original)
    return original


# グループ削除
async def delete_group(
    db: AsyncSession,
    original: model.Groups,
) -> Optional[model.Groups]:
    original.publish = False
    await db.commit()
    await db.refresh(original)
    return original
