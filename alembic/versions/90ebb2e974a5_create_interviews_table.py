"""create_interviews_table

Revision ID: 90ebb2e974a5
Revises: 81472fc7cbd6
Create Date: 2025-10-04 15:07:38.207091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90ebb2e974a5'
down_revision: Union[str, Sequence[str], None] = '81472fc7cbd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create interviews table
    op.create_table(
        'interviews',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('candidate_id', sa.String(), nullable=False),
        sa.Column('job_position_id', sa.String(), nullable=True),
        sa.Column('interview_template_id', sa.String(), nullable=True),
        sa.Column('interview_type', sa.Enum('JOB_POSITION', 'EXTENDED_PROFILE', name='interviewtypeenum'), nullable=False),
        sa.Column('status', sa.Enum('DRAFT', 'SCHEDULED', 'IN_PROGRESS', 'PAUSED', 'COMPLETED', 'CANCELLED', 'NO_SHOW', name='interviewstatusenum'), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('scheduled_at', sa.DateTime(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('interviewers', sa.JSON(), nullable=True),
        sa.Column('interviewer_notes', sa.Text(), nullable=True),
        sa.Column('candidate_notes', sa.Text(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('free_answers', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better query performance
    op.create_index('ix_interviews_candidate_id', 'interviews', ['candidate_id'])
    op.create_index('ix_interviews_job_position_id', 'interviews', ['job_position_id'])
    op.create_index('ix_interviews_status', 'interviews', ['status'])
    op.create_index('ix_interviews_interview_type', 'interviews', ['interview_type'])
    op.create_index('ix_interviews_scheduled_at', 'interviews', ['scheduled_at'])
    op.create_index('ix_interviews_created_at', 'interviews', ['created_at'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('ix_interviews_created_at', 'interviews')
    op.drop_index('ix_interviews_scheduled_at', 'interviews')
    op.drop_index('ix_interviews_interview_type', 'interviews')
    op.drop_index('ix_interviews_status', 'interviews')
    op.drop_index('ix_interviews_job_position_id', 'interviews')
    op.drop_index('ix_interviews_candidate_id', 'interviews')

    # Drop table
    op.drop_table('interviews')

    # Drop enums
    op.execute("DROP TYPE IF EXISTS interviewstatusenum")
    op.execute("DROP TYPE IF EXISTS interviewtypeenum")
