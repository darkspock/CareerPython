"""Create interview sessions table

Revision ID: create_interview_sessions
Revises: add_template_versioning
Create Date: 2025-01-20 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_interview_sessions'
down_revision = 'add_template_versioning'
branch_labels = None
depends_on = None


def upgrade():
    """Create interview sessions table"""
    op.create_table('interview_sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('interview_type', sa.String(), nullable=False),
        sa.Column('current_phase', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('template_id', sa.String(), nullable=False),
        sa.Column('questions_data', sa.JSON(), nullable=True),
        sa.Column('responses_data', sa.JSON(), nullable=True),
        sa.Column('progress_percentage', sa.Float(), nullable=False),
        sa.Column('estimated_completion_time', sa.DateTime(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for performance
    op.create_index('idx_interview_sessions_user_id', 'interview_sessions', ['user_id'])
    op.create_index('idx_interview_sessions_status', 'interview_sessions', ['status'])
    op.create_index('idx_interview_sessions_template_id', 'interview_sessions', ['template_id'])
    op.create_index('idx_interview_sessions_started_at', 'interview_sessions', ['started_at'])
    op.create_index('idx_interview_sessions_user_status', 'interview_sessions', ['user_id', 'status'])


def downgrade():
    """Drop interview sessions table"""
    op.drop_index('idx_interview_sessions_user_status', table_name='interview_sessions')
    op.drop_index('idx_interview_sessions_started_at', table_name='interview_sessions')
    op.drop_index('idx_interview_sessions_template_id', table_name='interview_sessions')
    op.drop_index('idx_interview_sessions_status', table_name='interview_sessions')
    op.drop_index('idx_interview_sessions_user_id', table_name='interview_sessions')
    op.drop_table('interview_sessions')