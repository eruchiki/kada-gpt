from pydantic import BaseModel, Field
from datetime import datetime


class BaseUser(BaseModel):
    name: str = Field(None, example="テスト")
    email: str = Field(None, example="hoge@kagawa-u.ac.jp")
    group: str = Field(None, example="情シス")


class CreateUser(BaseUser):
    password: str = Field(None, example="XXXXXXXX")

    class Config:
        orm_mode = True


class ResponseUser(BaseUser):
    id: int
    group_id: int
    password: str
    create_time: datetime
    update_time: datetime
    admin: bool
    publish: bool


class UserInfo(BaseUser):
    id: int


class UpdateUser(CreateUser):
    id: int
    group_id: int
