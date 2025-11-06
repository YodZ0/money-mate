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
from .schemas import CrudTestCreateSchema


MODELS_TO_CREATE = [CrudTestCreateSchema(label=f"Test model {i}") for i in range(1, 11)]


async def create_models(
    session: AsyncSession,
    models_to_create: list[CrudTestCreateSchema],
) -> None:
    """
    Создаем тестовые данные в БД.
    """
    for model in models_to_create:
        stmt = insert(CrudTestModel).values(**model.model_dump(exclude={"id"}))
        await session.execute(stmt)


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    db_provider = DatabaseProvider(settings.db.dsn)
    async with db_provider.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        async with db_provider.session_factory() as session:
            await create_models(session, MODELS_TO_CREATE)
            await session.commit()
        yield
    finally:
        async with db_provider.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def crud_repository():
    db_provider = DatabaseProvider(settings.db.dsn)
    async with db_provider.session_factory() as session:
        yield CrudTestRepository(session)
