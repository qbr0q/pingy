from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.handlers.states import Registration
from app.bot.handlers.registration.mapper import BTN_TO_LANG_MAP
from app.bot.handlers.utils import show_main_menu
from app.core.locales import Translator
from app.database.models import User
from app.services.queue import match_manager


router = Router()


@router.message(Registration.language_choice)
async def language_process(message: Message, state: FSMContext,
                           i18n: Translator, user: User):
    db_lang = BTN_TO_LANG_MAP.get(message.text)
    user.interface_language = db_lang

    await show_main_menu(message, state, user, i18n)


@router.message(Registration.main_menu)
async def main_menu_process(message: Message, user: User,
                            i18n: Translator):
    buttons = i18n.get("buttons.main_menu")

    if message.text == buttons.get("next"):
        await match_manager.process_search(user)
