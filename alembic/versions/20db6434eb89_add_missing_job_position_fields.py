"""add_missing_job_position_fields

Revision ID: 20db6434eb89
Revises: f2acd41a4021
Create Date: 2025-10-04 12:12:12.432386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20db6434eb89'
down_revision: Union[str, Sequence[str], None] = 'f2acd41a4021'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
