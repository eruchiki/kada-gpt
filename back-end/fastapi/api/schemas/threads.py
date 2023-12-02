from pydantic import BaseModel, Field
from datetime import datetime


class ThreadBase(BaseModel):
    name: str = Field(None, example="テスト")
    model_name: str = Field(None, example="gpt4")
    relate_num: int
    collection_id: int
    search_method: str = Field(None, example="従来手法")


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

    class Config:
        orm_mode = True


class DisplayResponseThread(ResponseThread):
    collection_name: str


class UpdateResponseThread(ResponseThread):
    publish: bool


class DeleteResponseThread(ResponseThread):
    publish: bool


class CreateResponseThread(CreateThread):
    id: int

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    message_text: str
    response_text: str


class SendMessage(MessageBase):
    thead_id: int
    collection_name: str
    relate_num: int
    search_method: str
    model_name: str


class ResponseMessage(MessageBase):
    id: int

    class Config:
        orm_mode = True


class DesplayResponseMessage(ResponseMessage):
    id: int
    create_time: float
    created_at: datetime
    update_at: datetime
    relate_number: str
    document_id: str
