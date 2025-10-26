"""add_workflow_id_to_job_positions

Revision ID: c4d9a3e8b6f2
Revises: b9c3d8e4f7a1
Create Date: 2025-10-26 18:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4d9a3e8b6f2'
down_revision: Union[str, None] = 'b9c3d8e4f7a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add workflow_id column to job_positions
    op.add_column('job_positions', sa.Column('workflow_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_job_positions_workflow_id'), 'job_positions', ['workflow_id'], unique=False)


def downgrade() -> None:
    # Remove workflow_id column from job_positions
    op.drop_index(op.f('ix_job_positions_workflow_id'), table_name='job_positions')
    op.drop_column('job_positions', 'workflow_id')
