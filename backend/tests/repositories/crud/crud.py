from src.core.repositories.crud import CrudBaseRepository
from .models import CrudTestModel
from .schemas import CrudTestReadSchema, CrudTestCreateSchema, CrudTestUpdateSchema


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
    Тестовый репозиторий.
    """

    model_type = CrudTestModel
    read_schema_type = CrudTestReadSchema
