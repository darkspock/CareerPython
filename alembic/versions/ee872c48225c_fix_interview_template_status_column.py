"""fix_interview_template_status_column

Revision ID: ee872c48225c
Revises: d2010b29f497
Create Date: 2025-10-02 21:37:44.149663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee872c48225c'
down_revision: Union[str, Sequence[str], None] = 'd2010b29f497'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if status column exists before adding it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('interview_templates')]

    if 'status' not in columns:
        # Add status column with enum type
        op.execute("CREATE TYPE interviewtemplatestatusenum AS ENUM ('ENABLED', 'DRAFT', 'DISABLED')")
        op.add_column('interview_templates',
                     sa.Column('status',
                              sa.Enum('ENABLED', 'DRAFT', 'DISABLED', name='interviewtemplatestatusenum'),
                              nullable=False,
                              server_default='DRAFT'))

        # Add indexes that were missing
        op.create_index('idx_status_type', 'interview_templates', ['status', 'type'])
        op.create_index('idx_job_category_status', 'interview_templates', ['job_category', 'status'])
        op.create_index('idx_created_by_status', 'interview_templates', ['created_by', 'status'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove indexes first
    op.drop_index('idx_created_by_status', table_name='interview_templates')
    op.drop_index('idx_job_category_status', table_name='interview_templates')
    op.drop_index('idx_status_type', table_name='interview_templates')

    # Remove status column
    op.drop_column('interview_templates', 'status')

    # Drop enum type
    op.execute("DROP TYPE IF EXISTS interviewtemplatestatusenum")
