"""add_killer_questions_to_job_position

Revision ID: bd1f13e202d6
Revises: 79505323db15
Create Date: 2025-12-11 01:00:50.190322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bd1f13e202d6'
down_revision: Union[str, Sequence[str], None] = '79505323db15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add killer_questions column to job_positions table."""
    op.add_column('job_positions', sa.Column('killer_questions', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Remove killer_questions column from job_positions table."""
    op.drop_column('job_positions', 'killer_questions')
