from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from app.bot.handlers.states import Registration
from app.bot.keyboards.reply_keyboards import get_keyboard_by_path
from app.bot.shemas.room import CharActionDTO
from app.core.locales import Translator
from app.core.enums.redis import MatchResult
from app.database.models import User
from app.services.queue import queue_manager


async def set_user_state(state, new_state, bot_id, user_id):
    target_key = StorageKey(
        bot_id=bot_id, chat_id=user_id, user_id=user_id
    )
    await state.storage.set_state(target_key, new_state)


async def process_search(message: Message, state: FSMContext,
                         user: User, i18n: Translator):
    await message.answer(
        i18n.get("message.search_process"),
        reply_markup=get_keyboard_by_path("buttons.waiting")
    )
    await state.set_state(Registration.waiting)
    result = await queue_manager.process_search(user)
    if result.status == MatchResult.MATCHED:
        for chat_id in result.user_ids:
            await message.bot.send_message(
                chat_id=chat_id, text=i18n.get("message.found"),
                reply_markup=get_keyboard_by_path("buttons.active_chat")
            )
            await set_user_state(
                state, Registration.active_chat, message.bot.id, chat_id
            )


def get_action_config(i18n: Translator):
    main_menu_buttons = get_keyboard_by_path("buttons.main_menu")
    msg_partner_stop = i18n.get("message.partner_stop")
    msg_stop = i18n.get("message.stop")

    next_config = CharActionDTO(
        current_user_message=msg_stop,
        partner_message=msg_partner_stop,
        current_user_state=Registration.waiting,
        partner_state=Registration.main_menu,
        current_user_markup=get_keyboard_by_path("buttons.waiting"),
        partner_markup=main_menu_buttons
    )
    stop_config = CharActionDTO(
        current_user_message=msg_stop,
        partner_message=msg_partner_stop,
        current_user_state=Registration.main_menu,
        partner_state=Registration.main_menu,
        current_user_markup=main_menu_buttons,
        partner_markup=main_menu_buttons
    )

    return {
        i18n.get("buttons.active_chat.next").get("title"): next_config,
        i18n.get("buttons.active_chat.stop").get("title"): stop_config
    }


async def leave_chat(state, new_state, u_id, bot_id):
    left_user_id = await queue_manager.leave_chat(
        u_id
    )
    await set_user_state(state, new_state, bot_id, u_id)
    if left_user_id is not None:
        await leave_chat(state, Registration.main_menu, left_user_id, bot_id)
