"""Add scope field to interview_templates

Revision ID: 79505323db15
Revises: 509c56276b78
Create Date: 2025-12-09 23:49:33.566298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '79505323db15'
down_revision: Union[str, Sequence[str], None] = '509c56276b78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add scope column to interview_templates."""
    # Create the enum type first
    interviewtemplatescopeenum = sa.Enum('PIPELINE', 'APPLICATION', 'STANDALONE', name='interviewtemplatescopeenum')
    interviewtemplatescopeenum.create(op.get_bind(), checkfirst=True)

    # Add the column with a default value
    op.add_column('interview_templates', sa.Column(
        'scope',
        sa.Enum('PIPELINE', 'APPLICATION', 'STANDALONE', name='interviewtemplatescopeenum'),
        nullable=False,
        server_default='STANDALONE'
    ))

    # Create index for the new column
    op.create_index(op.f('ix_interview_templates_scope'), 'interview_templates', ['scope'], unique=False)

    # Migrate existing SCREENING templates to have scope=APPLICATION
    op.execute("""
        UPDATE interview_templates
        SET scope = 'APPLICATION'
        WHERE type = 'SCREENING'
    """)


def downgrade() -> None:
    """Remove scope column from interview_templates."""
    op.drop_index(op.f('ix_interview_templates_scope'), table_name='interview_templates')
    op.drop_column('interview_templates', 'scope')

    # Drop the enum type
    sa.Enum(name='interviewtemplatescopeenum').drop(op.get_bind(), checkfirst=True)
