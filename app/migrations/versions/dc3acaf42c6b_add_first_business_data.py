"""Add first business data

Revision ID: dc3acaf42c6b
Revises: 4918095df72e
Create Date: 2026-03-22 19:36:00.665075

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc3acaf42c6b'
down_revision: Union[str, None] = '4918095df72e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    meta = sa.MetaData()

    role_table = sa.Table(
        "role",
        meta,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("description", sa.String),
        sa.Column("is_super_user", sa.Boolean),
        sa.Column("internal_code", sa.String),
    )

    category_table = sa.Table(
        "category",
        meta,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("internal_code", sa.String),
        sa.Column("open_date", sa.DateTime),
        sa.Column("close_date", sa.DateTime),
    )

    edition_table = sa.Table(
        "edition",
        meta,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("start_date", sa.DateTime),
        sa.Column("end_date", sa.DateTime),
    )

    user_table = sa.Table(
        "user",
        meta,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String),
        sa.Column("email", sa.String),
        sa.Column("name", sa.String),
        sa.Column("password_hash", sa.String),
        sa.Column("status", sa.String),
        sa.Column("role_id", sa.Integer),
        sa.Column("category_id", sa.Integer),
        sa.Column("is_verified", sa.Boolean),
    )

    team_table = sa.Table(
        "team",
        meta,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("edition_id", sa.Integer),
        sa.Column("category_id", sa.Integer),
    )

    user_team_assoc = sa.Table(
        "user_team_association",
        meta,
        sa.Column("user_id", sa.Integer),
        sa.Column("team_id", sa.Integer),
    )

    request_assoc = sa.Table(
        "team_request_association",
        meta,
        sa.Column("team_id", sa.Integer),
        sa.Column("sender_user_id", sa.Integer),
        sa.Column("status", sa.String),
    )

    conn = op.get_bind()

    roles_to_insert = [
        {
            "name": "Common User",
            "description": "Standard user with basic access",
            "is_super_user": False,
            "internal_code": "common_user",
        },
        {
            "name": "Administrator",
            "description": "User with administrative privileges",
            "is_super_user": False,
            "internal_code": "admin"
        },
        {
            "name": "Super Administrator",
            "description": "User with super administrator privileges",
            "is_super_user": True,
            "internal_code": "superadmin",
        },
    ]
    for r in roles_to_insert:
        if not conn.execute(sa.text("SELECT 1 FROM role WHERE internal_code = :c"), {"c": r["internal_code"]}).fetchone():
            op.bulk_insert(role_table, [r])

    if not conn.execute(sa.text("SELECT 1 FROM category WHERE internal_code = 'cat_general'")).fetchone():
        op.bulk_insert(category_table, [{
            "name": "General", 
            "internal_code": "cat_general",
            "open_date": datetime(2026, 1, 12),
            "close_date": datetime(2026, 3, 12)
        }])

    if not conn.execute(sa.text("SELECT 1 FROM edition WHERE name = 'First Edition 2026'")).fetchone():
        op.bulk_insert(edition_table, [{
            "name": "First Edition 2026",
            "start_date": datetime(2026, 12, 12),
            "end_date": datetime(2026, 12, 14)
        }])

    def get_id(table_name: str, code_col: str, code_val: str) -> int:
        res = conn.execute(sa.text(f"SELECT id FROM {table_name} WHERE {code_col} = :v"), {"v": code_val}).fetchone()
        return res[0] if res else 0

    role_super = get_id("role", "internal_code", "superadmin")
    role_admin = get_id("role", "internal_code", "admin")
    role_common = get_id("role", "internal_code", "common_user")
    cat_id = get_id("category", "internal_code", "cat_general")
    ed_id = get_id("edition", "name", "First Edition 2026")

    default_hash = "$argon2id$v=19$m=65536,t=3,p=4$+t9b693b2xsjpNR6j7GWMg$3IB15WbxlyCIpV7kT1IXTP/4DIqj2De0m6MQa3zze7E" 

    users_to_insert = [
        {
            "username": "mballesteros",
            "name": "Maria Ballesteros",
            "email": "maria.ballesteros@unet.edu.ve",
            "password_hash": default_hash,
            "status": "ACTIVE",
            "role_id": role_super,
            "category_id": cat_id,
            "is_verified": True
        },
        {
            "username": "dbautista",
            "name": "Daniel Bautista",
            "email": "daniel.bautista.test@unet.edu.ve",
            "password_hash": default_hash,
            "status": "ACTIVE",
            "role_id": role_admin,
            "category_id": cat_id,
            "is_verified": True
        },
        {
            "username": "dmoreno",
            "name": "Douglas Moreno",
            "email": "douglas.moreno.test@unet.edu.ve",
            "password_hash": default_hash,
            "status": "ACTIVE",
            "role_id": role_common,
            "category_id": cat_id,
            "is_verified": True
        }
    ]

    for u in users_to_insert:
        if not conn.execute(sa.text("SELECT 1 FROM \"user\" WHERE email = :e"), {"e": u["email"]}).fetchone():
            op.bulk_insert(user_table, [u])

    if not conn.execute(
        sa.text("SELECT 1 FROM team WHERE name = 'UNET Cyber-Warriors'")
    ).fetchone():
        op.bulk_insert(
            team_table,
            [
                {
                    "name": "UNET Cyber-Warriors",
                    "edition_id": ed_id,
                    "category_id": cat_id,
                }
            ],
        )

    t_id = get_id("team", "name", "UNET Cyber-Warriors")
    u_daniel = get_id('"user"', "email", "daniel.bautista.test@unet.edu.ve")

    if t_id and u_daniel:
        if not conn.execute(
            sa.text("SELECT 1 FROM user_team_association WHERE user_id = :u"),
            {"u": u_daniel},
        ).fetchone():
            op.bulk_insert(user_team_assoc, [{"user_id": u_daniel, "team_id": t_id}])

        if not conn.execute(
            sa.text("SELECT 1 FROM team_request_association WHERE sender_user_id = :u"),
            {"u": u_daniel},
        ).fetchone():
            op.bulk_insert(
                request_assoc,
                [{"team_id": t_id, "sender_user_id": u_daniel, "status": "ACCEPTED"}],
            )

def downgrade() -> None:
    conn = op.get_bind()

    conn.execute(sa.text("DELETE FROM team_request_association"))
    conn.execute(sa.text("DELETE FROM user_team_association"))
    conn.execute(sa.text("DELETE FROM team WHERE name = 'UNET Cyber-Warriors'"))
    conn.execute(sa.text("DELETE FROM \"user\" WHERE email LIKE '%@unet.edu.ve'"))
    conn.execute(
        sa.text(
            "DELETE FROM role WHERE internal_code IN ('common_user', 'admin', 'superadmin')"
        )
    )
    conn.execute(sa.text("DELETE FROM category WHERE internal_code = 'cat_general'"))
    conn.execute(sa.text("DELETE FROM edition WHERE name = 'First Edition 2026'"))
