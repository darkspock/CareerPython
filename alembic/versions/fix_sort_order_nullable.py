"""Fix sort_order nullable issue

Revision ID: fix_sort_order_nullable
Revises: 4f985767f61f
Create Date: 2025-09-30 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fix_sort_order_nullable'
down_revision: Union[str, Sequence[str], None] = '4f985767f61f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Make sort_order non-nullable with default value."""
    # First, update any NULL values to 0
    op.execute("UPDATE interview_template_questions SET sort_order = 0 WHERE sort_order IS NULL")

    # Then make the column non-nullable
    op.alter_column('interview_template_questions', 'sort_order',
                   existing_type=sa.INTEGER(),
                   nullable=False,
                   server_default='0')


def downgrade() -> None:
    """Make sort_order nullable again."""
    op.alter_column('interview_template_questions', 'sort_order',
                   existing_type=sa.INTEGER(),
                   nullable=True,
                   server_default=None)