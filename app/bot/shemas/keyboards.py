from pydantic import BaseModel


class ReplyButtonDTO(BaseModel):
    title: str
    style: str | None = None


class InlineButtonDTO(BaseModel):
    title: str
    data: str
    url: str | None = None
    style: str | None = None
