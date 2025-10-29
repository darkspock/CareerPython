"""add style to workflow_stages

Revision ID: 1fea894de35f
Revises: 9e5f92b8d44f
Create Date: 2025-10-29 22:31:20.945508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fea894de35f'
down_revision: Union[str, Sequence[str], None] = '9e5f92b8d44f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add style column to workflow_stages table
    op.add_column('workflow_stages',
                  sa.Column('style', sa.JSON, nullable=True))

    # Update existing stages with default style based on stage_type
    from sqlalchemy import text
    
    # Set default styles for existing stages
    op.execute(text("""
        UPDATE workflow_stages 
        SET style = CASE 
            WHEN stage_type = 'SUCCESS' THEN '{"icon": "✅", "color": "#065f46", "background_color": "#d1fae5"}'::json
            WHEN stage_type = 'FAIL' THEN '{"icon": "❌", "color": "#991b1b", "background_color": "#fee2e2"}'::json
            WHEN stage_type = 'PROCESS' THEN '{"icon": "⚙️", "color": "#1e40af", "background_color": "#dbeafe"}'::json
            WHEN stage_type = 'REVIEW' THEN '{"icon": "👀", "color": "#92400e", "background_color": "#fef3c7"}'::json
            ELSE '{"icon": "📋", "color": "#374151", "background_color": "#f3f4f6"}'::json
        END
    """))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove style column from workflow_stages table
    op.drop_column('workflow_stages', 'style')
