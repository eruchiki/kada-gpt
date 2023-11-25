from sqlalchemy.ext.asyncio import AsyncSession
import api.models.threads as thread_model

# import api.models.users as user_model
import api.schemas.threads as thread_schema
from sqlalchemy import select
from typing import Tuple, Optional, List
from sqlalchemy.engine import Result, Row


# スレッド作成
async def create_thread(
    db: AsyncSession, thread_create: thread_schema.CreateThread
) -> thread_model.Threads:
    thread = thread_model.Threads(**thread_create.dict())
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return thread


# 全スレッド取得
async def get_all_thread(
    db: AsyncSession,
) -> Optional[List[Tuple[thread_schema.ThreadInfo]]]:
    result: Result[Tuple[thread_schema.ThreadInfo]] = await db.execute(
        select(
            thread_model.Threads.id,
            thread_model.Threads.name,
            thread_model.Threads.model_name,
            thread_model.Threads.search_method,
            thread_model.Collections.name,
        ).outerjoin(thread_model.Collections)
    )
    return result.all()


# 特定のスレッド取得
async def get_thread(
    db: AsyncSession, thread_id: int
) -> Optional[thread_schema.ResponseThread]:
    result: Result[Tuple[thread_schema.ResponseThread]] = await db.execute(
        select(
            thread_model.Threads.id,
            thread_model.Threads.group_id,
            thread_model.Threads.name,
            thread_model.Threads.model_name,
            thread_model.Threads.created_at,
            thread_model.Threads.update_at,
            thread_model.Threads.exsited,
            thread_model.Threads.collections_id,
            thread_model.Collections.name,
        )
        .outerjoin(thread_model.Collections)
        .filter(thread_model.Threads.id == thread_id)
    )
    thread_data: Optional[
        Row[Tuple[thread_schema.ResponseThread]]
    ] = result.first()
    return thread_data[0]


# スレッド情報更新
async def update_thread(
    db: AsyncSession, user_id: int, update_data: thread_schema.ThreadBase
) -> Optional[thread_schema.ResponseThread]:
    before_data = await get_thread(db, user_id)
    if before_data is not None:
        before_data.name = update_data.name
        before_data.model_name = update_data.model_name
        before_data.search_method = update_data.search_method
        before_data.collections_id = update_data.collection_id
    else:
        return None
    await db.commit()
    await db.refresh(before_data)
    return before_data


# スレッド削除
async def delete_thread(
    db: AsyncSession,
    user_id: int,
) -> Optional[thread_schema.ResponseCreateUser]:
    update_data = await get_thread(db, user_id)
    if update_data is not None:
        update_data.publish = False
    else:
        return None
    await db.commit()
    await db.refresh(update_data)
    return update_data


# メッセージ送信

# 　履歴取得
