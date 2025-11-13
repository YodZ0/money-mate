import contextlib
import re
from typing import Generic, Sequence, cast

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from src.core.enums import ModelActionEnum, DatabaseErrorEnum
from src.core.exceptions import (
    ModelNotFoundError,
    ModelIntegrityError,
    ModelAlreadyExistsError,
)
from src.core.schemas import ExceptionInfoSchema
from src.core.session_manager import SessionManagerProtocol
from src.core.type_vars import (
    ModelType,
    CreateSchemaBaseType,
    UpdateSchemaBaseType,
    ReadSchemaBaseType,
    IdType,
)


class CrudBaseRepository(
    Generic[
        ModelType,
        ReadSchemaBaseType,
        CreateSchemaBaseType,
        UpdateSchemaBaseType,
        IdType,
    ]
):
    model_type: type[ModelType]
    read_schema_type: type[ReadSchemaBaseType]

    def __init__(self, session_manager: SessionManagerProtocol) -> None:
        self._session_manager = session_manager

    async def get(self, id: IdType) -> ReadSchemaBaseType:
        """
        Получаем модель по идентификатору.
        """
        query = select(self.model_type).where(self.model_type.id == id)  # type: ignore
        async with self._session_manager.get_session() as s:
            model = (await s.execute(query)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundError(self.model_type, model_id=id)
            return self._model_validate(model)

    async def get_one_or_none(self, id: IdType) -> ReadSchemaBaseType | None:
        """
        Получаем модель по идентификатору или None.
        """
        with contextlib.suppress(ModelNotFoundError):
            return await self.get(id)
        return None

    async def get_by_ids(
        self,
        ids: Sequence[IdType],
        *,
        strict: bool = False,
    ) -> list[ReadSchemaBaseType]:
        """
        Получаем список моделей по идентификаторам.
        """
        query = select(self.model_type).where(self.model_type.id.in_(ids))
        async with self._session_manager.get_session() as s:
            models = (await s.execute(query)).scalars().all()
            self._check_get_by_ids_strict(ids, models, strict)
            return [self._model_validate(model) for model in models]

    async def get_all(self) -> list[ReadSchemaBaseType]:
        """
        Получаем список всех моделей.
        """
        query = select(self.model_type)
        async with self._session_manager.get_session() as s:
            models = (await s.execute(query)).scalars().all()
            return [self._model_validate(model) for model in models]

    async def create(self, create_obj: CreateSchemaBaseType) -> ReadSchemaBaseType:
        """
        Создаем модель.
        """
        statement = (
            insert(self.model_type)
            .values(**create_obj.model_dump(exclude={"id"}))
            .returning(self.model_type)
        )
        async with self._session_manager.get_session() as s:
            try:
                model = (await s.execute(statement)).scalar_one()
                return self._model_validate(model)
            except IntegrityError as integrity_error:
                exc_info = self._parse_asyncpg_integrity_error(integrity_error)
                if exc_info.error == DatabaseErrorEnum.UNIQUE_VIOLATION_ERROR:
                    raise ModelAlreadyExistsError(
                        self.model_type,
                        field=exc_info.field,
                        value=exc_info.value,
                        action=ModelActionEnum.INSERT,
                    ) from integrity_error
                if exc_info.error == DatabaseErrorEnum.FOREIGN_KEY_VIOLATION_ERROR:
                    raise ModelIntegrityError(
                        self.model_type,
                        action=ModelActionEnum.INSERT,
                    ) from integrity_error
                else:
                    raise ModelIntegrityError(
                        self.model_type,
                        action=ModelActionEnum.INSERT,
                    ) from integrity_error

    async def update(self, update_obj: UpdateSchemaBaseType) -> ReadSchemaBaseType:
        """
        Обновляем модель по идентификатору.
        """
        pk = update_obj.id
        statement = (
            update(self.model_type)
            .where(self.model_type.id == pk)  # type: ignore
            .values(**update_obj.model_dump(exclude={"id"}, exclude_unset=True))
            .returning(self.model_type)
        )
        async with self._session_manager.get_session() as s:
            try:
                model = (await s.execute(statement)).scalar_one_or_none()
                if model is None:
                    raise ModelNotFoundError(self.model_type, model_id=update_obj.id)
                return self._model_validate(model)
            except IntegrityError as integrity_error:
                exc_info = self._parse_asyncpg_integrity_error(integrity_error)
                if exc_info.error == DatabaseErrorEnum.UNIQUE_VIOLATION_ERROR:
                    raise ModelAlreadyExistsError(
                        self.model_type,
                        field=exc_info.field,
                        value=exc_info.value,
                        action=ModelActionEnum.UPDATE,
                    ) from integrity_error
                if exc_info.error == DatabaseErrorEnum.FOREIGN_KEY_VIOLATION_ERROR:
                    raise ModelIntegrityError(
                        self.model_type,
                        action=ModelActionEnum.UPDATE,
                    ) from integrity_error
                else:
                    raise ModelIntegrityError(
                        self.model_type,
                        action=ModelActionEnum.UPDATE,
                    ) from integrity_error

    async def delete(self, id: IdType) -> None:
        """
        Удаляем модель по идентификатору.
        """
        async with self._session_manager.get_session() as s:
            try:
                statement = delete(self.model_type).where(self.model_type.id == id)  # type: ignore
                await s.execute(statement)
            except IntegrityError as integrity_error:
                raise ModelIntegrityError(
                    self.model_type,
                    action=ModelActionEnum.DELETE,
                ) from integrity_error

    def _model_validate(self, model: ModelType, **kwargs) -> ReadSchemaBaseType:
        """
        Приводим модель к схеме.
        """
        return self.read_schema_type.model_validate(
            model,
            from_attributes=True,
            **kwargs,
        )

    def _check_get_by_ids_strict(
        self,
        ids: Sequence[IdType],
        models: Sequence[ModelType],
        strict: bool,
    ) -> None:
        """
        Проверяем, что по идентификаторам получены все модели.
        """
        if strict and len(ids) != len(models):
            raise ModelNotFoundError(
                self.model_type,
                model_id=set(ids) - {cast(IdType, model.id) for model in models},
            )

    def _parse_asyncpg_integrity_error(
        self, exc: IntegrityError
    ) -> ExceptionInfoSchema:
        """
        Детализируем ошибку из обертки ошибок sqlalchemy.
        """
        orig = exc.orig
        exc_text = str(orig).split("\n")
        sqlstate = getattr(orig, "sqlstate", None)
        exc_info = ExceptionInfoSchema(sqlstate=sqlstate)

        parts = exc_text[0].split(":", 1)
        error_detail = None

        if len(parts) > 1:
            error_detail = parts[1].strip().capitalize()
            exc_info.error_detail = error_detail

        # Получаем field и value из DETAIL: (field)=(value)
        if len(exc_text) > 1:
            detail_line = exc_text[1]
            if detail_line is not None:
                detail_match = re.search(
                    r"\((?P<field>[^)]+)\)=\((?P<value>[^)]+)\)", detail_line
                )
                if detail_match:
                    exc_info.field = detail_match.group("field")
                    exc_info.value = detail_match.group("value")

        if sqlstate == "23505":  # UniqueViolationError
            exc_info.error = DatabaseErrorEnum.UNIQUE_VIOLATION_ERROR
            exc_info.constraint = self._get_error_constraint(
                exc_info.error, error_detail
            )
        elif sqlstate == "23503":  # ForeignKeyViolationError
            exc_info.error = DatabaseErrorEnum.FOREIGN_KEY_VIOLATION_ERROR
            exc_info.constraint = self._get_error_constraint(
                exc_info.error, error_detail
            )
        elif sqlstate == "23502":  # NotNullViolationError
            exc_info.error = DatabaseErrorEnum.NOT_NULL_VIOLATION_ERROR

        else:
            exc_info.error = DatabaseErrorEnum.INTEGRITY_ERROR

        return exc_info

    @staticmethod
    def _get_error_constraint(
        error: DatabaseErrorEnum | str,
        detail: str,
    ) -> str | None:
        """
        Получаем ограничение constraint.
        """
        error_code_pattern_mapper = {
            DatabaseErrorEnum.UNIQUE_VIOLATION_ERROR: r'uq_[^"]+',
            DatabaseErrorEnum.FOREIGN_KEY_VIOLATION_ERROR: r'fk_[^"]+',
        }
        constraint_match = re.search(error_code_pattern_mapper.get(error, None), detail)
        if constraint_match:
            return constraint_match.group(0)
        return None
