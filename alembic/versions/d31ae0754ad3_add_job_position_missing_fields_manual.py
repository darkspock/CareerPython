"""add_job_position_missing_fields_manual

Revision ID: d31ae0754ad3
Revises: 7e2f70c545ab
Create Date: 2025-10-07 12:34:29.468653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd31ae0754ad3'
down_revision: Union[str, Sequence[str], None] = 'c0a26ba41d13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add missing fields to job_positions table
    op.add_column('job_positions', sa.Column('skills', sa.JSON(), nullable=True))
    op.add_column('job_positions', sa.Column('application_url', sa.String(), nullable=True))
    op.add_column('job_positions', sa.Column('application_email', sa.String(), nullable=True))

    # Change description column from String to Text
    op.alter_column('job_positions', 'description',
                    existing_type=sa.String(),
                    type_=sa.Text(),
                    nullable=True)

    # Remove priority_level column if it exists
    try:
        op.drop_column('job_positions', 'priority_level')
    except Exception:
        # Column might not exist, ignore error
        pass

    # Change position_level from String to Enum if the table exists
    # Note: This would need the enum to be created first, but for now we'll leave it as String
    # op.alter_column('job_positions', 'position_level',
    #                 existing_type=sa.String(),
    #                 type_=sa.Enum('JUNIOR', 'MID', 'SENIOR', 'LEAD', name='jobpositionlevelenum'),
    #                 nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove added fields
    op.drop_column('job_positions', 'application_email')
    op.drop_column('job_positions', 'application_url')
    op.drop_column('job_positions', 'skills')

    # Change description back from Text to String
    op.alter_column('job_positions', 'description',
                    existing_type=sa.Text(),
                    type_=sa.String(),
                    nullable=True)

    # Add back priority_level column
    op.add_column('job_positions', sa.Column('priority_level', sa.String(), nullable=True, default='medium'))
