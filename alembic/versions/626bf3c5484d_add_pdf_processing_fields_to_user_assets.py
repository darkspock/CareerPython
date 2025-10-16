"""add_pdf_processing_fields_to_user_assets

Revision ID: 626bf3c5484d
Revises: 8834d0700341
Create Date: 2025-09-17 12:07:50.694120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '626bf3c5484d'
down_revision: Union[str, Sequence[str], None] = '8834d0700341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add PDF processing metadata columns to user_assets table
    op.add_column('user_assets', sa.Column('file_name', sa.String(), nullable=True))
    op.add_column('user_assets', sa.Column('file_size', sa.Integer(), nullable=True))
    op.add_column('user_assets', sa.Column('content_type', sa.String(), nullable=True))
    op.add_column('user_assets', sa.Column('processing_status', sa.String(), nullable=True, server_default='pending'))
    op.add_column('user_assets', sa.Column('processing_error', sa.Text(), nullable=True))
    op.add_column('user_assets', sa.Column('text_content', sa.Text(), nullable=True))
    op.add_column('user_assets', sa.Column('file_metadata', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove PDF processing metadata columns from user_assets table
    op.drop_column('user_assets', 'file_metadata')
    op.drop_column('user_assets', 'text_content')
    op.drop_column('user_assets', 'processing_error')
    op.drop_column('user_assets', 'processing_status')
    op.drop_column('user_assets', 'content_type')
    op.drop_column('user_assets', 'file_size')
    op.drop_column('user_assets', 'file_name')
