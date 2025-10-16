"""add_employment_type_to_job_positions

Revision ID: be9c4f10a5e0
Revises: d31ae0754ad3
Create Date: 2025-10-07 21:29:53.759914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be9c4f10a5e0'
down_revision: Union[str, Sequence[str], None] = 'd31ae0754ad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create EmploymentType enum in database
    op.execute("""
    CREATE TYPE employmenttype AS ENUM (
        'full_time', 'part_time', 'contract', 'temporary', 'internship', 'volunteer', 'other'
    );
    """)

    # Add employment_type column to job_positions table
    op.add_column('job_positions', sa.Column('employment_type', sa.Enum('full_time', 'part_time', 'contract', 'temporary', 'internship', 'volunteer', 'other', name='employmenttype'), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove employment_type column
    op.drop_column('job_positions', 'employment_type')

    # Drop EmploymentType enum
    op.execute("DROP TYPE employmenttype;");
