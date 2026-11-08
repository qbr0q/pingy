from app.services.redis import redis_manager
from app.database.models import User
from app.core.enums.redis import StreamType, MatchResult
from app.core.shemas.match import MatchResultDTO
from app.services.room import room_manager
from .script import MATCH_OR_QUEUE_SCRIPT


class MatchClient:
    def __init__(self):
        self.redis = redis_manager.client
        self.room_manager = room_manager
        self._script = self.redis.register_script(
            MATCH_OR_QUEUE_SCRIPT
        )

    async def process_search(self, user: User):
        user_topic = "ALL" # fixme
        user_id = str(user.telegram_id)

        queue_key = f"{StreamType.QUEUE}:{user.search_language}:{user_topic}"
        queued_key = f"{queue_key}:queued_set"
        active_key = StreamType.ACTIVE

        status, partner_id = await self._script(
            keys=[queue_key, queued_key, active_key], args=[user_id]
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
                f"{StreamType.USER_ROOM}:{u_id}:{StreamType.ROOM}", room_id
            )
            # добавление пользователей в множество "активных"
            await self.redis.sadd(
                StreamType.ACTIVE, u_id
            )


match_manager = MatchClient()
