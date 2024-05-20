from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CollectionBase(BaseModel):
    name: str = Field(None, json_schema_extra={"example": "テスト"})
    group_id: int
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


class DelateResponseCollection(ResponseCollectionBase):
    pass


class AddDocument(BaseModel):
    create_user_id: int


class AddResponseDocument(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseDocuments(BaseModel):
    id: int
    collection_id: int
    create_user_id: int
    uri: str
    created_at: datetime
    update_at: datetime


class DelateResponseDocument(BaseModel):
    id: int
    collection_id: int
    create_user_id: int
    uri: str
    created_at: datetime
    update_at: datetime
