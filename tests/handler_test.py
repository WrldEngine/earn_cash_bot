import pytest

from unittest.mock import AsyncMock
from app.handlers.user import cmd_help


@pytest.mark.asyncio
async def test_echo_handler() -> AsyncMock:
    text_mock = "Okay"
    message_mock = AsyncMock(text=text_mock)
    await cmd_help(message=message_mock)

    message_mock.answer.assert_called_with(text_mock)
