"""Переделал связи

Revision ID: 63e68137c1f8
Revises: 259ec4aa7a64
Create Date: 2025-12-25 23:24:55.162486

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "63e68137c1f8"
down_revision: Union[str, Sequence[str], None] = "259ec4aa7a64"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("usersimages")
    op.add_column("users", sa.Column("image_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "users", "images", ["image_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="foreignkey")
    op.drop_column("users", "image_id")
    op.create_table(
        "usersimages",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "image_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["image_id"], ["images.id"], name=op.f("usersimages_image_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("usersimages_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("usersimages_pkey")),
    )
