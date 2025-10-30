"""add candidate comments table

Revision ID: 3bf4ac14a74a
Revises: ed932e5360d5
Create Date: 2025-10-30 23:13:05.566953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bf4ac14a74a'
down_revision: Union[str, Sequence[str], None] = 'ed932e5360d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Create candidate_comments table."""
    # Create enum types if they don't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'commentreviewstatus') THEN
                CREATE TYPE commentreviewstatus AS ENUM ('reviewed', 'pending');
            END IF;
            
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'commentvisibility') THEN
                CREATE TYPE commentvisibility AS ENUM ('private', 'shared_with_candidate');
            END IF;
        END $$;
    """)
    
    # Create candidate_comments table
    op.create_table(
        'candidate_comments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_candidate_id', sa.String(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=True),
        sa.Column('stage_id', sa.String(), nullable=True),
        sa.Column('created_by_user_id', sa.String(), nullable=False),
        sa.Column('review_status', sa.Enum('reviewed', 'pending', name='commentreviewstatus', native_enum=False, length=20), nullable=False, server_default='reviewed'),
        sa.Column('visibility', sa.Enum('private', 'shared_with_candidate', name='commentvisibility', native_enum=False, length=30), nullable=False, server_default='private'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_candidate_id'], ['company_candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workflow_id'], ['company_workflows.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['stage_id'], ['workflow_stages.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['company_users.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_candidate_comments_company_candidate_id', 'candidate_comments', ['company_candidate_id'])
    op.create_index('ix_candidate_comments_workflow_id', 'candidate_comments', ['workflow_id'])
    op.create_index('ix_candidate_comments_stage_id', 'candidate_comments', ['stage_id'])
    op.create_index('ix_candidate_comments_created_by_user_id', 'candidate_comments', ['created_by_user_id'])
    op.create_index('ix_candidate_comments_review_status', 'candidate_comments', ['review_status'])


def downgrade() -> None:
    """Downgrade schema - Drop candidate_comments table."""
    op.drop_index('ix_candidate_comments_review_status', table_name='candidate_comments')
    op.drop_index('ix_candidate_comments_created_by_user_id', table_name='candidate_comments')
    op.drop_index('ix_candidate_comments_stage_id', table_name='candidate_comments')
    op.drop_index('ix_candidate_comments_workflow_id', table_name='candidate_comments')
    op.drop_index('ix_candidate_comments_company_candidate_id', table_name='candidate_comments')
    op.drop_table('candidate_comments')
    op.execute("DROP TYPE IF EXISTS commentreviewstatus")
    op.execute("DROP TYPE IF EXISTS commentvisibility")
