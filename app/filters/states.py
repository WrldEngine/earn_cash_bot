from typing import Final

from aiogram.filters import Filter, StateFilter
from aiogram.fsm.state import State, StatesGroup


class ChatStates(StatesGroup):
    AwaitingPurprose = State()
    ReadyToRespond = State()
