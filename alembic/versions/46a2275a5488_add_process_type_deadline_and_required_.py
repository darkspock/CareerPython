"""add_process_type_deadline_and_required_roles_to_interviews

Revision ID: 46a2275a5488
Revises: a1a673c0093e
Create Date: 2025-11-14 12:16:37.967281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '46a2275a5488'
down_revision: Union[str, Sequence[str], None] = 'a1a673c0093e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add process_type column (VARCHAR instead of ENUM to avoid migration issues)
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE interviews ADD COLUMN process_type VARCHAR;
        EXCEPTION
            WHEN duplicate_column THEN null;
        END $$;
    """)
    
    # Create index on process_type
    op.execute("""
        DO $$ BEGIN
            CREATE INDEX ix_interviews_process_type ON interviews(process_type);
        EXCEPTION
            WHEN duplicate_table THEN null;
        END $$;
    """)
    
    # Add deadline_date column
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE interviews ADD COLUMN deadline_date TIMESTAMP;
        EXCEPTION
            WHEN duplicate_column THEN null;
        END $$;
    """)
    
    # Add required_roles column (JSONB for better indexing support)
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE interviews ADD COLUMN required_roles JSONB;
        EXCEPTION
            WHEN duplicate_column THEN null;
        END $$;
    """)
    
    # Create GIN index for required_roles (JSONB supports GIN indexes)
    op.execute("""
        DO $$ BEGIN
            CREATE INDEX ix_interviews_required_roles_gin ON interviews USING GIN (required_roles);
        EXCEPTION
            WHEN duplicate_table THEN null;
        END $$;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove required_roles column
    op.execute("""
        DO $$ BEGIN
            DROP INDEX IF EXISTS ix_interviews_required_roles_gin;
            ALTER TABLE interviews DROP COLUMN IF EXISTS required_roles;
        EXCEPTION
            WHEN undefined_table THEN null;
        END $$;
    """)
    
    # Remove deadline_date column
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE interviews DROP COLUMN IF EXISTS deadline_date;
        EXCEPTION
            WHEN undefined_table THEN null;
        END $$;
    """)
    
    # Remove process_type column
    op.execute("""
        DO $$ BEGIN
            DROP INDEX IF EXISTS ix_interviews_process_type;
            ALTER TABLE interviews DROP COLUMN IF EXISTS process_type;
        EXCEPTION
            WHEN undefined_table THEN null;
        END $$;
    """)
