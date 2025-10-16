"""create_interview_answers_table

Revision ID: ea0148a31532
Revises: 90ebb2e974a5
Create Date: 2025-10-04 15:16:01.143260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea0148a31532'
down_revision: Union[str, Sequence[str], None] = '90ebb2e974a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create interview_answers table
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
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE')
    )

    # Create indexes for better query performance
    op.create_index('ix_interview_answers_interview_id', 'interview_answers', ['interview_id'])
    op.create_index('ix_interview_answers_question_id', 'interview_answers', ['question_id'])
    op.create_index('ix_interview_answers_interview_question', 'interview_answers', ['interview_id', 'question_id'])
    op.create_index('ix_interview_answers_score', 'interview_answers', ['score'])
    op.create_index('ix_interview_answers_answered_at', 'interview_answers', ['answered_at'])
    op.create_index('ix_interview_answers_scored_at', 'interview_answers', ['scored_at'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('ix_interview_answers_scored_at', 'interview_answers')
    op.drop_index('ix_interview_answers_answered_at', 'interview_answers')
    op.drop_index('ix_interview_answers_score', 'interview_answers')
    op.drop_index('ix_interview_answers_interview_question', 'interview_answers')
    op.drop_index('ix_interview_answers_question_id', 'interview_answers')
    op.drop_index('ix_interview_answers_interview_id', 'interview_answers')

    # Drop table
    op.drop_table('interview_answers')
