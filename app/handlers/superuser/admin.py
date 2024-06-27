from typing import Any

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.methods import TelegramMethod

from app.repositories import UserRepository, TasksRepository
from app.models import Users
from app.filters import AdminFilter

router = Router()
router.message.filter(AdminFilter())


@router.message(Command("task"))
async def cmd_add_task(
    message: Message,
    command: CommandObject,
    tasks_service: TasksRepository,
) -> TelegramMethod[Any]:
    command_args: str = command.args

    if command_args is None:
        return await message.answer("Аргументов нет")

    commands_dict = dict(
        arg.split("=") for arg in command_args.replace(" ", "").split(";")
    )

    await tasks_service.create(**commands_dict)
    await message.answer("Таск успешно создан")
