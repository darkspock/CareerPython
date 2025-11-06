"""rename company_workflows to candidate_application_workflows

Revision ID: 0cb15438510c
Revises: 2e865dcbd49e
Create Date: 2025-11-06 08:00:49.792028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cb15438510c'
down_revision: Union[str, Sequence[str], None] = '2e865dcbd49e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - rename company_workflows to candidate_application_workflows."""
    # Rename the table
    op.rename_table('company_workflows', 'candidate_application_workflows')
    
    # Rename indexes if they exist
    # Check and rename index on company_id if it exists
    try:
        op.execute("ALTER INDEX IF EXISTS ix_company_workflows_company_id RENAME TO ix_candidate_application_workflows_company_id")
    except:
        pass
    
    try:
        op.execute("ALTER INDEX IF EXISTS ix_company_workflows_id RENAME TO ix_candidate_application_workflows_id")
    except:
        pass
    
    try:
        op.execute("ALTER INDEX IF EXISTS ix_company_workflows_status RENAME TO ix_candidate_application_workflows_status")
    except:
        pass
    
    try:
        op.execute("ALTER INDEX IF EXISTS ix_company_workflows_is_default RENAME TO ix_candidate_application_workflows_is_default")
    except:
        pass
    
    try:
        op.execute("ALTER INDEX IF EXISTS ix_company_workflows_phase_id RENAME TO ix_candidate_application_workflows_phase_id")
    except:
        pass


def downgrade() -> None:
    """Downgrade schema - rename candidate_application_workflows back to company_workflows."""
    # Rename indexes back
    try:
        op.execute("ALTER INDEX IF EXISTS ix_candidate_application_workflows_company_id RENAME TO ix_company_workflows_company_id")
    except:
        pass
    
    try:
        op.execute("ALTER INDEX IF EXISTS ix_candidate_application_workflows_id RENAME TO ix_company_workflows_id")
    except:
        pass
    
    try:
        op.execute("ALTER INDEX IF EXISTS ix_candidate_application_workflows_status RENAME TO ix_company_workflows_status")
    except:
        pass
    
    try:
        op.execute("ALTER INDEX IF EXISTS ix_candidate_application_workflows_is_default RENAME TO ix_company_workflows_is_default")
    except:
        pass
    
    try:
        op.execute("ALTER INDEX IF EXISTS ix_candidate_application_workflows_phase_id RENAME TO ix_company_workflows_phase_id")
    except:
        pass
    
    # Rename the table back
    op.rename_table('candidate_application_workflows', 'company_workflows')
