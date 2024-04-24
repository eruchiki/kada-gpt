# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.sql import func
# from api.db import Base
# from sqlalchemy.orm import relationship


# class Users(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     group_id = Column(Integer, ForeignKey("groups.id"))
#     email = Column(String(500))
#     name = Column(String(1024))
#     password = Column(String(1024))
#     is_admin = Column(Boolean, default=False)
#     created_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     update_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     publish = Column(Boolean, default=True)

#     group = relationship("Groups", back_populates="user")
#     thread = relationship("Threads", back_populates="user")
#     collection = relationship("Collections", back_populates="user")
#     document = relationship("Documents", back_populates="user")
