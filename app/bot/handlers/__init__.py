from app.bot.handlers.command import router as command_router
from app.bot.handlers.registration import router as registration_router
from app.bot.handlers.message import router as message_router


routers = (command_router, registration_router, message_router)
