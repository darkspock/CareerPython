"""add company_type to companies

Revision ID: 493fdfc86996
Revises: dd9eeff66209
Create Date: 2025-11-09 22:12:16.411271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '493fdfc86996'
down_revision: Union[str, Sequence[str], None] = 'dd9eeff66209'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if column already exists (it was added manually before)
    from sqlalchemy import inspect
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('companies')]
    
    if 'company_type' not in columns:
        # Add company_type column
        op.add_column('companies', sa.Column('company_type', sa.Enum('startup_small', 'mid_size', 'enterprise', 'recruitment_agency', name='companytypeenum', native_enum=False, length=30), nullable=True, server_default='mid_size'))
        
        # Update existing records to 'mid_size'
        op.execute("UPDATE companies SET company_type = 'mid_size' WHERE company_type IS NULL")
        
        # Make column NOT NULL after updating existing records
        op.alter_column('companies', 'company_type', nullable=False)
    else:
        # Column already exists, just update NULL values
        op.execute("UPDATE companies SET company_type = 'mid_size' WHERE company_type IS NULL")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('companies', 'company_type')
