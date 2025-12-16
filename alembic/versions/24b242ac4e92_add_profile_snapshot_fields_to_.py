"""add_profile_snapshot_fields_to_candidate_applications

Revision ID: 24b242ac4e92
Revises: 24c5f229ed37
Create Date: 2025-12-16 20:05:31.425526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '24b242ac4e92'
down_revision: Union[str, Sequence[str], None] = '24c5f229ed37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add profile snapshot fields to candidate_applications table."""
    # Add profile_snapshot_markdown column
    op.add_column('candidate_applications', sa.Column(
        'profile_snapshot_markdown',
        sa.Text(),
        nullable=True
    ))

    # Add profile_snapshot_json column
    op.add_column('candidate_applications', sa.Column(
        'profile_snapshot_json',
        sa.JSON(),
        nullable=True
    ))

    # Add cv_file_id column
    op.add_column('candidate_applications', sa.Column(
        'cv_file_id',
        sa.String(),
        nullable=True
    ))


def downgrade() -> None:
    """Remove profile snapshot fields from candidate_applications table."""
    op.drop_column('candidate_applications', 'cv_file_id')
    op.drop_column('candidate_applications', 'profile_snapshot_json')
    op.drop_column('candidate_applications', 'profile_snapshot_markdown')
