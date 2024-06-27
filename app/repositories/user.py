from typing import List
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, select

from app.models import Users
from .base import AbstractRepository


@dataclass(frozen=True)
class UserRepository(AbstractRepository):
    _model: Users
    _session: AsyncSession

    async def create(self, **data) -> Users:
        async with self._session as session:
            instance = self._model(**data)

            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            return instance

    async def delete(self, **filters) -> None:
        async with self._session as session:
            await session.execute(delete(self._model).filter_by(**filters))
            await session.commit()

    async def get_single_record(self, **filters) -> Users:
        async with self._session as session:
            result = await session.execute(select(self._model).filter_by(**filters))
            return result.scalar_one_or_none()

    async def get_multi_records(
        self, order: str = "id", limit: int = 100, offset: int = 0
    ) -> List[Users]:
        async with self._session as session:
            stmt = select(self._model).order_by(order).limit(limit).offset(offset)

            result = await session.execute(stmt)
            return result.scalars().all()

    async def commit(self, *instances: Users) -> None:
        async with self._session as session:
            session.add_all(instances)
            await session.commit()
