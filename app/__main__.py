import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.client.bot import DefaultBotProperties

from logger import setup_logging

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from .handlers import user, admin, group, errors
from .factory import redis_storage, session_factory
from .settings import settings
from .middlewares import (
    TasksRepositoryMiddleware,
    UserRepositoryMiddleware,
    DBSessionMiddleware,
    UserAuthMiddleware,
    UserManager,
)


async def main() -> None:
    await setup_logging()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=RedisStorage(redis=redis_storage()))

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="locales/{locale}",
        ),
        default_locale="en",
        manager=UserManager(),
    )

    dp.update.middleware(DBSessionMiddleware(session_factory=session_factory()))
    dp.update.middleware(UserRepositoryMiddleware())
    dp.update.middleware(TasksRepositoryMiddleware())
    dp.update.middleware(UserAuthMiddleware())
    dp.include_routers(admin.router, user.router, group.router, errors.router)
    i18n_middleware.setup(dispatcher=dp)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
