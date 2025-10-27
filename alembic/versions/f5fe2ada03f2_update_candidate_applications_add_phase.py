"""update_candidate_applications_add_phase

Revision ID: f5fe2ada03f2
Revises: dc0860c5ff5a
Create Date: 2025-10-27 07:25:02.014675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5fe2ada03f2'
down_revision: Union[str, Sequence[str], None] = 'dc0860c5ff5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add phase_id column to candidate_applications table (company_candidates)
    op.add_column('company_candidates', sa.Column('phase_id', sa.String(), nullable=True))
    op.create_foreign_key('fk_company_candidates_phase_id', 'company_candidates', 'company_phases', ['phase_id'], ['id'])
    op.create_index('ix_company_candidates_phase_id', 'company_candidates', ['phase_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop phase_id column
    op.drop_index('ix_company_candidates_phase_id', table_name='company_candidates')
    op.drop_constraint('fk_company_candidates_phase_id', 'company_candidates', type_='foreignkey')
    op.drop_column('company_candidates', 'phase_id')
