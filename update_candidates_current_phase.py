#!/usr/bin/env python3
"""
Script to update existing candidates with current_phase_id
"""
import psycopg2
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'careerpython',
    'user': 'careerpython',
    'password': 'careerpython'
}

def update_candidates():
    """Update existing candidates with current_phase_id"""
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get all candidates with workflow_id but no current_phase_id
        cursor.execute("""
            SELECT id, workflow_id, phase_id 
            FROM company_candidates 
            WHERE workflow_id IS NOT NULL 
            AND current_phase_id IS NULL
        """)
        
        candidates = cursor.fetchall()
        print(f"Found {len(candidates)} candidates to update")
        
        # Get phase_id from workflows
        cursor.execute("""
            SELECT id, phase_id 
            FROM company_workflows 
            WHERE id IN (
                SELECT DISTINCT workflow_id 
                FROM company_candidates 
                WHERE workflow_id IS NOT NULL
            )
        """)
        
        workflow_phases = {row[0]: row[1] for row in cursor.fetchall()}
        print(f"Found {len(workflow_phases)} workflow-phase mappings")
        
        # Update candidates
        updated_count = 0
        for candidate_id, workflow_id, phase_id in candidates:
            if workflow_id in workflow_phases:
                current_phase_id = workflow_phases[workflow_id]
                cursor.execute("""
                    UPDATE company_candidates 
                    SET current_phase_id = %s 
                    WHERE id = %s
                """, (current_phase_id, candidate_id))
                updated_count += 1
                print(f"Updated candidate {candidate_id} with current_phase_id {current_phase_id}")
        
        conn.commit()
        print(f"✅ Updated {updated_count} candidates with current_phase_id")
        return True
        
    except Exception as e:
        print(f"❌ Error updating candidates: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def main():
    print("🚀 Updating candidates with current_phase_id...")
    print("-" * 50)
    
    if update_candidates():
        print("✅ Update completed successfully!")
    else:
        print("❌ Update failed")

if __name__ == "__main__":
    main()
