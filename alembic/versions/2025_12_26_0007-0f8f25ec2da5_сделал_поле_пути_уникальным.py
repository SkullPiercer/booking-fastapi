"""Сделал поле пути уникальным

Revision ID: 0f8f25ec2da5
Revises: 63e68137c1f8
Create Date: 2025-12-26 00:07:37.459234

"""

from typing import Sequence, Union

from alembic import op


revision: str = "0f8f25ec2da5"
down_revision: Union[str, Sequence[str], None] = "63e68137c1f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "images", ["file_path"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "images", type_="unique")
