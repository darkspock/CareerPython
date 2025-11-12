"""add interview_interviewers table

Revision ID: add_interview_interviewers
Revises: add_interview_mode
Create Date: 2025-01-28 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'add_interview_interviewers'
down_revision: Union[str, Sequence[str], None] = 'add_interview_mode'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Create interview_interviewers table
    if 'interview_interviewers' not in inspector.get_table_names():
        op.create_table(
            'interview_interviewers',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('interview_id', sa.String(), nullable=False),
            sa.Column('user_id', sa.String(), nullable=False),
            sa.Column('name', sa.String(), nullable=True),
            sa.Column('is_external', sa.Boolean(), nullable=False, server_default='false'),
            sa.Column('invited_at', sa.DateTime(), nullable=True),
            sa.Column('accepted_at', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column('created_by', sa.String(), nullable=True),
            sa.Column('updated_by', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        
        # Create indexes
        op.create_index(
            op.f('ix_interview_interviewers_id'),
            'interview_interviewers',
            ['id'],
            unique=False
        )
        
        op.create_index(
            op.f('ix_interview_interviewers_interview_id'),
            'interview_interviewers',
            ['interview_id'],
            unique=False
        )
        
        op.create_index(
            op.f('ix_interview_interviewers_user_id'),
            'interview_interviewers',
            ['user_id'],
            unique=False
        )
        
        # Create unique constraint for interview_id + user_id
        op.create_unique_constraint(
            'uq_interview_interviewer',
            'interview_interviewers',
            ['interview_id', 'user_id']
        )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Remove interview_interviewers table
    if 'interview_interviewers' in inspector.get_table_names():
        op.drop_constraint('uq_interview_interviewer', 'interview_interviewers', type_='unique')
        op.drop_index(op.f('ix_interview_interviewers_user_id'), table_name='interview_interviewers')
        op.drop_index(op.f('ix_interview_interviewers_interview_id'), table_name='interview_interviewers')
        op.drop_index(op.f('ix_interview_interviewers_id'), table_name='interview_interviewers')
        op.drop_table('interview_interviewers')

