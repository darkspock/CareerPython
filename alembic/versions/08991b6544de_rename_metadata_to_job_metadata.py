"""rename metadata to job_metadata

Revision ID: 08991b6544de
Revises: 897fbc25edac
Create Date: 2025-10-14 20:51:10.668964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08991b6544de'
down_revision: Union[str, Sequence[str], None] = '897fbc25edac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename metadata column to job_metadata to avoid SQLAlchemy conflicts
    op.alter_column('async_jobs', 'metadata', new_column_name='job_metadata')


def downgrade() -> None:
    """Downgrade schema."""
    # Rename job_metadata column back to metadata
    op.alter_column('async_jobs', 'job_metadata', new_column_name='metadata')
