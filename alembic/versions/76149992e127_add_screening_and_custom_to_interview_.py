"""add SCREENING and CUSTOM to interview template type enum

Revision ID: 76149992e127
Revises: create_interview_answers
Create Date: 2025-11-13 00:30:00.207515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '76149992e127'
down_revision: Union[str, Sequence[str], None] = 'create_interview_answers'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    
    # Add SCREENING and CUSTOM values to interviewtemplatetypeenum
    # PostgreSQL doesn't support IF NOT EXISTS for ALTER TYPE ADD VALUE,
    # so we need to check if the value exists first
    try:
        # Check if SCREENING already exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'SCREENING' 
                AND enumtypid = (
                    SELECT oid FROM pg_type WHERE typname = 'interviewtemplatetypeenum'
                )
            )
        """)).scalar()
        
        if not result:
            conn.execute(text("ALTER TYPE interviewtemplatetypeenum ADD VALUE 'SCREENING'"))
    except Exception as e:
        # If SCREENING already exists or enum doesn't exist, continue
        print(f"Note: SCREENING value may already exist: {e}")
    
    try:
        # Check if CUSTOM already exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'CUSTOM' 
                AND enumtypid = (
                    SELECT oid FROM pg_type WHERE typname = 'interviewtemplatetypeenum'
                )
            )
        """)).scalar()
        
        if not result:
            conn.execute(text("ALTER TYPE interviewtemplatetypeenum ADD VALUE 'CUSTOM'"))
    except Exception as e:
        # If CUSTOM already exists or enum doesn't exist, continue
        print(f"Note: CUSTOM value may already exist: {e}")


def downgrade() -> None:
    """Downgrade schema."""
    # Note: PostgreSQL doesn't support removing enum values directly
    # This would require recreating the enum type, which is complex and risky
    # For now, we'll leave the values in place
    # If you need to remove them, you would need to:
    # 1. Create a new enum without these values
    # 2. Alter the column to use the new enum
    # 3. Drop the old enum
    # 4. Rename the new enum to the old name
    pass
