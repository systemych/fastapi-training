"""initial migration

Revision ID: dce68724b049
Revises:
Create Date: 2025-03-21 11:54:21.744535

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "dce68724b049"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("hotels")
