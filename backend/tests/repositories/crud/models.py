from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base


class CrudParentTestModel(Base):
    __tablename__ = "crud_parent_test_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    children: Mapped[list["CrudTestModel"]] = relationship(back_populates="parent")


class CrudTestModel(Base):
    __tablename__ = "crud_test_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("crud_parent_test_model.id"),
        nullable=False,
    )

    parent: Mapped["CrudParentTestModel"] = relationship(back_populates="children")
