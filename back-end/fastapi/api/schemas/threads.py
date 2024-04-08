from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ThreadBase(BaseModel):
    name: str = Field(None, json_schema_extra={"example": "テスト"})
    model_name: str = Field(None, json_schema_extra={"example": "gpt4"})
    relate_num: int
    collection_id: int
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
    user_id: int
    thead_id: int
    collection_name: Optional[str] = Field(None, description="コレクション名を指定")
    relate_num: Optional[int] = Field(None, example=5)
    search_method: Optional[str] = Field(None, description="検索手法を指定")
    model_name: Optional[str] = Field(None, description="モデル名を指定")
    message_text: str = Field(None, description="メッセージ")


class ResponseMessage(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
    response_text: str


class DesplayResponseMessage(ResponseMessage):
    id: int
    create_time: float
    created_at: datetime
    update_at: datetime
    relate_number: str
    document_id: str
