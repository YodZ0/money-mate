import pytest
from typing import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import DatabaseProvider
from src.core.models.base import Base

from tests.settings import settings

from .crud import CrudTestRepository
from .models import CrudTestModel
from .schemas import CrudTestReadSchema


MODELS_TO_CREATE = [
    CrudTestReadSchema(id=i, label=f"Test model {i}") for i in range(1, 11)
]


async def create_models(
    session: AsyncSession,
    models_to_create: list[CrudTestReadSchema],
) -> None:
    """
    Создаем тестовые данные в БД.
    """
    for model in models_to_create:
        stmt = insert(CrudTestModel).values(**model.model_dump())
        await session.execute(stmt)


@asynccontextmanager
async def make_crud_repository(
    models_to_create: list[CrudTestReadSchema],
) -> AsyncIterator[CrudTestRepository]:
    db_provider = DatabaseProvider(settings.db.dsn)
    async with db_provider.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        async with db_provider.session_factory() as session:
            await create_models(session, models_to_create)
            yield CrudTestRepository(session)
    finally:
        async with db_provider.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def crud_repository() -> AsyncIterator[CrudTestRepository]:
    async with make_crud_repository(MODELS_TO_CREATE) as repository:
        yield repository
