"""add_job_position_publishing_flow_fields

Revision ID: 509c56276b78
Revises: d4e5f6a7b8c9
Create Date: 2025-12-09 18:45:32.030918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '509c56276b78'
down_revision: Union[str, Sequence[str], None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add job position publishing flow fields."""
    # Content fields
    op.add_column('job_positions', sa.Column('skills', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('languages', sa.JSON(), nullable=True))

    # Standard fields
    op.add_column('job_positions', sa.Column('department_id', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('employment_type', sa.String(length=30), nullable=True))
    op.add_column('job_positions', sa.Column('experience_level', sa.String(length=30), nullable=True))
    op.add_column('job_positions', sa.Column('work_location_type', sa.String(length=30), nullable=True))
    op.add_column('job_positions', sa.Column('office_locations', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('remote_restrictions', sa.String(length=500), nullable=True))
    op.add_column('job_positions', sa.Column('number_of_openings', sa.Integer(), nullable=True, server_default='1'))
    op.add_column('job_positions', sa.Column('requisition_id', sa.String(length=100), nullable=True))

    # Financial fields
    op.add_column('job_positions', sa.Column('salary_currency', sa.String(length=3), nullable=True))
    op.add_column('job_positions', sa.Column('salary_min', sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column('job_positions', sa.Column('salary_max', sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column('job_positions', sa.Column('salary_period', sa.String(length=20), nullable=True))
    op.add_column('job_positions', sa.Column('show_salary', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('job_positions', sa.Column('budget_max', sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column('job_positions', sa.Column('approved_budget_max', sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column('job_positions', sa.Column('financial_approver_id', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('approved_at', sa.DateTime(), nullable=True))

    # Ownership fields
    op.add_column('job_positions', sa.Column('hiring_manager_id', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('recruiter_id', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('created_by_id', sa.String(), nullable=True))

    # Lifecycle / Publishing flow fields
    op.add_column('job_positions', sa.Column('status', sa.String(length=30), nullable=True, server_default='draft'))
    op.add_column('job_positions', sa.Column('closed_reason', sa.String(length=30), nullable=True))
    op.add_column('job_positions', sa.Column('closed_at', sa.DateTime(), nullable=True))
    op.add_column('job_positions', sa.Column('published_at', sa.DateTime(), nullable=True))

    # Custom fields snapshot
    op.add_column('job_positions', sa.Column('custom_fields_config', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('source_workflow_id', sa.String(), nullable=True))

    # Pipeline and screening references
    op.add_column('job_positions', sa.Column('candidate_pipeline_id', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('screening_template_id', sa.String(), nullable=True))

    # Create indexes for frequently queried columns
    op.create_index(op.f('ix_job_positions_department_id'), 'job_positions', ['department_id'], unique=False)
    op.create_index(op.f('ix_job_positions_hiring_manager_id'), 'job_positions', ['hiring_manager_id'], unique=False)
    op.create_index(op.f('ix_job_positions_recruiter_id'), 'job_positions', ['recruiter_id'], unique=False)
    op.create_index(op.f('ix_job_positions_requisition_id'), 'job_positions', ['requisition_id'], unique=False)
    op.create_index(op.f('ix_job_positions_status'), 'job_positions', ['status'], unique=False)

    # Data migration: Set default values for existing records
    op.execute("UPDATE job_positions SET number_of_openings = 1 WHERE number_of_openings IS NULL")
    op.execute("UPDATE job_positions SET show_salary = false WHERE show_salary IS NULL")
    op.execute("UPDATE job_positions SET status = 'draft' WHERE status IS NULL")

    # Migrate visibility to status for existing public positions
    op.execute("""
        UPDATE job_positions
        SET status = 'published', published_at = created_at
        WHERE visibility = 'public' AND status = 'draft'
    """)


def downgrade() -> None:
    """Remove job position publishing flow fields."""
    # Drop indexes
    op.drop_index(op.f('ix_job_positions_status'), table_name='job_positions')
    op.drop_index(op.f('ix_job_positions_requisition_id'), table_name='job_positions')
    op.drop_index(op.f('ix_job_positions_recruiter_id'), table_name='job_positions')
    op.drop_index(op.f('ix_job_positions_hiring_manager_id'), table_name='job_positions')
    op.drop_index(op.f('ix_job_positions_department_id'), table_name='job_positions')

    # Drop columns
    op.drop_column('job_positions', 'screening_template_id')
    op.drop_column('job_positions', 'candidate_pipeline_id')
    op.drop_column('job_positions', 'source_workflow_id')
    op.drop_column('job_positions', 'custom_fields_config')
    op.drop_column('job_positions', 'published_at')
    op.drop_column('job_positions', 'closed_at')
    op.drop_column('job_positions', 'closed_reason')
    op.drop_column('job_positions', 'status')
    op.drop_column('job_positions', 'created_by_id')
    op.drop_column('job_positions', 'recruiter_id')
    op.drop_column('job_positions', 'hiring_manager_id')
    op.drop_column('job_positions', 'approved_at')
    op.drop_column('job_positions', 'financial_approver_id')
    op.drop_column('job_positions', 'approved_budget_max')
    op.drop_column('job_positions', 'budget_max')
    op.drop_column('job_positions', 'show_salary')
    op.drop_column('job_positions', 'salary_period')
    op.drop_column('job_positions', 'salary_max')
    op.drop_column('job_positions', 'salary_min')
    op.drop_column('job_positions', 'salary_currency')
    op.drop_column('job_positions', 'requisition_id')
    op.drop_column('job_positions', 'number_of_openings')
    op.drop_column('job_positions', 'remote_restrictions')
    op.drop_column('job_positions', 'office_locations')
    op.drop_column('job_positions', 'work_location_type')
    op.drop_column('job_positions', 'experience_level')
    op.drop_column('job_positions', 'employment_type')
    op.drop_column('job_positions', 'department_id')
    op.drop_column('job_positions', 'languages')
    op.drop_column('job_positions', 'skills')
