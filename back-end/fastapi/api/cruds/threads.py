from sqlalchemy.ext.asyncio import AsyncSession
import api.models.model as model
import api.schemas.threads as thread_schema
from sqlalchemy import select
from typing import Tuple, Optional, List
from sqlalchemy.engine import Result, Row
from qdrant_client import QdrantClient
import api.models.qdrant as qdrant
import api.module.answer_create as answer_create
import json


# スレッド作成
async def create_thread(
    db: AsyncSession, thread_create: thread_schema.CreateThread
) -> model.Threads:
    thread = model.Threads(**thread_create.model_dump())
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return thread


# 全スレッド取得
async def get_all_thread(
    db: AsyncSession,
    user_id: int,
) -> Optional[List[Tuple[thread_schema.DisplayResponseThread]]]:
    result: Result = await db.execute(
        select(
            model.Threads.id,
            model.Threads.group_id,
            model.Threads.name,
            model.Threads.model_name,
            model.Threads.relate_num,
            model.Threads.search_method,
            model.Threads.created_at,
            model.Threads.update_at,
            model.Threads.collections_id,
            model.Collections.name.label("collection_name"),
        )
        .outerjoin(model.Collections)
        .filter(model.Threads.publish, model.Threads.create_user_id == user_id)
    )
    return result.all()


# 特定のスレッド取得
async def get_thread(
    db: AsyncSession, user_id: int, thread_id: int
) -> Optional[thread_schema.ChatHistoryResponseThread]:
    result: Result = await db.execute(
        select(model.Threads).filter(
            model.Threads.id == thread_id, model.Threads.publish
        )
    )
    thread_data = result.first()
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
    original.collections_id = update_data.collections_id
    await db.commit()
    await db.refresh(original)
    return original


# スレッド削除
async def delete_thread(
    db: AsyncSession,
    thread_id: int,
    original: model.Threads,
) -> Optional[thread_schema.DeleteResponseThread]:
    update_data = await get_thread(db, thread_id)
    if update_data is not None:
        original.publish = False
    else:
        return None
    await db.commit()
    await db.refresh(original)
    return original


# メッセージ送信
async def send_message(
    db: AsyncSession, vs: QdrantClient, send_chat: thread_schema.SendMessage
) -> model.Chat:
    # info: Result = await db.execute(
    #     select(
    #         model.Documents.id,
    #         model.Documents.collection_id,
    #         model.Documents.create_user_id,
    #         model.Documents.uri,
    #         model.Documents.created_at,
    #     ).filter(
    #         model.Documents.publish,
    #         model.Documents.create_user_id == send_chat.user_id,
    #         model.Documents.collection_id == send_chat.collection_id,
    #     )
    # )
    # document_info = []
    # for row in info:
    #     doc_meta = {"id": int(row[0]), "uri": str(row[3])}
    #     document_info.append(doc_meta)
    vs_client = qdrant.VectorStore(
        collection_id=str(send_chat.collection_id), client=vs
    )
    vs_client.set_qdrant()
    result = await answer_create.answer(
        query=send_chat.message_text, db=vs_client.qdrant, mode="select"
    )
    with open("test.txt", "w") as f:
        f.write(json.dumps(result).encode().decode("unicode-escape"))
    output = {
        "response_text": result["answer"],
    }
    chat = model.Chat(**dict(**send_chat.model_dump(), **output))
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


# 履歴取得
async def get_history(
    db: AsyncSession, thread_id: int
) -> Optional[List[thread_schema.DesplayResponseMessage]]:
    result: Result[Tuple[thread_schema.DesplayResponseMessage]] = (
        await db.execute(
            select(
                model.Chat.id,
                model.Chat.message_text,
                model.Chat.response_text,
                model.Chat.relate_number,
                model.Chat.document_id,
                model.Chat.create_time,
                model.Chat.created_at,
                model.Chat.update_at,
            )
            .outerjoin(model.Collections)
            .filter(model.Chat.publish, model.Chat.thread_id == thread_id)
        )
    )
    return result.all()
