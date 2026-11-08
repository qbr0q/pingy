from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.core.locales import Translator
from app.bot.keyboards.reply_keyboards import main_menu_buttons
from app.bot.handlers.states import Registration
from app.database.models import User


async def show_main_menu(message: Message, state: FSMContext,
                         user: User, i18n: Translator):
    await message.answer(
        i18n.get("message.main_menu", priority_lang=user.interface_language),
        reply_markup=main_menu_buttons()
    )
    await state.set_state(Registration.main_menu)
