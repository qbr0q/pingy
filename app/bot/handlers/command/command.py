from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.bot.keyboards.reply_keyboards import langs_buttons
from app.bot.handlers.states import Registration
from app.core.locales import Translator
from app.core.services.user import create_user
from app.database.models import User


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext,
                session: AsyncSession, user: User, i18n: Translator):
    if not user:
        user = create_user(message.from_user)
        session.add(user)
        await message.answer(
            i18n.get("start.welcome"),
            reply_markup=langs_buttons()
        )
        await state.set_state(Registration.language_choice)
