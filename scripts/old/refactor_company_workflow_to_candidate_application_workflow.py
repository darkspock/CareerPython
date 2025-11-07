#!/usr/bin/env python3
"""
Script to refactor CandidateApplicationWorkflow to CandidateApplicationWorkflow
This script will:
1. Rename all class names
2. Update import paths
3. Update file names where appropriate
"""

import os
import re
import shutil
from pathlib import Path

# Mapping of old to new names
REPLACEMENTS = {
    # Class names
    'CandidateApplicationWorkflow': 'CandidateApplicationWorkflow',
    'CandidateApplicationWorkflowId': 'CandidateApplicationWorkflowId',
    
    # Module paths
    'src.candidate_application_workflow': 'src.candidate_application_workflow',
    'from src.candidate_application_workflow': 'from src.candidate_application_workflow',
    'import src.candidate_application_workflow': 'import src.candidate_application_workflow',
    
    # Table names (for migrations)
    'candidate_application_workflows': 'candidate_application_workflows',
    'candidate_application_workflow': 'candidate_application_workflow',
}

def replace_in_file(file_path: Path):
    """Replace all occurrences in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main refactoring function"""
    base_dir = Path(__file__).parent.parent
    
    # Find all Python files
    python_files = list(base_dir.rglob('*.py'))
    
    # Exclude __pycache__ and .venv
    python_files = [
        f for f in python_files 
        if '__pycache__' not in str(f) and '.venv' not in str(f)
    ]
    
    updated_count = 0
    for file_path in python_files:
        if replace_in_file(file_path):
            updated_count += 1
    
    print(f"\n✅ Refactoring complete! Updated {updated_count} files.")
    print("\n⚠️  Next steps:")
    print("1. Rename directory: src/candidate_application_workflow -> src/candidate_application_workflow")
    print("2. Create database migration for table rename")
    print("3. Update frontend files")
    print("4. Run tests")

if __name__ == '__main__':
    main()

