import pytest

from src.core.exceptions.repository import ModelNotFoundError

from .schemas import CrudTestReadSchema, CrudTestCreateSchema, CrudTestUpdateSchema


@pytest.mark.asyncio
async def test_get(crud_repository):
    """
    Тест метода get.
    """
    expected = CrudTestReadSchema(id=1, label="Test model 1")
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
    expected = CrudTestReadSchema(id=1, label="Test model 1")
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
        CrudTestReadSchema(id=1, label="Test model 1"),
        CrudTestReadSchema(id=2, label="Test model 2"),
        CrudTestReadSchema(id=3, label="Test model 3"),
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
        CrudTestReadSchema(id=i, label=f"Test model {i}") for i in range(1, 11)
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
    expected = CrudTestReadSchema(id=11, label="Test model 11")
    create_model = CrudTestCreateSchema(label="Test model 11")
    new_obj = await crud_repository.create(create_model)
    assert expected == new_obj


@pytest.mark.asyncio
async def test_update():
    """
    Тест метода update.
    """
    # 1. Create object
    # 2. Read object by Id
    # 3. Assert Create object == Read object
    # 4. Update object
    # 5. Read object by Id
    # 6. Assert Update object == Read object
    pass


@pytest.mark.asyncio
async def test_delete():
    """
    Тест метода delete.
    """
    # 1. Create object
    # 2. Read object by Id
    # 3. Assert Create object == Read object
    # 4. Delete object by Id
    # 5. Read object by Id
    # 6. Assert result == None
    pass
