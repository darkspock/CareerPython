"""Add resume fields to company_candidate

Revision ID: 77429c29143e
Revises: 468a891f5208
Create Date: 2025-10-23 23:21:39.273783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '77429c29143e'
down_revision: Union[str, Sequence[str], None] = '468a891f5208'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add resume fields to company_candidates table
    op.add_column('company_candidates', sa.Column('lead_id', sa.String(), nullable=True))
    op.add_column('company_candidates', sa.Column('source', sa.String(length=100), nullable=False, server_default='manual_import'))
    op.add_column('company_candidates', sa.Column('resume_url', sa.String(length=500), nullable=True))
    op.add_column('company_candidates', sa.Column('resume_uploaded_by', sa.String(), nullable=True))
    op.add_column('company_candidates', sa.Column('resume_uploaded_at', sa.DateTime(), nullable=True))

    # Create indexes
    op.create_index(op.f('ix_company_candidates_lead_id'), 'company_candidates', ['lead_id'], unique=False)
    op.create_index(op.f('ix_company_candidates_source'), 'company_candidates', ['source'], unique=False)

    # Create foreign key constraint
    op.create_foreign_key(None, 'company_candidates', 'company_users', ['resume_uploaded_by'], ['id'])

    # Remove default value after migration
    op.alter_column('company_candidates', 'source', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key constraint
    op.drop_constraint(None, 'company_candidates', type_='foreignkey')

    # Drop indexes
    op.drop_index(op.f('ix_company_candidates_source'), table_name='company_candidates')
    op.drop_index(op.f('ix_company_candidates_lead_id'), table_name='company_candidates')

    # Drop columns
    op.drop_column('company_candidates', 'resume_uploaded_at')
    op.drop_column('company_candidates', 'resume_uploaded_by')
    op.drop_column('company_candidates', 'resume_url')
    op.drop_column('company_candidates', 'source')
    op.drop_column('company_candidates', 'lead_id')
