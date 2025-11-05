"""add job_position_comments and activities tables

Revision ID: 50ed4e79550f
Revises: 097285f6962f
Create Date: 2025-01-09 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50ed4e79550f'
down_revision: Union[str, None] = '097285f6962f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create job_position_comments and job_position_activities tables."""
    
    # Create job_position_comments table
    op.create_table(
        'job_position_comments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('job_position_id', sa.String(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=True),
        sa.Column('stage_id', sa.String(), nullable=True),
        sa.Column('created_by_user_id', sa.String(), nullable=False),
        sa.Column('review_status', sa.String(length=20), nullable=False),
        sa.Column('visibility', sa.String(length=30), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['job_position_id'], ['job_positions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workflow_id'], ['job_position_workflows.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['company_users.id'], ondelete='SET NULL'),
    )
    op.create_index(op.f('ix_job_position_comments_id'), 'job_position_comments', ['id'], unique=False)
    op.create_index(op.f('ix_job_position_comments_job_position_id'), 'job_position_comments', ['job_position_id'], unique=False)
    op.create_index(op.f('ix_job_position_comments_workflow_id'), 'job_position_comments', ['workflow_id'], unique=False)
    op.create_index(op.f('ix_job_position_comments_stage_id'), 'job_position_comments', ['stage_id'], unique=False)
    op.create_index(op.f('ix_job_position_comments_created_by_user_id'), 'job_position_comments', ['created_by_user_id'], unique=False)
    op.create_index(op.f('ix_job_position_comments_review_status'), 'job_position_comments', ['review_status'], unique=False)
    
    # Create job_position_activities table
    op.create_table(
        'job_position_activities',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('job_position_id', sa.String(), nullable=False),
        sa.Column('activity_type', sa.String(length=30), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('performed_by_user_id', sa.String(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['job_position_id'], ['job_positions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['performed_by_user_id'], ['company_users.id'], ondelete='SET NULL'),
    )
    op.create_index(op.f('ix_job_position_activities_id'), 'job_position_activities', ['id'], unique=False)
    op.create_index(op.f('ix_job_position_activities_job_position_id'), 'job_position_activities', ['job_position_id'], unique=False)
    op.create_index(op.f('ix_job_position_activities_activity_type'), 'job_position_activities', ['activity_type'], unique=False)
    op.create_index(op.f('ix_job_position_activities_performed_by_user_id'), 'job_position_activities', ['performed_by_user_id'], unique=False)
    op.create_index(op.f('ix_job_position_activities_created_at'), 'job_position_activities', ['created_at'], unique=False)


def downgrade() -> None:
    """Drop job_position_comments and job_position_activities tables."""
    op.drop_index(op.f('ix_job_position_activities_created_at'), table_name='job_position_activities')
    op.drop_index(op.f('ix_job_position_activities_performed_by_user_id'), table_name='job_position_activities')
    op.drop_index(op.f('ix_job_position_activities_activity_type'), table_name='job_position_activities')
    op.drop_index(op.f('ix_job_position_activities_job_position_id'), table_name='job_position_activities')
    op.drop_index(op.f('ix_job_position_activities_id'), table_name='job_position_activities')
    op.drop_table('job_position_activities')
    
    op.drop_index(op.f('ix_job_position_comments_review_status'), table_name='job_position_comments')
    op.drop_index(op.f('ix_job_position_comments_created_by_user_id'), table_name='job_position_comments')
    op.drop_index(op.f('ix_job_position_comments_stage_id'), table_name='job_position_comments')
    op.drop_index(op.f('ix_job_position_comments_workflow_id'), table_name='job_position_comments')
    op.drop_index(op.f('ix_job_position_comments_job_position_id'), table_name='job_position_comments')
    op.drop_index(op.f('ix_job_position_comments_id'), table_name='job_position_comments')
    op.drop_table('job_position_comments')
