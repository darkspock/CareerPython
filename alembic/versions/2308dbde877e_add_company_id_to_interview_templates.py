"""add company_id to interview_templates

Revision ID: 2308dbde877e
Revises: aa149d83a13e
Create Date: 2025-11-11 15:12:05.591262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2308dbde877e'
down_revision: Union[str, Sequence[str], None] = 'aa149d83a13e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add company_id column to interview_templates table
    op.add_column('interview_templates', sa.Column('company_id', sa.String(), nullable=True))
    # Create index for better query performance
    op.create_index(op.f('ix_interview_templates_company_id'), 'interview_templates', ['company_id'], unique=False)
    # Create composite index for common queries (company_id + status)
    op.create_index('idx_company_id_status', 'interview_templates', ['company_id', 'status'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('idx_company_id_status', table_name='interview_templates')
    op.drop_index(op.f('ix_interview_templates_company_id'), table_name='interview_templates')
    # Drop column
    op.drop_column('interview_templates', 'company_id')
