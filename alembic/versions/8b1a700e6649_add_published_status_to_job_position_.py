"""add_published_status_to_job_position_status_enum

Revision ID: 8b1a700e6649
Revises: add_company_user_company_roles
Create Date: 2025-11-04 07:48:11.001120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b1a700e6649'
down_revision: Union[str, Sequence[str], None] = 'add_company_user_company_roles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add PUBLISHED status to jobpositionstatus enum."""
    # Add published value to the existing enum (lowercase to match Python enum values)
    # Note: PostgreSQL requires this to be done in a transaction and cannot use IF NOT EXISTS
    # We'll use a try-except approach or check if the value exists first
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'published' 
                AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'jobpositionstatus')
            ) THEN
                ALTER TYPE jobpositionstatus ADD VALUE 'published';
            END IF;
        END $$;
    """)


def downgrade() -> None:
    """Downgrade schema - Remove PUBLISHED status from enum."""
    # Note: PostgreSQL doesn't support removing enum values directly
    # This would require recreating the enum without PUBLISHED and updating all references
    # For now, we'll leave it as a no-op since removing enum values is complex
    pass
