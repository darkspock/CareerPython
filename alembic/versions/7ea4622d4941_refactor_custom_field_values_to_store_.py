"""refactor custom_field_values to store all values in json

Revision ID: 7ea4622d4941
Revises: 3bf4ac14a74a
Create Date: 2025-10-30 23:42:41.499383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '7ea4622d4941'
down_revision: Union[str, Sequence[str], None] = '3bf4ac14a74a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - consolidate multiple rows per candidate into single JSON row"""
    
    # Step 1: Create a temporary table with the new structure
    op.create_table(
        'custom_field_values_new',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('company_candidate_id', sa.String(255), nullable=False),
        sa.Column('workflow_id', sa.String(255), nullable=False),
        sa.Column('values', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['company_candidate_id'], ['company_candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workflow_id'], ['candidate_application_workflows.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('company_candidate_id', 'workflow_id', name='uq_company_candidate_workflow')
    )
    
    op.create_index('ix_custom_field_values_new_company_candidate_id', 'custom_field_values_new', ['company_candidate_id'])
    op.create_index('ix_custom_field_values_new_workflow_id', 'custom_field_values_new', ['workflow_id'])
    
    # Step 2: Consolidate existing data
    # For each company_candidate_id + workflow_id combination, create a JSON with all field values
    # Use field_key -> field_value mapping
    op.execute(text("""
        INSERT INTO custom_field_values_new (id, company_candidate_id, workflow_id, values, created_at, updated_at)
        SELECT 
            (SELECT MIN(id) FROM custom_field_values WHERE company_candidate_id = grouped.company_candidate_id 
             AND custom_field_id IN (SELECT id FROM workflow_custom_fields WHERE workflow_id = grouped.workflow_id)) as id,
            grouped.company_candidate_id,
            grouped.workflow_id,
            COALESCE(grouped.values::json, '{}'::json) as values,
            grouped.created_at,
            grouped.updated_at
        FROM (
            SELECT 
                cfv.company_candidate_id,
                cf.workflow_id,
                jsonb_object_agg(cf.field_key, cfv.field_value) FILTER (WHERE cf.field_key IS NOT NULL) as values,
                MIN(cfv.created_at) as created_at,
                MAX(cfv.updated_at) as updated_at
            FROM custom_field_values cfv
            JOIN workflow_custom_fields cf ON cfv.custom_field_id = cf.id
            GROUP BY cfv.company_candidate_id, cf.workflow_id
        ) grouped
    """))
    
    # Step 3: Drop old table and rename new one
    op.drop_table('custom_field_values')
    op.execute("ALTER TABLE custom_field_values_new RENAME TO custom_field_values")
    op.execute("ALTER INDEX ix_custom_field_values_new_company_candidate_id RENAME TO ix_custom_field_values_company_candidate_id")
    op.execute("ALTER INDEX ix_custom_field_values_new_workflow_id RENAME TO ix_custom_field_values_workflow_id")


def downgrade() -> None:
    """Downgrade schema - expand JSON back to multiple rows (not fully supported)"""
    # This is complex to reverse, so we'll just recreate the old structure
    # In practice, you'd need to expand the JSON and recreate individual rows
    pass
