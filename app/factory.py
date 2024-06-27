from .settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from redis.asyncio import ConnectionPool, Redis


def session_factory() -> async_sessionmaker:
    engine = create_async_engine(url=settings.build_postgres_dsn())
    return async_sessionmaker(engine, expire_on_commit=False)


def redis_storage() -> Redis:
    redis = Redis(
        connection_pool=ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DATABASE,
        )
    )

    return redis
