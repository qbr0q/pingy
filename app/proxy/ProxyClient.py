from aiogram.client.session.aiohttp import AiohttpSession

from app.core import config


class ProxyClient:
    def __init__(self):
        self.proxy = config.proxy
        self._session = None

    @property
    def session(self):
        if not self._session:
            self._session = AiohttpSession(proxy=self.proxy.url)
        return self._session
