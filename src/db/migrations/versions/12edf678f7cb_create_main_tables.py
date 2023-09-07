"""create main tables.

Revision ID: 12edf678f7cb
Revises:
Create Date: 2023-09-05 12:33:01.738494

"""
from typing import Optional, Sequence, Tuple, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "12edf678f7cb"
down_revision: Optional[str] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    """Create timestamp in DB."""
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_user_table() -> None:
    """Create User table."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("slack_id", sa.Numeric, nullable=False, index=True, unique=True),
        *timestamps(),
    )


def create_leetcode_update_table() -> None:
    """Create Leetcode Update table."""
    op.create_table(
        "leetcode_updates",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("leetcode_update", sa.Integer, nullable=False),
        sa.Column("date", sa.Date, nullable=False, index=True, unique=True),
        sa.Column(
            "posters_slack_id",
            sa.String,
            sa.ForeignKey("users.slack_id", ondelete="CASCADE"),
            nullable=False,
        ),
        *timestamps(),
    )


def upgrade() -> None:
    """Upgrade db."""
    create_user_table()
    create_leetcode_update_table()


def downgrade() -> None:
    """Downgrade db."""
    op.drop_table("users")
    op.drop_table("leetcode_update")
