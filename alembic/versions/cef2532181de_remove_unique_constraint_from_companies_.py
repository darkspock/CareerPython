"""remove_unique_constraint_from_companies_domain

Revision ID: cef2532181de
Revises: 493fdfc86996
Create Date: 2025-11-10 18:29:07.346450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cef2532181de'
down_revision: Union[str, Sequence[str], None] = '493fdfc86996'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove unique constraint from companies.domain
    # Drop the unique index
    op.drop_index('ix_companies_domain', table_name='companies')
    # Recreate the index without unique constraint
    op.create_index('ix_companies_domain', 'companies', ['domain'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Restore unique constraint on companies.domain
    # Drop the non-unique index
    op.drop_index('ix_companies_domain', table_name='companies')
    # Recreate the index with unique constraint
    op.create_index('ix_companies_domain', 'companies', ['domain'], unique=True)
