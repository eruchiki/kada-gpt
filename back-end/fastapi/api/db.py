from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase


DB_URL = "mysql+aiomysql://root@db:3306/api?charset=utf8"

async_engine = create_async_engine(DB_URL, echo=True)
db_session = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with db_session() as session:
        yield session
