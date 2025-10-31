from typing import Optional
from src.core.schemas import (
    ResponseSchema,
    RequestSchema,
    ReadSchemaInt,
    CreateSchemaInt,
    UpdateSchemaInt,
)


class CategoryTypeReadSchema(ResponseSchema, ReadSchemaInt):
    label: str


class CategoryTypeCreateSchema(RequestSchema, CreateSchemaInt):
    label: str


class CategoryTypeUpdateSchema(RequestSchema, UpdateSchemaInt):
    label: Optional[str] = None
