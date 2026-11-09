from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from app.bot.handlers.states import Registration
from app.bot.handlers.registration.mapper import BTN_TO_LANG_MAP
from app.bot.handlers.utils import show_main_menu
from app.core.locales import Translator
from app.core.enums.redis import MatchResult
from app.database.models import User
from app.services.queue import match_manager
from app.services.room import room_manager


router = Router()


@router.message(Registration.language_choice)
async def language_process(message: Message, state: FSMContext,
                           i18n: Translator, user: User):
    db_lang = BTN_TO_LANG_MAP.get(message.text)
    user.interface_language = db_lang

    await show_main_menu(message, state, user, i18n)


@router.message(Registration.main_menu)
async def main_menu_process(message: Message, state: FSMContext,
                            user: User, i18n: Translator):
    buttons = i18n.get("buttons.main_menu")

    if message.text == buttons.get("next"):
        await message.answer(
            i18n.get("message.search_process")
        )
        result = await match_manager.process_search(user)
        if result.status == MatchResult.MATCHED:
            for chat_id in result.user_ids:
                await message.bot.send_message(
                    chat_id=chat_id, text=i18n.get("message.found")
                )
                target_key = StorageKey(
                    bot_id=message.bot.id, chat_id=chat_id, user_id=chat_id
                )
                await state.storage.set_state(target_key, Registration.active_chat)


@router.message(Registration.active_chat)
async def active_chat_process(message: Message):
    receiver_ids = await room_manager.get_receiver_ids(
        str(message.from_user.id)
    )
    for chat_id in receiver_ids:
        await message.bot.send_message(
            chat_id=chat_id, text=message.text
        )


