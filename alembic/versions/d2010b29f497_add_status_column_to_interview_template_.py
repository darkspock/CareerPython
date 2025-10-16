"""add status column to interview_template_sections

Revision ID: d2010b29f497
Revises: fix_sort_order_nullable
Create Date: 2025-10-02 21:11:35.087855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2010b29f497'
down_revision: Union[str, Sequence[str], None] = 'fix_sort_order_nullable'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add status column to interview_template_sections table
    op.add_column(
        'interview_template_sections',
        sa.Column(
            'status',
            sa.Enum('ENABLED', 'DRAFT', 'DISABLED', name='interviewtemplatesectionstatusenum'),
            nullable=False,
            server_default='DRAFT'
        )
    )

    # Add index for status column
    op.create_index(
        'ix_interview_template_sections_status',
        'interview_template_sections',
        ['status']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove index
    op.drop_index('ix_interview_template_sections_status', table_name='interview_template_sections')

    # Remove status column
    op.drop_column('interview_template_sections', 'status')
