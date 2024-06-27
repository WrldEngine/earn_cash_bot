from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.settings import settings


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == settings.ADMIN_CHAT_ID
