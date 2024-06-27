import logging

__all__ = ["database", "setup_logger", "logging_decorator"]

database: logging.Logger = logging.getLogger("app.models")
info: logging.Logger = logging.getLogger("app")


async def setup_logging(level: int = logging.INFO) -> None:
    for name in ["aiogram.middlewares", "aiogram.event", "aiohttp.access"]:
        logging.getLogger(name).setLevel(logging.WARNING)

    logging.basicConfig(
        format="%(asctime)s[%(levelname)s] | %(name)s: %(message)s",
        datefmt="[%H:%M:%S]",
        level=level,
    )
