#!/usr/bin/env python3
"""
Simple script to create admin user using SQL directly
"""

import os
import sys
import uuid
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import settings
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user():
    """Create an admin user using raw SQL"""

    # Database connection
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        try:
            # Admin user data
            admin_email = "admin@careerpython.com"
            admin_password = "admin123"

            # Check if admin user already exists
            result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": admin_email})
            existing_user = result.fetchone()

            if existing_user:
                user_id = existing_user[0]
                print(f"Admin user {admin_email} already exists with ID: {user_id}")

                # Check if already staff
                result = conn.execute(text("SELECT id FROM staff WHERE user_id = :user_id"), {"user_id": user_id})
                existing_staff = result.fetchone()
                if existing_staff:
                    print("✅ User is already staff!")
                    return
                else:
                    print("Making existing user admin...")
            else:
                # Create user
                user_id = str(uuid.uuid4())
                hashed_password = pwd_context.hash(admin_password)

                conn.execute(text("""
                    INSERT INTO users (id, email, hashed_password, is_active, subscription_tier)
                    VALUES (:id, :email, :password, :is_active, :subscription_tier)
                """), {
                    "id": user_id,
                    "email": admin_email,
                    "password": hashed_password,
                    "is_active": True,
                    "subscription_tier": "premium"
                })
                print(f"👤 Created user: {admin_email}")

            # Create staff record with admin role
            staff_id = str(uuid.uuid4())
            conn.execute(text("""
                INSERT INTO staff (id, user_id, roles, status)
                VALUES (:id, :user_id, :roles, :status)
            """), {
                "id": staff_id,
                "user_id": user_id,
                "roles": ["admin"],  # This will be stored as array
                "status": "active"
            })

            # Commit transaction
            conn.commit()

            print("✅ Admin user created successfully!")
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Password: {admin_password}")
            print(f"👤 User ID: {user_id}")
            print(f"🔧 Staff ID: {staff_id}")
            print("\n🌐 You can now login at:")
            print("   1. Go to: http://localhost:3000/auth/login")
            print("   2. Login with the credentials above")
            print("   3. Access admin panel: http://localhost:3000/admin")

        except Exception as e:
            conn.rollback()
            print(f"❌ Error creating admin user: {e}")
            raise

if __name__ == "__main__":
    create_admin_user()