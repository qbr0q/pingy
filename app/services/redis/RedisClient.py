import redis.asyncio as redis

from app.core import config


class RedisClient:
    def __init__(self):
        self._client = None
        self.redis_config = config.redis

    @property
    def client(self):
        if not self._client:
            self._client = self._get_client()
        return self._client

    def _get_client(self):
        return redis.from_url(
            self.redis_config.url, encoding="utf-8", decode_responses=True
        )


redis_manager = RedisClient()
