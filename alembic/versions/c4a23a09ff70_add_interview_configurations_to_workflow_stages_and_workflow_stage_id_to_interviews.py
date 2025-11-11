"""add interview_configurations to workflow_stages and workflow_stage_id to interviews

Revision ID: c4a23a09ff70
Revises: 2308dbde877e
Create Date: 2025-01-27 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'c4a23a09ff70'
down_revision: Union[str, Sequence[str], None] = '2308dbde877e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add interview_configurations column to workflow_stages table (JSON field)
    op.add_column(
        'workflow_stages',
        sa.Column('interview_configurations', postgresql.JSON(astext_type=sa.Text()), nullable=True)
    )
    
    # Check if interviews table exists before adding column
    conn = op.get_bind()
    inspector = inspect(conn)
    tables = inspector.get_table_names()
    
    if 'interviews' in tables:
        # Check if workflow_stage_id column already exists
        columns = [col['name'] for col in inspector.get_columns('interviews')]
        
        if 'workflow_stage_id' not in columns:
            # Add workflow_stage_id column to interviews table
            op.add_column(
                'interviews',
                sa.Column('workflow_stage_id', sa.String(), nullable=True)
            )
            
            # Add foreign key constraint from interviews.workflow_stage_id to workflow_stages.id
            op.create_foreign_key(
                'fk_interviews_workflow_stage_id',
                'interviews',
                'workflow_stages',
                ['workflow_stage_id'],
                ['id'],
                ondelete='SET NULL'
            )
            
            # Add index for better query performance
            op.create_index(
                op.f('ix_interviews_workflow_stage_id'),
                'interviews',
                ['workflow_stage_id'],
                unique=False
            )


def downgrade() -> None:
    """Downgrade schema."""
    # Check if interviews table exists before dropping column
    conn = op.get_bind()
    inspector = inspect(conn)
    tables = inspector.get_table_names()
    
    if 'interviews' in tables:
        # Check if workflow_stage_id column exists
        columns = [col['name'] for col in inspector.get_columns('interviews')]
        
        if 'workflow_stage_id' in columns:
            # Drop index
            op.drop_index(op.f('ix_interviews_workflow_stage_id'), table_name='interviews')
            
            # Drop foreign key constraint
            op.drop_constraint('fk_interviews_workflow_stage_id', 'interviews', type_='foreignkey')
            
            # Drop column
            op.drop_column('interviews', 'workflow_stage_id')
    
    # Drop column from workflow_stages
    op.drop_column('workflow_stages', 'interview_configurations')

