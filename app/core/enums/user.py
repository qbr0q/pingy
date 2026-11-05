from enum import StrEnum


class UserStatus(StrEnum):
    IDLE = "idle"
    SEARCHING = "searching"
    IN_CHAT = "in_chat"
    BANNED = "banned"


class UserLanguage(StrEnum):
    RU = "Русский 🇷🇺"
    EN = "English 🇬🇧"
