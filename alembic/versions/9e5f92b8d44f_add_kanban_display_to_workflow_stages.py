"""add kanban_display to workflow_stages

Revision ID: 9e5f92b8d44f
Revises: f3dae2005c88
Create Date: 2025-10-29 15:58:45.494682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e5f92b8d44f'
down_revision: Union[str, Sequence[str], None] = 'f3dae2005c88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add kanban_display column to workflow_stages table
    op.add_column('workflow_stages', 
                  sa.Column('kanban_display', sa.String(10), nullable=False, server_default='column'))
    
    # Add check constraint
    op.create_check_constraint(
        'ck_workflow_stages_kanban_display',
        'workflow_stages',
        "kanban_display IN ('column', 'row', 'none')"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove check constraint
    op.drop_constraint('ck_workflow_stages_kanban_display', 'workflow_stages', type_='check')
    
    # Remove kanban_display column
    op.drop_column('workflow_stages', 'kanban_display')
