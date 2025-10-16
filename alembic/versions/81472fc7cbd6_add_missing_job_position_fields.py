"""add_missing_job_position_fields

Revision ID: 81472fc7cbd6
Revises: 20db6434eb89
Create Date: 2025-10-04 14:50:12.385181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81472fc7cbd6'
down_revision: Union[str, Sequence[str], None] = '20db6434eb89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
