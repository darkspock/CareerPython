"""add_application_id_to_interviews

Revision ID: 0822302c5334
Revises: 757a00387070
Create Date: 2025-10-13 07:32:25.802996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0822302c5334'
down_revision: Union[str, Sequence[str], None] = '757a00387070'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add application_id column to interviews table
    op.add_column('interviews', sa.Column('application_id', sa.String(), nullable=True))

    # Create index on application_id for better query performance
    op.create_index(op.f('ix_interviews_application_id'), 'interviews', ['application_id'], unique=False)

    # Add foreign key constraint to candidate_applications table
    op.create_foreign_key(
        'fk_interviews_application_id_candidate_applications',
        'interviews',
        'candidate_applications',
        ['application_id'],
        ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key constraint
    op.drop_constraint('fk_interviews_application_id_candidate_applications', 'interviews', type_='foreignkey')

    # Drop index
    op.drop_index(op.f('ix_interviews_application_id'), table_name='interviews')

    # Drop application_id column
    op.drop_column('interviews', 'application_id')
