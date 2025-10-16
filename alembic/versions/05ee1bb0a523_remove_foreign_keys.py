"""remove_foreign_keys

Revision ID: 05ee1bb0a523
Revises: 227aa7de74e5
Create Date: 2025-10-08 16:07:02.660084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05ee1bb0a523'
down_revision: Union[str, Sequence[str], None] = '227aa7de74e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove foreign key constraints
    op.drop_constraint('user_assets_user_id_fkey', 'user_assets', type_='foreignkey')
    op.drop_constraint('companies_user_id_fkey', 'companies', type_='foreignkey')
    op.drop_constraint('job_applications_user_id_fkey', 'job_applications', type_='foreignkey')
    op.drop_constraint('resumes_user_id_fkey', 'resumes', type_='foreignkey')
    op.drop_constraint('usage_tracking_user_id_fkey', 'usage_tracking', type_='foreignkey')


def downgrade() -> None:
    """Downgrade schema."""
    # Re-add foreign key constraints
    op.create_foreign_key('user_assets_user_id_fkey', 'user_assets', 'users', ['user_id'], ['id'])
    op.create_foreign_key('companies_user_id_fkey', 'companies', 'users', ['user_id'], ['id'])
    op.create_foreign_key('job_applications_user_id_fkey', 'job_applications', 'users', ['user_id'], ['id'])
    op.create_foreign_key('resumes_user_id_fkey', 'resumes', 'users', ['user_id'], ['id'])
    op.create_foreign_key('usage_tracking_user_id_fkey', 'usage_tracking', 'users', ['user_id'], ['id'])
