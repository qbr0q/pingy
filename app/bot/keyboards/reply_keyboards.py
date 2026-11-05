from app.bot.keyboards.utils import get_reply_keyboard
from app.bot.shemas.keyboards import ReplyButtonDTO
from app.core.enums.user import UserLanguage


def langs_buttons():
    buttons_data = [
        ReplyButtonDTO(title=UserLanguage.RU),
        ReplyButtonDTO(title=UserLanguage.EN)
    ]
    return get_reply_keyboard(buttons_data)
