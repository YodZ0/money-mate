import pytest
from typing import AsyncGenerator

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import DatabaseProvider
from src.core.session_manager import SessionManagerImpl
from src.core.models.base import Base

from tests.settings import settings

from .crud import CrudParentTestRepository, CrudTestRepository
from .models import CrudParentTestModel, CrudTestModel
from .schemas import CrudParentTestCreateSchema, CrudTestCreateSchema


MODELS_TO_CREATE = [
    CrudTestCreateSchema.model_validate(
        {
            "label": f"Test model {i}",
            "parentId": 1,
        }
    )
    for i in range(1, 11)
]


async def create_models(
    session: AsyncSession,
    models_to_create: list[CrudTestCreateSchema],
) -> None:
    """
    Создаем тестовые данные в БД.
    """
    stmt = insert(CrudParentTestModel).values(
        **CrudParentTestCreateSchema(name="Parent 1").model_dump(exclude={"id"})
    )
    await session.execute(stmt)
    for model in models_to_create:
        stmt = insert(CrudTestModel).values(**model.model_dump(exclude={"id"}))
        await session.execute(stmt)


@pytest.fixture(scope="function", autouse=True)
async def prepare_db():
    """
    Создаем таблицы в БД, наполняем данными, очищаем до и после каждого теста.
    """
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
async def crud_repository() -> AsyncGenerator[CrudTestRepository]:
    """
    Репозиторий для модели CrudTestModel.
    """
    db_provider = DatabaseProvider(settings.db.dsn)
    async with db_provider.session_factory() as session:
        yield CrudTestRepository(SessionManagerImpl(session))  # type: ignore


@pytest.fixture
async def crud_parent_repository() -> AsyncGenerator[CrudParentTestRepository]:
    """
    Репозиторий для модели CrudParentTestModel.
    """
    db_provider = DatabaseProvider(settings.db.dsn)
    async with db_provider.session_factory() as session:
        yield CrudParentTestRepository(SessionManagerImpl(session))  # type: ignore
