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
async def test_create_already_exists(crud_repository):
    """
    Тест метода create на обработку исключения UniqueViolationError.
    """
    with pytest.raises(ModelAlreadyExistsError) as exc_info:
        existing_model = CrudTestCreateSchema.model_validate(
            {"label": "Test model 1", "parentId": 1}
        )
        await crud_repository.create(existing_model)
    assert exc_info.value.model == CrudTestModel
    assert exc_info.value.field == "label"
    assert exc_info.value.value == "Test model 1"
    assert exc_info.value.action == ModelActionEnum.INSERT


@pytest.mark.asyncio
async def test_create_with_integrity_error(crud_repository):
    """
    Тест метода create на обработку общей ошибки создания/обновления модели.
    """
    with pytest.raises(ModelIntegrityError) as exc_info:
        non_existing_parent_model = CrudTestCreateSchema.model_validate(
            {"label": "Test model 12", "parentId": 2}
        )
        await crud_repository.create(non_existing_parent_model)
    assert exc_info.value.model == CrudTestModel
    assert exc_info.value.action == ModelActionEnum.INSERT


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
async def test_update_already_exists(crud_repository):
    """
    Тест метода update на обработку исключения UniqueViolationError.
    """
    # Check existing model with id=10
    expected_before_update = CrudTestReadSchema(
        id=10, label="Test model 10", parent_id=1
    )
    before_update = await crud_repository.get(id=10)
    assert expected_before_update == before_update

    # Try to fail update because of unique label
    with pytest.raises(ModelAlreadyExistsError) as exc_info:
        obj_update = CrudTestUpdateSchema(id=10, label="Test model 1")
        await crud_repository.update(obj_update)
    assert exc_info.value.model == CrudTestModel
    assert exc_info.value.action == ModelActionEnum.UPDATE

    # Check if model did not change
    expected_after_update = await crud_repository.get(id=10)
    assert expected_after_update == expected_before_update


@pytest.mark.asyncio
async def test_update_with_integrity_error(crud_repository):
    """
    Тест метода update на обработку общей ошибки создания/обновления модели.
    """
    # Check existing model with id=10
    expected_before_update = CrudTestReadSchema(
        id=10, label="Test model 10", parent_id=1
    )
    before_update = await crud_repository.get(id=10)
    assert expected_before_update == before_update

    # Try to fail update because of nonexistent parent id
    with pytest.raises(ModelIntegrityError) as exc_info:
        obj_update = CrudTestUpdateSchema.model_validate({"id": 10, "parentId": 99})
        await crud_repository.update(obj_update)
    assert exc_info.value.model == CrudTestModel
    assert exc_info.value.action == ModelActionEnum.UPDATE

    # Try to fail update because of nullable parent field
    with pytest.raises(ModelIntegrityError) as exc_info:
        obj_update = CrudTestUpdateSchema.model_validate({"id": 10, "parentId": None})
        await crud_repository.update(obj_update)
    assert exc_info.value.model == CrudTestModel
    assert exc_info.value.action == ModelActionEnum.UPDATE

    # Check if model did not change
    expected_after_update = await crud_repository.get(id=10)
    assert expected_after_update == expected_before_update


@pytest.mark.asyncio
async def test_delete(crud_repository):
    """
    Тест метода delete.
    """
    objects_before_delete = await crud_repository.get_all()
    assert len(objects_before_delete) == 10

    await crud_repository.delete(id=10)

    objects_after_delete = await crud_repository.get_all()
    assert len(objects_after_delete) == 9


@pytest.mark.asyncio
async def test_delete_with_integrity_error(crud_parent_repository):
    """
    Тест метода delete на обработку исключения ForeignKeyViolationError.
    """
    with pytest.raises(ModelIntegrityError) as exc_info:
        await crud_parent_repository.delete(id=1)
    assert exc_info.value.model == CrudParentTestModel
    assert exc_info.value.action == ModelActionEnum.DELETE
