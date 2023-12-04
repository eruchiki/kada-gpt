from sqlalchemy.ext.asyncio import AsyncSession
import api.models.model as model
import api.schemas.threads as thread_schema
from sqlalchemy import select
from typing import Tuple, Optional, List
from sqlalchemy.engine import Result, Row


# スレッド作成
async def create_thread(
    db: AsyncSession, thread_create: thread_schema.CreateThread
) -> model.Threads:
    thread = model.Threads(**thread_create.dict())
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return thread


# 全スレッド取得
async def get_all_thread(
    db: AsyncSession,
) -> Optional[List[thread_schema.DisplayResponseThread]]:
    result: Result[
        Tuple[thread_schema.DisplayResponseThread]
    ] = await db.execute(
        select(
            model.Threads.id,
            model.Threads.group_id,
            model.Threads.name,
            model.Threads.model_name,
            model.Threads.relate_num,
            model.Threads.search_method,
            model.Threads.collections_id,
            model.Collections.name.label("collection_name"),
        )
        .outerjoin(model.Collections)
        .filter(model.Threads.publish)
    )
    return result.all()


# 特定のスレッド取得
async def get_thread(
    db: AsyncSession, thread_id: int
) -> Optional[thread_schema.ResponseThread]:
    result: Result[Tuple[thread_schema.ResponseThread]] = await db.execute(
        select(model.Threads)
        .outerjoin(model.Collections)
        .filter(model.Threads.id == thread_id)
    )
    thread_data: Optional[
        Row[Tuple[thread_schema.ResponseThread]]
    ] = result.first()
    return thread_data[0] if thread_data is not None else None


# スレッド情報更新
async def update_thread(
    db: AsyncSession,
    update_data: thread_schema.UpdateThread,
    original: model.Threads,
) -> Optional[thread_schema.UpdateResponseThread]:
    original.name = update_data.name
    original.model_name = update_data.model_name
    original.relate_num = update_data.relate_num
    original.search_method = update_data.search_method
    original.collections_id = update_data.collection_id
    await db.commit()
    await db.refresh(original)
    return original


# スレッド削除
async def delete_thread(
    db: AsyncSession,
    user_id: int,
    original: model.Threads,
) -> Optional[thread_schema.ResponseThread]:
    update_data = await get_thread(db, user_id)
    if update_data is not None:
        original.publish = False
    else:
        return None
    await db.commit()
    await db.refresh(original)
    return original


# メッセージ送信
# async def send_message(
#     db: AsyncSession,
#     user_id: int,
#     original: model.Threads,
# ):
# 　履歴取得
