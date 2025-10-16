"""merge_migrations

Revision ID: 45b5b18505bb
Revises: 4beb07b3df8e, create_interview_sessions
Create Date: 2025-09-23 18:48:52.997092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45b5b18505bb'
down_revision: Union[str, Sequence[str], None] = ('4beb07b3df8e', 'create_interview_sessions')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
