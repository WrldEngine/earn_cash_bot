from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.methods import TelegramMethod, EditMessageText

from aiogram_i18n import I18nContext

from app.repositories import UserRepository, TasksRepository
from app.models import Users, CurrencyType
from app.filters import ChatTypeFilter
from app.keyboards import inline, default

router = Router()
router.message.filter(ChatTypeFilter(chat_type=["private"]))


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    user: Users,
    user_service: UserRepository,
    i18n: I18nContext,
) -> TelegramMethod[Any]:

    await message.answer(
        text=i18n.messages.start(name=user.mention),
        reply_markup=default.start_profile_buttons(i18n),
    )

    if not user.currency:
        await message.answer(
            text=i18n.messages.choose_currency(),
            reply_markup=inline.choose_currency(),
        )


@router.callback_query(F.data == "uzs_currency_choice")
async def callback_currency_choice(
    callback: CallbackQuery,
    user: Users,
    user_service: UserRepository,
    i18n: I18nContext,
) -> TelegramMethod[Any]:

    user.currency = CurrencyType.UZS

    await user_service.commit(user)
    await callback.answer(
        i18n.alerts.currency_success(),
        show_alert=True,
    )


@router.callback_query(F.data == "rub_currency_choice")
async def callback_currency_choice(
    callback: CallbackQuery,
    user: Users,
    user_service: UserRepository,
    i18n: I18nContext,
) -> TelegramMethod[Any]:

    user.currency = CurrencyType.RUB

    await user_service.commit(user)
    await callback.answer(
        i18n.alerts.currency_success(),
        show_alert=True,
    )


@router.message(F.text)
async def msg_profile(
    message: Message,
    user: Users,
    user_service: UserRepository,
    tasks_service: TasksRepository,
    i18n: I18nContext,
) -> TelegramMethod[Any]:

    if message.text == i18n.btn.profile():
        await message.answer(text=i18n.messages.show_profile(**user.__dict__))

    if message.text == i18n.btn.tasks():
        tasks = await tasks_service.get_multi_records()
        await message.answer(
            text=i18n.messages.show_tasks_list(),
            reply_markup=inline.show_tasks_menu(i18n=i18n, tasks=tasks, user=user),
        )


@router.callback_query(F.data)
async def callback_task_id_choice(
    callback: CallbackQuery,
    bot: Bot,
    user: Users,
    user_service: UserRepository,
    tasks_service: TasksRepository,
    i18n: I18nContext,
) -> TelegramMethod[Any]:

    current_task = await tasks_service.get_single_record(id=int(callback.data))

    if not current_task:
        return await callback.message.edit_text(i18n.messages.deleted())

    subscr_checking = await bot.get_chat_member(
        chat_id=current_task.link, user_id=callback.from_user.id
    )

    if subscr_checking.status == "left":
        await callback.message.edit_text(
            i18n.messages.not_subscribed(id=callback.data)
        )

    else:
        try:
            current_task.participants.append(user)
            await tasks_service.commit(current_task)
        except:
            await callback.message.edit_text("Already Exists")

        await callback.message.edit_text(i18n.messages.successful_task_done())
