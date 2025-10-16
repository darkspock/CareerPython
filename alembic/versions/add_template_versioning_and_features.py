"""Add template versioning and advanced features

Revision ID: add_template_versioning
Revises:
Create Date: 2025-01-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_template_versioning'
down_revision = None  # This should be set to the latest migration
branch_labels = None
depends_on = None


def upgrade():
    """Add versioning and advanced features to interview templates"""

    # Add versioning columns
    op.add_column('interview_templates', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('interview_templates', sa.Column('is_current_version', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('interview_templates', sa.Column('parent_template_id', sa.String(), nullable=True))

    # Add extended metadata columns
    op.add_column('interview_templates', sa.Column('created_by', sa.String(), nullable=True))
    op.add_column('interview_templates', sa.Column('tags', sa.JSON(), nullable=True))
    op.add_column('interview_templates', sa.Column('metadata', sa.JSON(), nullable=True))

    # Create new indexes for versioning and performance
    op.create_index('idx_version_current', 'interview_templates', ['id', 'version', 'is_current_version'])
    op.create_index('idx_created_by_status', 'interview_templates', ['created_by', 'status'])
    op.create_index('idx_parent_template', 'interview_templates', ['parent_template_id'])
    op.create_index('idx_version', 'interview_templates', ['version'])
    op.create_index('idx_is_current_version', 'interview_templates', ['is_current_version'])

    # Update existing data to set default values
    op.execute("UPDATE interview_templates SET version = 1 WHERE version IS NULL")
    op.execute("UPDATE interview_templates SET is_current_version = true WHERE is_current_version IS NULL")


def downgrade():
    """Remove versioning and advanced features from interview templates"""

    # Drop indexes
    op.drop_index('idx_is_current_version', table_name='interview_templates')
    op.drop_index('idx_version', table_name='interview_templates')
    op.drop_index('idx_parent_template', table_name='interview_templates')
    op.drop_index('idx_created_by_status', table_name='interview_templates')
    op.drop_index('idx_version_current', table_name='interview_templates')

    # Drop columns
    op.drop_column('interview_templates', 'metadata')
    op.drop_column('interview_templates', 'tags')
    op.drop_column('interview_templates', 'created_by')
    op.drop_column('interview_templates', 'parent_template_id')
    op.drop_column('interview_templates', 'is_current_version')
    op.drop_column('interview_templates', 'version')