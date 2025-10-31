from typing import Protocol

from ..repositories import CategoryRepositoryImpl
from ..schemas.category import (
    CategoryReadSchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)


class CategoryServiceProtocol(Protocol):

    async def all_categories(self) -> list[CategoryReadSchema]: ...

    async def create_category(
        self,
        new_cat: CategoryCreateSchema,
    ) -> CategoryReadSchema: ...

    async def update_category(
        self,
        upd_cat: CategoryUpdateSchema,
    ) -> CategoryReadSchema: ...

    async def delete_category(self, cat_id: int) -> None: ...


class CategoryServiceImpl:

    def __init__(self, category_repository: CategoryRepositoryImpl) -> None:
        self.category_repository = category_repository

    async def all_categories(self) -> list[CategoryReadSchema]:
        return await self.category_repository.get_all()

    async def create_category(
        self,
        new_cat: CategoryCreateSchema,
    ) -> CategoryReadSchema:
        return await self.category_repository.create(new_cat)

    async def update_category(
        self,
        upd_cat: CategoryUpdateSchema,
    ) -> CategoryReadSchema:
        return await self.category_repository.update(upd_cat)

    async def delete_category(self, cat_id: int) -> None:
        return await self.category_repository.delete(cat_id)
