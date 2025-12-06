"""add use_conversational_mode to interview_templates

Revision ID: dba5b34b4c44
Revises: 46a2275a5488
Create Date: 2025-12-06 11:13:17.184881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'dba5b34b4c44'
down_revision: Union[str, Sequence[str], None] = '46a2275a5488'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add use_conversational_mode column to interview_templates
    op.add_column('interview_templates',
        sa.Column('use_conversational_mode', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('interview_templates', 'use_conversational_mode')
