from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# The function declarative_base() returns a class which is used to create database tables
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-base-class
BaseTable = declarative_base()  # type: ignore


class Users(BaseTable):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")  # type: ignore


class Items(BaseTable):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")  # type: ignore
