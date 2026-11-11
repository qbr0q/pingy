from enum import StrEnum
from .reference import LanguageDB


class StreamType(StrEnum):
    QUEUE = "queue"
    ROOM = "room"
    USER_ROOM = "user"
    ACTIVE = "active_users"
    QUEUED_SET = "queued_set"


class Themes(StrEnum):
    ALL = "all"


class Queue(StrEnum):
    RussianAll = f"{StreamType.QUEUE}:{LanguageDB.RU}:{Themes.ALL}"
    EnglishAll = f"{StreamType.QUEUE}:{LanguageDB.EN}:{Themes.ALL}"


class MatchResult(StrEnum):
    MATCHED = "matched"
    UNKNOWN = "unknown"
