"""add_test_user_for_company_testing

Revision ID: 40f3b85654d7
Revises: ea0148a31532
Create Date: 2025-10-04 16:11:48.853862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40f3b85654d7'
down_revision: Union[str, Sequence[str], None] = 'ea0148a31532'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insert test user for company testing
    op.execute("""
        INSERT INTO users (id, username, email, is_active, created_at, updated_at)
        VALUES ('user-123', 'testuser', 'testuser@example.com', true, now(), now())
        ON CONFLICT (id) DO NOTHING;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove test user
    op.execute("DELETE FROM users WHERE id = 'user-123';")
