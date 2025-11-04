from typing import Optional

from src.core.schemas.repository import (
    ReadSchemaInt,
    CreateSchemaInt,
    UpdateSchemaInt,
)
from src.core.schemas.request_response import RequestSchema, ResponseSchema


class CrudTestReadSchema(ResponseSchema, ReadSchemaInt):
    label: str


class CrudTestCreateSchema(RequestSchema, CreateSchemaInt):
    label: str


class CrudTestUpdateSchema(RequestSchema, UpdateSchemaInt):
    label: Optional[str] = None
