from aiogram import Bot, Dispatcher

from app.database import SessionLocal
from app.core import config
from app.core.utils import DataTransfer
from app.bot.handlers import routers
from app.core.middlewares import *


def include_routers(dp):
    for router in routers:
        dp.include_router(router)


def include_middleware(dp):
    dp.update.middleware(DbSessionMiddleware(session_pool=SessionLocal))
    dp.update.middleware(UserRegistrationMiddleware())
    dp.update.middleware(TranslateMiddleware())


async def setup_app():
    bot = Bot(token=config.private.bot_token)
    dp = Dispatcher()

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
