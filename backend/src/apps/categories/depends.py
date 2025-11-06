from typing import Annotated
from fastapi import Depends

from src.core.depends import SessionManager
from .repositories import CategoryRepositoryImpl, CategoryTypeRepositoryImpl
from .services import (
    CategoryServiceProtocol,
    CategoryServiceImpl,
    CategoryTypeServiceProtocol,
    CategoryTypeServiceImpl,
)


#### REPOSITORIES ####
def get_category_repository(
    session_manager: SessionManager,
) -> CategoryRepositoryImpl:
    return CategoryRepositoryImpl(session_manager)


def get_category_type_repository(
    session_manager: SessionManager,
) -> CategoryTypeRepositoryImpl:
    return CategoryTypeRepositoryImpl(session_manager)


CategoryRepository = Annotated[
    CategoryRepositoryImpl,
    Depends(get_category_repository),
]

CategoryTypeRepository = Annotated[
    CategoryTypeRepositoryImpl,
    Depends(get_category_type_repository),
]


#### SERVICES ####
def get_category_service(repository: CategoryRepository) -> CategoryServiceProtocol:
    return CategoryServiceImpl(repository)


def get_category_type_service(
    repository: CategoryTypeRepository,
) -> CategoryTypeServiceProtocol:
    return CategoryTypeServiceImpl(repository)


CategoryService = Annotated[
    CategoryServiceProtocol,
    Depends(get_category_service),
]

CategoryTypeService = Annotated[
    CategoryTypeServiceProtocol,
    Depends(get_category_type_service),
]
