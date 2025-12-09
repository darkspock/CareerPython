# Evaluation Plans - Backend Implementation Tasks

## Overview

This document contains the detailed backend implementation tasks for the Evaluation Plans feature with three-tier override system.

**Reference Documents:**
- `EvaluationPlans.md` - Original PRD
- `EvaluationPlans_analysis.md` - Technical analysis
- `EvaluationPlans_UX_analysis.md` - UX requirements

---

## Phase 1: Core Entities - EvaluationPlan

### Task 1.1: Create EvaluationPlan Domain Layer

**Location:** `src/interview_bc/evaluation_plan/domain/`

#### 1.1.1 Create Value Objects

**File:** `src/interview_bc/evaluation_plan/domain/value_objects/evaluation_plan_id.py`
```python
# Create EvaluationPlanId value object
# - Extend from base ULID ID pattern
# - Include generate() class method
# - Include from_string() class method
```

**File:** `src/interview_bc/evaluation_plan/domain/value_objects/plan_stage_config_id.py`
```python
# Create PlanStageConfigId value object
# - Same pattern as EvaluationPlanId
```

**File:** `src/interview_bc/evaluation_plan/domain/value_objects/__init__.py`
```python
# Export both value objects
```

#### 1.1.2 Create Enums

**File:** `src/interview_bc/evaluation_plan/domain/enums/evaluation_plan_status.py`
```python
# Create EvaluationPlanStatusEnum
# Values: DRAFT, ACTIVE, ARCHIVED
```

**File:** `src/interview_bc/evaluation_plan/domain/enums/__init__.py`
```python
# Export enum
```

#### 1.1.3 Create Exceptions

**File:** `src/interview_bc/evaluation_plan/domain/exceptions/evaluation_plan_exceptions.py`
```python
# Create exceptions:
# - EvaluationPlanNotFoundError
# - EvaluationPlanValidationError
# - PlanStageConfigNotFoundError
# - IncompatibleWorkflowError
```

#### 1.1.4 Create EvaluationPlan Entity

**File:** `src/interview_bc/evaluation_plan/domain/entities/evaluation_plan.py`

```python
@dataclass
class EvaluationPlan:
    id: EvaluationPlanId
    company_id: CompanyId
    name: str
    description: Optional[str]
    department: Optional[str]
    workflow_id: Optional[WorkflowId]  # Optional compatibility constraint
    status: EvaluationPlanStatusEnum
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: EvaluationPlanId,
        company_id: CompanyId,
        name: str,
        description: Optional[str] = None,
        department: Optional[str] = None,
        workflow_id: Optional[WorkflowId] = None
    ) -> 'EvaluationPlan':
        # Validation:
        # - name must be non-empty, min 3 chars
        # - company_id required
        # Returns new instance with DRAFT status

    def update(
        self,
        name: str,
        description: Optional[str],
        department: Optional[str],
        workflow_id: Optional[WorkflowId]
    ) -> None:
        # Update mutable fields
        # Cannot change workflow_id if plan is ACTIVE and used by positions

    def activate(self) -> None:
        # Change status to ACTIVE
        # Validation: must have at least one stage config

    def archive(self) -> None:
        # Change status to ARCHIVED
        # Validation: cannot archive if used by active positions

    def is_compatible_with_workflow(self, workflow_id: WorkflowId) -> bool:
        # Check if plan can be used with given workflow
        # If self.workflow_id is None, compatible with all
        # If self.workflow_id is set, must match
```

#### 1.1.5 Create PlanStageConfig Entity

**File:** `src/interview_bc/evaluation_plan/domain/entities/plan_stage_config.py`

```python
@dataclass
class PlanStageConfig:
    id: PlanStageConfigId
    plan_id: EvaluationPlanId
    workflow_stage_id: WorkflowStageId
    interview_configurations: List[InterviewConfiguration]  # Reuse existing VO
    sort_order: int
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: PlanStageConfigId,
        plan_id: EvaluationPlanId,
        workflow_stage_id: WorkflowStageId,
        interview_configurations: List[InterviewConfiguration],
        sort_order: int = 0
    ) -> 'PlanStageConfig':
        # Validation:
        # - plan_id required
        # - workflow_stage_id required
        # - interview_configurations can be empty list

    def update_configurations(
        self,
        interview_configurations: List[InterviewConfiguration]
    ) -> None:
        # Replace interview configurations

    def add_configuration(
        self,
        config: InterviewConfiguration
    ) -> None:
        # Add to list if not already present

    def remove_configuration(
        self,
        template_id: str
    ) -> None:
        # Remove configuration by template_id
```

