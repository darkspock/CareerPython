"""fix phase_id length in job_position_stages

Revision ID: aa149d83a13e
Revises: cef2532181de
Create Date: 2025-11-10 20:14:27.522901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa149d83a13e'
down_revision: Union[str, Sequence[str], None] = 'cef2532181de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Change phase_id from VARCHAR(26) to VARCHAR to support UUIDs (36 characters)
    op.alter_column('job_position_stages', 'phase_id',
                    existing_type=sa.String(length=26),
                    type_=sa.String(),
                    existing_nullable=True)
    # Change id from VARCHAR(26) to VARCHAR to support UUIDs (36 characters)
    op.alter_column('job_position_stages', 'id',
                    existing_type=sa.String(length=26),
                    type_=sa.String(),
                    existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert phase_id back to VARCHAR(26)
    op.alter_column('job_position_stages', 'phase_id',
                    existing_type=sa.String(),
                    type_=sa.String(length=26),
                    existing_nullable=True)
    # Revert id back to VARCHAR(26)
    op.alter_column('job_position_stages', 'id',
                    existing_type=sa.String(),
                    type_=sa.String(length=26),
                    existing_nullable=False)
