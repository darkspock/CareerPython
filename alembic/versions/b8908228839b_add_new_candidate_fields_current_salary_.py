"""add_new_candidate_fields_current_salary_linkedin_consent_roles_skills

Revision ID: b8908228839b
Revises: dfb8ecc3985a
Create Date: 2025-10-04 11:22:08.368203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8908228839b'
down_revision: Union[str, Sequence[str], None] = 'dfb8ecc3985a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new fields to candidates table
    op.add_column('candidates', sa.Column('current_annual_salary', sa.Integer(), nullable=True))
    op.add_column('candidates', sa.Column('linkedin_url', sa.String(), nullable=True))
    op.add_column('candidates', sa.Column('data_consent', sa.Boolean(), nullable=True))
    op.add_column('candidates', sa.Column('data_consent_on', sa.Date(), nullable=True))
    op.add_column('candidates', sa.Column('current_roles', sa.JSON(), nullable=True))
    op.add_column('candidates', sa.Column('expected_roles', sa.JSON(), nullable=True))
    op.add_column('candidates', sa.Column('skills', sa.JSON(), nullable=True))
    op.add_column('candidates', sa.Column('created_on', sa.Date(), nullable=False, server_default=sa.text('CURRENT_DATE')))
    op.add_column('candidates', sa.Column('updated_on', sa.Date(), nullable=False, server_default=sa.text('CURRENT_DATE')))
    op.add_column('candidates', sa.Column('timezone', sa.String(), nullable=True))
    op.add_column('candidates', sa.Column('candidate_notes', sa.Text(), nullable=True))

    # Update currency column to have default value 'EUR'
    op.alter_column('candidates', 'currency', server_default='EUR')


def downgrade() -> None:
    """Downgrade schema."""
    # Remove added columns
    op.drop_column('candidates', 'current_annual_salary')
    op.drop_column('candidates', 'linkedin_url')
    op.drop_column('candidates', 'data_consent')
    op.drop_column('candidates', 'data_consent_on')
    op.drop_column('candidates', 'current_roles')
    op.drop_column('candidates', 'expected_roles')
    op.drop_column('candidates', 'skills')
    op.drop_column('candidates', 'created_on')
    op.drop_column('candidates', 'updated_on')
    op.drop_column('candidates', 'timezone')
    op.drop_column('candidates', 'candidate_notes')

    # Remove currency default
    op.alter_column('candidates', 'currency', server_default=None)
