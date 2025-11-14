"""create interview_answers table

Revision ID: create_interview_answers
Revises: add_interview_interviewers
Create Date: 2025-01-28 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'create_interview_answers'
down_revision: Union[str, Sequence[str], None] = 'add_interview_interviewers'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Create interview_answers table
    # Check that interviews table exists first
    if 'interviews' not in inspector.get_table_names():
        raise Exception("Cannot create interview_answers table: interviews table does not exist. Please run migration 4072171060a4 first.")
    
    if 'interview_answers' not in inspector.get_table_names():
        op.create_table(
            'interview_answers',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('interview_id', sa.String(), nullable=False),
            sa.Column('question_id', sa.String(), nullable=False),
            sa.Column('question_text', sa.Text(), nullable=True),
            sa.Column('answer_text', sa.Text(), nullable=True),
            sa.Column('score', sa.Float(), nullable=True),
            sa.Column('feedback', sa.Text(), nullable=True),
            sa.Column('answered_at', sa.DateTime(), nullable=True),
            sa.Column('scored_at', sa.DateTime(), nullable=True),
            sa.Column('scored_by', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
            sa.Column('created_by', sa.String(), nullable=True),
            sa.Column('updated_by', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        
        # Create indexes
        op.create_index(
            op.f('ix_interview_answers_id'),
            'interview_answers',
            ['id'],
            unique=False
        )
        
        op.create_index(
            op.f('ix_interview_answers_interview_id'),
            'interview_answers',
            ['interview_id'],
            unique=False
        )
        
        op.create_index(
            op.f('ix_interview_answers_question_id'),
            'interview_answers',
            ['question_id'],
            unique=False
        )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)
    
    if 'interview_answers' in inspector.get_table_names():
        op.drop_index(op.f('ix_interview_answers_question_id'), table_name='interview_answers')
        op.drop_index(op.f('ix_interview_answers_interview_id'), table_name='interview_answers')
        op.drop_index(op.f('ix_interview_answers_id'), table_name='interview_answers')
        op.drop_table('interview_answers')

