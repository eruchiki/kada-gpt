from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class CreateGroup(BaseModel):
    name: Optional[str] = Field(None, json_schema_extra={"example": "test"})


class CreateResponseGroup(CreateGroup):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseGroup(CreateGroup):
    id: int
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateGroup(CreateGroup):
    pass