#### 1.1.6 Create Repository Interfaces

**File:** `src/interview_bc/evaluation_plan/domain/repositories/evaluation_plan_repository_interface.py`

```python
class EvaluationPlanRepositoryInterface(ABC):
    @abstractmethod
    def save(self, plan: EvaluationPlan) -> None: pass

    @abstractmethod
    def get_by_id(self, id: EvaluationPlanId) -> Optional[EvaluationPlan]: pass

    @abstractmethod
    def list_by_company(
        self,
        company_id: CompanyId,
        status: Optional[EvaluationPlanStatusEnum] = None,
        workflow_id: Optional[WorkflowId] = None
    ) -> List[EvaluationPlan]: pass

    @abstractmethod
    def delete(self, id: EvaluationPlanId) -> None: pass

    @abstractmethod
    def count_positions_using_plan(self, id: EvaluationPlanId) -> int: pass
```

**File:** `src/interview_bc/evaluation_plan/domain/repositories/plan_stage_config_repository_interface.py`

```python
class PlanStageConfigRepositoryInterface(ABC):
    @abstractmethod
    def save(self, config: PlanStageConfig) -> None: pass

    @abstractmethod
    def get_by_id(self, id: PlanStageConfigId) -> Optional[PlanStageConfig]: pass

    @abstractmethod
    def get_by_plan_and_stage(
        self,
        plan_id: EvaluationPlanId,
        stage_id: WorkflowStageId
    ) -> Optional[PlanStageConfig]: pass

    @abstractmethod
    def list_by_plan(self, plan_id: EvaluationPlanId) -> List[PlanStageConfig]: pass

    @abstractmethod
    def delete(self, id: PlanStageConfigId) -> None: pass

    @abstractmethod
    def delete_by_plan(self, plan_id: EvaluationPlanId) -> None: pass
```

---

### Task 1.2: Create EvaluationPlan Infrastructure Layer

**Location:** `src/interview_bc/evaluation_plan/infrastructure/`

#### 1.2.1 Create Database Models

**File:** `src/interview_bc/evaluation_plan/infrastructure/models/evaluation_plan_model.py`

```python
class EvaluationPlanModel(Base):
    __tablename__ = 'evaluation_plans'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    company_id: Mapped[str] = mapped_column(String, ForeignKey('companies.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    workflow_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey('workflows.id'), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default='DRAFT')
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    stage_configs = relationship('PlanStageConfigModel', back_populates='plan', cascade='all, delete-orphan')
```

**File:** `src/interview_bc/evaluation_plan/infrastructure/models/plan_stage_config_model.py`

```python
class PlanStageConfigModel(Base):
    __tablename__ = 'plan_stage_configs'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    plan_id: Mapped[str] = mapped_column(String, ForeignKey('evaluation_plans.id', ondelete='CASCADE'), nullable=False, index=True)
    workflow_stage_id: Mapped[str] = mapped_column(String, nullable=False)
    interview_configurations: Mapped[Optional[List[dict]]] = mapped_column(JSON, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    plan = relationship('EvaluationPlanModel', back_populates='stage_configs')

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('plan_id', 'workflow_stage_id', name='uq_plan_stage_configs_plan_stage'),
    )
```

#### 1.2.2 Create Repository Implementations

**File:** `src/interview_bc/evaluation_plan/infrastructure/repositories/evaluation_plan_repository.py`

```python
class EvaluationPlanRepository(EvaluationPlanRepositoryInterface):
    def __init__(self, database: Database):
        self._database = database

    def save(self, plan: EvaluationPlan) -> None:
        # Convert entity to model and save
        # Handle both insert and update

    def get_by_id(self, id: EvaluationPlanId) -> Optional[EvaluationPlan]:
        # Query and convert to entity

    def list_by_company(
        self,
        company_id: CompanyId,
        status: Optional[EvaluationPlanStatusEnum] = None,
        workflow_id: Optional[WorkflowId] = None
    ) -> List[EvaluationPlan]:
        # Query with filters

    def delete(self, id: EvaluationPlanId) -> None:
        # Delete plan (cascade deletes stage configs)

    def count_positions_using_plan(self, id: EvaluationPlanId) -> int:
        # Count job_positions with this evaluation_plan_id

    def _to_domain(self, model: EvaluationPlanModel) -> EvaluationPlan:
        # Convert model to entity

    def _to_model(self, entity: EvaluationPlan) -> EvaluationPlanModel:
        # Convert entity to model
```

**File:** `src/interview_bc/evaluation_plan/infrastructure/repositories/plan_stage_config_repository.py`

