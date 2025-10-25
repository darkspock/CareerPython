"""replace_required_outcome_with_allow_skip

Revision ID: 01c58d14cc89
Revises: d0e9ca4a73b2
Create Date: 2025-10-25 23:13:13.311348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01c58d14cc89'
down_revision: Union[str, Sequence[str], None] = 'd0e9ca4a73b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Replace required_outcome column with allow_skip boolean."""
    # Add new allow_skip column (default False = stage is required)
    op.add_column('workflow_stages', sa.Column('allow_skip', sa.Boolean(), nullable=False, server_default='false'))

    # Drop old required_outcome column
    op.drop_column('workflow_stages', 'required_outcome')


def downgrade() -> None:
    """Restore required_outcome column, remove allow_skip."""
    # Add back required_outcome column
    op.add_column('workflow_stages', sa.Column('required_outcome', sa.String(length=20), nullable=True))

    # Drop allow_skip column
    op.drop_column('workflow_stages', 'allow_skip')
