# Evaluation Plans - Technical Analysis

## 1. Executive Summary

This document analyzes the "Evaluation Plans" PRD against the existing codebase architecture to determine implementation feasibility, identify gaps, and recommend an implementation strategy.

**Key Finding:** The current architecture already has partial support for the concept through `interview_configurations` at the `WorkflowStage` level. However, this is at the wrong abstraction level for the PRD requirements. The PRD proposes a new intermediate entity that separates **content (templates)** from **structure (workflow)**, enabling role-specific interview configurations.

---

## 2. Current Architecture Analysis

### 2.1 Existing Entities and Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CURRENT ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐      1:N      ┌───────────────────┐                      │
│  │   Workflow   │──────────────→│   WorkflowStage   │                      │
│  │              │               │                   │                      │
│  │ - company_id │               │ - interview_      │                      │
│  │ - phase_id   │               │   configurations  │←─ [InterviewConfig]  │
│  │ - is_default │               │   (template_id    │                      │
│  └──────────────┘               │    + mode)        │                      │
│         ↑                       └───────────────────┘                      │
│         │                                                                   │
│         │ references                                                        │
│         │                                                                   │
│  ┌──────────────────┐                                                      │
│  │   JobPosition    │                                                      │
│  │                  │    ┌─────────────────────────────┐                   │
│  │ - workflow_id    │    │   InterviewTemplate         │                   │
│  │ - phase_workflows│    │                             │                   │
│  │                  │    │ - company_id                │                   │
│  └──────────────────┘    │ - sections/questions        │                   │
│                          └─────────────────────────────┘                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Key Files Examined

| Entity | Location | Purpose |
|--------|----------|---------|
| `Workflow` | `src/shared_bc/customization/workflow/domain/entities/workflow.py` | Process structure (stages sequence) |
| `WorkflowStage` | `src/shared_bc/customization/workflow/domain/entities/workflow_stage.py` | Individual stage with embedded `interview_configurations` |
| `InterviewConfiguration` | `src/interview_bc/interview/domain/value_objects/interview_configuration.py` | Value object: `template_id` + `mode` |
| `InterviewTemplate` | `src/interview_bc/interview_template/domain/entities/interview_template.py` | Question sets with sections |
| `JobPosition` | `src/company_bc/job_position/domain/entities/job_position.py` | Links to workflow, can have phase-specific workflows |
| `PositionStageAssignment` | `src/company_bc/position_stage_assignment/domain/entities/position_stage_assignment.py` | Position-level user assignments (override pattern) |

### 2.3 Current Limitations

1. **Interview templates are bound to workflow stages**, not to job roles/positions
2. **All positions using the same workflow get identical interview content**
3. **No separation between process structure and assessment content**
4. **To change interview content, you must either:**
   - Modify the workflow stage (affects all positions)
   - Create a duplicate workflow (redundant structure)

---

## 3. PRD Requirements vs Current State

### 3.1 Gap Analysis

| PRD Requirement | Current State | Gap |
|-----------------|---------------|-----|
| Evaluation Plan entity (content package) | Not exists | **NEW ENTITY NEEDED** |
| Stage-to-template mapping per plan | `WorkflowStage.interview_configurations` | Exists but at wrong level |
| Workflow compatibility check | N/A | **NEW LOGIC NEEDED** |
| JobPosition → Plan assignment | Only `workflow_id` exists | **NEW FIELD NEEDED** |
| Same workflow, different content | Not supported | **CORE GAP** |
| Template library for reuse | `InterviewTemplate` exists | Partial (no library UI) |
| Position-level template override | Not exists | **NEW ENTITY NEEDED** (like `PositionStageAssignment`) |

### 3.2 Core Problem Statement

```
CURRENT:  JobPosition → Workflow → Stage → Templates (fixed)
                                            ↑
                                    Cannot vary by role or position

PROPOSED (Three-Tier Override System):

JobPosition ─┬─→ PositionInterviewConfig ─→ Templates  (Priority 1: Position-specific)
             │         ↓ (if not set)
             ├─→ EvaluationPlan.PlanStageConfig ─→ Templates  (Priority 2: Role-specific)
             │         ↓ (if not set)
             └─→ Workflow → Stage.interview_configs ─→ Templates  (Priority 3: Default)
```

