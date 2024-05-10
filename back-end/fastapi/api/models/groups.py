# from sqlalchemy import Column, Integer, String, Boolean, DateTime
# from sqlalchemy.sql import func
# from api.db import Base
# from sqlalchemy.orm import relationship


# class Groups(Base):
#     __tablename__ = "groups"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(1024))
#     created_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     update_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )
#     publish = Column(Boolean, default=True)
#     user = relationship("Users", back_populates="group")
#     thread = relationship("Threads", back_populates="group")
