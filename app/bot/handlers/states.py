from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    language_choice = State()
    main_menu = State()
    active_chat = State()
