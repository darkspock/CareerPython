"""rename_current_roles_to_desired_roles

Revision ID: f52d88709135
Revises: be9c4f10a5e0
Create Date: 2025-10-07 21:40:10.159318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f52d88709135'
down_revision: Union[str, Sequence[str], None] = 'be9c4f10a5e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename current_roles column to desired_roles
    op.alter_column('job_positions', 'current_roles', new_column_name='desired_roles')


def downgrade() -> None:
    """Downgrade schema."""
    # Rename desired_roles column back to current_roles
    op.alter_column('job_positions', 'desired_roles', new_column_name='current_roles')
