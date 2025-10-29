"""remove current_phase_id and use only phase_id

Revision ID: 64d439a82754
Revises: da3d71d5621f
Create Date: 2025-10-29 23:52:19.309007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64d439a82754'
down_revision: Union[str, Sequence[str], None] = 'da3d71d5621f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Copy current_phase_id values to phase_id where phase_id is null
    op.execute("""
        UPDATE company_candidates 
        SET phase_id = current_phase_id 
        WHERE current_phase_id IS NOT NULL AND phase_id IS NULL
    """)
    
    # Drop the current_phase_id column and its index
    op.drop_index('ix_company_candidates_current_phase_id', table_name='company_candidates')
    op.drop_column('company_candidates', 'current_phase_id')


def downgrade() -> None:
    """Downgrade schema."""
    # Add current_phase_id column back
    op.add_column('company_candidates', sa.Column('current_phase_id', sa.String(), nullable=True))
    op.create_index('ix_company_candidates_current_phase_id', 'company_candidates', ['current_phase_id'])
    
    # Copy phase_id values to current_phase_id
    op.execute("""
        UPDATE company_candidates 
        SET current_phase_id = phase_id 
        WHERE phase_id IS NOT NULL
    """)
