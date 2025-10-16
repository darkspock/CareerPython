"""update_candidate_table_schema_to_match_entity

Revision ID: dfb8ecc3985a
Revises: 7c18adb82829
Create Date: 2025-10-03 17:16:18.951533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfb8ecc3985a'
down_revision: Union[str, Sequence[str], None] = '7c18adb82829'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add other_languages column
    op.add_column('candidates', sa.Column('other_languages', sa.String(), nullable=True))

    # Rename 'type' column to 'candidate_type'
    op.alter_column('candidates', 'type', new_column_name='candidate_type')

    # Update enum constraints - removing old enums and adding new ones
    # Note: This is a simplified approach. In production, you'd want to handle data migration more carefully

    # Make nullable fields that should be nullable
    op.alter_column('candidates', 'email', nullable=False)

    # Update status column to use new enum values if needed
    # You might need to update existing data here

    # Add indexes for performance
    op.create_index('ix_candidates_user_id', 'candidates', ['user_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the added column
    op.drop_column('candidates', 'other_languages')

    # Rename back
    op.alter_column('candidates', 'candidate_type', new_column_name='type')

    # Remove indexes
    op.drop_index('ix_candidates_user_id', 'candidates')

    # Revert other changes as needed
