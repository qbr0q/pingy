from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.core.locales import Translator
from app.bot.keyboards.reply_keyboards import get_keyboard_by_path
from app.bot.handlers.states import Registration
from app.database.models import User


async def show_main_menu(message: Message, state: FSMContext,
                         user: User, i18n: Translator):
    await message.answer(
        i18n.get("message.main_menu", priority_lang=user.interface_language),
        reply_markup=get_keyboard_by_path("buttons.main_menu")
    )
    await state.set_state(Registration.main_menu)
