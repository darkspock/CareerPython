"""fix_published_status_case

Revision ID: 9da74c883e6b
Revises: 8b1a700e6649
Create Date: 2025-11-04 07:59:22.542517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9da74c883e6b'
down_revision: Union[str, Sequence[str], None] = '8b1a700e6649'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Fix published status case - add 'published' (lowercase) to match Python enum values"""
    # Add 'published' in lowercase if it doesn't exist
    # Note: We can't update records in the same transaction due to PostgreSQL's enum restrictions
    # If there are any records with 'PUBLISHED', they will need to be updated separately
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
    """Downgrade - cannot remove enum values easily, so this is a no-op"""
    # Note: PostgreSQL doesn't support removing enum values directly
    # We leave 'published' in the enum
    pass
