"""create interviews table

Revision ID: 4072171060a4
Revises: 2308dbde877e
Create Date: 2025-11-12 22:40:59.114940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text
import psycopg2


# revision identifiers, used by Alembic.
revision: str = '4072171060a4'
down_revision: Union[str, Sequence[str], None] = '2308dbde877e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Create interviews table if it doesn't exist
    if 'interviews' not in inspector.get_table_names():
        # Use existing enum types or create if they don't exist
        # Note: Enums may already exist from previous migrations
        result = conn.execute(text("SELECT COUNT(*) FROM pg_type WHERE typname = 'interviewstatusenum'")).scalar()
        if result == 0:
            # Try to create, but ignore if it already exists
            conn.execute(text("""
                DO $$ 
                BEGIN
                    CREATE TYPE interviewstatusenum AS ENUM ('ENABLED', 'DISABLED', 'SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED');
                EXCEPTION 
                    WHEN duplicate_object THEN NULL;
                END $$;
            """))
        
        # Check if interviewtypeenum exists, if not create it
        # Note: Enum may already exist from a previous migration attempt
        result = conn.execute(text("SELECT COUNT(*) FROM pg_type WHERE typname = 'interviewtypeenum'")).scalar()
        if result == 0:
            # Try to create, but ignore if it already exists
            conn.execute(text("""
                DO $$ 
                BEGIN
                    CREATE TYPE interviewtypeenum AS ENUM ('EXTENDED_PROFILE', 'POSITION_INTERVIEW', 'TECHNICAL', 'BEHAVIORAL', 'CULTURAL_FIT');
                EXCEPTION 
                    WHEN duplicate_object THEN NULL;
                END $$;
            """))
        
        # Create interviews table with basic columns (columns added in later migrations will be added separately)
        op.create_table(
            'interviews',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('candidate_id', sa.String(), nullable=False),
            sa.Column('job_position_id', sa.String(), nullable=True),
            sa.Column('application_id', sa.String(), nullable=True),
            sa.Column('interview_template_id', sa.String(), nullable=True),
            sa.Column('interview_type', sa.String(), nullable=False, server_default='POSITION_INTERVIEW'),  # Will be converted to enum later
            sa.Column('status', sa.String(), nullable=False, server_default='ENABLED'),  # Will be converted to enum later
            sa.Column('title', sa.String(), nullable=True),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('scheduled_at', sa.DateTime(), nullable=True),
            sa.Column('started_at', sa.DateTime(), nullable=True),
            sa.Column('finished_at', sa.DateTime(), nullable=True),
            sa.Column('duration_minutes', sa.Integer(), nullable=True),
            sa.Column('interviewers', sa.JSON(), nullable=True),  # List of interviewer names
            sa.Column('interviewer_notes', sa.Text(), nullable=True),
            sa.Column('candidate_notes', sa.Text(), nullable=True),
            sa.Column('score', sa.Float(), nullable=True),  # Overall interview score (0-100)
            sa.Column('feedback', sa.Text(), nullable=True),
            sa.Column('free_answers', sa.Text(), nullable=True),  # Free text answers from candidate
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column('created_by', sa.String(), nullable=True),  # User ID who created the interview
            sa.Column('updated_by', sa.String(), nullable=True),  # User ID who last updated the interview
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['application_id'], ['candidate_applications.id'], ondelete='SET NULL')
        )
        
        # Create indexes
        op.create_index(op.f('ix_interviews_id'), 'interviews', ['id'], unique=False)
        op.create_index(op.f('ix_interviews_candidate_id'), 'interviews', ['candidate_id'], unique=False)
        op.create_index(op.f('ix_interviews_job_position_id'), 'interviews', ['job_position_id'], unique=False)
        op.create_index(op.f('ix_interviews_application_id'), 'interviews', ['application_id'], unique=False)
        op.create_index(op.f('ix_interviews_interview_template_id'), 'interviews', ['interview_template_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Remove interviews table if it exists
    if 'interviews' in inspector.get_table_names():
        op.drop_index(op.f('ix_interviews_interview_template_id'), table_name='interviews')
        op.drop_index(op.f('ix_interviews_application_id'), table_name='interviews')
        op.drop_index(op.f('ix_interviews_job_position_id'), table_name='interviews')
        op.drop_index(op.f('ix_interviews_candidate_id'), table_name='interviews')
        op.drop_index(op.f('ix_interviews_id'), table_name='interviews')
        op.drop_table('interviews')
        
        # Drop enum types
        op.execute("DROP TYPE IF EXISTS interviewstatusenum")
        op.execute("DROP TYPE IF EXISTS interviewtypeenum")
