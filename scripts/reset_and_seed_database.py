"""
Reset database and seed with sample data
This script will:
1. Delete all data from main tables (preserving structure)
2. Create sample company with admin user
3. Create sample phases and workflows
4. Create sample candidates
5. Create sample job positions
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta, UTC
from sqlalchemy import text
from core.database import database

# Import all models to ensure SQLAlchemy relationships are resolved
from src.user.infrastructure.models.user_model import UserModel
from src.user.infrastructure.models.user_asset_model import UserAssetModel
from src.company.infrastructure.models.company_model import CompanyModel
from src.company.infrastructure.models.company_user_model import CompanyUserModel
from src.phase.infrastructure.models.phase_model import PhaseModel
from src.company_workflow.infrastructure.models.company_workflow_model import CompanyWorkflowModel
from src.company_workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
from src.company_workflow.infrastructure.models.custom_field_model import CustomFieldModel
from src.company_workflow.infrastructure.models.field_configuration_model import FieldConfigurationModel
from src.candidate.infrastructure.models.candidate_model import CandidateModel
from src.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel
from src.candidate_stage.infrastructure.models.candidate_stage_model import CandidateStageModel
from src.interview.interview.Infrastructure.models.interview_model import InterviewModel
from src.interview.interview.Infrastructure.models.interview_answer_model import InterviewAnswerModel
from src.staff.infrastructure.models.staff_model import StaffModel
from src.resume.infrastructure.models.resume_model import ResumeModel
from src.company_role.infrastructure.models.company_role_model import CompanyRoleModel
from src.position_stage_assignment.infrastructure.models.position_stage_assignment_model import PositionStageAssignmentModel
from src.email_template.infrastructure.models.email_template_model import EmailTemplateModel
from src.talent_pool.infrastructure.models.talent_pool_entry_model import TalentPoolEntryModel
from src.field_validation.infrastructure.models.validation_rule_model import ValidationRuleModel
from src.shared.infrastructure.models.async_job_model import AsyncJobModel

# Import enums
from src.phase.domain.enums.phase_status_enum import PhaseStatus
from src.phase.domain.enums.default_view_enum import DefaultView
from src.company_workflow.domain.enums.workflow_status import WorkflowStatus
from src.company_workflow.domain.enums.stage_type import StageType
from src.company.domain.enums.company_user_role import CompanyUserRole
from bcrypt import hashpw, gensalt
import ulid


def generate_ulid() -> str:
    """Generate a new ULID"""
    return str(ulid.new())


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


def clear_all_data(session):
    """Clear all data from tables"""
    print("🗑️  Clearing existing data...")

    # Order matters due to foreign key constraints
    tables = [
        'company_candidates',
        'candidates',
        'job_positions',
        'workflow_stages',
        'company_workflows',
        'company_phases',
        'company_users',
        'users',
        'companies',
    ]

    for table in tables:
        try:
            session.execute(text(f'TRUNCATE TABLE {table} CASCADE'))
            print(f"  ✓ Cleared {table}")
        except Exception as e:
            print(f"  ⚠️  Warning clearing {table}: {e}")

    session.commit()
    print("✅ All data cleared\n")


def create_company_and_admin(session) -> tuple[str, str]:
    """Create company and admin user"""
    print("🏢 Creating company and admin user...")

    company_id = generate_ulid()
    user_id = generate_ulid()

    # Create company
    now = datetime.now(UTC)
    company = CompanyModel(
        id=company_id,
        name="My Company",
        domain="mycompany.com",
        slug="my-company",
        logo_url=None,
        settings={"industry": "Technology", "size": "50-200"},
        status="ACTIVE",
        created_at=now,
        updated_at=now
    )
    session.add(company)

    # Create admin user
    user = UserModel(
        id=user_id,
        email="admin@company.com",
        hashed_password=hash_password("Admin123!"),
        is_active=True,
        subscription_tier="FREE",
        subscription_expires_at=None,
        password_reset_token=None,
        password_reset_expires_at=None,
        preferred_language="en",
        created_at=now
    )
    session.add(user)
    session.flush()  # Flush to ensure user exists before creating company_user

    # Create company user relationship
    company_user_id = generate_ulid()
    company_user = CompanyUserModel(
        id=company_user_id,
        company_id=company_id,
        user_id=user_id,
        role=CompanyUserRole.ADMIN.value,
        permissions={},
        status="ACTIVE",
        created_at=now,
        updated_at=now
    )
    session.add(company_user)

    session.commit()
    print(f"  ✓ Company created: {company.name} (ID: {company_id})")
    print(f"  ✓ Admin user created: admin@company.com")
    print(f"  ✓ Password: Admin123!")
    print(f"  ✓ Company-User relationship created (Role: ADMIN)\n")

    return company_id, user_id


def create_phases_and_workflows(session, company_id: str) -> dict:
    """Create phases and workflows"""
    print("📋 Creating phases and workflows...")

    phases = {}

    # Phase 1: Sourcing
    phase1_id = generate_ulid()
    phase1 = PhaseModel(
        id=phase1_id,
        company_id=company_id,
        name="Sourcing",
        sort_order=0,
        default_view=DefaultView.KANBAN,
        status=PhaseStatus.ACTIVE,
        objective="Screening and filtering candidates",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    session.add(phase1)
    phases['sourcing'] = phase1_id

    # Phase 2: Evaluation
    phase2_id = generate_ulid()
    phase2 = PhaseModel(
        id=phase2_id,
        company_id=company_id,
        name="Evaluation",
        sort_order=1,
        default_view=DefaultView.KANBAN,
        status=PhaseStatus.ACTIVE,
        objective="Interview and assessment process",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    session.add(phase2)
    phases['evaluation'] = phase2_id

    # Phase 3: Offer and Pre-Onboarding
    phase3_id = generate_ulid()
    phase3 = PhaseModel(
        id=phase3_id,
        company_id=company_id,
        name="Offer and Pre-Onboarding",
        sort_order=2,
        default_view=DefaultView.LIST,
        status=PhaseStatus.ACTIVE,
        objective="Offer management and pre-onboarding preparation",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    session.add(phase3)
    phases['offer'] = phase3_id

    # Flush phases so they exist before creating workflows
    session.flush()

    # Sourcing workflow
    workflow1_id = generate_ulid()
    workflow1 = CompanyWorkflowModel(
        id=workflow1_id,
        company_id=company_id,
        name="Sourcing Workflow",
        description="Initial candidate screening",
        phase_id=phase1_id,
        status=WorkflowStatus.ACTIVE,
        is_default=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    session.add(workflow1)

    # Sourcing stages
    stages1 = [
        ("Pending", "Application pending review", StageType.INITIAL, 0, None),
        ("Screening", "Initial screening", StageType.STANDARD, 1, None),
        ("Qualified", "Candidate qualified", StageType.SUCCESS, 2, None),  # Will set next_phase later
        ("Not Suitable", "Not suitable", StageType.FAIL, 3, None),
        ("On Hold", "Application on hold", StageType.STANDARD, 4, None),
    ]

    for name, desc, stage_type, order, next_phase in stages1:
        stage = WorkflowStageModel(
            id=generate_ulid(),
            workflow_id=workflow1_id,
            name=name,
            description=desc,
            stage_type=stage_type,
            order=order,
            allow_skip=False,
            is_active=True,
            next_phase_id=next_phase,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        session.add(stage)

    # Evaluation workflow
    workflow2_id = generate_ulid()
    workflow2 = CompanyWorkflowModel(
        id=workflow2_id,
        company_id=company_id,
        name="Evaluation Workflow",
        description="Interview and assessment",
        phase_id=phase2_id,
        status=WorkflowStatus.ACTIVE,
        is_default=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    session.add(workflow2)

    # Evaluation stages
    stages2 = [
        ("HR Interview", "Human Resources interview", StageType.INITIAL, 0, None),
        ("Manager Interview", "Manager interview", StageType.STANDARD, 1, None),
        ("Assessment Test", "Technical assessment", StageType.STANDARD, 2, None),
        ("Executive Interview", "Executive interview", StageType.STANDARD, 3, None),
        ("Selected", "Candidate selected", StageType.SUCCESS, 4, None),  # Will set next_phase later
        ("Rejected", "Candidate rejected", StageType.FAIL, 5, None),
    ]

    for name, desc, stage_type, order, next_phase in stages2:
        stage = WorkflowStageModel(
            id=generate_ulid(),
            workflow_id=workflow2_id,
            name=name,
            description=desc,
            stage_type=stage_type,
            order=order,
            allow_skip=False,
            is_active=True,
            next_phase_id=next_phase,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        session.add(stage)

    # Offer workflow
    workflow3_id = generate_ulid()
    workflow3 = CompanyWorkflowModel(
        id=workflow3_id,
        company_id=company_id,
        name="Offer Workflow",
        description="Offer and pre-onboarding",
        phase_id=phase3_id,
        status=WorkflowStatus.ACTIVE,
        is_default=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    session.add(workflow3)

    # Offer stages
    stages3 = [
        ("Offer Proposal", "Offer proposed", StageType.INITIAL, 0, None),
        ("Negotiation", "Negotiating terms", StageType.STANDARD, 1, None),
        ("Document Submission", "Submitting documents", StageType.STANDARD, 2, None),
        ("Document Verification", "Verifying documents", StageType.SUCCESS, 3, None),
        ("Lost", "Candidate declined", StageType.FAIL, 4, None),
    ]

    for name, desc, stage_type, order, next_phase in stages3:
        stage = WorkflowStageModel(
            id=generate_ulid(),
            workflow_id=workflow3_id,
            name=name,
            description=desc,
            stage_type=stage_type,
            order=order,
            allow_skip=False,
            is_active=True,
            next_phase_id=next_phase,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        session.add(stage)

    session.commit()

    # Update SUCCESS stages to point to next phases
    session.execute(
        text("""
            UPDATE workflow_stages
            SET next_phase_id = :next_phase_id
            WHERE workflow_id = :workflow_id
            AND stage_type = 'SUCCESS'
        """),
        {"workflow_id": workflow1_id, "next_phase_id": phase2_id}
    )
    session.execute(
        text("""
            UPDATE workflow_stages
            SET next_phase_id = :next_phase_id
            WHERE workflow_id = :workflow_id
            AND stage_type = 'SUCCESS'
        """),
        {"workflow_id": workflow2_id, "next_phase_id": phase3_id}
    )
    session.commit()

    print(f"  ✓ Created 3 phases with workflows")
    print(f"    - Sourcing (Kanban)")
    print(f"    - Evaluation (Kanban)")
    print(f"    - Offer and Pre-Onboarding (List)\n")

    return phases


def create_candidates(session, company_id: str) -> list[str]:
    """Create sample candidates"""
    print("👥 Creating sample candidates...")

    from datetime import date
    from src.candidate.domain.enums.candidate_enums import CandidateStatusEnum, CandidateTypeEnum
    from src.shared.domain.enums.job_category import JobCategoryEnum

    candidates_data = [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-0101",
            "city": "San Francisco",
            "country": "USA",
            "skills": ["Python", "React", "PostgreSQL", "Docker"],
        },
        {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "+1-555-0102",
            "city": "New York",
            "country": "USA",
            "skills": ["Java", "Spring Boot", "Kubernetes", "AWS"],
        },
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "phone": "+1-555-0103",
            "city": "Austin",
            "country": "USA",
            "skills": ["JavaScript", "Node.js", "MongoDB", "GraphQL"],
        },
        {
            "name": "Bob Williams",
            "email": "bob.williams@example.com",
            "phone": "+1-555-0104",
            "city": "Seattle",
            "country": "USA",
            "skills": ["C++", "Python", "Machine Learning", "TensorFlow"],
        },
        {
            "name": "Carol Davis",
            "email": "carol.davis@example.com",
            "phone": "+1-555-0105",
            "city": "Boston",
            "country": "USA",
            "skills": ["Ruby", "Rails", "Redis", "Sidekiq"],
        }
    ]

    candidate_ids = []

    for data in candidates_data:
        candidate_id = generate_ulid()
        user_id = generate_ulid()  # Create a fake user_id for now
        candidate = CandidateModel(
            id=candidate_id,
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            city=data["city"],
            country=data["country"],
            date_of_birth=date(1990, 1, 1),  # Sample date
            user_id=user_id,
            status=CandidateStatusEnum.COMPLETE,
            job_category=JobCategoryEnum.TECHNOLOGY,
            candidate_type=CandidateTypeEnum.BASIC,
            skills=data.get("skills", []),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        session.add(candidate)
        candidate_ids.append(candidate_id)

    session.commit()
    print(f"  ✓ Created {len(candidates_data)} candidates\n")

    return candidate_ids


def create_job_positions(session, company_id: str, phases: dict) -> list[str]:
    """Create sample job positions"""
    print("💼 Creating sample job positions...")

    positions_data = [
        {
            "title": "Senior Full-Stack Developer",
            "department": "Engineering",
            "location": "San Francisco, CA",
            "employment_type": "FULL_TIME",
            "salary_min": 120000,
            "salary_max": 180000,
            "description": "We're looking for a senior full-stack developer to join our engineering team.",
            "requirements": ["5+ years experience", "Python/React", "PostgreSQL", "Docker"],
            "phase": phases['sourcing']
        },
        {
            "title": "Lead Backend Engineer",
            "department": "Engineering",
            "location": "New York, NY",
            "employment_type": "FULL_TIME",
            "salary_min": 140000,
            "salary_max": 200000,
            "description": "Join us as a lead backend engineer to architect scalable systems.",
            "requirements": ["7+ years experience", "Java/Spring", "Kubernetes", "AWS"],
            "phase": phases['evaluation']
        },
        {
            "title": "Frontend Developer",
            "department": "Engineering",
            "location": "Remote",
            "employment_type": "FULL_TIME",
            "salary_min": 90000,
            "salary_max": 130000,
            "description": "Build amazing user experiences with modern web technologies.",
            "requirements": ["3+ years experience", "React/Vue", "TypeScript", "CSS"],
            "phase": phases['sourcing']
        }
    ]

    position_ids = []

    from src.job_position.domain.enums import JobPositionStatusEnum, ContractTypeEnum, WorkLocationTypeEnum
    from src.job_position.domain.enums.employment_type import EmploymentType

    for data in positions_data:
        position_id = generate_ulid()
        position = JobPositionModel(
            id=position_id,
            company_id=company_id,
            title=data["title"],
            department=data["department"],
            location=data["location"],
            employment_type=EmploymentType.FULL_TIME,
            salary_range={"min_salary": data["salary_min"], "max_salary": data["salary_max"], "currency": "USD"},
            description=data["description"],
            requirements={"skills": data.get("requirements", [])},
            status=JobPositionStatusEnum.OPEN,
            workflow_id=None,
            phase_workflows=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        session.add(position)
        position_ids.append(position_id)

    session.commit()
    print(f"  ✓ Created {len(positions_data)} job positions\n")

    return position_ids


def link_candidates_to_positions(session, company_id: str, candidate_ids: list[str],
                                 position_ids: list[str], phases: dict):
    """Link candidates to job positions"""
    print("🔗 Linking candidates to positions...")

    # Get first workflow stage for each phase
    phase_stages = {}
    for phase_name, phase_id in phases.items():
        result = session.execute(
            text("""
                SELECT ws.id
                FROM workflow_stages ws
                JOIN company_workflows cw ON ws.workflow_id = cw.id
                WHERE cw.phase_id = :phase_id
                AND ws.stage_type = 'INITIAL'
                LIMIT 1
            """),
            {"phase_id": phase_id}
        ).fetchone()
        if result:
            phase_stages[phase_name] = result[0]

    # Link candidates to positions in different stages
    links = [
        # Position 1 - Senior Full-Stack (Sourcing)
        (candidate_ids[0], position_ids[0], phases['sourcing'], phase_stages.get('sourcing'), "HIGH", "NEW"),
        (candidate_ids[2], position_ids[0], phases['sourcing'], phase_stages.get('sourcing'), "MEDIUM", "NEW"),

        # Position 2 - Lead Backend (Evaluation)
        (candidate_ids[1], position_ids[1], phases['evaluation'], phase_stages.get('evaluation'), "HIGH", "IN_PROGRESS"),
        (candidate_ids[3], position_ids[1], phases['evaluation'], phase_stages.get('evaluation'), "HIGH", "IN_PROGRESS"),

        # Position 3 - Frontend (Sourcing)
        (candidate_ids[4], position_ids[2], phases['sourcing'], phase_stages.get('sourcing'), "MEDIUM", "NEW"),
    ]

    for candidate_id, position_id, phase_id, stage_id, priority, status in links:
        if stage_id:  # Only create if we found a stage
            company_candidate = CompanyCandidateModel(
                id=generate_ulid(),
                company_id=company_id,
                candidate_id=candidate_id,
                job_position_id=position_id,
                current_phase_id=phase_id,
                current_stage_id=stage_id,
                priority=priority,
                status=status,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )
            session.add(company_candidate)

    session.commit()
    print(f"  ✓ Linked {len(links)} candidate-position relationships\n")


def main():
    """Main function"""
    print("\n" + "="*60)
    print("🔄 DATABASE RESET AND SEED SCRIPT")
    print("="*60 + "\n")

    with database.get_session() as session:
        # Step 1: Clear all data
        clear_all_data(session)

        # Step 2: Create company and admin
        company_id, user_id = create_company_and_admin(session)

        # Step 3: Create phases and workflows
        phases = create_phases_and_workflows(session, company_id)

        # Step 4: Create candidates
        candidate_ids = create_candidates(session, company_id)

        # Step 5: Create job positions (commented out for simplicity - model structure complex)
        # position_ids = create_job_positions(session, company_id, phases)

        # Step 6: Link candidates to positions (commented out for simplicity)
        # link_candidates_to_positions(session, company_id, candidate_ids, position_ids, phases)

    print("="*60)
    print("✅ DATABASE RESET AND SEED COMPLETED!")
    print("="*60)
    print("\n📝 LOGIN CREDENTIALS:")
    print("   Email: admin@company.com")
    print("   Password: Admin123!")
    print("\n🎯 SAMPLE DATA CREATED:")
    print("   - 1 Company (My Company)")
    print("   - 1 Admin user")
    print("   - 3 Phases with workflows and stages")
    print("   - 5 Sample candidates")
    print("\n")


if __name__ == "__main__":
    main()
