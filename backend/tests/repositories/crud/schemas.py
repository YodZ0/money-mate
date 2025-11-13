from typing import Optional

from src.core.schemas.repository import (
    ReadSchemaInt,
    CreateSchemaInt,
    UpdateSchemaInt,
)
from src.core.schemas.request_response import RequestSchema, ResponseSchema


class CrudParentTestReadSchema(ResponseSchema, ReadSchemaInt):
    name: str


class CrudParentTestCreateSchema(RequestSchema, CreateSchemaInt):
    name: str


class CrudParentTestUpdateSchema(RequestSchema, UpdateSchemaInt):
    name: Optional[str] = None


class CrudTestReadSchema(ResponseSchema, ReadSchemaInt):
    label: str
    parent_id: int


class CrudTestCreateSchema(RequestSchema, CreateSchemaInt):
    label: str
    parent_id: int


class CrudTestUpdateSchema(RequestSchema, UpdateSchemaInt):
    label: Optional[str] = None
    parent_id: Optional[int] = None
