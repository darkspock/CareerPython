"""create_resumes_table

Revision ID: 757a00387070
Revises: 05ee1bb0a523
Create Date: 2025-10-10 18:44:16.312262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '757a00387070'
down_revision: Union[str, Sequence[str], None] = '05ee1bb0a523'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create resumes table
    op.create_table(
        'resumes',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('candidate_id', sa.String(), sa.ForeignKey('candidates.id'), nullable=False, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('resume_type', sa.String(50), nullable=False, index=True),
        sa.Column('status', sa.String(50), nullable=False, default='DRAFT', index=True),
        sa.Column('ai_enhancement_status', sa.String(50), nullable=False, default='NOT_REQUESTED'),

        # Content columns
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('key_aspects', sa.JSON(), nullable=True),
        sa.Column('intro_letter', sa.Text(), nullable=True),
        sa.Column('skills', sa.JSON(), nullable=True),
        sa.Column('achievements', sa.JSON(), nullable=True),

        # AI generated content columns
        sa.Column('ai_summary', sa.Text(), nullable=True),
        sa.Column('ai_key_aspects', sa.JSON(), nullable=True),
        sa.Column('ai_skills_recommendations', sa.JSON(), nullable=True),
        sa.Column('ai_achievements', sa.JSON(), nullable=True),
        sa.Column('ai_intro_letter', sa.Text(), nullable=True),

        # Formatting preferences
        sa.Column('template', sa.String(100), nullable=False, default='modern'),
        sa.Column('color_scheme', sa.String(50), nullable=False, default='blue'),
        sa.Column('font_family', sa.String(100), nullable=False, default='Arial'),
        sa.Column('include_photo', sa.Boolean(), nullable=False, default=False),
        sa.Column('sections_order', sa.JSON(), nullable=True),

        # Additional data
        sa.Column('general_data', sa.JSON(), nullable=True),
        sa.Column('custom_content', sa.JSON(), nullable=True),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('resumes')
