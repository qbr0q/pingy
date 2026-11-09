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

    async def _get_user_room_id(self, user_id):
        return await self.redis.get(f"{StreamType.USER_ROOM}:{user_id}:{StreamType.ROOM}")

    async def _get_other_members(self, room_id, current_user_id):
        all_members = await self.redis.smembers(f"{StreamType.ROOM}:{room_id}")
        return all_members - {current_user_id}

    async def get_receiver_ids(self, current_user_id):
        room_id = await self._get_user_room_id(current_user_id)
        a = await self._get_other_members(room_id, current_user_id)
        return a


room_manager = RoomClient()
