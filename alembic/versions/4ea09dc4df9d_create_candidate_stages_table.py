"""create_candidate_stages_table

Revision ID: 4ea09dc4df9d
Revises: 9041203a0081
Create Date: 2025-10-27 10:12:06.006034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ea09dc4df9d'
down_revision: Union[str, Sequence[str], None] = '9041203a0081'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Phase 12: Create candidate_stages table."""
    op.create_table(
        'candidate_stages',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('candidate_application_id', sa.String(length=26), nullable=False),
        sa.Column('phase_id', sa.String(length=26), nullable=True),
        sa.Column('workflow_id', sa.String(length=26), nullable=True),
        sa.Column('stage_id', sa.String(length=26), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('estimated_cost', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('actual_cost', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['candidate_application_id'], ['candidate_applications.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['phase_id'], ['company_phases.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['workflow_id'], ['candidate_application_workflows.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['stage_id'], ['workflow_stages.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_candidate_stages_candidate_application_id', 'candidate_stages', ['candidate_application_id'])
    op.create_index('ix_candidate_stages_phase_id', 'candidate_stages', ['phase_id'])
    op.create_index('ix_candidate_stages_workflow_id', 'candidate_stages', ['workflow_id'])
    op.create_index('ix_candidate_stages_stage_id', 'candidate_stages', ['stage_id'])


def downgrade() -> None:
    """Downgrade schema - Phase 12: Drop candidate_stages table."""
    op.drop_index('ix_candidate_stages_stage_id', table_name='candidate_stages')
    op.drop_index('ix_candidate_stages_workflow_id', table_name='candidate_stages')
    op.drop_index('ix_candidate_stages_phase_id', table_name='candidate_stages')
    op.drop_index('ix_candidate_stages_candidate_application_id', table_name='candidate_stages')
    op.drop_table('candidate_stages')
