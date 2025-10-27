"""add_phase_workflows_to_job_positions

Revision ID: 19324f77c6bf
Revises: 4ea09dc4df9d
Create Date: 2025-10-27 11:05:35.668297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19324f77c6bf'
down_revision: Union[str, Sequence[str], None] = '4ea09dc4df9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Phase 12.8: Add phase_workflows JSON field to job_positions

    This allows positions to configure different workflows for each phase.
    The phase_workflows field stores a mapping of phase_id -> workflow_id.
    We keep workflow_id for backwards compatibility (it represents the default/legacy workflow).
    """
    op.add_column('job_positions', sa.Column('phase_workflows', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema - Phase 12.8: Remove phase_workflows field"""
    op.drop_column('job_positions', 'phase_workflows')
