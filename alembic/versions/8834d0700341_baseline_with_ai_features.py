"""baseline_with_ai_features

Revision ID: 8834d0700341
Revises: 
Create Date: 2025-09-17 09:19:59.160555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8834d0700341'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # This is a baseline migration - all tables already exist with AI features
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # This is a baseline migration - no downgrade needed
    pass
