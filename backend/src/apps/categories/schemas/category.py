from typing import Optional
from src.core.schemas import (
    ResponseSchema,
    RequestSchema,
    ReadSchemaInt,
    CreateSchemaInt,
    UpdateSchemaInt,
)


class CategoryReadSchema(ResponseSchema, ReadSchemaInt):
    label: str
    cat_type_id: int


class CategoryCreateSchema(RequestSchema, CreateSchemaInt):
    label: str
    cat_type_id: int


class CategoryUpdateSchema(RequestSchema, UpdateSchemaInt):
    label: Optional[str] = None
    cat_type_id: Optional[int] = None
