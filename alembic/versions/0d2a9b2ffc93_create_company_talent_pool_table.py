"""create_company_talent_pool_table

Revision ID: 0d2a9b2ffc93
Revises: 83e7b78ffa8a
Create Date: 2025-10-26 21:22:14.235676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d2a9b2ffc93'
down_revision: Union[str, Sequence[str], None] = '83e7b78ffa8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create company_talent_pool table
    op.create_table(
        'company_talent_pool',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('company_id', sa.String(length=36), nullable=False),
        sa.Column('candidate_id', sa.String(length=36), nullable=False),
        sa.Column('source_application_id', sa.String(length=36), nullable=True),
        sa.Column('source_position_id', sa.String(length=36), nullable=True),
        sa.Column('added_reason', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('added_by_user_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_company_talent_pool_company_id', 'company_talent_pool', ['company_id'])
    op.create_index('ix_company_talent_pool_candidate_id', 'company_talent_pool', ['candidate_id'])
    op.create_index('ix_company_talent_pool_status', 'company_talent_pool', ['status'])
    op.create_index('ix_company_talent_pool_rating', 'company_talent_pool', ['rating'])

    # Create unique constraint to prevent duplicate entries
    op.create_unique_constraint(
        'uq_company_talent_pool_company_candidate',
        'company_talent_pool',
        ['company_id', 'candidate_id']
    )

    # Create foreign keys
    op.create_foreign_key(
        'fk_company_talent_pool_company_id',
        'company_talent_pool',
        'companies',
        ['company_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_company_talent_pool_candidate_id',
        'company_talent_pool',
        'candidates',
        ['candidate_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign keys
    op.drop_constraint('fk_company_talent_pool_candidate_id', 'company_talent_pool', type_='foreignkey')
    op.drop_constraint('fk_company_talent_pool_company_id', 'company_talent_pool', type_='foreignkey')

    # Drop unique constraint
    op.drop_constraint('uq_company_talent_pool_company_candidate', 'company_talent_pool', type_='unique')

    # Drop indexes
    op.drop_index('ix_company_talent_pool_rating', 'company_talent_pool')
    op.drop_index('ix_company_talent_pool_status', 'company_talent_pool')
    op.drop_index('ix_company_talent_pool_candidate_id', 'company_talent_pool')
    op.drop_index('ix_company_talent_pool_company_id', 'company_talent_pool')

    # Drop table
    op.drop_table('company_talent_pool')
