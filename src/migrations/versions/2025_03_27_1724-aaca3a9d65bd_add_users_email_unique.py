"""add users.email unique

Revision ID: aaca3a9d65bd
Revises: fd61246b9cc0
Create Date: 2025-03-27 17:24:30.672922

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aaca3a9d65bd"
down_revision: Union[str, None] = "fd61246b9cc0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