---

## 4. Proposed Data Model

### 4.1 New Entities

```python
# New Entity: EvaluationPlan
@dataclass
class EvaluationPlan:
    id: EvaluationPlanId
    company_id: CompanyId
    name: str                              # e.g., "Senior Frontend Kit"
    description: Optional[str]
    department: Optional[str]              # e.g., "Engineering"
    workflow_id: Optional[WorkflowId]      # Optional: enforce compatibility
    status: EvaluationPlanStatusEnum       # DRAFT, ACTIVE, ARCHIVED
    created_at: datetime
    updated_at: datetime

# New Entity: PlanStageConfig (The Stage-Template Mapping)
@dataclass
class PlanStageConfig:
    id: PlanStageConfigId
    plan_id: EvaluationPlanId
    workflow_stage_id: WorkflowStageId
    interview_configurations: List[InterviewConfiguration]  # Reuse existing VO
    sort_order: int
    created_at: datetime
    updated_at: datetime
```

### 4.2 New Entity: PositionInterviewConfig (Position-Level Override)

```python
# New Entity: PositionInterviewConfig (Position-Specific Template Override)
# Similar pattern to existing PositionStageAssignment for user overrides
@dataclass
class PositionInterviewConfig:
    id: PositionInterviewConfigId
    position_id: JobPositionId
    stage_id: WorkflowStageId
    interview_configurations: List[InterviewConfiguration]  # Reuse existing VO
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: PositionInterviewConfigId,
        position_id: str,
        stage_id: str,
        interview_configurations: List[InterviewConfiguration]
    ) -> 'PositionInterviewConfig':
        """Create a position-specific interview configuration override"""
        return PositionInterviewConfig(
            id=id,
            position_id=JobPositionId.from_string(position_id),
            stage_id=WorkflowStageId.from_string(stage_id),
            interview_configurations=interview_configurations,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
```

### 4.3 Modified Entity: JobPosition

```python
@dataclass
class JobPosition:
    # ... existing fields ...
    job_position_workflow_id: Optional[JobPositionWorkflowId]
    evaluation_plan_id: Optional[EvaluationPlanId]  # NEW FIELD
    # Note: Position-specific interview configs stored in separate entity
    # (PositionInterviewConfig) following same pattern as PositionStageAssignment
    # ...
```

### 4.4 Database Schema Changes

```sql
-- New table: evaluation_plans
CREATE TABLE evaluation_plans (
    id VARCHAR PRIMARY KEY,
    company_id VARCHAR NOT NULL REFERENCES companies(id),
    name VARCHAR NOT NULL,
    description TEXT,
    department VARCHAR,
    workflow_id VARCHAR REFERENCES workflows(id),  -- Optional compatibility
    status VARCHAR NOT NULL DEFAULT 'DRAFT',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
CREATE INDEX ix_evaluation_plans_company_id ON evaluation_plans(company_id);
CREATE INDEX ix_evaluation_plans_workflow_id ON evaluation_plans(workflow_id);

-- New table: plan_stage_configs
CREATE TABLE plan_stage_configs (
    id VARCHAR PRIMARY KEY,
    plan_id VARCHAR NOT NULL REFERENCES evaluation_plans(id) ON DELETE CASCADE,
    workflow_stage_id VARCHAR NOT NULL,  -- Not FK (cross-workflow flexibility)
    interview_configurations JSON,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    UNIQUE(plan_id, workflow_stage_id)
);
CREATE INDEX ix_plan_stage_configs_plan_id ON plan_stage_configs(plan_id);

-- New table: position_interview_configs (Position-Level Overrides)
-- Follows same pattern as position_stage_assignments for user overrides
CREATE TABLE position_interview_configs (
    id VARCHAR PRIMARY KEY,
    position_id VARCHAR NOT NULL REFERENCES job_positions(id) ON DELETE CASCADE,
    stage_id VARCHAR NOT NULL,  -- WorkflowStageId
    interview_configurations JSON NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    UNIQUE(position_id, stage_id)
);
CREATE INDEX ix_position_interview_configs_position_id ON position_interview_configs(position_id);
CREATE INDEX ix_position_interview_configs_stage_id ON position_interview_configs(stage_id);

-- Alter job_positions table
ALTER TABLE job_positions ADD COLUMN evaluation_plan_id VARCHAR REFERENCES evaluation_plans(id);
CREATE INDEX ix_job_positions_evaluation_plan_id ON job_positions(evaluation_plan_id);
```

