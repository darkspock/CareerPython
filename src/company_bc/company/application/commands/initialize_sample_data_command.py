from dataclasses import dataclass
from datetime import date
from typing import Optional
import random
from sqlalchemy import text

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_bc.company.domain.enums.company_user_role import CompanyUserRole
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_bc.company_candidate.domain.enums import CandidatePriority
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.framework.application.command_bus import Command, CommandHandler, CommandBus
from src.auth_bc.user.application.commands.create_user_command import CreateUserCommand
from src.company_bc.company.application.commands.add_company_user_command import AddCompanyUserCommand
from src.candidate_bc.candidate.application.commands.create_candidate import CreateCandidateCommand
from src.company_bc.company_candidate.application.commands.create_company_candidate_command import (
    CreateCompanyCandidateCommand
)
from src.company_bc.company_candidate.application.commands.assign_workflow_command import (
    AssignWorkflowCommand
)
from src.company_bc.job_position.application.commands.create_job_position import CreateJobPositionCommand
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.company_bc.job_position.domain.value_objects.stage_id import StageId
from src.company_bc.job_position.domain.enums import JobPositionVisibilityEnum
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.company_bc.candidate_application.application.commands.create_candidate_application import CreateCandidateApplicationCommand
from core.database import SQLAlchemyDatabase


@dataclass(frozen=True)
class InitializeSampleDataCommand(Command):
    """Command to initialize sample data for a company to evaluate the software"""
    company_id: CompanyId
    company_user_id: CompanyUserId  # User who will own the sample data
    num_candidates: int = 50  # Number of sample candidates to create
    num_recruiters: int = 3  # Number of recruiter users to create
    num_viewers: int = 2  # Number of viewer users to create
    num_job_positions: int = 10  # Number of sample job positions to create


