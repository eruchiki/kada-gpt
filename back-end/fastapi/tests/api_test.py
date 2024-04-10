import pytest
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from api.db import get_db, Base
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def async_client() -> AsyncClient:
    # Async用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db() -> AsyncSession:
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url="http://chat") as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_read(async_client: AsyncClient) -> None:
    # groupに関するapiテスト
    # create
    response = await async_client.post(
        "/chat/groups", json={"name": "グループ1"}
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == 1
    assert response_obj["name"] == "グループ1"
    # all get
    response = await async_client.get("/chat/groups")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["id"] == 1
    assert response_obj[0]["name"] == "グループ1"
    # get
    response = await async_client.get("/chat/groups/1")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == 1
    assert response_obj["name"] == "グループ1"
    # 404 test
    response = await async_client.get("/chat/groups/2")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    # update
    response = await async_client.patch(
        "/chat/groups/1", json={"name": "グループ更新"}
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["name"] == "グループ更新"
    # delate
    response = await async_client.post(
        "/chat/groups", json={"name": "グループ2"}
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == 2
    assert response_obj["name"] == "グループ2"
    response = await async_client.delete("/chat/groups/2")
    assert response.status_code == starlette.status.HTTP_200_OK
    # 確認
    response = await async_client.get("/chat/groups/2")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    # userに関するapiテスト
    # create
    response = await async_client.post(
        "/chat/users",
        json={
            "name": "user1",
            "email": "hogehoge@gmail.com",
            "password": "password",
            "group_id": 1,
        },
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == 1
    assert response_obj["name"] == "user1"
    # get list
    response = await async_client.get("/chat/users")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    # get
    response = await async_client.get("/chat/users/1")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == 1
    assert response_obj["name"] == "user1"
    assert response_obj["password"] == "password"
    assert response_obj["email"] == "hogehoge@gmail.com"
    assert response_obj["group_id"] == 1
    assert response_obj["is_admin"] is False
    # 404 test
    response = await async_client.get("/chat/users/2")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    # update
    response = await async_client.patch(
        "/chat/users/1",
        json={
            "name": "user1",
            "email": "fugafuga@gmail.com",
            "password": "password",
        },
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["email"] == "fugafuga@gmail.com"
    # delate
    response = await async_client.post(
        "/chat/users",
        json={
            "name": "user2",
            "email": "hogehoge@gmail.com",
            "password": "password",
            "group_id": 1,
        },
    )
    response_obj = response.json()
    assert response_obj["id"] == 2
    assert response_obj["name"] == "user2"
    assert response.status_code == starlette.status.HTTP_200_OK
    response = await async_client.delete("/chat/users/2")
    assert response.status_code == starlette.status.HTTP_200_OK
    # 確認
    response = await async_client.get("/chat/users/2")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    # collectionに関するテスト
    # create
    response = await async_client.post(
        "/chat/collections", json={"name": "test", "create_user_id": 1}
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    # get
    # response = await async_client.get("/chat/collections/1?create_user_id=1")
    # assert response.status_code == starlette.status.HTTP_200_OK
    # response_obj = response.json()
    # assert response_obj["id"] == 1
    # assert response_obj["create_user_id"] == 1
    # assert response_obj["name"] == "test"
    # get list
    response = await async_client.get("/chat/collections")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    # document add
    fileName1 = "/src/tests/fit.pdf"
    fileName2 = "/src/tests/jsai.pdf"

    fileDataBinary1 = open(fileName1, "rb").read()
    fileDataBinary2 = open(fileName2, "rb").read()

    mime_type = "application/pdf"
    fileList = fileList = [
        ("files", (fileName1, fileDataBinary1, mime_type)),
        ("files", (fileName2, fileDataBinary2, mime_type)),
    ]

    response = await async_client.post(
        "/chat/collections/1?create_user_id=1", files=fileList
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    print(response_obj)
    assert len(response_obj) == 2
    assert response_obj[0]["id"] == 1
    assert response_obj[1]["id"] == 2
    # threadに関するテスト
    # create
    response = await async_client.post(
        "/chat/users/1/thread",
        json={"name": "test", "model_name": "gpt4",
              "relate_num": 4, "collections_id": 1,
              "search_method": "default", "create_user_id": 1,
              "group_id": 1}
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    # get
    response = await async_client.get("/chat/users/1/thread/1")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == 1
    assert response_obj["create_user_id"] == 1
    assert response_obj["group_id"] == 1
    assert response_obj["model_name"] == "gpt4"
    assert response_obj["search_method"] == "default"
    assert response_obj["name"] == "test"
    assert response_obj["collections_id"] == 1
    assert response_obj["relate_num"] == 4
    assert response.status_code == starlette.status.HTTP_200_OK
    # get list
    response = await async_client.get("/chat/users/1/thread")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
