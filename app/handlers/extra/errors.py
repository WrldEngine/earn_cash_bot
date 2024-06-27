from typing import Any

from aiogram import F, Router
from aiogram.methods import TelegramMethod
from aiogram.types import ErrorEvent
from aiogram_i18n import I18nContext

from logger import info as logger


router = Router()


""" @router.error()
async def error_handler(error: ErrorEvent, i18n: I18nContext) -> TelegramMethod[Any]:
    logger.error(error.exception)
    return error.update.message.answer(text=i18n.messages.error()) """
