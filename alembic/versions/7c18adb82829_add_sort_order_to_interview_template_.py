"""add_sort_order_to_interview_template_sections

Revision ID: 7c18adb82829
Revises: ee872c48225c
Create Date: 2025-10-02 22:00:05.572412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c18adb82829'
down_revision: Union[str, Sequence[str], None] = 'ee872c48225c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add sort_order column to interview_template_sections table
    op.add_column('interview_template_sections',
                 sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'))

    # Create index for sort_order
    op.create_index('ix_interview_template_sections_sort_order', 'interview_template_sections', ['sort_order'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove index first
    op.drop_index('ix_interview_template_sections_sort_order', table_name='interview_template_sections')

    # Remove sort_order column
    op.drop_column('interview_template_sections', 'sort_order')
