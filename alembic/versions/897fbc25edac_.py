"""create async jobs table

Revision ID: 897fbc25edac
Revises: 34e8e57aefb2
Create Date: 2025-10-14 05:49:49.173666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '897fbc25edac'
down_revision: Union[str, Sequence[str], None] = '34e8e57aefb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create async_jobs table for generic async job tracking
    op.create_table(
        'async_jobs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('job_type', sa.String(50), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=True),
        sa.Column('entity_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('completed_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('results', postgresql.JSON(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('job_metadata', postgresql.JSON(), nullable=True),
        sa.Column('timeout_seconds', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for efficient queries
    op.create_index('idx_async_jobs_type_entity', 'async_jobs', ['job_type', 'entity_type', 'entity_id'])
    op.create_index('idx_async_jobs_status', 'async_jobs', ['status'])
    op.create_index('idx_async_jobs_created_at', 'async_jobs', ['created_at'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes first
    op.drop_index('idx_async_jobs_created_at', table_name='async_jobs')
    op.drop_index('idx_async_jobs_status', table_name='async_jobs')
    op.drop_index('idx_async_jobs_type_entity', table_name='async_jobs')

    # Drop table
    op.drop_table('async_jobs')