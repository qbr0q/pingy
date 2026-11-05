from pathlib import Path

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from app.core.locales import i18n


class TranslateMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        user_lang = data["user"].interface_language if data["user"] else event.message.from_user.language_code

        i18n._lang = user_lang
        data["i18n"] = i18n

        return await handler(event, data)
