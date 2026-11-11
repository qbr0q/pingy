from app.bot.keyboards.utils import get_reply_keyboard
from app.bot.shemas.keyboards import ReplyButtonDTO
from app.core.enums.user import UserLanguage
from app.core.locales import i18n


def get_keyboard_by_path(path):
    buttons = i18n.get(path)

    buttons_data = [
        ReplyButtonDTO(**button) for button in buttons.values()
    ]
    return get_reply_keyboard(buttons_data)


def langs_buttons():
    buttons_data = [
        ReplyButtonDTO(title=UserLanguage.RU),
        ReplyButtonDTO(title=UserLanguage.EN)
    ]
    return get_reply_keyboard(buttons_data)
