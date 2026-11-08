from pydantic import BaseModel


class MatchResultDTO(BaseModel):
    status: str
    room_id: str | None = None
    user_ids: set[int] = None
