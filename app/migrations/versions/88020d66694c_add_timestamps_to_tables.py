"""Add timestamps to tables

Revision ID: 88020d66694c
Revises:
Create Date: 2026-02-22 22:43:49.321126

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "88020d66694c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "category",
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "category",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    op.add_column(
        "edition",
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "edition",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    op.add_column(
        "evaluation",
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "evaluation",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    op.add_column(
        "role",
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "role",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    op.add_column(
        "sponsor",
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "sponsor",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    op.add_column(
        "team",
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "team",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    op.add_column(
        "user",
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    op.drop_column("user", "updated_at")
    op.drop_column("user", "created_at")

    op.drop_column("team", "updated_at")
    op.drop_column("team", "created_at")

    op.drop_column("sponsor", "updated_at")
    op.drop_column("sponsor", "created_at")

    op.drop_column("role", "updated_at")
    op.drop_column("role", "created_at")

    op.drop_column("evaluation", "updated_at")
    op.drop_column("evaluation", "created_at")

    op.drop_column("edition", "updated_at")
    op.drop_column("edition", "created_at")

    op.drop_column("category", "updated_at")
    op.drop_column("category", "created_at")
