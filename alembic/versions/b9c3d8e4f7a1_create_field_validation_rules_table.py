"""create_field_validation_rules_table

Revision ID: b9c3d8e4f7a1
Revises: fix_sort_order_nullable
Create Date: 2025-10-26 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9c3d8e4f7a1'
down_revision: Union[str, Sequence[str], None] = '8c9671e585af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create field_validation_rules table
    op.create_table(
        'field_validation_rules',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('custom_field_id', sa.String(length=255), nullable=False),
        sa.Column('stage_id', sa.String(length=255), nullable=False),
        sa.Column('rule_type', sa.String(length=50), nullable=False),
        sa.Column('comparison_operator', sa.String(length=50), nullable=False),
        sa.Column('position_field_path', sa.String(length=255), nullable=True),
        sa.Column('comparison_value', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('validation_message', sa.Text(), nullable=False),
        sa.Column('auto_reject', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['custom_field_id'], ['workflow_custom_fields.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['stage_id'], ['workflow_stages.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index(op.f('ix_field_validation_rules_custom_field_id'), 'field_validation_rules', ['custom_field_id'], unique=False)
    op.create_index(op.f('ix_field_validation_rules_stage_id'), 'field_validation_rules', ['stage_id'], unique=False)
    op.create_index(op.f('ix_field_validation_rules_is_active'), 'field_validation_rules', ['is_active'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index(op.f('ix_field_validation_rules_is_active'), table_name='field_validation_rules')
    op.drop_index(op.f('ix_field_validation_rules_stage_id'), table_name='field_validation_rules')
    op.drop_index(op.f('ix_field_validation_rules_custom_field_id'), table_name='field_validation_rules')

    # Drop table
    op.drop_table('field_validation_rules')
