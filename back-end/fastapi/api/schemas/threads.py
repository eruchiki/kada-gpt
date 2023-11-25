from pydantic import BaseModel, Field


class ThreadBase(BaseModel):
    name: str = Field(None, example="テスト")
    model_name: str = Field(None, example="gpt4")
    collection_name: str = Field(None, example="test")
    search_method: str = Field(None, example="従来手法")


class CreateThread(ThreadBase):
    create_user_id: int
    group_id: int

    class Config:
        orm_mode = True


class ThreadInfo(ThreadBase):
    id: int

    class Config:
        orm_mode = True


class ResponseThread(ThreadBase):
    id: int


class DelateThread(ThreadBase):
    publish: bool
