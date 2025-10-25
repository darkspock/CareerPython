"""remove obsolete company columns

Revision ID: e01d8be86325
Revises: d39d547ee84c
Create Date: 2025-10-25 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e01d8be86325'
down_revision: Union[str, Sequence[str], None] = 'd39d547ee84c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Remove obsolete columns from companies table.
    These columns are no longer part of the simplified Company domain model.
    """
    # Drop obsolete columns from companies table
    op.drop_column('companies', 'user_id')
    op.drop_column('companies', 'sector')
    op.drop_column('companies', 'size')
    op.drop_column('companies', 'location')
    op.drop_column('companies', 'website')
    op.drop_column('companies', 'culture')
    op.drop_column('companies', 'external_data')


def downgrade() -> None:
    """
    Restore obsolete columns to companies table.
    Note: Data will be lost and cannot be recovered.
    """
    # Restore columns (data will be NULL)
    op.add_column('companies', sa.Column('external_data', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('companies', sa.Column('culture', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('companies', sa.Column('website', sa.String(), nullable=True))
    op.add_column('companies', sa.Column('location', sa.String(), nullable=True))
    op.add_column('companies', sa.Column('size', sa.Integer(), nullable=True))
    op.add_column('companies', sa.Column('sector', sa.String(), nullable=True))
    op.add_column('companies', sa.Column('user_id', sa.String(), nullable=True))
