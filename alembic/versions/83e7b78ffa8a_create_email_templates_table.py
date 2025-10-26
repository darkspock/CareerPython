"""create_email_templates_table

Revision ID: 83e7b78ffa8a
Revises: d5e8f4a9b3c7
Create Date: 2025-10-26 20:53:34.746252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83e7b78ffa8a'
down_revision: Union[str, Sequence[str], None] = 'd5e8f4a9b3c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create email_templates table
    op.create_table(
        'email_templates',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=False),
        sa.Column('stage_id', sa.String(), nullable=True),  # NULL = applies to all stages
        sa.Column('template_name', sa.String(length=200), nullable=False),
        sa.Column('template_key', sa.String(length=100), nullable=False),
        sa.Column('subject', sa.String(length=500), nullable=False),
        sa.Column('body_html', sa.Text(), nullable=False),
        sa.Column('body_text', sa.Text(), nullable=True),
        sa.Column('available_variables', sa.JSON(), nullable=False),  # List of available variables
        sa.Column('trigger_event', sa.String(length=100), nullable=False),  # stage_entered, stage_completed, application_created, etc.
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_email_templates_workflow_id', 'email_templates', ['workflow_id'])
    op.create_index('ix_email_templates_stage_id', 'email_templates', ['stage_id'])
    op.create_index('ix_email_templates_trigger_event', 'email_templates', ['trigger_event'])

    # Create unique constraint on workflow_id + stage_id + trigger_event
    op.create_unique_constraint(
        'uq_email_templates_workflow_stage_trigger',
        'email_templates',
        ['workflow_id', 'stage_id', 'trigger_event']
    )

    # Add foreign key to company_workflows
    op.create_foreign_key(
        'fk_email_templates_workflow_id',
        'email_templates',
        'company_workflows',
        ['workflow_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # Add foreign key to workflow_stages
    op.create_foreign_key(
        'fk_email_templates_stage_id',
        'email_templates',
        'workflow_stages',
        ['stage_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_email_templates_stage_id', 'email_templates', type_='foreignkey')
    op.drop_constraint('fk_email_templates_workflow_id', 'email_templates', type_='foreignkey')
    op.drop_constraint('uq_email_templates_workflow_stage_trigger', 'email_templates', type_='unique')
    op.drop_index('ix_email_templates_trigger_event', 'email_templates')
    op.drop_index('ix_email_templates_stage_id', 'email_templates')
    op.drop_index('ix_email_templates_workflow_id', 'email_templates')
    op.drop_table('email_templates')
