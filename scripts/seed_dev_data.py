#!/usr/bin/env python3
"""
Seed development database with sample data
Creates:
- 1 Company with admin user
- 3 Phases with workflows (automatically via InitializeCompanyPhasesCommand)
- 50 Sample candidates
- Company-candidate relationships
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, UTC

# Import domain objects first
from src.company.domain.value_objects import CompanyId
from src.user.domain.value_objects.UserId import UserId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.company.domain.enums.company_user_role import CompanyUserRole

# Import commands
from src.company.application.commands.create_company_command import CreateCompanyCommand
from src.user.application.commands.create_user_command import CreateUserCommand
from src.company.application.commands.add_company_user_command import AddCompanyUserCommand
from src.company.application.commands.initialize_sample_data_command import InitializeSampleDataCommand

# Import infrastructure
from core.container import Container

# Initialize container after all imports
container = Container()
command_bus = container.command_bus()


def create_company_and_admin():
    """Create company and admin user"""
    print("🏢 Creating company and admin user...")
    
    company_id = CompanyId.generate()
    user_id = UserId.generate()
    
    # Check if company already exists
    company_repo = container.company_repository()
    existing_company = company_repo.get_by_domain("mycompany.com")
    if existing_company:
        print(f"  ⚠️  Company with domain 'mycompany.com' already exists (ID: {existing_company.id.value})")
        company_id = existing_company.id
    else:
        # Create company (this will automatically create phases via InitializeCompanyPhasesCommand)
        create_company_cmd = CreateCompanyCommand(
            id=company_id.value,
            name="My Company",
            domain="mycompany.com",
            logo_url=None,
            settings={"industry": "Technology", "size": "50-200"}
        )
        command_bus.dispatch(create_company_cmd)
        print(f"  ✓ Company created: My Company (ID: {company_id.value})")
    
    # Check if user already exists
    user_repo = container.user_repository()
    existing_user = user_repo.get_by_email("admin@company.com")
    if existing_user:
        print(f"  ⚠️  User with email 'admin@company.com' already exists (ID: {existing_user.id.value})")
        user_id = existing_user.id
    else:
        # Create admin user
        create_user_cmd = CreateUserCommand(
            id=user_id,
            email="admin@company.com",
            password="Admin123!",
            is_active=True
        )
        command_bus.dispatch(create_user_cmd)
        print(f"  ✓ Admin user created: admin@company.com")
        print(f"  ✓ Password: Admin123!")
    
    # Check if company_user relationship exists
    company_user_repo = container.company_user_repository()
    existing_company_user = company_user_repo.get_by_company_and_user(company_id, user_id)
    if existing_company_user:
        print(f"  ⚠️  Company-user relationship already exists (ID: {existing_company_user.id.value})")
        company_user_id = existing_company_user.id
    else:
        # Link user to company as admin
        company_user_id = CompanyUserId.generate()
        add_company_user_cmd = AddCompanyUserCommand(
            id=company_user_id,
            company_id=company_id,
            user_id=user_id,
            role=CompanyUserRole.ADMIN,
            permissions={}
        )
        command_bus.dispatch(add_company_user_cmd)
        print(f"  ✓ Company-user relationship created (Role: ADMIN)")
    
    print()
    return company_id, user_id, company_user_id




def main():
    """Main function"""
    print("\n" + "="*60)
    print("🌱 SEEDING DEVELOPMENT DATABASE")
    print("="*60 + "\n")
    
    try:
        # Step 1: Create company and admin
        company_id, user_id, company_user_id = create_company_and_admin()
        
        # Step 2: Initialize sample data (users, candidates and company-candidate relationships)
        print("👥 Creating sample users, candidates and relationships...")
        initialize_sample_data_cmd = InitializeSampleDataCommand(
            company_id=company_id,
            company_user_id=company_user_id,
            num_candidates=50,
            num_recruiters=3,
            num_viewers=2
        )
        command_bus.dispatch(initialize_sample_data_cmd)
        print("  ✓ Sample data created\n")
        
        print("="*60)
        print("✅ DATABASE SEEDING COMPLETED!")
        print("="*60)
        print("\n📝 LOGIN CREDENTIALS:")
        print("   Email: admin@company.com")
        print("   Password: Admin123!")
        print("\n🎯 SAMPLE DATA CREATED:")
        print("   - 1 Company (My Company)")
        print("   - 1 Admin user (admin@company.com)")
        print("   - 3 Recruiter users (recruiter1@company.com, recruiter2@company.com, recruiter3@company.com)")
        print("   - 2 Viewer users (viewer1@company.com, viewer2@company.com)")
        print("   - 3 Phases with workflows and stages (auto-created)")
        print("   - 50 Sample candidates with workflow assignments")
        print("\n📝 ADDITIONAL USER CREDENTIALS:")
        print("   Recruiters: recruiter1@company.com / Recruiter123!")
        print("   Viewers: viewer1@company.com / Viewer123!")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

