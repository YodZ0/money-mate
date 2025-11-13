from src.core.repositories.crud import CrudBaseRepository
from .models import CrudParentTestModel, CrudTestModel
from .schemas import (
    CrudParentTestReadSchema,
    CrudParentTestCreateSchema,
    CrudParentTestUpdateSchema,
    CrudTestReadSchema,
    CrudTestCreateSchema,
    CrudTestUpdateSchema,
)


class CrudParentTestRepository(
    CrudBaseRepository[
        CrudParentTestModel,
        CrudParentTestReadSchema,
        CrudParentTestCreateSchema,
        CrudParentTestUpdateSchema,
        int,
    ]
):
    """
    Тестовый репозиторий родительской модели CrudParentTestModel.
    """

    model_type = CrudParentTestModel
    read_schema_type = CrudParentTestReadSchema


class CrudTestRepository(
    CrudBaseRepository[
        CrudTestModel,
        CrudTestReadSchema,
        CrudTestCreateSchema,
        CrudTestUpdateSchema,
        int,
    ]
):
    """
    Тестовый репозиторий дочерней модели CrudTestModel.
    """

    model_type = CrudTestModel
    read_schema_type = CrudTestReadSchema
