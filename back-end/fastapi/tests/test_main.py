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
    response = await async_client.post("/chat/groups", json={"name": "グループ1"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == 1
    assert response_obj["name"] == "グループ1"
    response = await async_client.get("/chat/groups")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["id"] == 1
    assert response_obj[0]["name"] == "グループ1"
    response = await async_client.get("/chat/groups/1")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == 1
    assert response_obj["name"] == "グループ1"
    response = await async_client.get("/chat/groups/2")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    response = await async_client.patch(
        "/chat/groups/1", json={"name": "グループ更新"}
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["name"] == "グループ更新"
    response = await async_client.post("/chat/groups", json={"name": "グループ2"})
    response_obj = response.json()
    assert response_obj["id"] == 2
    assert response_obj["name"] == "グループ2"
    assert response.status_code == starlette.status.HTTP_200_OK
    response = await async_client.delete("/chat/groups/2")
    response_obj = response.json()
    response = await async_client.get("/chat/groups/2")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
