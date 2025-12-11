"""add_candidate_application_workflow_id_to_job_positions

Revision ID: 9a9b358849b9
Revises: bd1f13e202d6
Create Date: 2025-12-11 18:32:24.137515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9a9b358849b9'
down_revision: Union[str, Sequence[str], None] = 'bd1f13e202d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add candidate_application_workflow_id column to job_positions table."""
    op.add_column('job_positions', sa.Column('candidate_application_workflow_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_job_positions_candidate_application_workflow_id'), 'job_positions', ['candidate_application_workflow_id'], unique=False)


def downgrade() -> None:
    """Remove candidate_application_workflow_id column from job_positions table."""
    op.drop_index(op.f('ix_job_positions_candidate_application_workflow_id'), table_name='job_positions')
    op.drop_column('job_positions', 'candidate_application_workflow_id')
