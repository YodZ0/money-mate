from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .category_type import CategoryType


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    cat_type_id: Mapped[int] = mapped_column(
        ForeignKey("category_types.id", ondelete="RESTRICT"),
        nullable=False,
    )

    category_type: Mapped["CategoryType"] = relationship(
        back_populates="categories",
    )
