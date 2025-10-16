"""create_candidate_applications_table

Revision ID: 4e2e1a8dbcb1
Revises: 3fb8aa54c17a
Create Date: 2025-10-08 13:19:58.032775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e2e1a8dbcb1'
down_revision: Union[str, Sequence[str], None] = '3fb8aa54c17a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create candidate_applications table
    op.create_table('candidate_applications',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('candidate_id', sa.String(), nullable=False),
        sa.Column('job_position_id', sa.String(), nullable=False),
        sa.Column('application_status', sa.Enum('applied', 'reviewing', 'interviewed', 'rejected', 'accepted', 'withdrawn', name='applicationstatusenum'), nullable=False),
        sa.Column('applied_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
        sa.ForeignKeyConstraint(['job_position_id'], ['job_positions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidate_applications_application_status'), 'candidate_applications', ['application_status'], unique=False)
    op.create_index(op.f('ix_candidate_applications_candidate_id'), 'candidate_applications', ['candidate_id'], unique=False)
    op.create_index(op.f('ix_candidate_applications_id'), 'candidate_applications', ['id'], unique=False)
    op.create_index(op.f('ix_candidate_applications_job_position_id'), 'candidate_applications', ['job_position_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_candidate_applications_job_position_id'), table_name='candidate_applications')
    op.drop_index(op.f('ix_candidate_applications_id'), table_name='candidate_applications')
    op.drop_index(op.f('ix_candidate_applications_candidate_id'), table_name='candidate_applications')
    op.drop_index(op.f('ix_candidate_applications_application_status'), table_name='candidate_applications')
    op.drop_table('candidate_applications')
    # Drop the enum type
    op.execute('DROP TYPE IF EXISTS applicationstatusenum')
