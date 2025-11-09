"""add job_position_stages table

Revision ID: 31a03ac9bc19
Revises: 33aae23e0ca8
Create Date: 2025-11-08 08:38:52.667685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31a03ac9bc19'
down_revision: Union[str, Sequence[str], None] = '33aae23e0ca8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('job_position_stages',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('job_position_id', sa.String(length=26), nullable=False),
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
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['job_position_id'], ['job_positions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['phase_id'], ['company_phases.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['stage_id'], ['workflow_stages.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_position_stages_id'), 'job_position_stages', ['id'], unique=False)
    op.create_index(op.f('ix_job_position_stages_job_position_id'), 'job_position_stages', ['job_position_id'], unique=False)
    op.create_index(op.f('ix_job_position_stages_stage_id'), 'job_position_stages', ['stage_id'], unique=False)
    op.create_index(op.f('ix_job_position_stages_started_at'), 'job_position_stages', ['started_at'], unique=False)
    op.create_index(op.f('ix_job_position_stages_completed_at'), 'job_position_stages', ['completed_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_job_position_stages_completed_at'), table_name='job_position_stages')
    op.drop_index(op.f('ix_job_position_stages_started_at'), table_name='job_position_stages')
    op.drop_index(op.f('ix_job_position_stages_stage_id'), table_name='job_position_stages')
    op.drop_index(op.f('ix_job_position_stages_job_position_id'), table_name='job_position_stages')
    op.drop_index(op.f('ix_job_position_stages_id'), table_name='job_position_stages')
    op.drop_table('job_position_stages')
