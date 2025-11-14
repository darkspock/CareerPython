#!/usr/bin/env python3
"""
Script to create an admin user for testing the admin panel
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import settings
from src.auth_bc.user.infrastructure.models.user_model import UserModel
from src.auth_bc.staff.infrastructure.models.staff_model import StaffModel
from src.auth_bc.staff.domain.enums.staff_enums import RoleEnum, StaffStatusEnum
from src.framework.domain.entities.base import generate_id
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user():
    """Create an admin user for testing"""

    # Database connection
    database_url = settings.DATABASE_URL
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = SessionLocal()

    try:
        # Admin user data
        admin_email = "admin@careerpython.com"
        admin_password = "admin123"

        # Check if admin user already exists
        existing_user = session.query(UserModel).filter(UserModel.email == admin_email).first()
        if existing_user:
            print(f"Admin user {admin_email} already exists!")
            return

        # Create user
        hashed_password = pwd_context.hash(admin_password)
        user = UserModel(
            id=generate_id(),
            email=admin_email,
            hashed_password=hashed_password,
            is_active=True
        )

        session.add(user)
        session.flush()  # Get the user ID

        # Create staff record with admin role
        staff = StaffModel(
            id=generate_id(),
            user_id=user.id,
            roles=[RoleEnum.ADMIN],
            status=StaffStatusEnum.ACTIVE
        )

        session.add(staff)
        session.commit()

        print(f"✅ Admin user created successfully!")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print(f"   User ID: {user.id}")
        print(f"   Staff ID: {staff.id}")

    except Exception as e:
        session.rollback()
        print(f"❌ Error creating admin user: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    create_admin_user()