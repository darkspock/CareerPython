"""add_preferred_language_to_users

Revision ID: 34e8e57aefb2
Revises: 8ddb25af3529
Create Date: 2025-10-13 18:02:13.563597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34e8e57aefb2'
down_revision: Union[str, Sequence[str], None] = '8ddb25af3529'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add preferred_language column to users table
    op.add_column('users', sa.Column('preferred_language', sa.String(length=5), nullable=False, server_default='es'))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove preferred_language column from users table
    op.drop_column('users', 'preferred_language')
