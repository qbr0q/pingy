from sqlmodel import SQLModel, Field


class BaseReference(SQLModel):
    id: int = Field(default=None, primary_key=True)
    code: str = Field(primary_key=True, max_length=32)
    name: str = Field(max_length=64)
    description: str | None = Field(default=None, max_length=255)


class RbUserStatus(BaseReference, table=True):
    __tablename__ = "rb_user_status"
