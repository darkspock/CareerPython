"""add_timestamps_to_candidates_table

Revision ID: 41bbef1a6bc6
Revises: 84909f5f7d72
Create Date: 2025-09-20 08:36:02.236638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41bbef1a6bc6'
down_revision: Union[str, Sequence[str], None] = '84909f5f7d72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add created_at and updated_at columns to candidates table
    op.add_column('candidates', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('candidates', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Set default values for existing records
    op.execute("UPDATE candidates SET created_at = NOW(), updated_at = NOW() WHERE created_at IS NULL")
    
    # Make columns non-nullable after setting default values
    op.alter_column('candidates', 'created_at', nullable=False)
    op.alter_column('candidates', 'updated_at', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove created_at and updated_at columns from candidates table
    op.drop_column('candidates', 'updated_at')
    op.drop_column('candidates', 'created_at')
