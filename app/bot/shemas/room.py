from pydantic import BaseModel, ConfigDict
from aiogram.fsm.state import State
from aiogram.types import ReplyKeyboardMarkup


class CharActionDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_user_message: str
    partner_message: str
    current_user_state: State
    partner_state: State
    current_user_markup: ReplyKeyboardMarkup
    partner_markup: ReplyKeyboardMarkup
