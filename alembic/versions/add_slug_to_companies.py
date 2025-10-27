"""add_slug_to_companies

Revision ID: add_slug_to_companies
Revises: 4bbde09b6dee
Create Date: 2025-10-27 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_slug_to_companies'
down_revision: Union[str, None] = '4bbde09b6dee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add slug column to companies table"""
    # Add slug column as nullable first
    op.add_column('companies', sa.Column('slug', sa.String(length=255), nullable=True))

    # Generate slugs for existing companies from their names
    op.execute("""
        UPDATE companies
        SET slug = LOWER(REGEXP_REPLACE(REGEXP_REPLACE(name, '[^a-zA-Z0-9\\s-]', '', 'g'), '\\s+', '-', 'g'))
        WHERE slug IS NULL
    """)

    # Make slug unique
    op.create_unique_constraint('uq_companies_slug', 'companies', ['slug'])

    # Create index for faster lookups
    op.create_index('ix_companies_slug', 'companies', ['slug'])


def downgrade() -> None:
    """Remove slug column from companies table"""
    op.drop_index('ix_companies_slug', table_name='companies')
    op.drop_constraint('uq_companies_slug', 'companies', type_='unique')
    op.drop_column('companies', 'slug')
