#!/usr/bin/env python3
"""
Script to delete all interviews from the database
This will also delete related interview answers due to CASCADE constraints
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.containers import Container

def delete_all_interviews():
    """Delete all interviews from the database"""
    print("🗑️  Deleting all interviews from the database...")
    
    container = Container()
    database = container.database()
    
    try:
        with database.get_session() as session:
            # Check if interview_answers table exists and delete answers first
            from sqlalchemy import inspect
            inspector = inspect(session.bind)
            table_names = inspector.get_table_names()
            
            # Delete all interview answers first (if table exists)
            if 'interview_answers' in table_names:
                from src.interview_bc.interview.Infrastructure.models.interview_answer_model import InterviewAnswerModel
                try:
                    answer_count = session.query(InterviewAnswerModel).count()
                    if answer_count > 0:
                        print(f"  Found {answer_count} interview answers, deleting...")
                        session.query(InterviewAnswerModel).delete()
                        print(f"  ✓ Deleted {answer_count} interview answers")
                except Exception as e:
                    print(f"  ⚠️  Could not delete interview answers: {e}")
            
            # Delete all interview interviewers (if table exists)
            if 'interview_interviewers' in table_names:
                from src.interview_bc.interview.Infrastructure.models.interview_interviewer_model import InterviewInterviewerModel
                try:
                    interviewer_count = session.query(InterviewInterviewerModel).count()
                    if interviewer_count > 0:
                        print(f"  Found {interviewer_count} interview-interviewer relationships, deleting...")
                        session.query(InterviewInterviewerModel).delete()
                        print(f"  ✓ Deleted {interviewer_count} interview-interviewer relationships")
                except Exception as e:
                    print(f"  ⚠️  Could not delete interview interviewers: {e}")
            
            # Delete all interviews
            from src.interview_bc.interview.Infrastructure.models.interview_model import InterviewModel
            interview_count = session.query(InterviewModel).count()
            if interview_count > 0:
                print(f"  Found {interview_count} interviews, deleting...")
                session.query(InterviewModel).delete()
                print(f"  ✓ Deleted {interview_count} interviews")
            else:
                print("  No interviews found in the database")
            
            session.commit()
            print("\n✅ All interviews deleted successfully!")
            
    except Exception as e:
        print(f"\n❌ Error deleting interviews: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🗑️  DELETE ALL INTERVIEWS")
    print("="*60 + "\n")
    
    response = input("⚠️  WARNING: This will delete ALL interviews and their answers. Continue? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Operation cancelled.")
        sys.exit(0)
    
    delete_all_interviews()
    print("\n")

