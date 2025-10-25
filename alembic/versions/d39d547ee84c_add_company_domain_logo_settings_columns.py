"""add company domain logo settings columns

Revision ID: d39d547ee84c
Revises: 77429c29143e
Create Date: 2025-10-24 18:32:54.187694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd39d547ee84c'
down_revision: Union[str, Sequence[str], None] = '77429c29143e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new columns to companies table
    op.add_column('companies', sa.Column('domain', sa.String(), nullable=True))
    op.add_column('companies', sa.Column('logo_url', sa.String(), nullable=True))
    op.add_column('companies', sa.Column('settings', sa.JSON(), nullable=True))

    # Create unique index on domain
    op.create_index(op.f('ix_companies_domain'), 'companies', ['domain'], unique=True)

    # Set default empty dict for settings column for existing rows
    op.execute("UPDATE companies SET settings = '{}' WHERE settings IS NULL")
    op.execute("UPDATE companies SET domain = LOWER(REPLACE(name, ' ', '')) || '.com' WHERE domain IS NULL")

    # Make columns non-nullable after setting defaults
    op.alter_column('companies', 'settings', nullable=False)
    op.alter_column('companies', 'domain', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_companies_domain'), table_name='companies')
    op.drop_column('companies', 'settings')
    op.drop_column('companies', 'logo_url')
    op.drop_column('companies', 'domain')
