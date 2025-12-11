"""Add field_properties_config to workflow_stages

Revision ID: 7bbe4dc2824a
Revises: 9a9b358849b9
Create Date: 2025-12-11 23:25:42.881993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7bbe4dc2824a'
down_revision: Union[str, Sequence[str], None] = '9a9b358849b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add field_properties_config column to workflow_stages table."""
    op.add_column('workflow_stages', sa.Column('field_properties_config', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Remove field_properties_config column from workflow_stages table."""
    op.drop_column('workflow_stages', 'field_properties_config')
