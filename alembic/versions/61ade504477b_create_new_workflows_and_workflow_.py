"""create new workflows and workflow_stages tables

Revision ID: 61ade504477b
Revises: 0cb15438510c
Create Date: 2025-11-06 11:22:54.345047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '61ade504477b'
down_revision: Union[str, Sequence[str], None] = '0cb15438510c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Drop old tables and create new generic workflow tables."""
    
    # Drop old tables if they exist (in correct order due to foreign keys)
    op.execute("DROP TABLE IF EXISTS workflow_stages CASCADE")
    op.execute("DROP TABLE IF EXISTS candidate_application_workflows CASCADE")
    op.execute("DROP TABLE IF EXISTS company_workflows CASCADE")
    
    # Drop old enum types if they exist
    op.execute("DROP TYPE IF EXISTS workflowstatus CASCADE")
    op.execute("DROP TYPE IF EXISTS stagetype CASCADE")
    op.execute("DROP TYPE IF EXISTS stageoutcome CASCADE")
    
    # Create new enum types
    op.execute("""
        CREATE TYPE workflowtypeenum AS ENUM ('PO', 'CA', 'CO')
    """)
    op.execute("""
        CREATE TYPE workflowdisplayenum AS ENUM ('kanban', 'list')
    """)
    op.execute("""
        CREATE TYPE workflowstatusenum AS ENUM ('draft', 'active', 'archived')
    """)
    op.execute("""
        CREATE TYPE workflowstagetypeenum AS ENUM ('success', 'initial', 'progress', 'fail', 'hold')
    """)
    op.execute("""
        CREATE TYPE kanbandisplayenum AS ENUM ('column', 'row', 'hidden')
    """)
    
    # Create workflows table
    op.create_table('workflows',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_id', sa.String(), nullable=False),
        sa.Column('workflow_type', sa.Enum('PO', 'CA', 'CO', name='workflowtypeenum', native_enum=False, length=30), nullable=False),
        sa.Column('display', sa.Enum('kanban', 'list', name='workflowdisplayenum', native_enum=False, length=20), nullable=False, server_default='kanban'),
        sa.Column('phase_id', sa.String(255), nullable=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(), nullable=False, server_default=''),
        sa.Column('status', sa.Enum('draft', 'active', 'archived', name='workflowstatusenum', native_enum=False, length=20), nullable=False, server_default='draft'),
        sa.Column('is_default', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for workflows table
    op.create_index('ix_workflows_id', 'workflows', ['id'], unique=False)
    op.create_index('ix_workflows_company_id', 'workflows', ['company_id'], unique=False)
    op.create_index('ix_workflows_workflow_type', 'workflows', ['workflow_type'], unique=False)
    op.create_index('ix_workflows_status', 'workflows', ['status'], unique=False)
    op.create_index('ix_workflows_is_default', 'workflows', ['is_default'], unique=False)
    op.create_index('ix_workflows_phase_id', 'workflows', ['phase_id'], unique=False)
    
    # Create foreign key constraint for phase_id (if company_phases table exists)
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'company_phases') THEN
                ALTER TABLE workflows 
                ADD CONSTRAINT fk_workflows_phase_id 
                FOREIGN KEY (phase_id) REFERENCES company_phases(id) ON DELETE SET NULL;
            END IF;
        END $$;
    """)
    
    # Create workflow_stages table
    op.create_table('workflow_stages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(), nullable=False, server_default=''),
        sa.Column('stage_type', sa.Enum('success', 'initial', 'progress', 'fail', 'hold', name='workflowstagetypeenum', native_enum=False, length=20), nullable=False, server_default='initial'),
        sa.Column('order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('allow_skip', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('estimated_duration_days', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('default_role_ids', sa.JSON(), nullable=True),
        sa.Column('default_assigned_users', sa.JSON(), nullable=True),
        sa.Column('email_template_id', sa.String(255), nullable=True),
        sa.Column('custom_email_text', sa.Text(), nullable=True),
        sa.Column('deadline_days', sa.Integer(), nullable=True),
        sa.Column('estimated_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('next_phase_id', sa.String(255), nullable=True),
        sa.Column('kanban_display', sa.Enum('column', 'row', 'hidden', name='kanbandisplayenum', native_enum=False, length=30), nullable=False, server_default='column'),
        sa.Column('style', sa.JSON(), nullable=True),
        sa.Column('validation_rules', sa.JSON(), nullable=True),
        sa.Column('recommended_rules', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for workflow_stages table
    op.create_index('ix_workflow_stages_id', 'workflow_stages', ['id'], unique=False)
    op.create_index('ix_workflow_stages_workflow_id', 'workflow_stages', ['workflow_id'], unique=False)
    op.create_index('ix_workflow_stages_order', 'workflow_stages', ['order'], unique=False)
    op.create_index('ix_workflow_stages_stage_type', 'workflow_stages', ['stage_type'], unique=False)
    
    # Create foreign key constraint for next_phase_id (if company_phases table exists)
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'company_phases') THEN
                ALTER TABLE workflow_stages 
                ADD CONSTRAINT fk_workflow_stages_next_phase_id 
                FOREIGN KEY (next_phase_id) REFERENCES company_phases(id) ON DELETE SET NULL;
            END IF;
        END $$;
    """)
    
    # Create foreign key constraint for email_template_id (if email_templates table exists)
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'email_templates') THEN
                ALTER TABLE workflow_stages 
                ADD CONSTRAINT fk_workflow_stages_email_template_id 
                FOREIGN KEY (email_template_id) REFERENCES email_templates(id) ON DELETE SET NULL;
            END IF;
        END $$;
    """)


def downgrade() -> None:
    """Downgrade schema - Remove new tables and restore old structure."""
    
    # Drop new tables
    op.drop_index('ix_workflow_stages_stage_type', table_name='workflow_stages')
    op.drop_index('ix_workflow_stages_order', table_name='workflow_stages')
    op.drop_index('ix_workflow_stages_workflow_id', table_name='workflow_stages')
    op.drop_index('ix_workflow_stages_id', table_name='workflow_stages')
    op.drop_table('workflow_stages')
    
    op.drop_index('ix_workflows_phase_id', table_name='workflows')
    op.drop_index('ix_workflows_is_default', table_name='workflows')
    op.drop_index('ix_workflows_status', table_name='workflows')
    op.drop_index('ix_workflows_workflow_type', table_name='workflows')
    op.drop_index('ix_workflows_company_id', table_name='workflows')
    op.drop_index('ix_workflows_id', table_name='workflows')
    op.drop_table('workflows')
    
    # Drop new enum types
    op.execute("DROP TYPE IF EXISTS kanbandisplayenum CASCADE")
    op.execute("DROP TYPE IF EXISTS workflowstagetypeenum CASCADE")
    op.execute("DROP TYPE IF EXISTS workflowstatusenum CASCADE")
    op.execute("DROP TYPE IF EXISTS workflowdisplayenum CASCADE")
    op.execute("DROP TYPE IF EXISTS workflowtypeenum CASCADE")
    
    # Note: Old tables (candidate_application_workflows, company_workflows, workflow_stages) 
    # are not recreated in downgrade as they were dropped in upgrade.
    # If needed, they should be restored from a backup or previous migration.
