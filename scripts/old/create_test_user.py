#!/usr/bin/env python3
"""
Create a test user for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.container import container
from src.user.application.commands.create_user import CreateUserCommand

def create_test_user():
    """Create a test user"""
    try:
        command_bus = container.command_bus()
        
        command = CreateUserCommand(
            email="testuser@example.com",
            password="testpass123"
        )
        
        user_id = command_bus.dispatch(command)
        print(f"✅ Created test user with ID: {user_id}")
        print(f"📧 Email: testuser@example.com")
        print(f"🔑 Password: testpass123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_test_user()