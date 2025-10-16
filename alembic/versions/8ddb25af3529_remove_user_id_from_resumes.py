"""remove_user_id_from_resumes

Revision ID: 8ddb25af3529
Revises: 0822302c5334
Create Date: 2025-10-13 10:35:09.653260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ddb25af3529'
down_revision: Union[str, Sequence[str], None] = '0822302c5334'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove user_id column from resumes table as it's redundant with candidate_id."""
    # Drop indexes that reference user_id
    op.drop_index('idx_resume_user_type', table_name='resumes')
    op.drop_index('ix_resumes_user_id', table_name='resumes')

    # Drop user_id column
    op.drop_column('resumes', 'user_id')


def downgrade() -> None:
    """Add back user_id column to resumes table."""
    # Add user_id column back
    op.add_column('resumes', sa.Column('user_id', sa.String(), nullable=False))

    # Recreate indexes
    op.create_index('ix_resumes_user_id', 'resumes', ['user_id'], unique=False)
    op.create_index('idx_resume_user_type', 'resumes', ['user_id', 'resume_type'], unique=False)
