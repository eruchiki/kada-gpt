from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CollectionBase(BaseModel):
    name: str = Field(None, json_schema_extra={"example": "テスト"})
    create_user_id: int


class CreateCollection(CollectionBase):
    pass


class CreateResponseCollection(CreateCollection):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseCollectionBase(CollectionBase):
    id: int
    created_at: datetime
    update_at: datetime
    publish: bool


class DelateResponseCollection(ResponseCollectionBase):
    pass
