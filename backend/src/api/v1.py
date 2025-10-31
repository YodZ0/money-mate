from fastapi import APIRouter
from src.settings import settings

from src.apps.categories.router import router as categories_router

router_v1 = APIRouter(prefix=settings.api.v1.prefix)
# Include API routers
router_v1.include_router(categories_router)
