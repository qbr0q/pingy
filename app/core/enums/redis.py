from enum import StrEnum
from .reference import LanguageDB


class Themes(StrEnum):
    ALL = "all"


class Queue(StrEnum):
    RussianAll = f"queue:{LanguageDB.RU}:{Themes.ALL}"
    EnglishAll = f"queue:{LanguageDB.EN}:{Themes.ALL}"
