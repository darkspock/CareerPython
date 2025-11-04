"""add job position workflow tables and remove status column

Revision ID: 46965f28b9c8
Revises: 317a3757e21a
Create Date: 2025-11-04 13:58:19.787186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46965f28b9c8'
down_revision: Union[str, Sequence[str], None] = '317a3757e21a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add job position workflow tables and remove status column"""
    
    # Step 1: Create job_position_workflows table
    op.create_table(
        'job_position_workflows',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('workflow_type', sa.String(length=50), nullable=False),
        sa.Column('default_view', sa.String(length=20), nullable=False, server_default='kanban'),
        sa.Column('stages', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('custom_fields_config', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_job_position_workflows_id'), 'job_position_workflows', ['id'], unique=False)
    op.create_index(op.f('ix_job_position_workflows_company_id'), 'job_position_workflows', ['company_id'], unique=False)
    op.create_index(op.f('ix_job_position_workflows_workflow_type'), 'job_position_workflows', ['workflow_type'], unique=False)
    
    # Step 2: Add new columns to job_positions table
    op.add_column('job_positions', sa.Column('job_position_workflow_id', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('stage_id', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('custom_fields_values', sa.JSON(), nullable=True))
    
    # Create indexes for new columns
    op.create_index(op.f('ix_job_positions_job_position_workflow_id'), 'job_positions', ['job_position_workflow_id'], unique=False)
    op.create_index(op.f('ix_job_positions_stage_id'), 'job_positions', ['stage_id'], unique=False)
    
    # Step 3: Remove status column from job_positions
    # Note: Since the table is empty (as per user confirmation), we can safely drop the column
    op.drop_column('job_positions', 'status')


def downgrade() -> None:
    """Downgrade schema - Restore status column and drop workflow tables"""
    
    # Step 1: Add status column back to job_positions
    op.add_column('job_positions', sa.Column('status', sa.Enum('DRAFT', 'ACTIVE', 'PAUSED', 'CLOSED', 'ARCHIVED', name='jobpositionstatus'), nullable=True, server_default='DRAFT'))
    
    # Step 2: Drop indexes for new columns
    op.drop_index(op.f('ix_job_positions_stage_id'), table_name='job_positions')
    op.drop_index(op.f('ix_job_positions_job_position_workflow_id'), table_name='job_positions')
    
    # Step 3: Remove new columns from job_positions
    op.drop_column('job_positions', 'custom_fields_values')
    op.drop_column('job_positions', 'stage_id')
    op.drop_column('job_positions', 'job_position_workflow_id')
    
    # Step 4: Drop job_position_workflows table
    op.drop_index(op.f('ix_job_position_workflows_workflow_type'), table_name='job_position_workflows')
    op.drop_index(op.f('ix_job_position_workflows_company_id'), table_name='job_position_workflows')
    op.drop_index(op.f('ix_job_position_workflows_id'), table_name='job_position_workflows')
    op.drop_table('job_position_workflows')