```python
class PlanStageConfigRepository(PlanStageConfigRepositoryInterface):
    # Implement all interface methods
    # Similar pattern to EvaluationPlanRepository
```

#### 1.2.3 Create Database Migration

**File:** `alembic/versions/xxxx_add_evaluation_plans_tables.py`

```python
"""add evaluation plans tables

Revision ID: xxxx
Revises: [previous]
Create Date: [date]
"""

def upgrade():
    # Create evaluation_plans table
    op.create_table(
        'evaluation_plans',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('department', sa.String(), nullable=True),
        sa.Column('workflow_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id']),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'])
    )
    op.create_index('ix_evaluation_plans_company_id', 'evaluation_plans', ['company_id'])
    op.create_index('ix_evaluation_plans_workflow_id', 'evaluation_plans', ['workflow_id'])
    op.create_index('ix_evaluation_plans_status', 'evaluation_plans', ['status'])

    # Create plan_stage_configs table
    op.create_table(
        'plan_stage_configs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('plan_id', sa.String(), nullable=False),
        sa.Column('workflow_stage_id', sa.String(), nullable=False),
        sa.Column('interview_configurations', sa.JSON(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['plan_id'], ['evaluation_plans.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('plan_id', 'workflow_stage_id', name='uq_plan_stage_configs_plan_stage')
    )
    op.create_index('ix_plan_stage_configs_plan_id', 'plan_stage_configs', ['plan_id'])

def downgrade():
    op.drop_table('plan_stage_configs')
    op.drop_table('evaluation_plans')
```

---

### Task 1.3: Create EvaluationPlan Application Layer

**Location:** `src/interview_bc/evaluation_plan/application/`

#### 1.3.1 Create DTOs

**File:** `src/interview_bc/evaluation_plan/application/dtos/evaluation_plan_dto.py`

```python
@dataclass
class EvaluationPlanDto:
    id: str
    company_id: str
    name: str
    description: Optional[str]
    department: Optional[str]
    workflow_id: Optional[str]
    status: str
    stage_config_count: int
    position_count: int  # Number of positions using this plan
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(
        entity: EvaluationPlan,
        stage_config_count: int = 0,
        position_count: int = 0
    ) -> 'EvaluationPlanDto':
        # Convert entity to DTO
```

**File:** `src/interview_bc/evaluation_plan/application/dtos/plan_stage_config_dto.py`

```python
@dataclass
class PlanStageConfigDto:
    id: str
    plan_id: str
    workflow_stage_id: str
    workflow_stage_name: Optional[str]  # Enriched from workflow
    interview_configurations: List[dict]  # InterviewConfiguration as dict
    sort_order: int
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(
        entity: PlanStageConfig,
        stage_name: Optional[str] = None
    ) -> 'PlanStageConfigDto':
        # Convert entity to DTO
```

**File:** `src/interview_bc/evaluation_plan/application/dtos/evaluation_plan_full_dto.py`

```python
@dataclass
class EvaluationPlanFullDto:
    """Full DTO with stage configs included"""
    id: str
    company_id: str
    name: str
    description: Optional[str]
    department: Optional[str]
    workflow_id: Optional[str]
    workflow_name: Optional[str]  # Enriched
    status: str
    stage_configs: List[PlanStageConfigDto]
    position_count: int
    created_at: datetime
    updated_at: datetime
```

#### 1.3.2 Create Commands

**File:** `src/interview_bc/evaluation_plan/application/commands/create_evaluation_plan_command.py`

```python
@dataclass(frozen=True)
class CreateEvaluationPlanCommand(Command):
    id: EvaluationPlanId
    company_id: CompanyId
    name: str
    description: Optional[str] = None
    department: Optional[str] = None
    workflow_id: Optional[WorkflowId] = None


class CreateEvaluationPlanCommandHandler(CommandHandler[CreateEvaluationPlanCommand]):
    def __init__(
        self,
        repository: EvaluationPlanRepositoryInterface,
        workflow_repository: WorkflowRepositoryInterface  # To validate workflow exists
    ):
        self._repository = repository
        self._workflow_repository = workflow_repository

    def execute(self, command: CreateEvaluationPlanCommand) -> None:
        # Validate workflow exists if provided
        if command.workflow_id:
            workflow = self._workflow_repository.get_by_id(command.workflow_id)
            if not workflow:
                raise EvaluationPlanValidationError(f"Workflow {command.workflow_id} not found")

        # Create entity
        plan = EvaluationPlan.create(
            id=command.id,
            company_id=command.company_id,
            name=command.name,
            description=command.description,
            department=command.department,
            workflow_id=command.workflow_id
        )

        # Save
        self._repository.save(plan)
```

