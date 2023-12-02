from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BaseUser(BaseModel):
    name: Optional[str] = Field(None, example="テスト")
    email: Optional[str] = Field(None, example="hoge@kagawa-u.ac.jp")


class CreateUser(BaseUser):
    password: str
    group_id: int


class CreateResponseUser(CreateUser):
    id: int

    class Config:
        orm_mode = True


class UpdateUser(BaseUser):
    group_id: int
    password: str


class ResponseUser(BaseUser):
    id: int
    group_id: int
    created_at: datetime
    update_at: datetime
    admin: bool

    class Config:
        orm_mode = True


class DisplayResponseUser(ResponseUser):
    group_name: str


class GertResponseUser(ResponseUser):
    group_name: str
    password: str


class DeleteResponseUser(ResponseUser):
    publish: bool
    password: str


class UpdateResponseUser(ResponseUser):
    password: str
