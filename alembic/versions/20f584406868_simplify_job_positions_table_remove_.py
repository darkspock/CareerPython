"""simplify_job_positions_table_remove_fields_add_visibility

Revision ID: 20f584406868
Revises: 46965f28b9c8
Create Date: 2025-11-04 15:14:30.747759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '20f584406868'
down_revision: Union[str, Sequence[str], None] = '46965f28b9c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Simplify job_positions table: remove fields, add visibility enum
    
    Step 1: Create jobpositionvisibility enum
    Step 2: Add visibility column with default 'hidden'
    Step 3: Migrate data from is_public to visibility (if is_public exists)
    Step 4: Drop columns that are now in custom_fields_values
    Step 5: Drop is_public column (if it exists)
    """
    
    # Step 1: Create jobpositionvisibility enum
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'jobpositionvisibility') THEN
                CREATE TYPE jobpositionvisibility AS ENUM ('hidden', 'internal', 'public');
            END IF;
        END $$;
    """)
    
    # Step 2: Add visibility column with default 'hidden'
    op.add_column('job_positions', sa.Column(
        'visibility', 
        postgresql.ENUM('hidden', 'internal', 'public', name='jobpositionvisibility', create_type=False),
        nullable=False,
        server_default='hidden'
    ))
    
    # Create index for visibility
    op.create_index(op.f('ix_job_positions_visibility'), 'job_positions', ['visibility'], unique=False)
    
    # Step 3: Migrate data from is_public to visibility (if is_public column exists)
    # Check if is_public column exists before migrating
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'job_positions' 
                AND column_name = 'is_public'
            ) THEN
                UPDATE job_positions 
                SET visibility = CASE 
                    WHEN is_public = TRUE THEN 'public'::jobpositionvisibility
                    ELSE 'internal'::jobpositionvisibility
                END;
            END IF;
        END $$;
    """)
    
    # Step 4: Migrate existing field data to custom_fields_values JSON (if table has data)
    # Note: The table is empty according to user, but we'll handle migration safely
    op.execute("""
        DO $$
        DECLARE
            rec RECORD;
            custom_fields JSONB;
        BEGIN
            -- Only migrate if there are records
            FOR rec IN SELECT id FROM job_positions LIMIT 1
            LOOP
                -- Migrate fields to custom_fields_values
                UPDATE job_positions
                SET custom_fields_values = COALESCE(custom_fields_values, '{}'::jsonb) || jsonb_build_object(
                    'location', location,
                    'work_location_type', work_location_type::text,
                    'salary_range', salary_range,
                    'contract_type', contract_type::text,
                    'requirements', requirements,
                    'position_level', position_level,
                    'number_of_openings', number_of_openings,
                    'application_instructions', application_instructions,
                    'benefits', benefits,
                    'working_hours', working_hours,
                    'travel_required', travel_required,
                    'languages_required', languages_required,
                    'visa_sponsorship', visa_sponsorship,
                    'contact_person', contact_person,
                    'department', department,
                    'reports_to', reports_to,
                    'desired_roles', desired_roles,
                    'skills', skills,
                    'application_url', application_url,
                    'application_email', application_email
                )
                WHERE id = rec.id;
            END LOOP;
        END $$;
    """)
    
    # Step 5: Drop columns that are now in custom_fields_values
    # Drop columns only if they exist (some may not exist)
    columns_to_drop = [
        'location',
        'work_location_type',
        'salary_range',
        'contract_type',
        'requirements',
        'position_level',
        'number_of_openings',
        'application_instructions',
        'benefits',
        'working_hours',
        'travel_required',
        'languages_required',
        'visa_sponsorship',
        'contact_person',
        'department',
        'reports_to',
        'desired_roles',
        'skills',
        'application_url',
        'application_email',
        'is_public',  # Replaced by visibility
        'employment_type'  # May not exist, but try to drop
    ]
    
    for column_name in columns_to_drop:
        op.execute(f"""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'job_positions' 
                    AND column_name = '{column_name}'
                ) THEN
                    ALTER TABLE job_positions DROP COLUMN {column_name};
                END IF;
            END $$;
        """)


def downgrade() -> None:
    """Downgrade schema - restore removed columns and remove visibility"""
    
    # Step 1: Add back all removed columns (with nullable=True since we don't have the data)
    op.add_column('job_positions', sa.Column('location', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('work_location_type', sa.Enum('REMOTE', 'ON_SITE', 'HYBRID', name='worklocationtype'), nullable=True))
    op.add_column('job_positions', sa.Column('salary_range', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('contract_type', sa.Enum('FULL_TIME', 'PART_TIME', 'CONTRACT', 'FREELANCE', 'INTERNSHIP', 'TEMPORARY', name='contracttype'), nullable=True))
    op.add_column('job_positions', sa.Column('requirements', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('position_level', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('number_of_openings', sa.Integer(), nullable=True))
    op.add_column('job_positions', sa.Column('application_instructions', sa.Text(), nullable=True))
    op.add_column('job_positions', sa.Column('benefits', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('working_hours', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('travel_required', sa.Integer(), nullable=True))
    op.add_column('job_positions', sa.Column('languages_required', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('visa_sponsorship', sa.Boolean(), nullable=True))
    op.add_column('job_positions', sa.Column('contact_person', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('department', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('reports_to', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('desired_roles', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('skills', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('application_url', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('application_email', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('is_public', sa.Boolean(), nullable=True, server_default='false'))
    
    # Step 2: Migrate visibility back to is_public
    op.execute("""
        UPDATE job_positions 
        SET is_public = CASE 
            WHEN visibility = 'public' THEN TRUE
            ELSE FALSE
        END;
    """)
    
    # Step 3: Drop visibility column and index
    op.drop_index(op.f('ix_job_positions_visibility'), table_name='job_positions')
    op.drop_column('job_positions', 'visibility')
    
    # Step 4: Drop enum type (optional, can leave it)
    # Note: PostgreSQL doesn't allow dropping enum types easily if they're used elsewhere
    # op.execute("DROP TYPE IF EXISTS jobpositionvisibility;")
