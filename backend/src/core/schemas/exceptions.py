from pydantic import BaseModel


class BusinessLogicExceptionSchema(BaseModel):
    """
    Схема базового исключения бизнес-логики.
    """

    type: str
    msg: str
    traceback: str | None


class ModelAlreadyExistsErrorSchema(BusinessLogicExceptionSchema):
    """
    Схема ошибки, возникающей при попытке создать модель
    с существующим уникальным полем.
    """

    field: str
    value: str


class ExceptionInfoSchema(BaseModel):
    """
    Схема детальной информации об ошибке.
    """

    sqlstate: str
    error: str = "Integrity error"
    error_detail: str | None = None
    constraint: str | None = None
    field: str | None = None
    value: str | None = None
