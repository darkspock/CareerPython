"""create_company_phases_table

Revision ID: c53639724872
Revises: 8ee6c519e370
Create Date: 2025-10-27 07:23:54.700479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c53639724872'
down_revision: Union[str, Sequence[str], None] = '2da4467310a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enum for default_view (only if it doesn't exist)
    op.execute("DO $$ BEGIN CREATE TYPE defaultview AS ENUM ('KANBAN', 'LIST'); EXCEPTION WHEN duplicate_object THEN null; END $$;")

    # Create company_phases table manually
    op.execute("""
        CREATE TABLE company_phases (
            id VARCHAR NOT NULL PRIMARY KEY,
            company_id VARCHAR NOT NULL,
            name VARCHAR(100) NOT NULL,
            sort_order INTEGER NOT NULL,
            default_view defaultview NOT NULL,
            objective TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT now(),
            updated_at TIMESTAMP NOT NULL DEFAULT now()
        )
    """)

    # Create indexes
    op.create_index('ix_company_phases_company_id', 'company_phases', ['company_id'])
    op.create_index('ix_company_phases_sort_order', 'company_phases', ['sort_order'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('ix_company_phases_sort_order', table_name='company_phases')
    op.drop_index('ix_company_phases_company_id', table_name='company_phases')

    # Drop table
    op.drop_table('company_phases')

    # Drop enum
    op.execute("DROP TYPE defaultview")
