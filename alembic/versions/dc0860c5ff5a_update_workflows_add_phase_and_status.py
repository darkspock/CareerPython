"""update_workflows_add_phase_and_status

Revision ID: dc0860c5ff5a
Revises: c53639724872
Create Date: 2025-10-27 07:24:21.081033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc0860c5ff5a'
down_revision: Union[str, Sequence[str], None] = 'c53639724872'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add phase_id column to candidate_application_workflows table
    op.add_column('candidate_application_workflows', sa.Column('phase_id', sa.String(), nullable=True))
    op.create_foreign_key('fk_candidate_application_workflows_phase_id', 'candidate_application_workflows', 'company_phases', ['phase_id'], ['id'])
    op.create_index('ix_candidate_application_workflows_phase_id', 'candidate_application_workflows', ['phase_id'])

    # Create or update WorkflowStatus enum
    # Check if enum exists, if not create it, if yes, skip for now
    op.execute("""
        DO $$
        BEGIN
            -- Check if the enum type exists
            IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'workflowstatus') THEN
                -- Update existing values
                UPDATE candidate_application_workflows SET status = 'draft' WHERE status = 'inactive';

                -- Recreate the enum
                ALTER TYPE workflowstatus RENAME TO workflowstatus_old;
                CREATE TYPE workflowstatus AS ENUM ('draft', 'active', 'archived');
                ALTER TABLE candidate_application_workflows ALTER COLUMN status TYPE workflowstatus USING status::text::workflowstatus;
                DROP TYPE workflowstatus_old;
            ELSE
                -- Create new enum
                CREATE TYPE workflowstatus AS ENUM ('draft', 'active', 'archived');
            END IF;
        END $$;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert WorkflowStatus enum changes
    op.execute("ALTER TYPE workflowstatus RENAME TO workflowstatus_old")
    op.execute("CREATE TYPE workflowstatus AS ENUM ('active', 'inactive', 'archived')")
    op.execute("UPDATE candidate_application_workflows SET status = 'inactive' WHERE status = 'draft'")
    op.execute("ALTER TABLE candidate_application_workflows ALTER COLUMN status TYPE workflowstatus USING status::text::workflowstatus")
    op.execute("DROP TYPE workflowstatus_old")

    # Drop phase_id column
    op.drop_index('ix_candidate_application_workflows_phase_id', table_name='candidate_application_workflows')
    op.drop_constraint('fk_candidate_application_workflows_phase_id', 'candidate_application_workflows', type_='foreignkey')
    op.drop_column('candidate_application_workflows', 'phase_id')
