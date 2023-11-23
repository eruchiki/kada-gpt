from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    name: str = Field(None, example="テスト")
    email: str = Field(None, example="hoge@kagawa-u.ac.jp")
    group: str = Field(None, example="情シス")


class CreateUser(BaseUser):
    password: str = Field(None, example="XXXXXXXX")

    class Config:
        orm_mode = True


class ResponseCreateUser(CreateUser):
    id: int


class UserInfo(BaseUser):
    id: int


class DeleteUser(UserInfo):
    admin: bool
