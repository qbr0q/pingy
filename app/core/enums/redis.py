from enum import StrEnum
from .reference import LanguageDB
from .user import UserTopic


class StreamType(StrEnum):
    QUEUE = "queue"
    ROOM = "room"
    USER_ROOM = "user"
    ACTIVE = "active_users"
    QUEUED_SET = "queued_set"


class Queue(StrEnum):
    RussianAll = f"{StreamType.QUEUE}:{LanguageDB.RU}:{UserTopic.ALL}"
    EnglishAll = f"{StreamType.QUEUE}:{LanguageDB.EN}:{UserTopic.ALL}"


class MatchResult(StrEnum):
    MATCHED = "matched"
    UNKNOWN = "unknown"
