"""
Script to create a simple company user with easy credentials
"""
import ulid

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


def create_simple_company_user():
    """Create a company user with simple credentials"""
    database = SQLAlchemyDatabase()
    session = database.get_session()

    try:
        # Initialize repositories
        company_repo = CompanyRepository(database)
        user_repo = SQLAlchemyUserRepository(database)
        company_user_repo = CompanyUserRepository(database)

        # Initialize handlers
        create_company_handler = CreateCompanyCommandHandler(company_repo)
        create_user_handler = CreateUserCommandHandler(user_repo)
        add_company_user_handler = AddCompanyUserCommandHandler(company_user_repo)

        # Generate IDs
        company_id = str(ulid.new())
        user_id = str(ulid.new())
        company_user_id = str(ulid.new())

        # Simple credentials
        email = "admin@company.com"
        password = "Admin123!"
        company_domain = "mycompany.com"

        print("=" * 60)
        print("Creating Simple Company User")
        print("=" * 60)

        # Check if user already exists
        existing_user = user_repo.get_by_email(email)
        if existing_user:
            print(f"\n⚠️  User with email {email} already exists!")
            print(f"   User ID: {existing_user.id.value}")
            user_id = existing_user.id.value
            print("   Skipping user creation...")
        else:
            # Create User
            print("\n1. Creating user...")
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

        # Check if company exists
        existing_company = company_repo.get_by_domain(company_domain)
        if existing_company:
            print(f"\n⚠️  Company with domain {company_domain} already exists!")
            print(f"   Company ID: {existing_company.id.value}")
            company_id = existing_company.id.value
            print("   Skipping company creation...")
        else:
            # Create Company
            print("\n2. Creating company...")
            company_command = CreateCompanyCommand(
                id=company_id,
                name="My Company",
                domain=company_domain,
                logo_url=None,
                settings={"timezone": "UTC"}
            )
            create_company_handler.execute(company_command)
            print(f"✓ Company created: {company_id}")
            print(f"  Name: My Company")
            print(f"  Domain: {company_domain}")

        # Check if company_user exists
        existing_company_user = company_user_repo.get_by_company_and_user(
            CompanyId.from_string(company_id),
            UserId.from_string(user_id)
        )

        if existing_company_user:
            print(f"\n⚠️  Company user relationship already exists!")
            print(f"   Company User ID: {existing_company_user.id.value}")
            print("   Skipping company_user creation...")
        else:
            # Link User to Company
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
        print("SUCCESS! Company user ready")
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
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    create_simple_company_user()