class InitializeSampleDataCommandHandler(CommandHandler[InitializeSampleDataCommand]):
    """Handler for initializing sample data"""

    def __init__(self, command_bus: CommandBus, database: SQLAlchemyDatabase):
        self._command_bus = command_bus
        self._database = database

    def _create_sample_users(
        self,
        company_id: CompanyId,
        num_recruiters: int,
        num_viewers: int
    ) -> None:
        """Create sample users with different roles"""
        # Create recruiters
        for i in range(1, num_recruiters + 1):
            try:
                user_id = UserId.generate()
                company_user_id = CompanyUserId.generate()

                # Create user
                create_user_cmd = CreateUserCommand(
                    id=user_id,
                    email=f"recruiter{i}@company.com",
                    password="Recruiter123!",
                    is_active=True
                )
                self._command_bus.dispatch(create_user_cmd)

                # Add user to company as recruiter
                add_company_user_cmd = AddCompanyUserCommand(
                    id=company_user_id,
                    company_id=company_id,
                    user_id=user_id,
                    role=CompanyUserRole.RECRUITER,
                    permissions=None  # Will use default recruiter permissions
                )
                self._command_bus.dispatch(add_company_user_cmd)
            except Exception:
                # Skip users that fail to create (e.g., duplicate emails)
                continue

        # Create viewers
        for i in range(1, num_viewers + 1):
            try:
                user_id = UserId.generate()
                company_user_id = CompanyUserId.generate()

                # Create user
                create_user_cmd = CreateUserCommand(
                    id=user_id,
                    email=f"viewer{i}@company.com",
                    password="Viewer123!",
                    is_active=True
                )
                self._command_bus.dispatch(create_user_cmd)

                # Add user to company as viewer
                add_company_user_cmd = AddCompanyUserCommand(
                    id=company_user_id,
                    company_id=company_id,
                    user_id=user_id,
                    role=CompanyUserRole.VIEWER,
                    permissions=None  # Will use default viewer permissions
                )
                self._command_bus.dispatch(add_company_user_cmd)
            except Exception:
                # Skip users that fail to create (e.g., duplicate emails)
                continue

    def execute(self, command: InitializeSampleDataCommand) -> None:
        """Handle the initialize sample data command"""
        # Step 1: Create users with different roles
        self._create_sample_users(
            command.company_id,
            command.num_recruiters,
            command.num_viewers
        )

        # Step 2: Create sample candidates
        candidate_ids = self._create_sample_candidates(command.num_candidates)

        # Step 3: Create one job position in active stage (before creating company candidates)
        active_job_position_id = self._create_active_job_position(command.company_id)

        # Step 4: Create company-candidate relationships with random workflow assignments
        # and link them to the active job position
        if candidate_ids:
            self._create_company_candidates(
                command.company_id,
                command.company_user_id,
                candidate_ids,
                active_job_position_id
            )

        # Step 5: Create additional sample job positions
        self._create_sample_job_positions(
            command.company_id,
            command.num_job_positions
        )

    def _create_sample_candidates(self, num_candidates: int) -> list[CandidateId]:
        """Create sample candidates"""
        first_names = [
            "John", "Jane", "Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry",
            "Ivy", "Jack", "Kate", "Liam", "Maya", "Noah", "Olivia", "Paul", "Quinn", "Rachel",
            "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier", "Yara", "Zoe", "Alex", "Beth",
            "Chris", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia", "Kevin", "Lisa",
            "Mike", "Nina", "Oscar", "Paula", "Quentin", "Rita", "Steve", "Tara", "Ulysses", "Vera"
        ]

        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
            "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
            "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
            "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
            "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts"
        ]

        cities = [
            "San Francisco", "New York", "Austin", "Seattle", "Boston", "Los Angeles", "Chicago", "Denver", "Miami", "Portland"
        ]

        countries = ["USA", "Canada", "Mexico", "UK", "Germany"]

        candidate_ids = []
        used_emails = set()

        for i in range(num_candidates):
            # Generate unique email
            attempts = 0
            while attempts < 100:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                email = f"{first_name.lower()}.{last_name.lower()}@example.com"

                if email not in used_emails:
                    used_emails.add(email)
                    break
                attempts += 1

            if email in used_emails and attempts >= 100:
                email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
                used_emails.add(email)

            phone = f"+1-555-{random.randint(1000, 9999)}"
            city = random.choice(cities)
            country = random.choice(countries)

            try:
                candidate_id = CandidateId.generate()
                # Create a dummy user_id for candidates (they don't need real users)
                dummy_user_id = UserId.generate()

                create_candidate_cmd = CreateCandidateCommand(
                    id=candidate_id,
                    name=f"{first_name} {last_name}",
                    date_of_birth=date(1990, 1, 1),  # Sample date
                    city=city,
                    country=country,
                    phone=phone,
                    email=email,
                    user_id=dummy_user_id
                )
                self._command_bus.dispatch(create_candidate_cmd)
                candidate_ids.append(candidate_id)
            except Exception:
                # Skip candidates that fail to create (e.g., duplicate emails)
                continue

        return candidate_ids

    def _create_active_job_position(
        self,
        company_id: CompanyId
    ) -> Optional[JobPositionId]:
        """Create one job position in an active stage"""
        # Get job position workflow and find an active stage
        with self._database.get_session() as session:
            # Get the job position workflow (JOB_POSITION_OPENING type)
            # Note: The workflow_type is stored as the enum name, not the value
            workflow_result = session.execute(
                text("""
                    SELECT w.id
                    FROM workflows w
                    WHERE w.company_id = :company_id
                    AND w.workflow_type = :workflow_type
                    LIMIT 1
                """),
                {
                    "company_id": company_id.value,
                    "workflow_type": WorkflowTypeEnum.JOB_POSITION_OPENING.name
                }
            ).fetchone()

            if not workflow_result:
                print(f"Warning: No job position workflow found for company {company_id.value}")
                return None

            workflow_id = workflow_result[0]

            # Find a stage with stage_type='PROGRESS' (typically "Under Review" or "Approved" which are active)
            # For job positions, PROGRESS stages typically map to 'active' status
            active_stage_result = session.execute(
                text("""
                    SELECT id
                    FROM workflow_stages
                    WHERE workflow_id = :workflow_id
                    AND stage_type = 'PROGRESS'
                    AND is_active = true
                    ORDER BY "order" ASC
                    LIMIT 1
                """),
                {"workflow_id": workflow_id}
            ).fetchone()

            if not active_stage_result:
                # If no PROGRESS stage found, try SUCCESS (Published/Closed)
                success_stage_result = session.execute(
                    text("""
                        SELECT id
                        FROM workflow_stages
                        WHERE workflow_id = :workflow_id
                        AND stage_type = 'SUCCESS'
                        AND is_active = true
                        ORDER BY "order" ASC
                        LIMIT 1
                    """),
                    {"workflow_id": workflow_id}
                ).fetchone()
                
                if success_stage_result:
                    stage_id = success_stage_result[0]
                else:
                    # If no active stage found, use initial stage as fallback
                    initial_stage_result = session.execute(
                        text("""
                            SELECT id
                            FROM workflow_stages
                            WHERE workflow_id = :workflow_id
                            AND stage_type = 'INITIAL'
                            AND is_active = true
                            ORDER BY "order" ASC
                            LIMIT 1
                        """),
                        {"workflow_id": workflow_id}
                    ).fetchone()
                    
                    if not initial_stage_result:
                        print(f"Warning: No active stage found for workflow {workflow_id}")
                        return None
                    
                    stage_id = initial_stage_result[0]
            else:
                stage_id = active_stage_result[0]

            job_position_workflow_id = JobPositionWorkflowId.from_string(workflow_id) if workflow_id else None
            stage_id_vo = StageId.from_string(stage_id) if stage_id else None

        # Create one job position in active stage
        try:
            job_position_id = JobPositionId.generate()
            
            create_job_position_cmd = CreateJobPositionCommand(
                id=job_position_id,
                company_id=company_id,
                job_position_workflow_id=job_position_workflow_id,
                stage_id=stage_id_vo,
                title="Senior Software Engineer",
                description="We are looking for an experienced software engineer to join our team. You will work on exciting projects and collaborate with talented colleagues.",
                job_category=JobCategoryEnum.TECHNOLOGY,
                visibility=JobPositionVisibilityEnum.PUBLIC
            )
            self._command_bus.dispatch(create_job_position_cmd)
            print(f"Created active job position: {job_position_id.value} in stage: {stage_id}")
            return job_position_id
        except Exception as e:
            print(f"Error creating active job position: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _create_company_candidates(
        self,
        company_id: CompanyId,
        company_user_id: CompanyUserId,
        candidate_ids: list[CandidateId],
        active_job_position_id: Optional[JobPositionId] = None
    ) -> None:
        """Create company-candidate relationships with random workflow assignments and link to active job position"""
        # Get workflows for the company
        with self._database.get_session() as session:
            # Get phases for the company
            phases_result = session.execute(
                text("""
                    SELECT id FROM company_phases
                    WHERE company_id = :company_id
                    ORDER BY sort_order ASC
                """),
                {"company_id": company_id.value}
            ).fetchall()

            if not phases_result:
                return

            phases = [row[0] for row in phases_result]

            # Get workflows and their initial stages
            workflows_info = {}
            for phase_id in phases:
                workflow_result = session.execute(
                    text("""
                        SELECT w.id, ws.id as initial_stage_id
                        FROM workflows w
                        LEFT JOIN workflow_stages ws ON w.id = ws.workflow_id
                        WHERE w.phase_id = :phase_id
                        AND ws.stage_type = 'INITIAL'
                        ORDER BY ws."order" ASC
                        LIMIT 1
                    """),
                    {"phase_id": phase_id}
                ).fetchone()

                if workflow_result:
                    workflows_info[workflow_result[0]] = {
                        'initial_stage_id': WorkflowStageId.from_string(workflow_result[1]) if workflow_result[1] else None
                    }

            if not workflows_info:
                return

            workflow_ids = list(workflows_info.keys())

            for candidate_id in candidate_ids:
                try:
                    # Generate company candidate ID
                    company_candidate_id = CompanyCandidateId.generate()

                    # Create company candidate first
                    create_cc_cmd = CreateCompanyCandidateCommand(
                        id=company_candidate_id,
                        company_id=company_id,
                        candidate_id=candidate_id,
                        created_by_user_id=company_user_id,
                        source="sample_data",
                        priority=CandidatePriority.MEDIUM
                    )
                    self._command_bus.dispatch(create_cc_cmd)

                    # Randomly select a workflow and assign it
                    workflow_id_str = random.choice(workflow_ids)
                    workflow_data = workflows_info[workflow_id_str]
                    initial_stage_id = workflow_data['initial_stage_id']

                    if initial_stage_id:
                        assign_workflow_cmd = AssignWorkflowCommand(
                            id=company_candidate_id,
                            workflow_id=WorkflowId.from_string(workflow_id_str),
                            initial_stage_id=initial_stage_id
                        )
                        self._command_bus.dispatch(assign_workflow_cmd)

                    # Link candidate to active job position if available
                    if active_job_position_id:
                        try:
                            create_application_cmd = CreateCandidateApplicationCommand(
                                candidate_id=str(candidate_id.value),
                                job_position_id=str(active_job_position_id.value),
                                notes="Sample data application"
                            )
                            self._command_bus.dispatch(create_application_cmd)
                        except Exception:
                            # Skip application creation if it fails (e.g., duplicate)
                            pass
                except Exception:
                    # Skip company-candidates that fail to create
                    continue

    def _create_sample_job_positions(
        self,
        company_id: CompanyId,
        num_job_positions: int
    ) -> None:
        """Create sample job positions"""
        job_titles = [
            "Senior Software Engineer",
            "Product Manager",
            "UX Designer",
            "Data Scientist",
            "DevOps Engineer",
            "Marketing Manager",
            "Sales Representative",
            "HR Specialist",
            "Financial Analyst",
            "Customer Success Manager",
            "Backend Developer",
            "Frontend Developer",
            "Full Stack Developer",
            "QA Engineer",
            "Technical Writer",
            "Business Analyst",
            "Project Manager",
            "Content Manager",
            "Operations Manager",
            "Account Executive"
        ]

        job_descriptions = [
            "We are looking for an experienced professional to join our team. You will work on exciting projects and collaborate with talented colleagues.",
            "Join our dynamic team and help shape the future of our products. This role offers great growth opportunities and competitive benefits.",
            "We need a creative and motivated individual who can bring fresh ideas to our team. You'll work in a collaborative environment with room for innovation.",
            "This position offers the opportunity to work on cutting-edge technology and make a real impact. We value diversity and inclusion.",
            "We're seeking a passionate professional who is eager to learn and grow. You'll be part of a supportive team that values work-life balance."
        ]

        job_categories = [
            JobCategoryEnum.TECHNOLOGY,
            JobCategoryEnum.SALES,
            JobCategoryEnum.MARKETING,
            JobCategoryEnum.HR,
            JobCategoryEnum.FINANCE,
            JobCategoryEnum.OPERATIONS,
            JobCategoryEnum.ADMINISTRATION,
            JobCategoryEnum.CUSTOMER_SERVICE,
            JobCategoryEnum.OTHER
        ]

        # Get job position workflow and initial stage
        with self._database.get_session() as session:
            # Get the job position workflow (JOB_POSITION_OPENING type)
            workflow_result = session.execute(
                text("""
                    SELECT w.id, ws.id as initial_stage_id
                    FROM workflows w
                    LEFT JOIN workflow_stages ws ON w.id = ws.workflow_id
                    WHERE w.company_id = :company_id
                    AND w.workflow_type = :workflow_type
                    AND ws.stage_type = 'initial'
                    ORDER BY ws."order" ASC
                    LIMIT 1
                """),
                {
                    "company_id": company_id.value,
                    "workflow_type": WorkflowTypeEnum.JOB_POSITION_OPENING.name
                }
            ).fetchone()

            if not workflow_result:
                # No job position workflow found, skip creating job positions
                return

            workflow_id = workflow_result[0]
            initial_stage_id = workflow_result[1]

            job_position_workflow_id = JobPositionWorkflowId.from_string(workflow_id) if workflow_id else None
            stage_id = StageId.from_string(initial_stage_id) if initial_stage_id else None

        # Create job positions
        for i in range(num_job_positions):
            try:
                job_position_id = JobPositionId.generate()
                title = random.choice(job_titles)
                description = random.choice(job_descriptions)
                category = random.choice(job_categories)
                
                # Random visibility (mostly public, some internal)
                visibility = random.choice([
                    JobPositionVisibilityEnum.PUBLIC,
                    JobPositionVisibilityEnum.PUBLIC,
                    JobPositionVisibilityEnum.PUBLIC,
                    JobPositionVisibilityEnum.INTERNAL,
                    JobPositionVisibilityEnum.HIDDEN
                ])

                create_job_position_cmd = CreateJobPositionCommand(
                    id=job_position_id,
                    company_id=company_id,
                    job_position_workflow_id=job_position_workflow_id,
                    stage_id=stage_id,
                    title=title,
                    description=description,
                    job_category=category,
                    visibility=visibility
                )
                self._command_bus.dispatch(create_job_position_cmd)
            except Exception:
                # Skip job positions that fail to create
                continue

