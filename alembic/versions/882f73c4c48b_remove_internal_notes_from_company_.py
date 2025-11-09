"""remove internal_notes from company_candidates

Revision ID: 882f73c4c48b
Revises: 1056ca1c18fa
Create Date: 2025-11-09 11:20:04.903519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '882f73c4c48b'
down_revision: Union[str, Sequence[str], None] = '1056ca1c18fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove internal_notes column from company_candidates table
    op.drop_column('company_candidates', 'internal_notes')
    # Note: Other detected changes (company_roles, job_position_stages indexes) are not included
    # as they may be part of other refactorings or are false positives


def downgrade() -> None:
    """Downgrade schema."""
    # Add back internal_notes column
    op.add_column('company_candidates', sa.Column('internal_notes', sa.Text(), nullable=False, server_default=''))
