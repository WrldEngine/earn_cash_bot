import pytest
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from app.models import Base
from app.settings import settings

engine_test = create_async_engine(settings.build_postgres_dsn(), echo=settings.DB_ECHO)


@pytest.fixture(autouse=True, scope="session")
async def database_lifetime_scope():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
