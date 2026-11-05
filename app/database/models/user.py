from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey, Column, Integer, DateTime, func, UniqueConstraint, Index, BigInteger

from app.core.enums.user import UserStatus


class User(SQLModel, table=True):
    __tablename__ = "user_profile"

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(),
            default=func.now(),
            server_default=func.now()
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(),
            default=func.now(),
            onupdate=func.now(),
            server_default=func.now()
        )
    )
    telegram_id: int = Field(sa_column=Column(BigInteger, unique=True))
    status: str = Field(default=UserStatus.IDLE)
    gender: str = Field(nullable=True)
    interface_language: str
    search_language: str
