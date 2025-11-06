from contextlib import asynccontextmanager
from typing import Protocol, AsyncIterator, AsyncContextManager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SessionManagerProtocol(Protocol):
    """
    Протокол менеджера сессий.
    """

    def get_session(self, immediate: bool = True) -> AsyncContextManager[AsyncSession]:
        """
        Получаем сессию для выполнения запроса.
        """
        ...


class SessionManagerImpl:
    """
    Реализация менеджера сессий.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @asynccontextmanager
    async def get_session(self, immediate: bool = True) -> AsyncIterator[AsyncSession]:
        """
        Получаем сессию для выполнения запроса.
        """
        if self._session.in_transaction():
            yield self._session
        else:
            async with self._session.begin():
                if immediate:
                    await self._session.execute(text("SET CONSTRAINTS ALL IMMEDIATE"))
                yield self._session
