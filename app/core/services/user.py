from app.database.models import User


def create_user(telegram_user):
    new_user = User(
        telegram_id=telegram_user.id,
        interface_language=telegram_user.language_code,
        search_language=telegram_user.language_code
    )
    return new_user
