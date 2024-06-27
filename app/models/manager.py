from typing import List

from .base import Base
from .enums import CurrencyType

from aiogram import html
from aiogram.utils.link import create_tg_link

from sqlalchemy import String, DECIMAL, Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


association_table = Table(
    "association_table",
    Base.metadata,
    Column("users_id", ForeignKey("users.id")),
    Column("tasks_id", ForeignKey("tasks.id")),
)


class Users(Base):
    telegram_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    locale: Mapped[str] = mapped_column(String(length=2), nullable=True)
    notifications: Mapped[bool] = mapped_column(default=True)
    balance: Mapped[int] = mapped_column(DECIMAL(precision=1000, scale=3), default=0)
    currency: Mapped[CurrencyType] = mapped_column(nullable=True)
    tasks: Mapped[List["Tasks"]] = relationship(
        secondary=association_table, overlaps="participants"
    )

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.telegram_id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)


class Tasks(Base):
    name: Mapped[str]
    link: Mapped[str]
    price_rub: Mapped[int] = mapped_column(DECIMAL(precision=1000, scale=3), default=0)
    price_uzs: Mapped[int] = mapped_column(DECIMAL(precision=1000, scale=3), default=0)
    participants: Mapped[List["Users"]] = relationship(
        secondary=association_table, lazy="selectin", overlaps="tasks"
    )
