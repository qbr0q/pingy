from app.core.enums.redis import StreamType, MatchResult
from app.core.shemas.match import MatchResultDTO
from app.database.models import User
from app.services.room import room_manager
from app.services.redis import redis_manager
from .script import MATCH_OR_QUEUE_SCRIPT


class QueueClient:
    def __init__(self):
        self.redis = redis_manager.client
        self.room_manager = room_manager
        self._script = self.redis.register_script(
            MATCH_OR_QUEUE_SCRIPT
        )
        self._lrem_count = 0

    @staticmethod
    def get_wait_queue_keys(user):
        user_topic = "ALL"
        queue_key = f"{StreamType.QUEUE}:{user.search_language}:{user_topic}"
        queue_set_key = f"{queue_key}:{StreamType.QUEUED_SET}"
        return queue_key, queue_set_key

    @staticmethod
    def get_user_mapping_room(u_id):
        return f"{StreamType.USER_ROOM}:{u_id}:{StreamType.ROOM}"

    @staticmethod
    def get_room_key(room_id):
        return f"{StreamType.ROOM}:{room_id}"

    async def get_user_room_id(self, u_id):
        user_room_key = self.get_user_mapping_room(u_id)
        return await self.redis.get(
            user_room_key
        )

    async def get_user_room(self, u_id):
        room_id = await self.get_user_room_id(u_id)
        return self.get_room_key(room_id)

    async def process_search(self, user: User):
        user_id = str(user.telegram_id)

        queue_key, queue_set_key = self.get_wait_queue_keys(
            user
        )
        active_key = StreamType.ACTIVE

        status, partner_id = await self._script(
            keys=[queue_key, queue_set_key, active_key], args=[user_id]
        )

        if status == MatchResult.MATCHED:
            # создает руму участников
            room_id = await self.room_manager.create_room(
                user_id, partner_id
            )
            # обновляем статусы
            await self._update_status(room_id, user_id, partner_id)

            return MatchResultDTO(
                status=MatchResult.MATCHED,
                room_id=room_id,
                user_ids={user_id, partner_id}
            )
        return MatchResultDTO(
            status=MatchResult.UNKNOWN
        )

    async def _update_status(self, room_id, *user_ids):
        for u_id in user_ids:
            # проставляем связь user -> room
            await self.redis.set(
                self.get_user_mapping_room(u_id), room_id
            )
            # добавление пользователей в множество "активных"
            await self.redis.sadd(
                StreamType.ACTIVE, u_id
            )

    async def remove_from_queue(self, user):
        queue_key, queue_set_key = self.get_wait_queue_keys(
            user
        )

        await self.redis.lrem(
            queue_key,
            self._lrem_count,
            user.telegram_id
        )
        await self.redis.srem(
            queue_set_key,
            user.telegram_id
        )

    async def leave_chat(self, u_id):
        room_key = await self.get_user_room(u_id)

        await self.remove_from_room(u_id, room_key)
        await self.remove_from_active(u_id)
        await self.del_user_mapping_room(u_id)

        return await self.cleanup_room(room_key)

    async def cleanup_room(self, room_key):
        if await self.redis.scard(room_key) <= 1:
            return await self.redis.spop(room_key)

    async def remove_from_room(self, u_id, room_key):
        await self.redis.srem(
            room_key, u_id
        )

    async def remove_from_active(self, u_id):
        await self.redis.srem(
            StreamType.ACTIVE, u_id
        )

    async def del_user_mapping_room(self, u_id):
        user_room_mapping_key = self.get_user_mapping_room(
            u_id
        )
        await self.redis.delete(
            user_room_mapping_key
        )


queue_manager = QueueClient()
