"""Add hashed_password to users

Revision ID: 480b17f97f02
Revises: 879c2c21ff31
Create Date: 2025-11-05 10:22:53.552176

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

_LEGACY_PASSWORD_PLACEHOLDER = "legacy-password-reset-required"


# revision identifiers, used by Alembic.
revision: str = '480b17f97f02'
down_revision: Union[str, None] = '879c2c21ff31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the hashed_password column and backfill existing rows."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("hashed_password", sa.String(length=255), nullable=True)
        )

    op.execute(
        sa.text(
            "UPDATE users SET hashed_password = :placeholder "
            "WHERE hashed_password IS NULL"
        ).bindparams(placeholder=_LEGACY_PASSWORD_PLACEHOLDER)
    )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "hashed_password",
            existing_type=sa.String(length=255),
            nullable=False,
        )


def downgrade() -> None:
    """Remove the hashed_password column."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("hashed_password")
