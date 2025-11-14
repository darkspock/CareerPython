"""add scoring_mode to interview_templates and link fields to interviews

Revision ID: add_scoring_links
Revises: c4a23a09ff70
Create Date: 2025-01-28 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'add_scoring_links'
down_revision: Union[str, Sequence[str], None] = 'c4a23a09ff70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Add scoring_mode to interview_templates
    if 'interview_templates' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('interview_templates')]
        
        if 'scoring_mode' not in columns:
            # Create enum type for ScoringModeEnum
            op.execute("""
                CREATE TYPE scoringmodeenum AS ENUM ('DISTANCE', 'ABSOLUTE')
            """)
            
            # Add scoring_mode column
            op.add_column(
                'interview_templates',
                sa.Column('scoring_mode', sa.Enum('DISTANCE', 'ABSOLUTE', name='scoringmodeenum', native_enum=False, length=20), nullable=True)
            )
            
            # Create index for better query performance
            op.create_index(
                op.f('ix_interview_templates_scoring_mode'),
                'interview_templates',
                ['scoring_mode'],
                unique=False
            )
    
    # Add link_token and link_expires_at to interviews
    if 'interviews' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('interviews')]
        
        if 'link_token' not in columns:
            # Add link_token column
            op.add_column(
                'interviews',
                sa.Column('link_token', sa.String(), nullable=True)
            )
            
            # Create index for link_token (for fast lookups)
            op.create_index(
                op.f('ix_interviews_link_token'),
                'interviews',
                ['link_token'],
                unique=False
            )
        
        if 'link_expires_at' not in columns:
            # Add link_expires_at column
            op.add_column(
                'interviews',
                sa.Column('link_expires_at', sa.DateTime(), nullable=True)
            )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Remove link fields from interviews
    if 'interviews' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('interviews')]
        
        if 'link_expires_at' in columns:
            op.drop_column('interviews', 'link_expires_at')
        
        if 'link_token' in columns:
            op.drop_index(op.f('ix_interviews_link_token'), table_name='interviews')
            op.drop_column('interviews', 'link_token')
    
    # Remove scoring_mode from interview_templates
    if 'interview_templates' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('interview_templates')]
        
        if 'scoring_mode' in columns:
            op.drop_index(op.f('ix_interview_templates_scoring_mode'), table_name='interview_templates')
            op.drop_column('interview_templates', 'scoring_mode')
            
            # Drop enum type
            op.execute("DROP TYPE IF EXISTS scoringmodeenum")

