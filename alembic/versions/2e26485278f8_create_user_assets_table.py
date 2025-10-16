"""create_user_assets_table

Revision ID: 2e26485278f8
Revises: 4e2e1a8dbcb1
Create Date: 2025-10-08 13:26:41.529334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e26485278f8'
down_revision: Union[str, Sequence[str], None] = '4e2e1a8dbcb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create asset type enum if it doesn't exist
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE assettypeenum AS ENUM ('pdf_resume', 'linkedin_profile', 'portfolio', 'cover_letter');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create processing status enum if it doesn't exist
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE processingstatusenum AS ENUM ('pending', 'processing', 'completed', 'failed');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create user_assets table
    op.create_table('user_assets',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('asset_type', sa.Enum('pdf_resume', 'linkedin_profile', 'portfolio', 'cover_letter', name='assettypeenum'), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('content_type', sa.String(), nullable=True),
        sa.Column('processing_status', sa.Enum('pending', 'processing', 'completed', 'failed', name='processingstatusenum'), nullable=False),
        sa.Column('processing_error', sa.Text(), nullable=True),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('file_metadata', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_assets_asset_type'), 'user_assets', ['asset_type'], unique=False)
    op.create_index(op.f('ix_user_assets_id'), 'user_assets', ['id'], unique=False)
    op.create_index(op.f('ix_user_assets_processing_status'), 'user_assets', ['processing_status'], unique=False)
    op.create_index(op.f('ix_user_assets_user_id'), 'user_assets', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_user_assets_user_id'), table_name='user_assets')
    op.drop_index(op.f('ix_user_assets_processing_status'), table_name='user_assets')
    op.drop_index(op.f('ix_user_assets_id'), table_name='user_assets')
    op.drop_index(op.f('ix_user_assets_asset_type'), table_name='user_assets')
    op.drop_table('user_assets')
    # Drop the enum types
    op.execute('DROP TYPE IF EXISTS assettypeenum')
    op.execute('DROP TYPE IF EXISTS processingstatusenum')
