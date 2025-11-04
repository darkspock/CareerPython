"""refactor_job_position_status_to_new_states

Revision ID: e8583501ef94
Revises: 9da74c883e6b
Create Date: 2025-11-04 08:27:00.155078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8583501ef94'
down_revision: Union[str, Sequence[str], None] = '9da74c883e6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Refactor job position status enum to new states: draft, active, paused, closed, archived
    
    Step 1: Add new enum values only. The data migration will be done in a separate step
    or manually after this migration commits.
    """
    
    # Add new enum values
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'draft' 
                AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'jobpositionstatus')
            ) THEN
                ALTER TYPE jobpositionstatus ADD VALUE 'draft';
            END IF;
            
            IF NOT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'active' 
                AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'jobpositionstatus')
            ) THEN
                ALTER TYPE jobpositionstatus ADD VALUE 'active';
            END IF;
            
            IF NOT EXISTS (
                SELECT 1 FROM pg_enum 
                WHERE enumlabel = 'archived' 
                AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'jobpositionstatus')
            ) THEN
                ALTER TYPE jobpositionstatus ADD VALUE 'archived';
            END IF;
        END $$;
    """)
    
    # Note: PostgreSQL requires enum values to be committed before they can be used in UPDATE statements.
    # The data migration will need to be done manually or in a separate migration after this one commits.
    # For now, we'll create a script that can be run separately:
    
    # Manual data migration script (run this after the migration):
    # UPDATE job_positions SET status = 'draft'::jobpositionstatus WHERE status::text IN ('PENDING', 'pending', 'APPROVED', 'approved');
    # UPDATE job_positions SET status = 'archived'::jobpositionstatus WHERE status::text IN ('REJECTED', 'rejected');
    # UPDATE job_positions SET status = 'active'::jobpositionstatus WHERE status::text IN ('OPEN', 'open', 'PUBLISHED', 'published');


def downgrade() -> None:
    """Downgrade schema - map new statuses back to old ones"""
    # Map new status values back to old ones
    op.execute("""
        UPDATE job_positions 
        SET status = CASE 
            WHEN status::text = 'draft' THEN 'pending'::jobpositionstatus
            WHEN status::text = 'active' THEN 'open'::jobpositionstatus
            WHEN status::text = 'archived' THEN 'closed'::jobpositionstatus
            WHEN status::text = 'closed' THEN 'closed'::jobpositionstatus
            WHEN status::text = 'paused' THEN 'paused'::jobpositionstatus
            ELSE status
        END
        WHERE status::text IN ('draft', 'active', 'archived');
    """)
    
    # Note: Cannot remove enum values in PostgreSQL easily, so old values remain
