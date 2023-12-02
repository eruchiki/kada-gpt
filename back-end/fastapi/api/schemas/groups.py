from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CreateGroup(BaseModel):
    name: Optional[str] = Field(None, example="test")


class CreateResponseGroup(CreateGroup):
    id: int

    class Config:
        orm_mode = True


class ResponseGroup(CreateGroup):
    id: int
    created_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True


class UpdateGroup(CreateGroup):
    pass
