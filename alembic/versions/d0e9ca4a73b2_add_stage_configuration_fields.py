"""add_stage_configuration_fields

Revision ID: d0e9ca4a73b2
Revises: e01d8be86325
Create Date: 2025-10-25 19:54:01.687530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0e9ca4a73b2'
down_revision: Union[str, Sequence[str], None] = 'e01d8be86325'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add new configuration fields to workflow_stages table."""
    # Add new fields for Phase 2: Enhanced Stage Configuration
    op.add_column('workflow_stages', sa.Column('default_roles', sa.JSON(), nullable=True))
    op.add_column('workflow_stages', sa.Column('default_assigned_users', sa.JSON(), nullable=True))
    op.add_column('workflow_stages', sa.Column('email_template_id', sa.String(length=255), nullable=True))
    op.add_column('workflow_stages', sa.Column('custom_email_text', sa.Text(), nullable=True))
    op.add_column('workflow_stages', sa.Column('deadline_days', sa.Integer(), nullable=True))
    op.add_column('workflow_stages', sa.Column('estimated_cost', sa.Numeric(precision=10, scale=2), nullable=True))


def downgrade() -> None:
    """Remove configuration fields from workflow_stages table."""
    op.drop_column('workflow_stages', 'estimated_cost')
    op.drop_column('workflow_stages', 'deadline_days')
    op.drop_column('workflow_stages', 'custom_email_text')
    op.drop_column('workflow_stages', 'email_template_id')
    op.drop_column('workflow_stages', 'default_assigned_users')
    op.drop_column('workflow_stages', 'default_roles')
