"""add stage tracking to applications

Revision ID: d5e8f4a9b3c7
Revises: a1b2c3d4e5f6
Create Date: 2025-10-26 18:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5e8f4a9b3c7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add workflow stage tracking columns to candidate_applications table
    op.add_column('candidate_applications',
                  sa.Column('current_stage_id', sa.String(), nullable=True))
    op.add_column('candidate_applications',
                  sa.Column('stage_entered_at', sa.DateTime(), nullable=True))
    op.add_column('candidate_applications',
                  sa.Column('stage_deadline', sa.DateTime(), nullable=True))
    op.add_column('candidate_applications',
                  sa.Column('task_status', sa.String(), nullable=False, server_default='pending'))

    # Add foreign key constraint for current_stage_id
    op.create_foreign_key(
        'fk_candidate_applications_current_stage_id',
        'candidate_applications',
        'workflow_stages',
        ['current_stage_id'],
        ['id'],
        ondelete='SET NULL'
    )

    # Add index on current_stage_id for query performance
    op.create_index(
        'ix_candidate_applications_current_stage_id',
        'candidate_applications',
        ['current_stage_id']
    )


def downgrade() -> None:
    # Drop index
    op.drop_index('ix_candidate_applications_current_stage_id', table_name='candidate_applications')

    # Drop foreign key constraint
    op.drop_constraint('fk_candidate_applications_current_stage_id', 'candidate_applications', type_='foreignkey')

    # Drop columns
    op.drop_column('candidate_applications', 'task_status')
    op.drop_column('candidate_applications', 'stage_deadline')
    op.drop_column('candidate_applications', 'stage_entered_at')
    op.drop_column('candidate_applications', 'current_stage_id')
