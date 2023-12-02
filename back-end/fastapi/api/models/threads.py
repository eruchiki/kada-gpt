# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Boolean,
#     DateTime,
#     ForeignKey,
#     Text,
# )
# from sqlalchemy.sql import func
# from api.db import Base
# from sqlalchemy.orm import relationship


# class Threads(Base):
#     __tablename__ = "threads"

#     id = Column(Integer, primary_key=True)
#     create_user_id = Column(Integer, ForeignKey("users.id"))
#     group_id = Column(Integer)
#     name = Column(String(1024))
#     model_name = Column(String(100))
#     search_method = Column(String(100))
#     relate_num = Column(Integer)
#     collections_id = Column(Integer, ForeignKey("collections.id"))
#     created_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     update_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     publish = Column(Boolean, default=True)
#     group = relationship("Groups", back_populates="thread")
#     collection = relationship("Collections", back_populates="thread")
#     chat = relationship("Chat", back_populates="thread")


# class Chat(Base):
#     __tablename__ = "chat"

#     id = Column(Integer, primary_key=True)
#     thread_id = Column(Integer, ForeignKey("threads.id"))
#     chat_id = Column(Integer)
#     message_text = Column(Text)
#     response_text = Column(Text)
#     created_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     update_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     relate_number = Column(Text)
#     document_id = Column(Text)
#     publish = Column(Boolean, default=True)
#     thread = relationship("Threads", back_populates="chat")


# class Collections(Base):
#     __tablename__ = "collections"

#     id = Column(Integer, primary_key=True)
#     create_user_id = Column(Integer, ForeignKey("users.id"))
#     name = Column(String(1024))
#     hash = Column(Text)
#     created_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     update_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     publish = Column(Boolean, default=True)
#     user = relationship("Users", back_populates="collection")
#     thread = relationship("Thread", back_populates="collection")
#     document = relationship("Documents", back_populates="collection")


# class Documents(Base):
#     __tablename__ = "documents"

#     id = Column(Integer, primary_key=True)
#     collection_id = Column(Integer, ForeignKey("collections.id"))
#     create_user_id = Column(Integer, ForeignKey("users.id"))
#     uri = Column(String(1000))
#     hash = Column(Text)
#     created_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     publish = Column(Boolean, default=True)
#     user = relationship("Users", back_populates="document")
#     collection = relationship("Collections", back_populates="document")
