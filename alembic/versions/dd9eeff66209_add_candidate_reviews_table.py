"""add candidate_reviews table

Revision ID: dd9eeff66209
Revises: 882f73c4c48b
Create Date: 2025-11-09 11:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dd9eeff66209'
down_revision: Union[str, Sequence[str], None] = '882f73c4c48b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create candidate_reviews table
    op.create_table('candidate_reviews',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('company_candidate_id', sa.String(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('workflow_id', sa.String(), nullable=True),
    sa.Column('stage_id', sa.String(), nullable=True),
    sa.Column('review_status', sa.String(), nullable=False),
    sa.Column('created_by_user_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['company_candidate_id'], ['company_candidates.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['stage_id'], ['workflow_stages.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['created_by_user_id'], ['company_users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidate_reviews_id'), 'candidate_reviews', ['id'], unique=False)
    op.create_index(op.f('ix_candidate_reviews_company_candidate_id'), 'candidate_reviews', ['company_candidate_id'], unique=False)
    op.create_index(op.f('ix_candidate_reviews_score'), 'candidate_reviews', ['score'], unique=False)
    op.create_index(op.f('ix_candidate_reviews_stage_id'), 'candidate_reviews', ['stage_id'], unique=False)
    op.create_index(op.f('ix_candidate_reviews_workflow_id'), 'candidate_reviews', ['workflow_id'], unique=False)
    op.create_index(op.f('ix_candidate_reviews_review_status'), 'candidate_reviews', ['review_status'], unique=False)
    op.create_index(op.f('ix_candidate_reviews_created_by_user_id'), 'candidate_reviews', ['created_by_user_id'], unique=False)
    # Note: Other detected changes (company_roles, job_position_stages indexes) are not included
    # as they may be part of other refactorings or are false positives


def downgrade() -> None:
    """Downgrade schema."""
    # Drop candidate_reviews table
    op.drop_index(op.f('ix_candidate_reviews_created_by_user_id'), table_name='candidate_reviews')
    op.drop_index(op.f('ix_candidate_reviews_review_status'), table_name='candidate_reviews')
    op.drop_index(op.f('ix_candidate_reviews_workflow_id'), table_name='candidate_reviews')
    op.drop_index(op.f('ix_candidate_reviews_stage_id'), table_name='candidate_reviews')
    op.drop_index(op.f('ix_candidate_reviews_score'), table_name='candidate_reviews')
    op.drop_index(op.f('ix_candidate_reviews_company_candidate_id'), table_name='candidate_reviews')
    op.drop_index(op.f('ix_candidate_reviews_id'), table_name='candidate_reviews')
    op.drop_table('candidate_reviews')