---

## 5. Implementation Strategy

### 5.1 Phase 1: Core Entities (Backend)

**Scope:** Create EvaluationPlan and PlanStageConfig entities with CRUD operations

**Files to Create:**
```
src/interview_bc/evaluation_plan/
├── domain/
│   ├── entities/
│   │   ├── evaluation_plan.py
│   │   └── plan_stage_config.py
│   ├── value_objects/
│   │   ├── evaluation_plan_id.py
│   │   └── plan_stage_config_id.py
│   ├── enums/
│   │   └── evaluation_plan_status.py
│   ├── exceptions/
│   │   └── evaluation_plan_exceptions.py
│   └── repositories/
│       ├── evaluation_plan_repository_interface.py
│       └── plan_stage_config_repository_interface.py
├── infrastructure/
│   ├── models/
│   │   ├── evaluation_plan_model.py
│   │   └── plan_stage_config_model.py
│   └── repositories/
│       ├── evaluation_plan_repository.py
│       └── plan_stage_config_repository.py
└── application/
    ├── commands/
    │   ├── create_evaluation_plan.py
    │   ├── update_evaluation_plan.py
    │   ├── add_stage_config.py
    │   └── remove_stage_config.py
    ├── queries/
    │   ├── get_evaluation_plan_by_id.py
    │   ├── list_evaluation_plans_by_company.py
    │   └── list_stage_configs_by_plan.py
    └── dtos/
        ├── evaluation_plan_dto.py
        └── plan_stage_config_dto.py
```

### 5.2 Phase 2: Integration with JobPosition

**Scope:** Add `evaluation_plan_id` to JobPosition, modify interview trigger logic

**Files to Modify:**
- `src/company_bc/job_position/domain/entities/job_position.py` - Add field
- `src/company_bc/job_position/infrastructure/models/job_position_model.py` - Add column
- `src/company_bc/job_position/application/commands/create_job_position.py` - Accept plan
- `src/company_bc/job_position/application/commands/update_job_position.py` - Update plan

### 5.3 Phase 3: Position Interview Config (Position-Level Overrides)

**Scope:** Create PositionInterviewConfig entity following `PositionStageAssignment` pattern

**Files to Create:**
```
src/company_bc/position_interview_config/
├── domain/
│   ├── entities/
│   │   └── position_interview_config.py
│   ├── value_objects/
│   │   └── position_interview_config_id.py
│   ├── exceptions/
│   │   └── position_interview_config_exceptions.py
│   └── repositories/
│       └── position_interview_config_repository_interface.py
├── infrastructure/
│   ├── models/
│   │   └── position_interview_config_model.py
│   └── repositories/
│       └── position_interview_config_repository.py
└── application/
    ├── commands/
    │   ├── set_position_interview_config.py
    │   └── remove_position_interview_config.py
    └── queries/
        ├── get_position_interview_configs.py
        └── position_interview_config_dto.py
```

### 5.4 Phase 4: Interview Trigger Logic (Three-Tier Resolution)

**Scope:** When candidate moves to stage, resolve interview templates using three-tier priority

