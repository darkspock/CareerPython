"""add application_question_answers table

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2025-12-07 19:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create application_question_answers table
    op.create_table(
        'application_question_answers',
        sa.Column('id', sa.String(26), primary_key=True),
        sa.Column('application_id', sa.String(26), sa.ForeignKey('candidate_applications.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', sa.String(26), sa.ForeignKey('application_questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('answer_value', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Create indexes
    op.create_index('ix_application_question_answers_application_id', 'application_question_answers', ['application_id'])
    op.create_index('ix_application_question_answers_question_id', 'application_question_answers', ['question_id'])

    # Unique constraint: one answer per question per application
    op.create_index(
        'uq_application_question_answer',
        'application_question_answers',
        ['application_id', 'question_id'],
        unique=True
    )

    # Composite index for efficient lookups
    op.create_index(
        'ix_application_answers_app_question',
        'application_question_answers',
        ['application_id', 'question_id']
    )


def downgrade() -> None:
    op.drop_index('ix_application_answers_app_question', 'application_question_answers')
    op.drop_index('uq_application_question_answer', 'application_question_answers')
    op.drop_index('ix_application_question_answers_question_id', 'application_question_answers')
    op.drop_index('ix_application_question_answers_application_id', 'application_question_answers')
    op.drop_table('application_question_answers')