**File:** `src/interview_bc/evaluation_plan/application/commands/update_evaluation_plan_command.py`

```python
@dataclass(frozen=True)
class UpdateEvaluationPlanCommand(Command):
    id: EvaluationPlanId
    name: str
    description: Optional[str] = None
    department: Optional[str] = None
    workflow_id: Optional[WorkflowId] = None


class UpdateEvaluationPlanCommandHandler(CommandHandler[UpdateEvaluationPlanCommand]):
    def __init__(
        self,
        repository: EvaluationPlanRepositoryInterface,
        workflow_repository: WorkflowRepositoryInterface
    ):
        # Implementation
        pass

    def execute(self, command: UpdateEvaluationPlanCommand) -> None:
        # Get existing plan
        # Validate workflow if changed
        # Update and save
        pass
```

**File:** `src/interview_bc/evaluation_plan/application/commands/activate_evaluation_plan_command.py`

```python
@dataclass(frozen=True)
class ActivateEvaluationPlanCommand(Command):
    id: EvaluationPlanId


class ActivateEvaluationPlanCommandHandler(CommandHandler[ActivateEvaluationPlanCommand]):
    def __init__(
        self,
        repository: EvaluationPlanRepositoryInterface,
        stage_config_repository: PlanStageConfigRepositoryInterface
    ):
        pass

    def execute(self, command: ActivateEvaluationPlanCommand) -> None:
        # Get plan
        # Validate has at least one stage config
        # Activate
        pass
```

**File:** `src/interview_bc/evaluation_plan/application/commands/archive_evaluation_plan_command.py`

```python
# Similar pattern - archive the plan
```

**File:** `src/interview_bc/evaluation_plan/application/commands/delete_evaluation_plan_command.py`

```python
# Delete plan (only if not used by positions or force=True)
```

**File:** `src/interview_bc/evaluation_plan/application/commands/set_stage_config_command.py`

```python
@dataclass(frozen=True)
class SetStageConfigCommand(Command):
    """Set or update stage config for a plan"""
    plan_id: EvaluationPlanId
    workflow_stage_id: WorkflowStageId
    interview_configurations: List[InterviewConfiguration]
    sort_order: int = 0


class SetStageConfigCommandHandler(CommandHandler[SetStageConfigCommand]):
    def __init__(
        self,
        plan_repository: EvaluationPlanRepositoryInterface,
        config_repository: PlanStageConfigRepositoryInterface,
        stage_repository: WorkflowStageRepositoryInterface
    ):
        pass

    def execute(self, command: SetStageConfigCommand) -> None:
        # Validate plan exists
        # Validate stage exists (if plan has workflow_id constraint)
        # Upsert stage config
        pass
```

**File:** `src/interview_bc/evaluation_plan/application/commands/remove_stage_config_command.py`

```python
@dataclass(frozen=True)
class RemoveStageConfigCommand(Command):
    plan_id: EvaluationPlanId
    workflow_stage_id: WorkflowStageId


class RemoveStageConfigCommandHandler(CommandHandler[RemoveStageConfigCommand]):
    # Delete the stage config
    pass
```

#### 1.3.3 Create Queries

**File:** `src/interview_bc/evaluation_plan/application/queries/get_evaluation_plan_by_id_query.py`

```python
@dataclass(frozen=True)
class GetEvaluationPlanByIdQuery(Query):
    id: EvaluationPlanId
    include_stage_configs: bool = True


class GetEvaluationPlanByIdQueryHandler(QueryHandler[GetEvaluationPlanByIdQuery, Optional[EvaluationPlanFullDto]]):
    def __init__(
        self,
        repository: EvaluationPlanRepositoryInterface,
        stage_config_repository: PlanStageConfigRepositoryInterface,
        workflow_repository: WorkflowRepositoryInterface,
        stage_repository: WorkflowStageRepositoryInterface
    ):
        pass

    def handle(self, query: GetEvaluationPlanByIdQuery) -> Optional[EvaluationPlanFullDto]:
        # Get plan
        # Get stage configs if requested
        # Enrich with workflow and stage names
        # Return DTO
        pass
```

**File:** `src/interview_bc/evaluation_plan/application/queries/list_evaluation_plans_query.py`

```python
@dataclass(frozen=True)
class ListEvaluationPlansQuery(Query):
    company_id: CompanyId
    status: Optional[EvaluationPlanStatusEnum] = None
    workflow_id: Optional[WorkflowId] = None  # Filter by compatible workflow
    department: Optional[str] = None


class ListEvaluationPlansQueryHandler(QueryHandler[ListEvaluationPlansQuery, List[EvaluationPlanDto]]):
    # List plans with filters
    pass
```

