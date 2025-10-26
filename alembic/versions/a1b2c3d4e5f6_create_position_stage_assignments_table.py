"""create_position_stage_assignments_table

Revision ID: a1b2c3d4e5f6
Revises: c4d9a3e8b6f2
Create Date: 2025-10-26 19:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'c4d9a3e8b6f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create position_stage_assignments table
    op.create_table(
        'position_stage_assignments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('position_id', sa.String(), nullable=False),
        sa.Column('stage_id', sa.String(), nullable=False),
        sa.Column('assigned_user_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['position_id'], ['job_positions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['stage_id'], ['workflow_stages.id'], ondelete='CASCADE')
    )

    # Create indexes for faster lookups
    op.create_index(op.f('ix_position_stage_assignments_position_id'), 'position_stage_assignments', ['position_id'], unique=False)
    op.create_index(op.f('ix_position_stage_assignments_stage_id'), 'position_stage_assignments', ['stage_id'], unique=False)

    # Create unique constraint for position_id + stage_id combination
    op.create_index('uq_position_stage_assignments_position_stage', 'position_stage_assignments', ['position_id', 'stage_id'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('uq_position_stage_assignments_position_stage', table_name='position_stage_assignments')
    op.drop_index(op.f('ix_position_stage_assignments_stage_id'), table_name='position_stage_assignments')
    op.drop_index(op.f('ix_position_stage_assignments_position_id'), table_name='position_stage_assignments')

    # Drop table
    op.drop_table('position_stage_assignments')
