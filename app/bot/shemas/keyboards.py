from pydantic import BaseModel


class ReplyButtonDTO(BaseModel):
    title: str
    style: str | None = None
