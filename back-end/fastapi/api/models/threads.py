from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from api.db import Base


class Threads(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    create_user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer)
    name = Column(String(1024))
    model_name = Column(String(100))
    search_method = Column(String(100))
    collections_id = Column(Integer, ForeignKey("collections.id"))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    exsited = Column(Boolean, default=True)


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    thred_id = Column(Integer, ForeignKey("threads.id"))
    text = Column(String(100))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    exsited = Column(Boolean, default=True)


class Collections(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    create_user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    exsited = Column(Boolean, default=True)


class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, ForeignKey("collections.id"))
    create_user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(1024))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    exsited = Column(Boolean, default=True)
