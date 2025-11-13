import pytest

from src.core.exceptions.repository import (
    ModelNotFoundError,
    ModelIntegrityError,
    ModelAlreadyExistsError,
)
from src.core.enums import ModelActionEnum

from .models import CrudParentTestModel, CrudTestModel
from .schemas import CrudTestReadSchema, CrudTestCreateSchema, CrudTestUpdateSchema


@pytest.mark.asyncio
async def test_get(crud_repository):
    """
    Тест метода get.
    """
    expected = CrudTestReadSchema(id=1, label="Test model 1", parent_id=1)
    read_dto = await crud_repository.get(id=1)
    assert expected == read_dto

    with pytest.raises(ModelNotFoundError) as exc_info:
        await crud_repository.get(id=99)
    assert exc_info.value.model_id == 99


@pytest.mark.asyncio
async def test_get_one_or_none(crud_repository):
    """
    Тест метода get_one_or_none.
    """
    expected = CrudTestReadSchema(id=1, label="Test model 1", parent_id=1)
    read_dto = await crud_repository.get_one_or_none(id=1)
    assert expected == read_dto
    non_existed = await crud_repository.get_one_or_none(id=99)
    assert non_existed is None


@pytest.mark.asyncio
async def test_get_by_ids(crud_repository):
    """
    Тест метода get_by_ids.
    """
    ids = [1, 2, 3]
    expected_list = [
        CrudTestReadSchema(id=i, label=f"Test model {i}", parent_id=1)
        for i in range(1, 4)
    ]
    result = await crud_repository.get_by_ids(ids)
    assert len(ids) == len(result)
    for model in result:
        assert model in expected_list


@pytest.mark.asyncio
async def test_get_all(crud_repository):
    """
    Тест метода get_all.
    """
    expected_list = [
        CrudTestReadSchema(id=i, label=f"Test model {i}", parent_id=1)
        for i in range(1, 11)
    ]
    result = await crud_repository.get_all()
    assert len(expected_list) == len(result)
    for model in result:
        assert model in expected_list


@pytest.mark.asyncio
async def test_create(crud_repository):
    """
    Тест метода create.
    """
    expected = CrudTestReadSchema(id=11, label="Test model 11", parent_id=1)
    create_model = CrudTestCreateSchema.model_validate(
        {"label": "Test model 11", "parentId": 1}
    )
    new_obj = await crud_repository.create(create_model)
    assert expected == new_obj


@pytest.mark.asyncio
async def test_update(crud_repository):
    """
    Тест метода update.
    """
    expected_before_update = CrudTestReadSchema(id=1, label="Test model 1", parent_id=1)
    obj_before_update = await crud_repository.get(id=1)
    assert expected_before_update == obj_before_update

    expected_after_update = CrudTestReadSchema(
        id=1, label="Updated Test model 1", parent_id=1
    )
    update_obj = CrudTestUpdateSchema(id=1, label="Updated Test model 1")
    obj_after_update = await crud_repository.update(update_obj)
    assert expected_after_update == obj_after_update

    updated_object = await crud_repository.get(id=1)
    assert expected_after_update == updated_object


@pytest.mark.asyncio
async def test_delete(crud_repository):
    """
    Тест метода delete.
    """
    objects_before_delete = await crud_repository.get_all()
    assert len(objects_before_delete) == 10

    await crud_repository.delete(id=10)

    objects_after_delete = await crud_repository.get_all()
    assert 9 == len(objects_after_delete)
    assert len(objects_after_delete) == 9

