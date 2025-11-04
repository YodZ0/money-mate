from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class CrudTestModel(Base):
    __tablename__ = "crud_test_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
