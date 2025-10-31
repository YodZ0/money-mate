from typing import Protocol

from ..repositories import CategoryTypeRepositoryImpl
from ..schemas import (
    CategoryTypeReadSchema,
    CategoryTypeCreateSchema,
    CategoryTypeUpdateSchema,
)


class CategoryTypeServiceProtocol(Protocol):

    async def all_types(self) -> list[CategoryTypeReadSchema]: ...

    async def create_type(
        self,
        new_type: CategoryTypeCreateSchema,
    ) -> CategoryTypeReadSchema: ...

    async def update_type(
        self,
        upd_type: CategoryTypeUpdateSchema,
    ) -> CategoryTypeReadSchema: ...

    async def delete_type(self, cat_type_id: int) -> None: ...


class CategoryTypeServiceImpl:

    def __init__(self, category_type_repository: CategoryTypeRepositoryImpl) -> None:
        self.category_type_repository = category_type_repository

    async def all_types(self) -> list[CategoryTypeReadSchema]:
        return await self.category_type_repository.get_all()

    async def create_type(
        self,
        new_type: CategoryTypeCreateSchema,
    ) -> CategoryTypeReadSchema:
        return await self.category_type_repository.create(new_type)

    async def update_type(
        self,
        upd_type: CategoryTypeUpdateSchema,
    ) -> CategoryTypeReadSchema:
        return await self.category_type_repository.update(upd_type)

    async def delete_type(self, cat_type_id: int) -> None:
        return await self.category_type_repository.delete(cat_type_id)
