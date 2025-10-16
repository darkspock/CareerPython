"""fix_desired_roles_column_type

Revision ID: 3fb8aa54c17a
Revises: f52d88709135
Create Date: 2025-10-07 21:41:22.535750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fb8aa54c17a'
down_revision: Union[str, Sequence[str], None] = 'f52d88709135'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Change desired_roles column type from INTEGER to JSON
    # First drop the default, then change type, then add new default
    op.execute("ALTER TABLE job_positions ALTER COLUMN desired_roles DROP DEFAULT")
    op.execute("""
        ALTER TABLE job_positions
        ALTER COLUMN desired_roles TYPE JSON
        USING CASE
            WHEN desired_roles IS NULL THEN NULL
            ELSE '[]'::JSON
        END
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Change desired_roles column type back from JSON to INTEGER
    op.execute("""
        ALTER TABLE job_positions
        ALTER COLUMN desired_roles TYPE INTEGER
        USING CASE
            WHEN desired_roles IS NULL THEN NULL
            ELSE 0
        END
    """)
