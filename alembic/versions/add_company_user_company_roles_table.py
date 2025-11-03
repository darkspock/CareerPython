"""add_company_user_company_roles_table

Revision ID: add_company_user_company_roles
Revises: 01k91yvpra1r
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_company_user_company_roles'
down_revision: Union[str, Sequence[str], None] = '01k91yvpra1r'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create company_user_company_roles table."""
    op.create_table(
        'company_user_company_roles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_user_id', sa.String(), nullable=False),
        sa.Column('company_role_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_user_id'], ['company_users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['company_role_id'], ['company_roles.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('company_user_id', 'company_role_id', name='uq_company_user_role'),
    )
    op.create_index('ix_company_user_company_roles_id', 'company_user_company_roles', ['id'])
    op.create_index('ix_company_user_company_roles_company_user_id', 'company_user_company_roles', ['company_user_id'])
    op.create_index('ix_company_user_company_roles_company_role_id', 'company_user_company_roles', ['company_role_id'])


def downgrade() -> None:
    """Drop company_user_company_roles table."""
    op.drop_index('ix_company_user_company_roles_company_role_id', 'company_user_company_roles')
    op.drop_index('ix_company_user_company_roles_company_user_id', 'company_user_company_roles')
    op.drop_index('ix_company_user_company_roles_id', 'company_user_company_roles')
    op.drop_table('company_user_company_roles')

