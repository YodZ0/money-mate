"""initial

Revision ID: 353f0106d459
Revises:
Create Date: 2025-10-26 18:19:19.944025

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "353f0106d459"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "account_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_account_types")),
        sa.UniqueConstraint("name", name=op.f("uq_account_types_name")),
    )
    op.create_table(
        "category_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("label", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_category_types")),
        sa.UniqueConstraint("label", name=op.f("uq_category_types_label")),
    )
    op.create_table(
        "currencies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("currency", sa.String(length=32), nullable=False),
        sa.Column("code", sa.String(length=3), nullable=False),
        sa.Column("symbol", sa.String(length=1), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_currencies")),
        sa.UniqueConstraint("code", name=op.f("uq_currencies_code")),
        sa.UniqueConstraint("currency", name=op.f("uq_currencies_currency")),
        sa.UniqueConstraint("symbol", name=op.f("uq_currencies_symbol")),
    )
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("label", sa.String(length=32), nullable=False),
        sa.Column("balance", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("acc_type_id", sa.Integer(), nullable=False),
        sa.Column("currency_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["acc_type_id"],
            ["account_types.id"],
            name=op.f("fk_accounts_acc_type_id_account_types"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["currency_id"],
            ["currencies.id"],
            name=op.f("fk_accounts_currency_id_currencies"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_accounts")),
        sa.UniqueConstraint("label", name=op.f("uq_accounts_label")),
    )
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("label", sa.String(length=64), nullable=False),
        sa.Column("cat_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cat_type_id"],
            ["category_types.id"],
            name=op.f("fk_categories_cat_type_id_category_types"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
        sa.UniqueConstraint("label", name=op.f("uq_categories_label")),
    )
    op.create_table(
        "periods",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("label", sa.String(length=64), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("acc_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["acc_id"],
            ["accounts.id"],
            name=op.f("fk_periods_acc_id_accounts"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_periods")),
        sa.UniqueConstraint("label", name=op.f("uq_periods_label")),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("period_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk_transactions_category_id_categories"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["period_id"],
            ["periods.id"],
            name=op.f("fk_transactions_period_id_periods"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transactions")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("transactions")
    op.drop_table("periods")
    op.drop_table("categories")
    op.drop_table("accounts")
    op.drop_table("currencies")
    op.drop_table("category_types")
    op.drop_table("account_types")
