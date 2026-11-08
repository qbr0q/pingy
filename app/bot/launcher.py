from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.database import SessionLocal
from app.core import config
from app.core.utils import DataTransfer
from app.core.middlewares import *
from app.bot.handlers import routers


def include_routers(dp):
    for router in routers:
        dp.include_router(router)


def include_middleware(dp):
    dp.update.middleware(DbSessionMiddleware(session_pool=SessionLocal))
    dp.update.middleware(UserRegistrationMiddleware())
    dp.update.middleware(TranslateMiddleware())


async def setup_app():
    bot = Bot(token=config.private.bot_token)
    storage = RedisStorage.from_url(config.redis.url)
    dp = Dispatcher(storage=storage)

    include_routers(dp)
    include_middleware(dp)

    return DataTransfer(
        bot=bot,
        dp=dp
    )


async def start_app():
    components = await setup_app()

    dp = components.dp
    bot = components.bot

    await dp.start_polling(
        bot
    )
