"""Add deleted status to team request enum

Revision ID: 4b7f2e1a8d9c
Revises: dc3acaf42c6b
Create Date: 2026-03-20 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4b7f2e1a8d9c"
down_revision: Union[str, None] = "dc3acaf42c6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE teamrequeststatus ADD VALUE IF NOT EXISTS 'DELETED'")


def downgrade() -> None:
    conn = op.get_bind()
    exists = conn.execute(
        sa.text(
            """
            SELECT 1
            FROM pg_type
            WHERE typname = 'teamrequeststatus'
            """
        )
    ).fetchone()

    if not exists:
        return

    op.execute(
        """
        UPDATE team_request_association
        SET status = 'DENIED'
        WHERE status::text = 'DELETED'
        """
    )

    op.execute("ALTER TYPE teamrequeststatus RENAME TO teamrequeststatus_old")
    op.execute("CREATE TYPE teamrequeststatus AS ENUM ('DENIED', 'PENDING', 'ACCEPTED')")
    op.execute(
        """
        ALTER TABLE team_request_association
        ALTER COLUMN status
        TYPE teamrequeststatus
        USING status::text::teamrequeststatus
        """
    )
    op.execute("DROP TYPE teamrequeststatus_old")
