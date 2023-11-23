from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from api.db import Base


class Users(Base):
    __tablename__ = "uers"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    email = Column(String(100))
    name = Column(String(1024))
    password = Column(String(1024))
    admin = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    exsited = Column(Boolean, default=True)


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(1024))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    exsited = Column(Boolean, default=True)