**File:** `src/interview_bc/evaluation_plan/application/queries/list_stage_configs_by_plan_query.py`

```python
@dataclass(frozen=True)
class ListStageConfigsByPlanQuery(Query):
    plan_id: EvaluationPlanId


class ListStageConfigsByPlanQueryHandler(QueryHandler[ListStageConfigsByPlanQuery, List[PlanStageConfigDto]]):
    # List all stage configs for a plan
    pass
```

---

### Task 1.4: Register in Container

**File:** `core/containers/interview_container.py` (or create new `evaluation_plan_container.py`)

```python
# Add providers for:
# - evaluation_plan_repository
# - plan_stage_config_repository
# - All command handlers
# - All query handlers
```

**File:** `core/containers/main_container.py`

```python
# Wire the new container
```

---

## Phase 2: JobPosition Integration

### Task 2.1: Add evaluation_plan_id to JobPosition

#### 2.1.1 Update Domain Entity

**File:** `src/company_bc/job_position/domain/entities/job_position.py`

```python
# Add field:
evaluation_plan_id: Optional[EvaluationPlanId]

# Update create() method to accept evaluation_plan_id
# Update update_details() method to accept evaluation_plan_id
# Update _from_repository() method
```

#### 2.1.2 Update Infrastructure Model

**File:** `src/company_bc/job_position/infrastructure/models/job_position_model.py`

```python
# Add column:
evaluation_plan_id: Mapped[Optional[str]] = mapped_column(
    String,
    ForeignKey('evaluation_plans.id'),
    nullable=True,
    index=True
)
```

#### 2.1.3 Update Repository

**File:** `src/company_bc/job_position/infrastructure/repositories/job_position_repository.py`

```python
# Update _to_domain() to handle evaluation_plan_id
# Update _to_model() to handle evaluation_plan_id
```

#### 2.1.4 Create Migration

**File:** `alembic/versions/xxxx_add_evaluation_plan_id_to_job_positions.py`

```python
def upgrade():
    op.add_column(
        'job_positions',
        sa.Column('evaluation_plan_id', sa.String(), nullable=True)
    )
    op.create_foreign_key(
        'fk_job_positions_evaluation_plan_id',
        'job_positions',
        'evaluation_plans',
        ['evaluation_plan_id'],
        ['id']
    )
    op.create_index(
        'ix_job_positions_evaluation_plan_id',
        'job_positions',
        ['evaluation_plan_id']
    )

def downgrade():
    op.drop_index('ix_job_positions_evaluation_plan_id')
    op.drop_constraint('fk_job_positions_evaluation_plan_id', 'job_positions')
    op.drop_column('job_positions', 'evaluation_plan_id')
```

#### 2.1.5 Update Commands

**File:** `src/company_bc/job_position/application/commands/create_job_position.py`

```python
# Add evaluation_plan_id to command
# Validate plan exists and is compatible with workflow
```

**File:** `src/company_bc/job_position/application/commands/update_job_position.py`

```python
# Add evaluation_plan_id to command
# Validate plan compatibility on change
```

#### 2.1.6 Update DTOs

**File:** `src/company_bc/job_position/application/queries/job_position_dto.py`

```python
# Add field:
evaluation_plan_id: Optional[str]
evaluation_plan_name: Optional[str]  # Enriched
```

---

## Phase 3: Position Interview Config (Position-Level Override)

### Task 3.1: Create PositionInterviewConfig Domain Layer

**Location:** `src/company_bc/position_interview_config/domain/`

#### 3.1.1 Create Value Objects

**File:** `src/company_bc/position_interview_config/domain/value_objects/position_interview_config_id.py`

```python
# Same pattern as other ID value objects
```

#### 3.1.2 Create Entity

**File:** `src/company_bc/position_interview_config/domain/entities/position_interview_config.py`

```python
@dataclass
class PositionInterviewConfig:
    id: PositionInterviewConfigId
    position_id: JobPositionId
    stage_id: WorkflowStageId
    interview_configurations: List[InterviewConfiguration]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: PositionInterviewConfigId,
        position_id: str,
        stage_id: str,
        interview_configurations: List[InterviewConfiguration]
    ) -> 'PositionInterviewConfig':
        # Validation and creation

    def update_configurations(
        self,
        interview_configurations: List[InterviewConfiguration]
    ) -> None:
        # Update configs
```

#### 3.1.3 Create Repository Interface

**File:** `src/company_bc/position_interview_config/domain/repositories/position_interview_config_repository_interface.py`

