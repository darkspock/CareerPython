"""add_created_at_to_users

Revision ID: 227aa7de74e5
Revises: 2e26485278f8
Create Date: 2025-10-08 16:02:57.770125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '227aa7de74e5'
down_revision: Union[str, Sequence[str], None] = '2e26485278f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add created_at column to users table
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove created_at column from users table
    op.drop_column('users', 'created_at')
