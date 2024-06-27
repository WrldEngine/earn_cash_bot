from typing import Optional, cast

from aiogram.types import TelegramObject, Message, User
from aiogram_i18n.managers import BaseManager

from app.models import Users
from app.repositories import UserRepository


class UserManager(BaseManager):
    async def set_locale(
        self,
        locale: str,
        user: Users,
        user_service: UserRepository,
    ) -> None:

        user.locale = locale
        await user_service.commit(user)

    async def get_locale(
        self,
        user: Optional[Users] = None,
        event_from_user: Optional[User] = None,
    ) -> str:

        if user:
            return user.locale

        if event_from_user:
            return event_from_user.language_code

        return cast(str, self.default_locale)