```python
class PositionInterviewConfigRepositoryInterface(ABC):
    @abstractmethod
    def save(self, config: PositionInterviewConfig) -> None: pass

    @abstractmethod
    def get_by_id(self, id: PositionInterviewConfigId) -> Optional[PositionInterviewConfig]: pass

    @abstractmethod
    def get_by_position_and_stage(
        self,
        position_id: JobPositionId,
        stage_id: WorkflowStageId
    ) -> Optional[PositionInterviewConfig]: pass

    @abstractmethod
    def list_by_position(self, position_id: JobPositionId) -> List[PositionInterviewConfig]: pass

    @abstractmethod
    def delete(self, id: PositionInterviewConfigId) -> None: pass

    @abstractmethod
    def delete_by_position_and_stage(
        self,
        position_id: JobPositionId,
        stage_id: WorkflowStageId
    ) -> None: pass
```

### Task 3.2: Create PositionInterviewConfig Infrastructure Layer

#### 3.2.1 Create Model

**File:** `src/company_bc/position_interview_config/infrastructure/models/position_interview_config_model.py`

```python
class PositionInterviewConfigModel(Base):
    __tablename__ = 'position_interview_configs'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    position_id: Mapped[str] = mapped_column(
        String,
        ForeignKey('job_positions.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    stage_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    interview_configurations: Mapped[List[dict]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint('position_id', 'stage_id', name='uq_position_interview_configs_position_stage'),
    )
```

#### 3.2.2 Create Repository

**File:** `src/company_bc/position_interview_config/infrastructure/repositories/position_interview_config_repository.py`

```python
# Implement all interface methods
```

#### 3.2.3 Create Migration

**File:** `alembic/versions/xxxx_add_position_interview_configs_table.py`

```python
def upgrade():
    op.create_table(
        'position_interview_configs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('position_id', sa.String(), nullable=False),
        sa.Column('stage_id', sa.String(), nullable=False),
        sa.Column('interview_configurations', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['position_id'], ['job_positions.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('position_id', 'stage_id', name='uq_position_interview_configs_position_stage')
    )
    op.create_index('ix_position_interview_configs_position_id', 'position_interview_configs', ['position_id'])
    op.create_index('ix_position_interview_configs_stage_id', 'position_interview_configs', ['stage_id'])

def downgrade():
    op.drop_table('position_interview_configs')
```

### Task 3.3: Create PositionInterviewConfig Application Layer

#### 3.3.1 Create Commands

**File:** `src/company_bc/position_interview_config/application/commands/set_position_interview_config_command.py`

```python
@dataclass(frozen=True)
class SetPositionInterviewConfigCommand(Command):
    position_id: JobPositionId
    stage_id: WorkflowStageId
    interview_configurations: List[InterviewConfiguration]


class SetPositionInterviewConfigCommandHandler(CommandHandler[SetPositionInterviewConfigCommand]):
    def __init__(
        self,
        repository: PositionInterviewConfigRepositoryInterface,
        position_repository: JobPositionRepositoryInterface,
        stage_repository: WorkflowStageRepositoryInterface
    ):
        pass

    def execute(self, command: SetPositionInterviewConfigCommand) -> None:
        # Validate position exists
        # Validate stage exists and belongs to position's workflow
        # Upsert config
        pass
```

**File:** `src/company_bc/position_interview_config/application/commands/remove_position_interview_config_command.py`

```python
@dataclass(frozen=True)
class RemovePositionInterviewConfigCommand(Command):
    position_id: JobPositionId
    stage_id: WorkflowStageId


class RemovePositionInterviewConfigCommandHandler(CommandHandler[RemovePositionInterviewConfigCommand]):
    # Delete the override, falling back to plan/stage default
    pass
```

#### 3.3.2 Create Queries

**File:** `src/company_bc/position_interview_config/application/queries/list_position_interview_configs_query.py`

```python
@dataclass(frozen=True)
class ListPositionInterviewConfigsQuery(Query):
    position_id: JobPositionId


class ListPositionInterviewConfigsQueryHandler(QueryHandler[...]):
    # Return all overrides for a position
    pass
```

---

## Phase 4: Interview Config Resolution Service

### Task 4.1: Create InterviewConfigResolver Service

**File:** `src/interview_bc/evaluation_plan/application/services/interview_config_resolver.py`

