from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram_i18n import I18nContext


def start_profile_buttons(i18n: I18nContext) -> ReplyKeyboardMarkup:

    kb = [
        [
            KeyboardButton(text=i18n.btn.profile()),
            KeyboardButton(text=i18n.btn.tasks()),
        ],
        [
            KeyboardButton(text=i18n.btn.more()),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Buttons"
    )

    return keyboard
