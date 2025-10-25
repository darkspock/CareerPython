"""
Script to create a test company user for login testing
"""
import ulid
from datetime import datetime

from core.database import SQLAlchemyDatabase
from src.company.application.commands.create_company_command import CreateCompanyCommand, CreateCompanyCommandHandler
from src.company.application.commands.add_company_user_command import AddCompanyUserCommand, AddCompanyUserCommandHandler
from src.company.domain.enums import CompanyUserRole
from src.company.domain.value_objects import CompanyId, CompanyUserId
from src.company.infrastructure.repositories.company_repository import CompanyRepository
from src.company.infrastructure.repositories.company_user_repository import CompanyUserRepository
from src.user.application.commands.create_user_command import CreateUserCommand, CreateUserCommandHandler
from src.user.domain.value_objects.UserId import UserId
from src.user.infrastructure.repositories.user_repository import SQLAlchemyUserRepository


def create_test_company_user():
    """Create a test company user with all required entities"""
    database = SQLAlchemyDatabase()
    session = database.get_session()

    try:
        # Initialize repositories
        company_repo = CompanyRepository(session)
        user_repo = SQLAlchemyUserRepository(database)
        company_user_repo = CompanyUserRepository(session)

        # Initialize handlers
        create_company_handler = CreateCompanyCommandHandler(company_repo)
        create_user_handler = CreateUserCommandHandler(user_repo)
        add_company_user_handler = AddCompanyUserCommandHandler(company_user_repo)

        # Use unique timestamp for domain
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Generate IDs
        company_id = str(ulid.new())
        user_id = str(ulid.new())
        company_user_id = str(ulid.new())

        # Set credentials
        email = f"company-{timestamp}@test.com"
        password = "Test1234!"
        company_domain = f"testcompany-{timestamp}.com"

        print("=" * 60)
        print("Creating Test Company User")
        print("=" * 60)

        # 1. Create Company
        print("\n1. Creating company...")
        company_command = CreateCompanyCommand(
            id=company_id,
            name=f"Test Company {timestamp}",
            domain=company_domain,
            logo_url=None,
            settings={"timezone": "UTC"}
        )
        create_company_handler.execute(company_command)
        print(f"✓ Company created: {company_id}")
        print(f"  Name: Test Company {timestamp}")
        print(f"  Domain: {company_domain}")

        # 2. Create User
        print("\n2. Creating user...")
        user_command = CreateUserCommand(
            id=UserId.from_string(user_id),
            email=email,
            password=password,
            is_active=True
        )
        create_user_handler.execute(user_command)
        print(f"✓ User created: {user_id}")
        print(f"  Email: {email}")
        print(f"  Password: {password}")

        # 3. Link User to Company
        print("\n3. Creating company-user relationship...")
        company_user_command = AddCompanyUserCommand(
            id=CompanyUserId.from_string(company_user_id),
            company_id=CompanyId.from_string(company_id),
            user_id=UserId.from_string(user_id),
            role=CompanyUserRole.ADMIN,
            permissions={
                "can_manage_candidates": True,
                "can_manage_workflows": True,
                "can_manage_interviews": True,
                "can_manage_users": True
            }
        )
        add_company_user_handler.execute(company_user_command)
        print(f"✓ Company user created: {company_user_id}")
        print(f"  Role: ADMIN")
        print(f"  Status: ACTIVE")

        # Commit transaction
        session.commit()

        print("\n" + "=" * 60)
        print("SUCCESS! Test company user created successfully")
        print("=" * 60)
        print("\nLogin Credentials:")
        print("-" * 60)
        print(f"Email:    {email}")
        print(f"Password: {password}")
        print(f"\nCompany ID: {company_id}")
        print(f"User ID:    {user_id}")
        print(f"Role:       ADMIN")
        print("\nLogin URL:")
        print("Frontend: http://localhost:5173/company/login")
        print("API:      http://localhost:8000/company/auth/login")
        print("=" * 60)

    except Exception as e:
        session.rollback()
        print(f"\n✗ Error creating company user: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    create_test_company_user()
