import uuid

from app.services.redis import redis_manager
from app.database.models import User
from app.core.enums.redis import StreamType, MatchResult
from app.core.shemas.match import MatchResultDTO


class RoomClient:
    def __init__(self):
        self.redis = redis_manager.client

    async def create_room(self, *args):
        room_id = self._generate_room_id()

        await self.redis.sadd(
            f"{StreamType.ROOM}:{room_id}", *args
        )
        return room_id

    @staticmethod
    def _generate_room_id():
        return str(uuid.uuid4())

    def get_room_other_members(self, room_members, current_user_id):
        pass


room_manager = RoomClient()