```python
@dataclass
class ResolvedInterviewConfig:
    """Result of interview config resolution"""
    interview_configurations: List[InterviewConfiguration]
    source: str  # 'position', 'plan', or 'stage'
    source_id: Optional[str]  # ID of the source entity


class InterviewConfigResolver:
    """
    Service to resolve interview configurations for a position/stage
    using three-tier priority system.
    """

    def __init__(
        self,
        position_interview_config_repo: PositionInterviewConfigRepositoryInterface,
        plan_stage_config_repo: PlanStageConfigRepositoryInterface,
        stage_repo: WorkflowStageRepositoryInterface,
        plan_repo: EvaluationPlanRepositoryInterface
    ):
        self._position_config_repo = position_interview_config_repo
        self._plan_config_repo = plan_stage_config_repo
        self._stage_repo = stage_repo
        self._plan_repo = plan_repo

    def resolve(
        self,
        position_id: JobPositionId,
        stage_id: WorkflowStageId,
        evaluation_plan_id: Optional[EvaluationPlanId] = None
    ) -> ResolvedInterviewConfig:
        """
        Resolve interview configurations using priority:
        1. Position-specific override (highest)
        2. Evaluation Plan config
        3. Workflow Stage default (lowest)
        """

        # Priority 1: Check position-specific override
        position_config = self._position_config_repo.get_by_position_and_stage(
            position_id, stage_id
        )
        if position_config and position_config.interview_configurations:
            return ResolvedInterviewConfig(
                interview_configurations=position_config.interview_configurations,
                source='position',
                source_id=str(position_config.id)
            )

        # Priority 2: Check Evaluation Plan config
        if evaluation_plan_id:
            plan_config = self._plan_config_repo.get_by_plan_and_stage(
                evaluation_plan_id, stage_id
            )
            if plan_config and plan_config.interview_configurations:
                return ResolvedInterviewConfig(
                    interview_configurations=plan_config.interview_configurations,
                    source='plan',
                    source_id=str(evaluation_plan_id)
                )

        # Priority 3: Fallback to workflow stage defaults
        stage = self._stage_repo.get_by_id(stage_id)
        if stage:
            return ResolvedInterviewConfig(
                interview_configurations=stage.interview_configurations or [],
                source='stage',
                source_id=str(stage_id)
            )

        # No config found
        return ResolvedInterviewConfig(
            interview_configurations=[],
            source='none',
            source_id=None
        )

    def resolve_all_stages(
        self,
        position_id: JobPositionId,
        workflow_id: WorkflowId,
        evaluation_plan_id: Optional[EvaluationPlanId] = None
    ) -> Dict[str, ResolvedInterviewConfig]:
        """
        Resolve configs for all stages in a workflow.
        Returns dict: stage_id -> ResolvedInterviewConfig
        """
        stages = self._stage_repo.list_by_workflow(workflow_id)
        result = {}
        for stage in stages:
            result[str(stage.id)] = self.resolve(
                position_id, stage.id, evaluation_plan_id
            )
        return result
```

### Task 4.2: Create Query for Resolved Config

**File:** `src/interview_bc/evaluation_plan/application/queries/get_resolved_interview_config_query.py`

```python
@dataclass(frozen=True)
class GetResolvedInterviewConfigQuery(Query):
    position_id: JobPositionId
    stage_id: WorkflowStageId


@dataclass
class ResolvedInterviewConfigDto:
    interview_configurations: List[dict]
    source: str
    source_id: Optional[str]
    source_name: Optional[str]  # Enriched name


class GetResolvedInterviewConfigQueryHandler(QueryHandler[...]):
    def __init__(
        self,
        resolver: InterviewConfigResolver,
        position_repository: JobPositionRepositoryInterface
    ):
        pass

    def handle(self, query: GetResolvedInterviewConfigQuery) -> ResolvedInterviewConfigDto:
        # Get position to find evaluation_plan_id
        # Call resolver
        # Enrich with source name
        # Return DTO
        pass
```

---

## Phase 5: REST API Endpoints

### Task 5.1: Create Evaluation Plan Router

**File:** `adapters/http/interview_app/evaluation_plan/routers/evaluation_plan_router.py`

