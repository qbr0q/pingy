from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey, Column, Integer, DateTime, func, UniqueConstraint, Index, BigInteger
from datetime import datetime
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "user_profile"

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(),
            default=func.now(),
            onupdate=func.now(),
            server_default=func.now()
        )
    )
    telegram_id: int = Field(sa_column=Column(BigInteger, unique=True))
    interface_language: str
    search_language: str


