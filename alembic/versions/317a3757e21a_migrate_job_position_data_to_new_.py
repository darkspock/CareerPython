"""migrate_job_position_data_to_new_statuses

Revision ID: 317a3757e21a
Revises: e8583501ef94
Create Date: 2025-11-04 08:33:36.559186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '317a3757e21a'
down_revision: Union[str, Sequence[str], None] = 'e8583501ef94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
