"""add_candidate_public_access

Revision ID: 2da4467310a8
Revises: 0d2a9b2ffc93
Create Date: 2025-10-26 23:46:11.998425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2da4467310a8'
down_revision: Union[str, Sequence[str], None] = '0d2a9b2ffc93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add is_public column to job_positions
    op.add_column('job_positions', sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'))

    # Add public_slug column to job_positions
    op.add_column('job_positions', sa.Column('public_slug', sa.String(length=255), nullable=True))

    # Create index for public_slug for faster lookups
    op.create_index('ix_job_positions_public_slug', 'job_positions', ['public_slug'], unique=True)

    # Create index for is_public for faster filtering
    op.create_index('ix_job_positions_is_public', 'job_positions', ['is_public'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('ix_job_positions_is_public', table_name='job_positions')
    op.drop_index('ix_job_positions_public_slug', table_name='job_positions')

    # Drop columns
    op.drop_column('job_positions', 'public_slug')
    op.drop_column('job_positions', 'is_public')
