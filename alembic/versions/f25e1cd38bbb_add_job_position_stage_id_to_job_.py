"""add job_position_stage_id to job_position_comments

Revision ID: f25e1cd38bbb
Revises: 31a03ac9bc19
Create Date: 2025-11-08 08:40:02.997842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f25e1cd38bbb'
down_revision: Union[str, Sequence[str], None] = '31a03ac9bc19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add job_position_stage_id column to job_position_comments table
    op.add_column('job_position_comments', sa.Column('job_position_stage_id', sa.String(length=26), nullable=True))
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_job_position_comments_job_position_stage_id',
        'job_position_comments',
        'job_position_stages',
        ['job_position_stage_id'],
        ['id'],
        ondelete='SET NULL'
    )
    
    # Add index
    op.create_index(
        op.f('ix_job_position_comments_job_position_stage_id'),
        'job_position_comments',
        ['job_position_stage_id'],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_job_position_comments_job_position_stage_id'), table_name='job_position_comments')
    op.drop_constraint('fk_job_position_comments_job_position_stage_id', 'job_position_comments', type_='foreignkey')
    op.drop_column('job_position_comments', 'job_position_stage_id')
