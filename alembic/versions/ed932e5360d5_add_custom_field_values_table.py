"""add custom field values table

Revision ID: ed932e5360d5
Revises: add_file_attachments_table
Create Date: 2025-10-30 18:14:04.989716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed932e5360d5'
down_revision: Union[str, Sequence[str], None] = 'add_file_attachments_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create custom_field_values table
    op.create_table(
        'custom_field_values',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('company_candidate_id', sa.String(255), nullable=False, index=True),
        sa.Column('custom_field_id', sa.String(255), nullable=False, index=True),
        sa.Column('field_value', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['company_candidate_id'], ['company_candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['custom_field_id'], ['workflow_custom_fields.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('company_candidate_id', 'custom_field_id', name='uq_company_candidate_custom_field')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('custom_field_values')
