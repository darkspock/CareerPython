"""add interview_mode to interviews

Revision ID: add_interview_mode
Revises: add_scoring_links
Create Date: 2025-01-28 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_interview_mode'
down_revision: Union[str, Sequence[str], None] = 'add_scoring_links'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Add interview_mode column to interviews
    if 'interviews' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('interviews')]
        
        if 'interview_mode' not in columns:
            # Create enum type for InterviewModeEnum
            op.execute("""
                CREATE TYPE interviewmodeenum AS ENUM ('AUTOMATIC', 'AI', 'MANUAL');
            """)
            
            # Add interview_mode column
            op.add_column(
                'interviews',
                sa.Column('interview_mode', postgresql.ENUM('AUTOMATIC', 'AI', 'MANUAL', name='interviewmodeenum', create_type=False), nullable=True)
            )
            
            # Create index on interview_mode
            op.create_index(
                op.f('ix_interviews_interview_mode'),
                'interviews',
                ['interview_mode'],
                unique=False
            )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Remove interview_mode from interviews
    if 'interviews' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('interviews')]
        
        if 'interview_mode' in columns:
            # Drop index
            op.drop_index(op.f('ix_interviews_interview_mode'), table_name='interviews')
            
            # Drop column
            op.drop_column('interviews', 'interview_mode')
            
            # Drop enum type
            op.execute("DROP TYPE IF EXISTS interviewmodeenum")

