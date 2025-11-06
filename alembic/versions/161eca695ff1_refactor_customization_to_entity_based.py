"""refactor customization to entity based

Revision ID: 161eca695ff1
Revises: 61ade504477b
Create Date: 2025-01-22 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '161eca695ff1'
down_revision: Union[str, Sequence[str], None] = '61ade504477b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Refactor customization to entity-based structure"""
    
    # Step 1: Create new entity_customizations table
    op.create_table(
        'entity_customizations',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=255), nullable=False),
        sa.Column('validation', sa.Text(), nullable=True),  # JSON-Logic
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('entity_type', 'entity_id', name='uq_entity_customizations_entity_type_id')
    )
    op.create_index('ix_entity_customizations_id', 'entity_customizations', ['id'], unique=False)
    op.create_index('ix_entity_customizations_entity_type', 'entity_customizations', ['entity_type'], unique=False)
    op.create_index('ix_entity_customizations_entity_id', 'entity_customizations', ['entity_id'], unique=False)
    op.create_index('ix_entity_customizations_entity_type_id', 'entity_customizations', ['entity_type', 'entity_id'], unique=False)
    
    # Step 2: Create new custom_fields table (replaces workflow_custom_fields)
    op.create_table(
        'custom_fields',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('entity_customization_id', sa.String(length=255), nullable=False),
        sa.Column('field_key', sa.String(length=100), nullable=False),
        sa.Column('field_name', sa.String(length=255), nullable=False),
        sa.Column('field_type', sa.String(length=50), nullable=False),
        sa.Column('field_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['entity_customization_id'], ['entity_customizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('entity_customization_id', 'field_key', name='uq_custom_fields_entity_customization_field_key')
    )
    op.create_index('ix_custom_fields_id', 'custom_fields', ['id'], unique=False)
    op.create_index('ix_custom_fields_entity_customization_id', 'custom_fields', ['entity_customization_id'], unique=False)
    
    # Step 3: Migrate data from workflow_custom_fields to entity_customizations + custom_fields
    # Only if workflow_custom_fields table exists
    op.execute(text("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'workflow_custom_fields') THEN
                -- For each unique workflow_id, create an EntityCustomization
                INSERT INTO entity_customizations (id, entity_type, entity_id, validation, metadata, created_at, updated_at)
                SELECT DISTINCT
                    'ec_' || workflow_id as id,
                    'CandidateApplication' as entity_type,
                    workflow_id as entity_id,
                    NULL as validation,
                    '{}'::jsonb as metadata,
                    MIN(created_at) as created_at,
                    MAX(updated_at) as updated_at
                FROM workflow_custom_fields
                GROUP BY workflow_id;
                
                -- Migrate custom fields to new structure
                INSERT INTO custom_fields (
                    id, entity_customization_id, field_key, field_name, field_type,
                    field_config, order_index, created_at, updated_at
                )
                SELECT
                    cf.id,
                    'ec_' || cf.workflow_id as entity_customization_id,
                    cf.field_key,
                    cf.field_name,
                    cf.field_type,
                    cf.field_config,
                    cf.order_index,
                    cf.created_at,
                    cf.updated_at
                FROM workflow_custom_fields cf;
            END IF;
        END $$;
    """))
    
    # Step 4: Update custom_field_values table
    # Add new columns if they don't exist
    op.execute(text("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'custom_field_values') THEN
                -- Add entity_type and entity_id columns if they don't exist
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'custom_field_values' AND column_name = 'entity_type') THEN
                    ALTER TABLE custom_field_values ADD COLUMN entity_type VARCHAR(50);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'custom_field_values' AND column_name = 'entity_id') THEN
                    ALTER TABLE custom_field_values ADD COLUMN entity_id VARCHAR(255);
                END IF;
                
                -- Migrate data: workflow_id -> entity_type + entity_id
                UPDATE custom_field_values
                SET entity_type = 'CandidateApplication',
                    entity_id = workflow_id
                WHERE workflow_id IS NOT NULL AND entity_type IS NULL;
                
                -- Create indexes for new columns
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_custom_field_values_entity_type') THEN
                    CREATE INDEX ix_custom_field_values_entity_type ON custom_field_values(entity_type);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_custom_field_values_entity_id') THEN
                    CREATE INDEX ix_custom_field_values_entity_id ON custom_field_values(entity_id);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_custom_field_values_entity_type_id') THEN
                    CREATE INDEX ix_custom_field_values_entity_type_id ON custom_field_values(entity_type, entity_id);
                END IF;
                
                -- Add unique constraint if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint 
                    WHERE conname = 'uq_custom_field_values_entity_type_id'
                ) THEN
                    ALTER TABLE custom_field_values 
                    ADD CONSTRAINT uq_custom_field_values_entity_type_id 
                    UNIQUE (entity_type, entity_id);
                END IF;
            END IF;
        END $$;
    """))
    
    # Step 5: Update field_configurations table (stage_field_configurations -> field_configurations)
    op.execute(text("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'stage_field_configurations') THEN
                -- Rename table if it exists
                ALTER TABLE stage_field_configurations RENAME TO field_configurations;
                
                -- Add new columns if they don't exist
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'field_configurations' AND column_name = 'entity_customization_id') THEN
                    ALTER TABLE field_configurations ADD COLUMN entity_customization_id VARCHAR(255);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'field_configurations' AND column_name = 'context_type') THEN
                    ALTER TABLE field_configurations ADD COLUMN context_type VARCHAR(50);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'field_configurations' AND column_name = 'context_id') THEN
                    ALTER TABLE field_configurations ADD COLUMN context_id VARCHAR(255);
                END IF;
                
                -- Migrate data: stage_id -> context_type='stage', context_id=stage_id
                -- Get entity_customization_id from custom_field_id -> entity_customization_id
                UPDATE field_configurations fc
                SET 
                    entity_customization_id = (
                        SELECT cf.entity_customization_id 
                        FROM custom_fields cf 
                        WHERE cf.id = fc.custom_field_id
                    ),
                    context_type = 'stage',
                    context_id = fc.stage_id
                WHERE fc.entity_customization_id IS NULL;
                
                -- Add foreign key constraint if entity_customization_id column exists
                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'field_configurations' AND column_name = 'entity_customization_id') THEN
                    -- Drop old foreign key if exists
                    IF EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'stage_field_configurations_stage_id_fkey'
                    ) THEN
                        ALTER TABLE field_configurations 
                        DROP CONSTRAINT stage_field_configurations_stage_id_fkey;
                    END IF;
                    
                    -- Add new foreign key
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'field_configurations_entity_customization_id_fkey'
                    ) THEN
                        ALTER TABLE field_configurations 
                        ADD CONSTRAINT field_configurations_entity_customization_id_fkey 
                        FOREIGN KEY (entity_customization_id) 
                        REFERENCES entity_customizations(id) ON DELETE CASCADE;
                    END IF;
                END IF;
                
                -- Create indexes
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_field_configurations_entity_customization_id') THEN
                    CREATE INDEX ix_field_configurations_entity_customization_id ON field_configurations(entity_customization_id);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_field_configurations_context') THEN
                    CREATE INDEX ix_field_configurations_context ON field_configurations(context_type, context_id);
                END IF;
                
                -- Update unique constraint
                IF EXISTS (
                    SELECT 1 FROM pg_constraint 
                    WHERE conname = 'uq_stage_field_configurations_stage_field'
                ) THEN
                    ALTER TABLE field_configurations 
                    DROP CONSTRAINT uq_stage_field_configurations_stage_field;
                END IF;
                
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint 
                    WHERE conname = 'uq_field_configurations_entity_field_context'
                ) THEN
                    ALTER TABLE field_configurations 
                    ADD CONSTRAINT uq_field_configurations_entity_field_context 
                    UNIQUE (entity_customization_id, custom_field_id, context_type, context_id);
                END IF;
            END IF;
        END $$;
    """))


def downgrade() -> None:
    """Downgrade schema - Revert to workflow-based structure"""
    
    # Note: This is a complex downgrade that would require restoring old data
    # For safety, we'll just drop the new tables and keep old data if it exists
    
    # Drop new tables
    op.execute("DROP TABLE IF EXISTS field_configurations CASCADE")
    op.execute("DROP TABLE IF EXISTS custom_fields CASCADE")
    op.execute("DROP TABLE IF EXISTS entity_customizations CASCADE")
    
    # Remove columns from custom_field_values if they exist
    op.execute(text("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'custom_field_values') THEN
                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'custom_field_values' AND column_name = 'entity_type') THEN
                    ALTER TABLE custom_field_values DROP COLUMN entity_type;
                END IF;
                IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'custom_field_values' AND column_name = 'entity_id') THEN
                    ALTER TABLE custom_field_values DROP COLUMN entity_id;
                END IF;
            END IF;
        END $$;
    """))