```python
router = APIRouter(prefix="/api/evaluation-plans", tags=["evaluation-plans"])

@router.post("/", response_model=EvaluationPlanResponse, status_code=201)
async def create_evaluation_plan(request: CreateEvaluationPlanRequest, ...):
    pass

@router.get("/{plan_id}", response_model=EvaluationPlanFullResponse)
async def get_evaluation_plan(plan_id: str, ...):
    pass

@router.get("/company/{company_id}", response_model=List[EvaluationPlanResponse])
async def list_evaluation_plans(
    company_id: str,
    status: Optional[str] = None,
    workflow_id: Optional[str] = None,
    department: Optional[str] = None,
    ...
):
    pass

@router.put("/{plan_id}", response_model=EvaluationPlanResponse)
async def update_evaluation_plan(plan_id: str, request: UpdateEvaluationPlanRequest, ...):
    pass

@router.post("/{plan_id}/activate", response_model=EvaluationPlanResponse)
async def activate_evaluation_plan(plan_id: str, ...):
    pass

@router.post("/{plan_id}/archive", response_model=EvaluationPlanResponse)
async def archive_evaluation_plan(plan_id: str, ...):
    pass

@router.delete("/{plan_id}", status_code=204)
async def delete_evaluation_plan(plan_id: str, force: bool = False, ...):
    pass

# Stage config endpoints
@router.put("/{plan_id}/stages/{stage_id}", response_model=PlanStageConfigResponse)
async def set_stage_config(
    plan_id: str,
    stage_id: str,
    request: SetStageConfigRequest,
    ...
):
    pass

@router.delete("/{plan_id}/stages/{stage_id}", status_code=204)
async def remove_stage_config(plan_id: str, stage_id: str, ...):
    pass

@router.get("/{plan_id}/stages", response_model=List[PlanStageConfigResponse])
async def list_stage_configs(plan_id: str, ...):
    pass
```

### Task 5.2: Create Position Interview Config Router

**File:** `adapters/http/company_app/job_position/routers/position_interview_config_router.py`

```python
router = APIRouter(prefix="/api/positions", tags=["position-interview-config"])

@router.get("/{position_id}/interview-configs", response_model=List[PositionInterviewConfigResponse])
async def list_position_interview_configs(position_id: str, ...):
    pass

@router.get("/{position_id}/interview-configs/{stage_id}", response_model=PositionInterviewConfigResponse)
async def get_position_interview_config(position_id: str, stage_id: str, ...):
    pass

@router.put("/{position_id}/interview-configs/{stage_id}", response_model=PositionInterviewConfigResponse)
async def set_position_interview_config(
    position_id: str,
    stage_id: str,
    request: SetPositionInterviewConfigRequest,
    ...
):
    pass

@router.delete("/{position_id}/interview-configs/{stage_id}", status_code=204)
async def remove_position_interview_config(position_id: str, stage_id: str, ...):
    pass

@router.get("/{position_id}/stages/{stage_id}/resolved-config", response_model=ResolvedInterviewConfigResponse)
async def get_resolved_interview_config(position_id: str, stage_id: str, ...):
    pass

@router.get("/{position_id}/interview-overview", response_model=PositionInterviewOverviewResponse)
async def get_position_interview_overview(position_id: str, ...):
    """Get all resolved configs for all stages of the position"""
    pass
```

### Task 5.3: Create Request/Response Schemas

**File:** `adapters/http/interview_app/evaluation_plan/schemas/`

```python
# Create all request and response Pydantic models:
# - CreateEvaluationPlanRequest
# - UpdateEvaluationPlanRequest
# - SetStageConfigRequest
# - EvaluationPlanResponse
# - EvaluationPlanFullResponse
# - PlanStageConfigResponse
# - etc.
```

### Task 5.4: Create Controllers

**File:** `adapters/http/interview_app/evaluation_plan/controllers/evaluation_plan_controller.py`

```python
# Create controller following established patterns
# Use mappers for DTO -> Response conversion
```

### Task 5.5: Wire Routers in main.py

**File:** `main.py`

```python
# Add imports and include routers:
from adapters.http.interview_app.evaluation_plan.routers.evaluation_plan_router import router as evaluation_plan_router
from adapters.http.company_app.job_position.routers.position_interview_config_router import router as position_interview_config_router

app.include_router(evaluation_plan_router)
app.include_router(position_interview_config_router)

# Add to container.wire()
```

---

## Testing Checklist

### Unit Tests

- [ ] EvaluationPlan entity creation and validation
- [ ] PlanStageConfig entity operations
- [ ] PositionInterviewConfig entity operations
- [ ] InterviewConfigResolver priority logic
- [ ] All command handlers
- [ ] All query handlers

### Integration Tests

- [ ] EvaluationPlan CRUD operations
- [ ] PlanStageConfig CRUD operations
- [ ] PositionInterviewConfig CRUD operations
- [ ] Plan assignment to position
- [ ] Override resolution with all three tiers

### API Tests

- [ ] All evaluation plan endpoints
- [ ] All position interview config endpoints
- [ ] Resolved config endpoint
- [ ] Error cases (not found, validation, compatibility)

---

## Completion Criteria

- [ ] All migrations applied successfully
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] API endpoints documented in OpenAPI
- [ ] mypy passes with no errors
- [ ] flake8 passes with no errors