**Key Logic Change:**
```python
# Current logic (in candidate movement handlers):
def get_interview_configs_for_stage(workflow_stage: WorkflowStage):
    return workflow_stage.interview_configurations

# New logic with three-tier override system:
def get_interview_configs_for_stage(
    position_id: JobPositionId,
    workflow_stage: WorkflowStage,
    evaluation_plan: Optional[EvaluationPlan] = None
) -> List[InterviewConfiguration]:
    """
    Resolve interview configurations using three-tier priority:
    1. Position-specific override (highest priority)
    2. Evaluation Plan config (role-specific)
    3. Workflow Stage default (lowest priority)
    """

    # Priority 1: Check position-specific override
    position_config = position_interview_config_repo.get_by_position_and_stage(
        position_id, workflow_stage.id
    )
    if position_config and position_config.interview_configurations:
        return position_config.interview_configurations

    # Priority 2: Check Evaluation Plan config
    if evaluation_plan:
        plan_config = plan_stage_config_repo.get_by_plan_and_stage(
            evaluation_plan.id, workflow_stage.id
        )
        if plan_config and plan_config.interview_configurations:
            return plan_config.interview_configurations

    # Priority 3: Fallback to workflow stage defaults
    return workflow_stage.interview_configurations
```

**Service Class:**
```python
class InterviewConfigResolver:
    """Service to resolve interview configurations for a position/stage"""

    def __init__(
        self,
        position_interview_config_repo: PositionInterviewConfigRepositoryInterface,
        plan_stage_config_repo: PlanStageConfigRepositoryInterface,
        workflow_stage_repo: WorkflowStageRepositoryInterface
    ):
        self._position_config_repo = position_interview_config_repo
        self._plan_config_repo = plan_stage_config_repo
        self._stage_repo = workflow_stage_repo

    def resolve(
        self,
        position: JobPosition,
        stage_id: WorkflowStageId
    ) -> Tuple[List[InterviewConfiguration], str]:
        """
        Returns (configs, source) where source is one of:
        - 'position': Position-specific override
        - 'plan': Evaluation Plan config
        - 'stage': Workflow Stage default
        """
        # Implementation follows priority order...
```

### 5.5 Phase 5: API & Frontend

**Scope:** REST endpoints and UI for managing Evaluation Plans and Position Overrides

**API Endpoints - Evaluation Plans:**
```
POST   /api/evaluation-plans                     - Create plan
GET    /api/evaluation-plans/{id}                - Get plan with configs
GET    /api/evaluation-plans/company/{company_id} - List plans
PUT    /api/evaluation-plans/{id}                - Update plan
DELETE /api/evaluation-plans/{id}                - Delete plan
POST   /api/evaluation-plans/{id}/stages         - Add stage config
PUT    /api/evaluation-plans/{id}/stages/{stage_id} - Update stage config
DELETE /api/evaluation-plans/{id}/stages/{stage_id} - Remove stage config
```

**API Endpoints - Position Interview Overrides:**
```
GET    /api/positions/{position_id}/interview-configs
       - Get all interview config overrides for a position

GET    /api/positions/{position_id}/interview-configs/{stage_id}
       - Get interview config override for specific stage

PUT    /api/positions/{position_id}/interview-configs/{stage_id}
       - Set/update interview config override for stage
       - Body: { "interview_configurations": [...] }

DELETE /api/positions/{position_id}/interview-configs/{stage_id}
       - Remove position-level override (fall back to plan/stage default)

GET    /api/positions/{position_id}/stages/{stage_id}/resolved-config
       - Get resolved interview config with source indication
       - Returns: { "configurations": [...], "source": "position|plan|stage" }
```

---

## 6. Architectural Considerations

### 6.1 Bounded Context Placement

**Recommendation:** Place in `interview_bc` since it's primarily about interview content packaging.

```
interview_bc/
├── interview/           # Existing: Interview execution
├── interview_template/  # Existing: Question templates
└── evaluation_plan/     # NEW: Content packaging layer
```

### 6.2 Three-Tier Override System

