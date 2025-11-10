#!/usr/bin/env python3
"""
Seed development database with sample data
Creates:
- 1 Company with admin user
- 7 Default roles (via InitializeOnboardingCommand)
- 5 Default pages in DRAFT status (via InitializeOnboardingCommand)
- 3 Phases with workflows for CANDIDATE_APPLICATION (via InitializeCompanyPhasesCommand)
- 1 Phase with workflow for JOB_POSITION_OPENING (via InitializeCompanyPhasesCommand)
- 50 Sample candidates (via InitializeSampleDataCommand)
- Company-candidate relationships (via InitializeSampleDataCommand)
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import domain objects first
from src.company_bc.company.domain.value_objects import CompanyId
from src.auth_bc.user.domain.value_objects import UserId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_bc.company.domain.enums.company_user_role import CompanyUserRole

# Import commands
from src.company_bc.company.application.commands.create_company_command import CreateCompanyCommand
from src.company_bc.company.application.commands.initialize_onboarding_command import InitializeOnboardingCommand
from src.company_bc.company.application.commands.initialize_sample_data_command import InitializeSampleDataCommand
from src.shared_bc.customization.phase.application.commands.initialize_company_phases_command import InitializeCompanyPhasesCommand
from src.auth_bc.user.application.commands.create_user_command import CreateUserCommand
from src.company_bc.company.application.commands.add_company_user_command import AddCompanyUserCommand

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
        # Create company
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
    
    # Initialize onboarding (roles + pages) - only if company was just created
    if not existing_company:
        print("📋 Initializing onboarding (roles and pages)...")
        onboarding_cmd = InitializeOnboardingCommand(
            company_id=company_id,
            create_roles=True,
            create_pages=True
        )
        command_bus.dispatch(onboarding_cmd)
        print("  ✓ Onboarding initialized (7 roles + 5 pages)\n")
    
    # Initialize workflows - only if company was just created
    if not existing_company:
        print("🔄 Initializing workflows...")
        workflows_cmd = InitializeCompanyPhasesCommand(
            company_id=company_id
        )
        command_bus.dispatch(workflows_cmd)
        print("  ✓ Workflows initialized (3 phases for CANDIDATE_APPLICATION + 1 phase for JOB_POSITION_OPENING)\n")
    
    print()
    return company_id, user_id, company_user_id




def main():
    """Main function"""
    print("\n" + "="*60)
    print("🌱 SEEDING DEVELOPMENT DATABASE")
    print("="*60 + "\n")
    
    try:
        # Step 1: Create company and admin (includes onboarding and workflows initialization)
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
        print("   - 7 Company roles (HR Manager, Recruiter, Tech Lead, Hiring Manager, Interviewer, Department Head, CTO)")
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

