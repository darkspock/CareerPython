"""update_stages_add_next_phase_and_type

Revision ID: 9041203a0081
Revises: f5fe2ada03f2
Create Date: 2025-10-27 07:25:29.923196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9041203a0081'
down_revision: Union[str, Sequence[str], None] = 'f5fe2ada03f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add next_phase_id column to workflow_stages table
    op.add_column('workflow_stages', sa.Column('next_phase_id', sa.String(), nullable=True))
    op.create_foreign_key('fk_workflow_stages_next_phase_id', 'workflow_stages', 'company_phases', ['next_phase_id'], ['id'])
    op.create_index('ix_workflow_stages_next_phase_id', 'workflow_stages', ['next_phase_id'])

    # Create or update StageType enum
    op.execute("""
        DO $$
        BEGIN
            -- Check if the enum type exists
            IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'stagetype') THEN
                -- Update existing values
                UPDATE workflow_stages SET stage_type = 'standard' WHERE stage_type IN ('intermediate', 'custom');
                UPDATE workflow_stages SET stage_type = 'success' WHERE stage_type = 'final';

                -- Recreate the enum
                ALTER TYPE stagetype RENAME TO stagetype_old;
                CREATE TYPE stagetype AS ENUM ('initial', 'standard', 'success', 'fail');
                ALTER TABLE workflow_stages ALTER COLUMN stage_type TYPE stagetype USING stage_type::text::stagetype;
                DROP TYPE stagetype_old;
            ELSE
                -- Create new enum
                CREATE TYPE stagetype AS ENUM ('initial', 'standard', 'success', 'fail');
            END IF;
        END $$;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert StageType enum changes
    op.execute("ALTER TYPE stagetype RENAME TO stagetype_old")
    op.execute("CREATE TYPE stagetype AS ENUM ('initial', 'intermediate', 'final', 'custom')")
    op.execute("UPDATE workflow_stages SET stage_type = 'final' WHERE stage_type = 'success'")
    op.execute("UPDATE workflow_stages SET stage_type = 'intermediate' WHERE stage_type IN ('standard', 'fail')")
    op.execute("ALTER TABLE workflow_stages ALTER COLUMN stage_type TYPE stagetype USING stage_type::text::stagetype")
    op.execute("DROP TYPE stagetype_old")

    # Drop next_phase_id column
    op.drop_index('ix_workflow_stages_next_phase_id', table_name='workflow_stages')
    op.drop_constraint('fk_workflow_stages_next_phase_id', 'workflow_stages', type_='foreignkey')
    op.drop_column('workflow_stages', 'next_phase_id')
