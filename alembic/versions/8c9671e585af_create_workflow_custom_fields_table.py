"""create_workflow_custom_fields_table

Revision ID: 8c9671e585af
Revises: e9ae81b01319
Create Date: 2025-10-26 11:37:18.689871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8c9671e585af'
down_revision: Union[str, Sequence[str], None] = 'e9ae81b01319'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create workflow_custom_fields table
    op.create_table(
        'workflow_custom_fields',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('workflow_id', sa.String(length=255), nullable=False),
        sa.Column('field_key', sa.String(length=100), nullable=False),
        sa.Column('field_name', sa.String(length=255), nullable=False),
        sa.Column('field_type', sa.String(length=50), nullable=False),
        sa.Column('field_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['workflow_id'], ['candidate_application_workflows.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('workflow_id', 'field_key', name='uq_workflow_custom_fields_workflow_field_key')
    )
    op.create_index(op.f('ix_workflow_custom_fields_workflow_id'), 'workflow_custom_fields', ['workflow_id'], unique=False)

    # Create stage_field_configurations table
    op.create_table(
        'stage_field_configurations',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('stage_id', sa.String(length=255), nullable=False),
        sa.Column('custom_field_id', sa.String(length=255), nullable=False),
        sa.Column('visibility', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['stage_id'], ['workflow_stages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['custom_field_id'], ['workflow_custom_fields.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('stage_id', 'custom_field_id', name='uq_stage_field_configurations_stage_field')
    )
    op.create_index(op.f('ix_stage_field_configurations_stage_id'), 'stage_field_configurations', ['stage_id'], unique=False)
    op.create_index(op.f('ix_stage_field_configurations_custom_field_id'), 'stage_field_configurations', ['custom_field_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop stage_field_configurations table
    op.drop_index(op.f('ix_stage_field_configurations_custom_field_id'), table_name='stage_field_configurations')
    op.drop_index(op.f('ix_stage_field_configurations_stage_id'), table_name='stage_field_configurations')
    op.drop_table('stage_field_configurations')

    # Drop workflow_custom_fields table
    op.drop_index(op.f('ix_workflow_custom_fields_workflow_id'), table_name='workflow_custom_fields')
    op.drop_table('workflow_custom_fields')
