from typing import Any

from aiogram import Router, F, html
from aiogram.types import Message, ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.link import create_tg_link
from aiogram.methods import TelegramMethod

from app.repositories import UserRepository
from app.models import Users
from app.filters import ChatTypeFilter, ChatStates

router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))
