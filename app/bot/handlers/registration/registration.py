from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.handlers.states import Registration
from app.bot.handlers.registration.mapper import BTN_TO_LANG_MAP
from app.database.models import User


router = Router()


@router.message(Registration.language_choice)
async def language_process(message: Message, state: FSMContext,
                           user: User):
    db_lang = BTN_TO_LANG_MAP.get(message.text)
    user.interface_language = db_lang
    await message.answer('готово ахи')
