"""Add company_user_invitation table

Revision ID: 01k91yvpra1r
Revises: 7ea4622d4941
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01k91yvpra1r'
down_revision: Union[str, Sequence[str], None] = '7ea4622d4941'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'company_user_invitations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('invited_by_user_id', sa.String(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('accepted_at', sa.DateTime(), nullable=True),
        sa.Column('rejected_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['invited_by_user_id'], ['company_users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token', name='uq_invitation_token')
    )
    
    # Create indexes
    op.create_index(op.f('ix_company_user_invitations_id'), 'company_user_invitations', ['id'], unique=False)
    op.create_index(op.f('ix_company_user_invitations_company_id'), 'company_user_invitations', ['company_id'], unique=False)
    op.create_index(op.f('ix_company_user_invitations_email'), 'company_user_invitations', ['email'], unique=False)
    op.create_index(op.f('ix_company_user_invitations_token'), 'company_user_invitations', ['token'], unique=False)
    op.create_index('ix_invitation_email_company', 'company_user_invitations', ['email', 'company_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_invitation_email_company', table_name='company_user_invitations')
    op.drop_index(op.f('ix_company_user_invitations_token'), table_name='company_user_invitations')
    op.drop_index(op.f('ix_company_user_invitations_email'), table_name='company_user_invitations')
    op.drop_index(op.f('ix_company_user_invitations_company_id'), table_name='company_user_invitations')
    op.drop_index(op.f('ix_company_user_invitations_id'), table_name='company_user_invitations')
    op.drop_table('company_user_invitations')

