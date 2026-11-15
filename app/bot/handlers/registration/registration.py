from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.handlers.states import Registration
from app.bot.handlers.registration.mapper import BTN_TO_LANG_MAP
from app.bot.handlers.utils import show_main_menu
from app.bot.keyboards.reply_keyboards import get_keyboard_by_path
from app.core.locales import Translator
from app.database.models import User
from app.services.queue import queue_manager
from app.services.room import room_manager
from .utils import process_search, get_action_config, leave_chat


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
    buttons = i18n.get("buttons.main_menu", only_title=True)

    if message.text == buttons.get("next"):
        await process_search(message, state, user, i18n)


@router.message(Registration.waiting)
async def waiting_process(message: Message, state: FSMContext,
                          user: User, i18n: Translator):
    buttons = i18n.get("buttons.waiting", only_title=True)

    if message.text == buttons.get("cancel_search"):
        await queue_manager.remove_from_queue(
            user
        )
        await message.answer(
            i18n.get("message.cancel_search"),
            reply_markup=get_keyboard_by_path("buttons.main_menu")
        )
        await state.set_state(Registration.main_menu)


@router.message(Registration.active_chat)
async def active_chat_process(message: Message, state: FSMContext,
                              user: User, i18n: Translator):
    buttons = i18n.get("buttons.active_chat", only_title=True)

    receiver_ids = await room_manager.get_receiver_ids(
        str(message.from_user.id)
    )
    msg_text = message.text

    if msg_text in buttons.values():
        btn_to_msg_map = get_action_config(i18n)
        action_config = btn_to_msg_map.get(
            msg_text
        )
        receiver_message = action_config.partner_message
        await leave_chat(
            state, action_config.current_user_state,
            user.telegram_id, message.bot.id
        )
        await message.answer(
            action_config.current_user_message,
            reply_markup=action_config.current_user_markup
        )
        if msg_text == buttons.get("next"):
            await process_search(message, state, user, i18n)
    else:
        receiver_message = msg_text
        action_config = None

    for chat_id in receiver_ids:
        await message.bot.send_message(
            chat_id=chat_id, text=receiver_message,
            reply_markup=action_config.partner_markup if action_config else None
        )
