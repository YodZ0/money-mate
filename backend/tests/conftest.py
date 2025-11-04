import pytest
import asyncio
from asyncio import AbstractEventLoop
from typing import Iterator


@pytest.fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    """
    Исправляет ошибку `RuntimeError: Event loop is closed`, возникающую из-за aioredis.
    https://stackoverflow.com/questions/61022713/pytest-asyncio-has-a-closed-event-loop-but-only-when-running-all-tests
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
