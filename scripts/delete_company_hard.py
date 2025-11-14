#!/usr/bin/env python3
"""
Script to HARD DELETE a company by ID (permanently removes from database)
Usage: python scripts/delete_company_hard.py <company_id>
WARNING: This will permanently delete the company and all related data!
"""
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from core.database import SQLAlchemyDatabase


def delete_company_hard(company_id: str):
    """Hard delete a company by ID - permanently removes from database"""
    database = SQLAlchemyDatabase()
    
    try:
        with database.get_session() as session:
            print(f"⚠️  WARNING: This will permanently delete company {company_id} and all related data!")
            print(f"Starting hard delete...")
            
            # Delete in order to respect foreign key constraints
            # 1. Delete company_candidates (and related data first)
            # Delete candidate_comments
            result = session.execute(
                text("""
                    DELETE FROM candidate_comments 
                    WHERE company_candidate_id IN (
                        SELECT id FROM company_candidates WHERE company_id = :company_id
                    )
                """),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} candidate_comments")
            
            # Delete candidate_reviews
            result = session.execute(
                text("""
                    DELETE FROM candidate_reviews 
                    WHERE company_candidate_id IN (
                        SELECT id FROM company_candidates WHERE company_id = :company_id
                    )
                """),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} candidate_reviews")
            
            # Now delete company_candidates
            result = session.execute(
                text("DELETE FROM company_candidates WHERE company_id = :company_id"),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} company_candidates")
            
            # 2. Delete job_positions
            result = session.execute(
                text("DELETE FROM job_positions WHERE company_id = :company_id"),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} job_positions")
            
            # 3. Delete workflow_stages first (before workflows)
            result = session.execute(
                text("""
                    DELETE FROM workflow_stages 
                    WHERE workflow_id IN (
                        SELECT id FROM workflows WHERE company_id = :company_id
                    )
                """),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} workflow_stages")
            
            # 4. Delete workflows (after stages are deleted)
            result = session.execute(
                text("DELETE FROM workflows WHERE company_id = :company_id"),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} workflows")
            
            # 5. Delete phases (skip if table doesn't exist)
            try:
                result = session.execute(
                    text("DELETE FROM company_phases WHERE company_id = :company_id"),
                    {'company_id': company_id}
                )
                print(f"   - Deleted {result.rowcount} phases")
            except Exception as e:
                if "does not exist" in str(e) or "UndefinedTable" in str(e):
                    print(f"   - Skipping phases (table doesn't exist)")
                else:
                    raise
            
            # 6. Delete company_pages
            result = session.execute(
                text("DELETE FROM company_pages WHERE company_id = :company_id"),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} company_pages")
            
            # 7. Delete company_roles
            result = session.execute(
                text("DELETE FROM company_roles WHERE company_id = :company_id"),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} company_roles")
            
            # 8. Delete company_user_invitations
            result = session.execute(
                text("DELETE FROM company_user_invitations WHERE company_id = :company_id"),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} company_user_invitations")
            
            # 9. Delete company_users
            result = session.execute(
                text("DELETE FROM company_users WHERE company_id = :company_id"),
                {'company_id': company_id}
            )
            print(f"   - Deleted {result.rowcount} company_users")
            
            # 10. Delete entity_customizations (skip if table/column doesn't exist)
            try:
                result = session.execute(
                    text("DELETE FROM entity_customizations WHERE company_id = :company_id"),
                    {'company_id': company_id}
                )
                print(f"   - Deleted {result.rowcount} entity_customizations")
            except Exception as e:
                if "does not exist" in str(e) or "UndefinedColumn" in str(e) or "UndefinedTable" in str(e):
                    print(f"   - Skipping entity_customizations (table/column doesn't exist)")
                    # Don't rollback - just continue
                else:
                    raise
            
            # Commit all deletions so far before deleting the company
            session.commit()
            print(f"   - Committed all related data deletions")
            
            # 11. Finally, delete the company itself
            result = session.execute(
                text("DELETE FROM companies WHERE id = :company_id"),
                {'company_id': company_id}
            )
            
            if result.rowcount == 0:
                print(f"❌ Company {company_id} not found")
                sys.exit(1)
            
            session.commit()
            print(f"✅ Company {company_id} permanently deleted from database")
            
    except Exception as e:
        print(f"❌ Error deleting company: {str(e)}")
        import traceback
        traceback.print_exc()
        session.rollback()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/delete_company_hard.py <company_id>")
        sys.exit(1)
    
    company_id = sys.argv[1]
    
    # Confirm deletion
    response = input(f"⚠️  Are you sure you want to PERMANENTLY delete company {company_id}? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Deletion cancelled")
        sys.exit(0)
    
    delete_company_hard(company_id)

