"""Add legal_notice and AI config fields to interview templates

Revision ID: 380733ccdc4d
Revises: 08991b6544de
Create Date: 2025-10-19 01:05:36.282412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '380733ccdc4d'
down_revision: Union[str, Sequence[str], None] = '08991b6544de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new columns to interview_templates table
    op.add_column('interview_templates', sa.Column('allow_ai_questions', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('interview_templates', sa.Column('legal_notice', sa.Text(), nullable=True))

    # Add new columns to interview_template_sections table
    op.add_column('interview_template_sections', sa.Column('allow_ai_questions', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('interview_template_sections', sa.Column('allow_ai_override_questions', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('interview_template_sections', sa.Column('legal_notice', sa.Text(), nullable=True))

    # Add new columns to interview_template_questions table
    op.add_column('interview_template_questions', sa.Column('allow_ai_followup', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('interview_template_questions', sa.Column('legal_notice', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove columns from interview_template_questions table
    op.drop_column('interview_template_questions', 'legal_notice')
    op.drop_column('interview_template_questions', 'allow_ai_followup')

    # Remove columns from interview_template_sections table
    op.drop_column('interview_template_sections', 'legal_notice')
    op.drop_column('interview_template_sections', 'allow_ai_override_questions')
    op.drop_column('interview_template_sections', 'allow_ai_questions')

    # Remove columns from interview_templates table
    op.drop_column('interview_templates', 'legal_notice')
    op.drop_column('interview_templates', 'allow_ai_questions')