**Keep `WorkflowStage.interview_configurations` as defaults.** EvaluationPlan and Position-level configs provide overrides.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THREE-TIER OVERRIDE HIERARCHY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Priority 1 (Highest): Position-Specific Override                          │
│  ┌─────────────────────────────────────────────────┐                       │
│  │  PositionInterviewConfig                        │                       │
│  │  - position_id + stage_id → templates           │                       │
│  │  - For unique position requirements             │                       │
│  │  - Example: "This specific Senior Dev role      │                       │
│  │    needs extra security assessment"             │                       │
│  └─────────────────────────────────────────────────┘                       │
│                          ↓ (if not set)                                    │
│                                                                             │
│  Priority 2: Evaluation Plan (Role-Specific)                               │
│  ┌─────────────────────────────────────────────────┐                       │
│  │  EvaluationPlan.PlanStageConfig                 │                       │
│  │  - plan_id + stage_id → templates               │                       │
│  │  - Reusable across positions of same role       │                       │
│  │  - Example: "Frontend Developer Kit"            │                       │
│  └─────────────────────────────────────────────────┘                       │
│                          ↓ (if not set)                                    │
│                                                                             │
│  Priority 3 (Default): Workflow Stage                                      │
│  ┌─────────────────────────────────────────────────┐                       │
│  │  WorkflowStage.interview_configurations         │                       │
│  │  - Company-wide defaults                        │                       │
│  │  - Example: "Standard screening for all roles"  │                       │
│  └─────────────────────────────────────────────────┘                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Priority Resolution Order:**
1. `PositionInterviewConfig` (position + stage specific) - **HIGHEST**
2. `EvaluationPlan.PlanStageConfig` (plan + stage specific)
3. `WorkflowStage.interview_configurations` (stage default) - **LOWEST**

### 6.3 Validation Rules

1. **Plan-Workflow Compatibility:**
   - If `EvaluationPlan.workflow_id` is set, validate that assigned stages exist in that workflow
   - Warn if plan is assigned to position with incompatible workflow

2. **Stage Coverage:**
   - Optional: Warn if plan doesn't cover all stages in workflow
   - Allow partial coverage (not all stages need interview content)

---

## 7. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing workflow-based interviews | High | Fallback to `WorkflowStage.interview_configurations` |
| Migration complexity for existing data | Medium | EvaluationPlan is optional; existing positions continue working |
| UI/UX complexity | Medium | Progressive disclosure; simple mode vs advanced mode |
| Performance (additional lookup) | Low | Single query with join; cache plan configs |

---

## 8. Recommendations

### 8.1 Immediate Actions

1. **Create new bounded context:** `interview_bc/evaluation_plan/`
2. **Start with minimal MVP:** EvaluationPlan + PlanStageConfig entities
3. **Add optional field to JobPosition:** Don't require migration

### 8.2 Future Enhancements

1. **Template Library UI:** Browse/import templates when creating plans
2. **Clone Plan:** Duplicate existing plan as starting point
3. **Plan Analytics:** Track which plans are used, effectiveness
4. **AI Recommendations:** Suggest templates based on job category

---

## 9. Implementation Estimate

| Phase | Scope | Complexity |
|-------|-------|------------|
| Phase 1: Core Entities (EvaluationPlan) | Domain, Infrastructure, CRUD Commands/Queries | Medium |
| Phase 2: JobPosition Integration | Field addition, migrations | Low |
| Phase 3: Position Interview Config | Position-level override entity (same pattern as PositionStageAssignment) | Medium |
| Phase 4: Interview Trigger Logic | Three-tier resolution service | Medium |
| Phase 5: API & Frontend | REST endpoints, React components for all three levels | Medium-High |

---

## 10. Conclusion

The Evaluation Plans feature with Position-level overrides addresses a real architectural gap: the inability to vary interview content at multiple levels while sharing the same workflow structure.

### Three-Tier Summary

| Level | Entity | Use Case | Example |
|-------|--------|----------|---------|
| **Company Default** | `WorkflowStage.interview_configurations` | Standard interviews for all roles | "Basic screening for everyone" |
| **Role-Specific** | `EvaluationPlan.PlanStageConfig` | Reusable kit for similar positions | "Frontend Developer Kit" |
| **Position-Specific** | `PositionInterviewConfig` | Unique requirements for one position | "This role needs security clearance check" |

### Key Benefits

- **Respects existing architecture** by reusing `InterviewConfiguration` value object
- **Follows established patterns** (same as `PositionStageAssignment` override pattern)
- **Is backwards compatible** by keeping `WorkflowStage.interview_configurations` as fallback
- **Enables role-specific content** via Evaluation Plans without duplicating workflows
- **Enables position-specific overrides** for unique hiring requirements
- **Clear override semantics** - higher specificity wins

**Recommendation:** Proceed with implementation following the phased approach outlined above.
