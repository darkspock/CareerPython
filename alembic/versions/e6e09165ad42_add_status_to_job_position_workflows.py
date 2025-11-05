"""add status to job_position_workflows

Revision ID: e6e09165ad42
Revises: 751125998941
Create Date: 2025-11-05 23:36:39.228618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e6e09165ad42'
down_revision: Union[str, Sequence[str], None] = '751125998941'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add status to job_position_workflows."""
    # Add status column with default value
    op.add_column(
        'job_position_workflows',
        sa.Column(
            'status',
            sa.String(length=20),
            nullable=False,
            server_default='published'
        )
    )
    
    # Create index on status
    op.create_index(
        op.f('ix_job_position_workflows_status'),
        'job_position_workflows',
        ['status'],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema - remove status from job_position_workflows."""
    # Drop index
    op.drop_index(
        op.f('ix_job_position_workflows_status'),
        table_name='job_position_workflows'
    )
    
    # Drop column
    op.drop_column('job_position_workflows', 'status')
