from app.bot.keyboards.utils import get_inline_keyboard
from app.bot.shemas.keyboards import InlineButtonDTO
from app.core.locales import i18n


def get_keyboard_by_path(path):
    buttons = i18n.get(path)

    buttons_data = [
        InlineButtonDTO(**button) for button in buttons
    ]
    return get_inline_keyboard(buttons_data)
