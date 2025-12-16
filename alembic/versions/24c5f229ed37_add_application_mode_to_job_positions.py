"""add_application_mode_to_job_positions

Revision ID: 24c5f229ed37
Revises: 8c6c3906e50c
Create Date: 2025-12-16 20:02:50.584591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '24c5f229ed37'
down_revision: Union[str, Sequence[str], None] = '8c6c3906e50c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add application_mode and required_sections to job_positions table."""
    # Add application_mode column with default 'short'
    op.add_column('job_positions', sa.Column(
        'application_mode',
        sa.String(length=20),
        nullable=False,
        server_default='short'
    ))

    # Add required_sections column (JSON array)
    op.add_column('job_positions', sa.Column(
        'required_sections',
        sa.JSON(),
        nullable=True
    ))


def downgrade() -> None:
    """Remove application_mode and required_sections from job_positions table."""
    op.drop_column('job_positions', 'required_sections')
    op.drop_column('job_positions', 'application_mode')
