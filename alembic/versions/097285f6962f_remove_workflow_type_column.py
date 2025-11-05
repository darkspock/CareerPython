"""remove_workflow_type_column

Revision ID: 097285f6962f
Revises: 7cd284a99d76
Create Date: 2025-11-05 00:04:05.977117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '097285f6962f'
down_revision: Union[str, Sequence[str], None] = '7cd284a99d76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop index if exists
    op.drop_index('ix_job_position_workflows_workflow_type', table_name='job_position_workflows', if_exists=True)
    # Drop column
    op.drop_column('job_position_workflows', 'workflow_type')


def downgrade() -> None:
    """Downgrade schema."""
    # Restore column (for rollback purposes)
    op.add_column('job_position_workflows', sa.Column('workflow_type', sa.String(50), nullable=False, server_default='standard'))
    op.create_index('ix_job_position_workflows_workflow_type', 'job_position_workflows', ['workflow_type'])
