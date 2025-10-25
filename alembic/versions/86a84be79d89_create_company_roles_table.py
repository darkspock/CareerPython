"""create_company_roles_table

Revision ID: 86a84be79d89
Revises: 01c58d14cc89
Create Date: 2025-10-25 23:19:12.126943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86a84be79d89'
down_revision: Union[str, Sequence[str], None] = '01c58d14cc89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create company_roles table."""
    op.create_table(
        'company_roles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    )
    op.create_index('ix_company_roles_id', 'company_roles', ['id'])
    op.create_index('ix_company_roles_company_id', 'company_roles', ['company_id'])

    # Create unique constraint for company_id + name
    op.create_unique_constraint('uq_company_roles_company_name', 'company_roles', ['company_id', 'name'])


def downgrade() -> None:
    """Drop company_roles table."""
    op.drop_index('ix_company_roles_company_id', 'company_roles')
    op.drop_index('ix_company_roles_id', 'company_roles')
    op.drop_table('company_roles')
