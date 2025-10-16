"""create_resume_tables_fixed

Revision ID: 8ea7f0f899f6
Revises: aaf599e723e6
Create Date: 2025-09-22 18:15:37.807878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ea7f0f899f6'
down_revision: Union[str, Sequence[str], None] = 'aaf599e723e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create resumes table (enum already exists)
    op.create_table('resumes',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('candidate_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('resume_type', sa.Enum('GENERAL', 'POSITION', 'ROLE', name='resumetype', create_type=False), nullable=False),
    sa.Column('position_id', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('content_data', sa.JSON(), nullable=True),
    sa.Column('ai_content', sa.JSON(), nullable=True),
    sa.Column('custom_content', sa.JSON(), nullable=True),
    sa.Column('formatting_preferences', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('last_generated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for resumes table
    op.create_index('idx_resume_candidate_type', 'resumes', ['candidate_id', 'resume_type'], unique=False)
    op.create_index('idx_resume_created_at', 'resumes', ['created_at'], unique=False)
    op.create_index('idx_resume_user_type', 'resumes', ['user_id', 'resume_type'], unique=False)
    op.create_index(op.f('ix_resumes_candidate_id'), 'resumes', ['candidate_id'], unique=False)
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)
    op.create_index(op.f('ix_resumes_resume_type'), 'resumes', ['resume_type'], unique=False)
    op.create_index(op.f('ix_resumes_user_id'), 'resumes', ['user_id'], unique=False)
    
    # Create resume_versions table
    op.create_table('resume_versions',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('resume_id', sa.String(), nullable=False),
    sa.Column('version_number', sa.Integer(), nullable=False),
    sa.Column('content_snapshot', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_action', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for resume_versions table
    op.create_index('idx_resume_version_created_at', 'resume_versions', ['created_at'], unique=False)
    op.create_index('idx_resume_version_number', 'resume_versions', ['resume_id', 'version_number'], unique=False)
    op.create_index('idx_resume_version_resume_id', 'resume_versions', ['resume_id'], unique=False)
    op.create_index(op.f('ix_resume_versions_id'), 'resume_versions', ['id'], unique=False)
    op.create_index(op.f('ix_resume_versions_resume_id'), 'resume_versions', ['resume_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop resume_versions table and its indexes
    op.drop_index(op.f('ix_resume_versions_resume_id'), table_name='resume_versions')
    op.drop_index(op.f('ix_resume_versions_id'), table_name='resume_versions')
    op.drop_index('idx_resume_version_resume_id', table_name='resume_versions')
    op.drop_index('idx_resume_version_number', table_name='resume_versions')
    op.drop_index('idx_resume_version_created_at', table_name='resume_versions')
    op.drop_table('resume_versions')
    
    # Drop resumes table and its indexes
    op.drop_index(op.f('ix_resumes_user_id'), table_name='resumes')
    op.drop_index(op.f('ix_resumes_resume_type'), table_name='resumes')
    op.drop_index(op.f('ix_resumes_id'), table_name='resumes')
    op.drop_index(op.f('ix_resumes_candidate_id'), table_name='resumes')
    op.drop_index('idx_resume_user_type', table_name='resumes')
    op.drop_index('idx_resume_created_at', table_name='resumes')
    op.drop_index('idx_resume_candidate_type', table_name='resumes')
    op.drop_table('resumes')
