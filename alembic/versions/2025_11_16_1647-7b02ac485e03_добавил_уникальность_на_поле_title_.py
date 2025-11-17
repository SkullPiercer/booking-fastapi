"""Добавил уникальность на поле title комнате

Revision ID: 7b02ac485e03
Revises: 108d52f6887e
Create Date: 2025-11-16 16:47:28.076297

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7b02ac485e03"
down_revision: Union[str, Sequence[str], None] = "108d52f6887e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "rooms", ["title"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "rooms", type_="unique")
