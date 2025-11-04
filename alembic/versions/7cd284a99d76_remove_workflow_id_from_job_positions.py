"""remove_workflow_id_from_job_positions

Revision ID: 7cd284a99d76
Revises: 20f584406868
Create Date: 2025-11-04 22:55:21.234993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cd284a99d76'
down_revision: Union[str, Sequence[str], None] = '20f584406868'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the workflow_id column from job_positions table
    op.drop_index('ix_job_positions_workflow_id', table_name='job_positions', if_exists=True)
    op.drop_column('job_positions', 'workflow_id')


def downgrade() -> None:
    """Downgrade schema."""
    # Restore the workflow_id column (for rollback purposes)
    op.add_column('job_positions', sa.Column('workflow_id', sa.String(), nullable=True))
    op.create_index('ix_job_positions_workflow_id', 'job_positions', ['workflow_id'], unique=False)
