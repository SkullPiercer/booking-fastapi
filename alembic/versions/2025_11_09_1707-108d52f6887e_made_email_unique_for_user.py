"""Made email unique for user

Revision ID: 108d52f6887e
Revises: 9f3b456556c4
Create Date: 2025-11-09 17:07:05.744829

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "108d52f6887e"
down_revision: Union[str, Sequence[str], None] = "9f3b456556c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
