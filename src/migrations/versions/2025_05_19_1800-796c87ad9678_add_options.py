"""add options

Revision ID: 796c87ad9678
Revises: 3227c4d58fb9
Create Date: 2025-05-19 18:00:54.151871

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "796c87ad9678"
down_revision: Union[str, None] = "3227c4d58fb9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "options",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=127), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_options",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("option_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["option_id"], ["options.id"], name="rooms_options_option_id_idx"
        ),
        sa.ForeignKeyConstraint(
            ["room_id"], ["rooms.id"], name="rooms_options_room_id_idx"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms_options")
    op.drop_table("options")
