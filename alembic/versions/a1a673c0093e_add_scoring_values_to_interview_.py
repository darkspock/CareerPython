"""add scoring_values to interview_template_questions

Revision ID: a1a673c0093e
Revises: 0506466d0c1b
Create Date: 2025-11-13 01:24:10.476337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1a673c0093e'
down_revision: Union[str, Sequence[str], None] = '0506466d0c1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('interview_template_questions', 
                  sa.Column('scoring_values', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('interview_template_questions', 'scoring_values')
