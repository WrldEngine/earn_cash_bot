from typing import List
from app.models import Tasks, Users, CurrencyType

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext


def choose_currency() -> InlineKeyboardMarkup:

    kb = [
        [
            InlineKeyboardButton(text="UZS", callback_data="uzs_currency_choice"),
            InlineKeyboardButton(text="RUB", callback_data="rub_currency_choice"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Choose currency",
    )

    return keyboard


def show_tasks_menu(
    i18n: I18nContext, tasks: List[Tasks], user: Users
) -> InlineKeyboardMarkup:

    kb = [
        [
            InlineKeyboardButton(
                text=i18n.btn.task_num(
                    price=(
                        task.price_uzs
                        if user.currency == CurrencyType.UZS
                        else task.price_rub
                    )
                ),
                callback_data=str(task.id),
            )
        ]
        for task in tasks
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb,
        row_width=1,
        input_field_placeholder="Choose Task",
    )

    return keyboard
