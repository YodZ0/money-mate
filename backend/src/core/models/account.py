from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .period import Period


class AccountType(Base):
    __tablename__ = "account_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    acc_type_id: Mapped[int] = mapped_column(
        ForeignKey("account_types.id", ondelete="RESTRICT"),
        nullable=False,
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="RESTRICT"),
        nullable=False,
    )

    periods: Mapped[List["Period"]] = relationship(back_populates="account")
