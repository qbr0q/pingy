from app.services.redis import redis_manager
from app.database.models import User


class MatchClient:
    def __init__(self):
        self.redis = redis_manager.client

    async def process_search(self, user: User):
        user_theme = "ALL"
        queue_key = f"queue:{user.search_language}:{user_theme}"

        partner_id = await self._get_early_user(queue_key)
        if partner_id:
            pass
        await self._push_queue_user(queue_key, user.telegram_id)

    async def _get_early_user(self, queue_key):
        return await self.redis.lpop(queue_key)

    async def _push_queue_user(self, queue_key, telegram_id):
        await self.redis.rpush(queue_key, telegram_id)


match_manager = MatchClient()
