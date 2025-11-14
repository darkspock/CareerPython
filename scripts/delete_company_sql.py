#!/usr/bin/env python3
"""
Script to delete a company by ID using direct SQL (soft delete)
Usage: python scripts/delete_company_sql.py <company_id>
"""
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from core.database import SQLAlchemyDatabase


def delete_company_sql(company_id: str):
    """Delete a company by ID using direct SQL"""
    database = SQLAlchemyDatabase()
    
    try:
        with database.get_session() as session:
            # Soft delete: update status to 'deleted'
            result = session.execute(
                text("""
                    UPDATE companies 
                    SET status = :status, updated_at = :updated_at
                    WHERE id = :company_id
                """),
                {
                    'status': 'deleted',
                    'updated_at': datetime.now(),
                    'company_id': company_id
                }
            )
            
            session.commit()
            
            if result.rowcount == 0:
                print(f"❌ Company {company_id} not found")
                sys.exit(1)
            
            print(f"✅ Company {company_id} deleted successfully (soft delete)")
            
    except Exception as e:
        print(f"❌ Error deleting company: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/delete_company_sql.py <company_id>")
        sys.exit(1)
    
    company_id = sys.argv[1]
    delete_company_sql(company_id)

