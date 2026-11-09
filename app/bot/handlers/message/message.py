from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
def message_process(message: Message):
    print()
