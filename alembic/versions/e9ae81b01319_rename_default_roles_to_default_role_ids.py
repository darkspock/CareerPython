"""rename_default_roles_to_default_role_ids

Revision ID: e9ae81b01319
Revises: 86a84be79d89
Create Date: 2025-10-25 23:56:07.298988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9ae81b01319'
down_revision: Union[str, Sequence[str], None] = '86a84be79d89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename default_roles column to default_role_ids in workflow_stages table."""
    # Rename column from default_roles to default_role_ids
    op.alter_column('workflow_stages', 'default_roles', new_column_name='default_role_ids')


def downgrade() -> None:
    """Revert default_role_ids column back to default_roles."""
    # Rename column back from default_role_ids to default_roles
    op.alter_column('workflow_stages', 'default_role_ids', new_column_name='default_roles')
