"""add_user_registrations_table

Revision ID: 8c6c3906e50c
Revises: 7bbe4dc2824a
Create Date: 2025-12-14 17:12:09.596325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8c6c3906e50c'
down_revision: Union[str, Sequence[str], None] = '7bbe4dc2824a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create user_registrations table."""
    op.create_table('user_registrations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('verification_token', sa.String(length=64), nullable=False),
        sa.Column('token_expires_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('processing_status', sa.String(length=20), nullable=False),
        sa.Column('company_id', sa.String(), nullable=True),
        sa.Column('job_position_id', sa.String(), nullable=True),
        sa.Column('existing_user_id', sa.String(), nullable=True),
        sa.Column('file_name', sa.String(length=255), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('content_type', sa.String(length=100), nullable=True),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('extracted_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index(op.f('ix_user_registrations_company_id'), 'user_registrations', ['company_id'], unique=False)
    op.create_index(op.f('ix_user_registrations_email'), 'user_registrations', ['email'], unique=False)
    op.create_index(op.f('ix_user_registrations_existing_user_id'), 'user_registrations', ['existing_user_id'], unique=False)
    op.create_index(op.f('ix_user_registrations_id'), 'user_registrations', ['id'], unique=False)
    op.create_index(op.f('ix_user_registrations_job_position_id'), 'user_registrations', ['job_position_id'], unique=False)
    op.create_index(op.f('ix_user_registrations_processing_status'), 'user_registrations', ['processing_status'], unique=False)
    op.create_index(op.f('ix_user_registrations_status'), 'user_registrations', ['status'], unique=False)
    op.create_index(op.f('ix_user_registrations_verification_token'), 'user_registrations', ['verification_token'], unique=True)


def downgrade() -> None:
    """Drop user_registrations table."""
    op.drop_index(op.f('ix_user_registrations_verification_token'), table_name='user_registrations')
    op.drop_index(op.f('ix_user_registrations_status'), table_name='user_registrations')
    op.drop_index(op.f('ix_user_registrations_processing_status'), table_name='user_registrations')
    op.drop_index(op.f('ix_user_registrations_job_position_id'), table_name='user_registrations')
    op.drop_index(op.f('ix_user_registrations_id'), table_name='user_registrations')
    op.drop_index(op.f('ix_user_registrations_existing_user_id'), table_name='user_registrations')
    op.drop_index(op.f('ix_user_registrations_email'), table_name='user_registrations')
    op.drop_index(op.f('ix_user_registrations_company_id'), table_name='user_registrations')
    op.drop_table('user_registrations')
