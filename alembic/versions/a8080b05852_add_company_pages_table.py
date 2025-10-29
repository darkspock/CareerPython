"""add company_pages table

Revision ID: a8080b05852
Revises: f5fe2ada03f2
Create Date: 2025-01-25 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a8080b05852'
down_revision = 'f5fe2ada03f2'
branch_labels = None
depends_on = None


def upgrade():
    """Add company_pages table"""
    # Create company_pages table
    op.create_table('company_pages',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('company_id', sa.String(length=255), nullable=False),
        sa.Column('page_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('html_content', sa.Text(), nullable=False),
        sa.Column('plain_text', sa.Text(), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=False),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('meta_keywords', sa.JSON(), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=True, default='es'),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('is_default', sa.Boolean(), nullable=True, default=False),
        sa.Column('version', sa.Integer(), nullable=True, default=1),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for performance
    op.create_index('idx_company_page_company_type', 'company_pages', ['company_id', 'page_type'])
    op.create_index('idx_company_page_status', 'company_pages', ['status'])
    op.create_index('idx_company_page_default', 'company_pages', ['company_id', 'page_type', 'is_default'])
    op.create_index('idx_company_page_company_status', 'company_pages', ['company_id', 'status'])
    op.create_index('idx_company_page_published', 'company_pages', ['company_id', 'status', 'published_at'])


def downgrade():
    """Remove company_pages table"""
    # Drop indexes
    op.drop_index('idx_company_page_published', table_name='company_pages')
    op.drop_index('idx_company_page_company_status', table_name='company_pages')
    op.drop_index('idx_company_page_default', table_name='company_pages')
    op.drop_index('idx_company_page_status', table_name='company_pages')
    op.drop_index('idx_company_page_company_type', table_name='company_pages')
    
    # Drop table
    op.drop_table('company_pages')
