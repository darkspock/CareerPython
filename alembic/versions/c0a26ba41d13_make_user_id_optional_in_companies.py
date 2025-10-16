"""make_user_id_optional_in_companies

Revision ID: c0a26ba41d13
Revises: 40f3b85654d7
Create Date: 2025-10-04 16:31:05.970049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0a26ba41d13'
down_revision: Union[str, Sequence[str], None] = '40f3b85654d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove unique constraint and make user_id nullable
    op.drop_constraint('companies_user_id_key', 'companies', type_='unique')
    op.alter_column('companies', 'user_id', nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Reverse the changes
    op.alter_column('companies', 'user_id', nullable=False)
    op.create_unique_constraint('companies_user_id_key', 'companies', ['user_id'])
