"""merge company pages migration

Revision ID: f3dae2005c88
Revises: 2a372a9e65de, a8080b05852
Create Date: 2025-10-29 09:45:23.144248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3dae2005c88'
down_revision: Union[str, Sequence[str], None] = ('2a372a9e65de', 'a8080b05852')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
