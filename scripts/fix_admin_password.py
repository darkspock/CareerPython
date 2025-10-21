#!/usr/bin/env python3
"""
Fix admin user password to use correct hashing method
"""

import os
import sys
import bcrypt

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import settings
from sqlalchemy import create_engine, text

def get_password_hash(password: str) -> str:
    """Use the same hashing method as PasswordService - bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def fix_admin_password():
    """Update admin user password to use correct hashing"""

    # Database connection
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        try:
            admin_email = "admin@careerpython.com"
            admin_password = "12345678"

            # Check if admin user exists
            result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": admin_email})
            user_record = result.fetchone()

            if not user_record:
                print(f"❌ Admin user {admin_email} not found!")
                return

            user_id = user_record[0]
            print(f"👤 Found admin user with ID: {user_id}")

            # Hash password using the same method as AuthUseCase
            correct_hash = get_password_hash(admin_password)
            print(f"🔑 Generated new hash: {correct_hash[:50]}...")

            # Update the user's password hash
            conn.execute(text("""
                UPDATE users
                SET hashed_password = :new_hash
                WHERE id = :user_id
            """), {
                "new_hash": correct_hash,
                "user_id": user_id
            })

            # Commit transaction
            conn.commit()

            print("✅ Admin password hash updated successfully!")
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Password: {admin_password}")
            print("\n🌐 You can now login at:")
            print("   1. Go to: http://localhost:5174/admin")
            print("   2. Login with the credentials above")

        except Exception as e:
            conn.rollback()
            print(f"❌ Error fixing admin password: {e}")
            raise

if __name__ == "__main__":
    fix_admin_password()