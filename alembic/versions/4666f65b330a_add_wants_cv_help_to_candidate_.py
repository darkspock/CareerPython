"""add_wants_cv_help_to_candidate_applications

Revision ID: 4666f65b330a
Revises: 24b242ac4e92
Create Date: 2025-12-17 08:54:50.712464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4666f65b330a'
down_revision: Union[str, Sequence[str], None] = '24b242ac4e92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('candidate_applications', sa.Column('wants_cv_help', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('candidate_applications', 'wants_cv_help')
