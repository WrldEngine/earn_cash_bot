from typing import Callable, Dict, Any, Awaitable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from aiogram_i18n import I18nMiddleware

from logger import database as logger


class UserAuthMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user_service = data["user_service"]
        chat_user = data["event_from_user"]

        user = await user_service.get_single_record(telegram_id=chat_user.id)

        if not user:
            i18n_middleware = data["i18n_middleware"]

            user_language = chat_user.language_code
            if user_language not in i18n_middleware.core.available_locales:
                user_language = i18n_middleware.core.default_locale

            user = await user_service.create(
                telegram_id=chat_user.id,
                name=chat_user.full_name,
                locale=user_language,
            )

            logger.info(f"New user in database {chat_user.id}")

        data["user"] = user

        return await handler(event, data)
