"""merge heads before adding workflow status

Revision ID: 751125998941
Revises: 50ed4e79550f, c97adedb18de
Create Date: 2025-11-05 23:36:13.745543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '751125998941'
down_revision: Union[str, Sequence[str], None] = ('50ed4e79550f', 'c97adedb18de')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
