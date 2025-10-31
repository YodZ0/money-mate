from src.core.models.category import Category
from src.core.repositories.crud import CrudBaseRepository
from ..schemas import (
    CategoryReadSchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)


class CategoryRepositoryImpl(
    CrudBaseRepository[
        Category,
        CategoryReadSchema,
        CategoryCreateSchema,
        CategoryUpdateSchema,
        int,
    ]
):
    model_type = Category
    read_schema_type = CategoryReadSchema
