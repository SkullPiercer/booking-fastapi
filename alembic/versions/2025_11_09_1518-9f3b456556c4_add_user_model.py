"""Add User model

Revision ID: 9f3b456556c4
Revises: c706cf3231f0
Create Date: 2025-11-09 15:18:55.430251

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9f3b456556c4"
down_revision: Union[str, Sequence[str], None] = "c706cf3231f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
