from fastapi import APIRouter

from src.core.schemas import StatusOKResponseSchema
from .schemas import CategoryReadSchema, CategoryCreateSchema, CategoryUpdateSchema
from .depends import CategoryService

__all__ = ("router",)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


### CATEGORIES ###
@router.get("/")
async def all_categories(service: CategoryService) -> list[CategoryReadSchema]:
    return await service.all_categories()


@router.post("/")
async def new_category(
    service: CategoryService,
    category: CategoryCreateSchema,
) -> CategoryReadSchema:
    return await service.create_category(category)


@router.patch("/")
async def update_category(
    service: CategoryService,
    category: CategoryUpdateSchema,
) -> CategoryReadSchema:
    return await service.update_category(category)


@router.delete("/{cat_id}")
async def delete_category(
    service: CategoryService,
    cat_id: int,
) -> StatusOKResponseSchema:
    await service.delete_category(cat_id)
    return StatusOKResponseSchema()


### CATEGORY TYPES ###
@router.get("/types")
async def all_category_types():
    pass


@router.post("/types")
async def new_category_type():
    pass


@router.patch("/types")
async def update_category_type():
    pass


@router.delete("/types/{type_id}")
async def delete_category_type(type_id: int):
    pass
