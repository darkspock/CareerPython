"""add_phase_status_field

Revision ID: 2a372a9e65de
Revises: add_slug_to_companies
Create Date: 2025-10-28 09:28:47.358504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a372a9e65de'
down_revision: Union[str, Sequence[str], None] = 'add_slug_to_companies'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create ENUM type for phase status
    op.execute("CREATE TYPE phasestatus AS ENUM ('DRAFT', 'ACTIVE', 'ARCHIVED')")

    # Add status column with default value ACTIVE
    op.add_column('company_phases',
        sa.Column('status', sa.Enum('DRAFT', 'ACTIVE', 'ARCHIVED', name='phasestatus', create_type=False),
                  nullable=False, server_default='ACTIVE'))

    # Create index on status column
    op.create_index('ix_company_phases_status', 'company_phases', ['status'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop index
    op.drop_index('ix_company_phases_status', 'company_phases')

    # Drop column
    op.drop_column('company_phases', 'status')

    # Drop ENUM type
    op.execute("DROP TYPE phasestatus")
