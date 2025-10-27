"""fix_intermediate_stage_type

Revision ID: 4bbde09b6dee
Revises: 19324f77c6bf
Create Date: 2025-10-27 18:00:57.375170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bbde09b6dee'
down_revision: Union[str, Sequence[str], None] = '19324f77c6bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Fix invalid stage_type values."""
    # Update all workflow stages with INTERMEDIATE stage_type to STANDARD
    op.execute("""
        UPDATE workflow_stages
        SET stage_type = 'STANDARD'
        WHERE stage_type = 'INTERMEDIATE'
    """)

    # Update all workflow stages with FINAL stage_type to SUCCESS
    # FINAL stages typically represent successful completion
    op.execute("""
        UPDATE workflow_stages
        SET stage_type = 'SUCCESS'
        WHERE stage_type = 'FINAL'
    """)


def downgrade() -> None:
    """Downgrade schema - Revert STANDARD back to INTERMEDIATE (if needed)."""
    # Note: We cannot accurately revert this as we don't know which STANDARD
    # stages were originally INTERMEDIATE. This is a data cleanup migration.
    pass
