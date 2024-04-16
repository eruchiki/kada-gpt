from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import api.models.model as model
from typing import Optional


class ThreadBase(BaseModel):
    name: str = Field(None, json_schema_extra={"example": "テスト"})
    model_name: str = Field(None, json_schema_extra={"example": "gpt4"})
    relate_num: int
    collections_id: int
    search_method: str = Field(None, json_schema_extra={"example": "従来手法"})


class CreateThread(ThreadBase):
    create_user_id: int
    group_id: int


class UpdateThread(ThreadBase):
    pass


class ResponseThread(ThreadBase):
    id: int
    group_id: int
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DisplayResponseThread(ResponseThread):
    collection_name: str


class ChatHistoryResponseThread(ResponseThread):
    publish: bool
    create_user_id: int


class UpdateResponseThread(ResponseThread):
    publish: bool


class DeleteResponseThread(ResponseThread):
    publish: bool


class CreateResponseThread(CreateThread):
    id: int
    model_config = ConfigDict(from_attributes=True)


# class MessageBase(BaseModel):
#     message_text: str
#     response_text: str


class SendMessage(BaseModel):
    create_user_id: int
    thread_id: int
    collection_id: int
    relate_num: int = Field(
        None, description="検索で取得するドキュメント数", example=3
    )
    search_method: str = Field(
        "default",
        description="検索手法を指定",
        json_schema_extra={"example": "select"},
    )
    model_name: str = Field(
        None,
        description="モデル名を指定",
        json_schema_extra={"example": "gpt-3.5-turbo"},
    )
    message_text: str = Field(
        None,
        description="メッセージ",
        json_schema_extra={"example": "Hello World!"},
    )


class ResponseMessage(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DesplayResponseMessage(ResponseMessage):
    message_text: str
    response_text: str
    relate_num: int
    created_at: datetime
    update_at: datetime
