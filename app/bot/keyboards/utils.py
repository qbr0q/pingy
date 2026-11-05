from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_reply_keyboard(raw_buttons_data, row_width=2):
    builder = ReplyKeyboardBuilder()

    buttons_data = [KeyboardButton(
        text=button_data.title,
        style=button_data.style
    ) for button_data in raw_buttons_data]
    builder.add(*buttons_data)
    builder.adjust(row_width)

    return builder.as_markup(resize_keyboard=True)


def get_inline_keyboard(raw_buttons_data, row_width=2):
    builder = InlineKeyboardBuilder()

    buttons_data = [InlineKeyboardButton(text=button_data.title,
                                         callback_data=button_data.callback,
                                         url=button_data.url,
                                         style=button_data.style)
                    for button_data in raw_buttons_data]
    builder.add(*buttons_data)
    builder.adjust(row_width)

    return builder.as_markup()
