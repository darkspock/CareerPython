"""add_current_job_level_and_expected_job_level_to_candidates

Revision ID: f2acd41a4021
Revises: b8908228839b
Create Date: 2025-10-04 11:48:40.578636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2acd41a4021'
down_revision: Union[str, Sequence[str], None] = 'b8908228839b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
