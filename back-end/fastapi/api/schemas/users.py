from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class BaseUser(BaseModel):
    name: Optional[str] = Field(None, json_schema_extra={"example": "テスト"})
    email: Optional[str] = Field(
        None, json_schema_extra={"example": "hogefuga@kagawa-u.ac.jp"}
    )


class CreateUser(BaseUser):
    password: str
    group_id: int


class CreateResponseUser(CreateUser):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseUser):
    group_id: int
    password: str


class ResponseUser(BaseUser):
    id: int
    group_id: int
    created_at: datetime
    update_at: datetime
    is_admin: bool
    model_config = ConfigDict(from_attributes=True)


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
