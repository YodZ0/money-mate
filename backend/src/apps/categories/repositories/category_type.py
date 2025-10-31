from src.core.models.category_type import CategoryType
from src.core.repositories.crud import CrudBaseRepository
from ..schemas import (
    CategoryTypeReadSchema,
    CategoryTypeCreateSchema,
    CategoryTypeUpdateSchema,
)


class CategoryTypeRepositoryImpl(
    CrudBaseRepository[
        CategoryType,
        CategoryTypeReadSchema,
        CategoryTypeCreateSchema,
        CategoryTypeUpdateSchema,
        int,
    ]
):
    model_type = CategoryType
    read_schema_type = CategoryTypeReadSchema
