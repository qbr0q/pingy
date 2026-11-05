from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    language_choice = State()
