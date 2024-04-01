from sqlalchemy.ext.asyncio import AsyncSession
import api.models.model as model
import api.schemas.collections as collection_schema
from sqlalchemy import select
from typing import Optional, List
from sqlalchemy.engine import Result


# コレクション作成
async def create_collection(
    db: AsyncSession, collection_create: collection_schema.CreateCollection
) -> model.Collections:
    collection = model.Collections(**collection_create.dict())
    db.add(collection)
    await db.commit()
    await db.refresh(collection)
    return collection


# 全コレクション取得
async def get_all_collection(
    db: AsyncSession,
) -> Optional[List[model.Collections]]:
    result: Result = await db.execute(
        select(model.Collections).filter(model.Collections.publish)
    )
    return result.all()


# 特定のコレクション取得
async def get_collection(
    db: AsyncSession, collection_id: int
) -> Optional[model.Collections]:
    result: Result = await db.execute(
        select(model.Collections).filter(
            model.Collections.id == collection_id, model.Collections.publish
        )
    )
    collection_data = result.first()
    return collection_data[0] if collection_data is not None else None


# コレクション削除
async def delete_collection(
    db: AsyncSession,
    original: model.Collections,
) -> Optional[model.Collections]:
    not original.publish
    await db.commit()
    await db.refresh(original)
    return original
