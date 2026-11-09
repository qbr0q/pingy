from app.bot.keyboards.utils import get_reply_keyboard
from app.bot.shemas.keyboards import ReplyButtonDTO
from app.core.enums.user import UserLanguage
from app.core.locales import i18n


def langs_buttons():
    buttons_data = [
        ReplyButtonDTO(title=UserLanguage.RU),
        ReplyButtonDTO(title=UserLanguage.EN)
    ]
    return get_reply_keyboard(buttons_data)


def main_menu_buttons():
    buttons = i18n.get("buttons.main_menu")

    buttons_data = [
        ReplyButtonDTO(title=button) for button in buttons.values()
    ]
    return get_reply_keyboard(buttons_data)


def active_chat_buttons():
    buttons = i18n.get("buttons.active_chat")

    buttons_data = [
        ReplyButtonDTO(title=button) for button in buttons.values()
    ]
    return get_reply_keyboard(buttons_data)
