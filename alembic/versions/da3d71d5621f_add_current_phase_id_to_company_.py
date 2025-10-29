"""add current_phase_id to company_candidates

Revision ID: da3d71d5621f
Revises: 1fea894de35f
Create Date: 2025-10-29 23:46:20.028161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da3d71d5621f'
down_revision: Union[str, Sequence[str], None] = '1fea894de35f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add current_phase_id column to company_candidates table
    op.add_column('company_candidates', sa.Column('current_phase_id', sa.String(), nullable=True))
    op.create_index('ix_company_candidates_current_phase_id', 'company_candidates', ['current_phase_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove current_phase_id column from company_candidates table
    op.drop_index('ix_company_candidates_current_phase_id', table_name='company_candidates')
    op.drop_column('company_candidates', 'current_phase_id')
