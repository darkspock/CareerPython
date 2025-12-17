"""add_wants_cv_help_to_user_registrations

Revision ID: 5777g76c441b
Revises: 4666f65b330a
Create Date: 2025-12-17 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5777g76c441b'
down_revision: Union[str, Sequence[str], None] = '4666f65b330a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user_registrations', sa.Column('wants_cv_help', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_registrations', 'wants_cv_help')
