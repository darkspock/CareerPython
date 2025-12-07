"""add_in_app_notifications_table

Revision ID: bdc7f8f711e4
Revises: dba5b34b4c44
Create Date: 2025-12-07 15:36:24.726233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bdc7f8f711e4'
down_revision: Union[str, Sequence[str], None] = 'dba5b34b4c44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'in_app_notifications',
        sa.Column('id', sa.String(26), primary_key=True),
        sa.Column('user_id', sa.String(26), nullable=False, index=True),
        sa.Column('company_id', sa.String(26), nullable=False, index=True),
        sa.Column('notification_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('priority', sa.String(20), nullable=False, server_default='NORMAL'),
        sa.Column('is_read', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('read_at', sa.DateTime, nullable=True),
        sa.Column('link', sa.String(500), nullable=True),
        sa.Column('metadata', sa.JSON, nullable=True),
    )

    # Create composite indexes for efficient queries
    op.create_index(
        'ix_in_app_notifications_user_company',
        'in_app_notifications',
        ['user_id', 'company_id']
    )
    op.create_index(
        'ix_in_app_notifications_user_unread',
        'in_app_notifications',
        ['user_id', 'company_id', 'is_read']
    )
    op.create_index(
        'ix_in_app_notifications_created',
        'in_app_notifications',
        ['user_id', 'company_id', 'created_at']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_in_app_notifications_created', table_name='in_app_notifications')
    op.drop_index('ix_in_app_notifications_user_unread', table_name='in_app_notifications')
    op.drop_index('ix_in_app_notifications_user_company', table_name='in_app_notifications')
    op.drop_table('in_app_notifications')
