from pydantic import BaseModel, Field


class Thread(BaseModel):
    id: int
    name: str = Field(None, example="テスト")
    model_name: str = Field(None, example="gpt4")
    collection_name: str = Field(None, example="test")
    method: str = Field(None, example="従来手法")
