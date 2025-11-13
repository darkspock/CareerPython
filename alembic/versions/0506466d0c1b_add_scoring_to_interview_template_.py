"""add SCORING to interview template question data type enum

Revision ID: 0506466d0c1b
Revises: 76149992e127
Create Date: 2025-11-13 00:58:17.655367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '0506466d0c1b'
down_revision: Union[str, Sequence[str], None] = '76149992e127'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    
    # Add SCORING value to interviewtemplatequestiondatatypeenum
    # PostgreSQL doesn't support IF NOT EXISTS for ALTER TYPE ADD VALUE,
    # so we need to check if the value exists first
    try:
        # Check if SCORING already exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'SCORING' 
                AND enumtypid = (
                    SELECT oid FROM pg_type WHERE typname = 'interviewtemplatequestiondatatypeenum'
                )
            )
        """)).scalar()
        
        if not result:
            conn.execute(text("ALTER TYPE interviewtemplatequestiondatatypeenum ADD VALUE 'SCORING'"))
    except Exception as e:
        # If SCORING already exists or enum doesn't exist, continue
        print(f"Note: SCORING value may already exist: {e}")


def downgrade() -> None:
    """Downgrade schema."""
    # Note: PostgreSQL doesn't support removing enum values directly
    # This would require recreating the enum type, which is complex and risky
    # For now, we'll leave the value in place
    pass
