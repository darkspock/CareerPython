# Workflow System - Technical Design

**Version**: 2.0
**Date**: 2025-10-26
**Based on**: WORKFLOW3.md, WORKFLOW2.md, WORKFLOW_SYSTEM_ARCHITECTURE.md

---

## Table of Contents

1. [General Architecture](#general-architecture)
2. [Data Model](#data-model)
3. [Workflows](#workflows)
4. [Custom Fields](#custom-fields)
5. [Roles and Task System](#roles-and-task-system)
6. [Email System](#email-system)
7. [Permission System](#permission-system)
8. [APIs](#apis)
9. [Domain Events](#domain-events)
10. [Frontend Implementation](#frontend-implementation)

---

## General Architecture

### Design Principles

The system follows Clean Architecture with CQRS:

```
Presentation Layer (Controllers, Routers, Schemas)
    ↓
Application Layer (Commands, Queries, Handlers, DTOs)
    ↓
Domain Layer (Entities, Value Objects, Events)
    ↓
Infrastructure Layer (Repositories, Models, External Services)
```

### System Modules

```
src/
├── workflow/                           # Workflows
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── company_workflow.py
│   │   │   └── workflow_stage.py
│   │   ├── value_objects/
│   │   │   ├── workflow_id.py
│   │   │   ├── workflow_stage_id.py
│   │   │   └── workflow_type.py
│   │   ├── enums/
│   │   │   ├── stage_type.py
│   │   │   └── workflow_status.py
│   │   └── infrastructure/
│   │       └── workflow_repository_interface.py
│   ├── application/
│   │   ├── commands/
│   │   ├── queries/
│   │   ├── handlers/
│   │   └── dtos/
│   ├── infrastructure/
│   │   ├── models/
│   │   └── repositories/
│   └── presentation/
│       ├── controllers/
│       ├── routers/
│       ├── schemas/
│       └── mappers/
│
├── candidate_application/              # Candidate applications
│   ├── domain/
│   │   ├── entities/
│   │   │   └── candidate_application.py
│   │   ├── value_objects/
│   │   │   ├── application_id.py
│   │   │   ├── application_data.py   # JSON data
│   │   │   └── shared_data.py         # JSON shared data
│   │   └── enums/
│   │       └── application_status.py
│   └── ...
│
├── position_stage_assignment/          # User-stage assignments
│   ├── domain/
│   │   ├── entities/
│   │   │   └── position_stage_assignment.py
│   │   └── value_objects/
│   │       └── assigned_user_ids.py   # Array of user IDs
│   └── ...
│
├── talent_pool/                        # Talent pool
│   ├── domain/
│   │   ├── entities/
│   │   │   └── company_talent_pool.py
│   │   └── value_objects/
│   └── ...
│
├── email_template/                     # Email templates
│   ├── domain/
│   │   ├── entities/
│   │   │   └── email_template.py
│   │   └── value_objects/
│   └── ...
│
└── workflow_custom_field/              # Custom fields
    ├── domain/
    │   ├── entities/
    │   │   ├── custom_field.py
    │   │   └── field_configuration.py
    │   ├── value_objects/
    │   │   ├── field_type.py
    │   │   └── field_visibility.py
    │   └── enums/
    └── ...
```

---

## Data Model

### Entity Relationship Diagram

```
Company
  ↓ 1:N
CompanyWorkflow
  ↓ 1:N
WorkflowStage ←─────┐
  ↓                 │
  ├─→ CustomField   │
  │   (N:N)         │
  │                 │
Position             │
  ↓                 │
  ├─→ Workflow (FK) │
  └─→ PositionStageAssignment
        ↓           │
        └─→ Stage ──┘
        └─→ UserIDs[]

CompanyCandidate
  ↓
CandidateApplication
  ├─→ Position
  ├─→ Workflow (copy)
  ├─→ CurrentStage
  ├─→ ApplicationData (JSON)
  └─→ SharedData (JSON)

CompanyTalentPool
  ├─→ CompanyCandidate
  └─→ Comments
```

### Main Tables

#### 1. `company_workflows`

```sql
CREATE TABLE company_workflows (
    id VARCHAR(255) PRIMARY KEY,
    company_id VARCHAR(255) NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    workflow_type VARCHAR(50) NOT NULL, -- 'prospecting' | 'selection'
    status VARCHAR(50) NOT NULL,        -- 'active' | 'inactive' | 'archived'
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_company_workflow_name UNIQUE(company_id, name)
);

CREATE INDEX idx_company_workflows_company ON company_workflows(company_id);
CREATE INDEX idx_company_workflows_type ON company_workflows(workflow_type);
CREATE INDEX idx_company_workflows_status ON company_workflows(status);
```

#### 2. `workflow_stages`

```sql
CREATE TABLE workflow_stages (
    id VARCHAR(255) PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL REFERENCES company_workflows(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    stage_type VARCHAR(50) NOT NULL,    -- 'initial' | 'intermediate' | 'final' | 'custom'
    order_index INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,

    -- Advanced configuration fields
    required_outcome VARCHAR(100),      -- Required outcome to advance
    estimated_duration_days INTEGER,    -- Estimated duration
    deadline_days INTEGER,              -- Deadline in days
    estimated_cost DECIMAL(10,2),       -- Estimated cost

    -- Default assignment fields
    default_roles JSONB,                -- ['Tech Lead', 'HR Manager']
    default_assigned_users JSONB,       -- ['user_id_1', 'user_id_2']

    -- Email fields
    email_template_id VARCHAR(255) REFERENCES email_templates(id),
    custom_email_text TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_workflow_stage_order UNIQUE(workflow_id, order_index)
);

CREATE INDEX idx_workflow_stages_workflow ON workflow_stages(workflow_id);
CREATE INDEX idx_workflow_stages_order ON workflow_stages(workflow_id, order_index);
```

#### 3. `workflow_custom_fields`

Defines custom fields for each workflow.

```sql
CREATE TABLE workflow_custom_fields (
    id VARCHAR(255) PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL REFERENCES company_workflows(id) ON DELETE CASCADE,
    field_key VARCHAR(100) NOT NULL,    -- Unique field identifier
    field_name VARCHAR(255) NOT NULL,   -- Display name
    field_type VARCHAR(50) NOT NULL,    -- Field type (see below)
    field_config JSONB,                 -- Type-specific configuration
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_workflow_field_key UNIQUE(workflow_id, field_key)
);

CREATE INDEX idx_workflow_custom_fields_workflow ON workflow_custom_fields(workflow_id);
```

**Field types (`field_type`):**
- `text_short`: Short text
- `text_long`: Text area
- `dropdown`: Dropdown list
- `checkbox`: Checkboxes
- `radio`: Radio buttons
- `date`: Date
- `datetime`: Date and time
- `time`: Time
- `file`: File attachment
- `currency`: Currency
- `integer`: Integer number
- `float`: Decimal number
- `percentage`: Percentage

**Examples of `field_config`:**
```json
// Dropdown
{
    "options": ["Junior", "Mid", "Senior", "Lead"],
    "allow_multiple": false
}

// Checkbox
{
    "options": ["Python", "Java", "JavaScript", "Go"]
}

// Currency
{
    "currency": "USD",
    "min": 0,
    "max": 1000000
}

// File
{
    "allowed_extensions": [".pdf", ".doc", ".docx"],
    "max_size_mb": 5
}
```

#### 4. `stage_field_configurations`

Defines how each field behaves in each stage.

```sql
CREATE TABLE stage_field_configurations (
    id VARCHAR(255) PRIMARY KEY,
    stage_id VARCHAR(255) NOT NULL REFERENCES workflow_stages(id) ON DELETE CASCADE,
    custom_field_id VARCHAR(255) NOT NULL REFERENCES workflow_custom_fields(id) ON DELETE CASCADE,
    visibility VARCHAR(50) NOT NULL,    -- 'hidden' | 'mandatory' | 'recommended' | 'optional'
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_stage_field UNIQUE(stage_id, custom_field_id)
);

CREATE INDEX idx_stage_field_configs_stage ON stage_field_configurations(stage_id);
CREATE INDEX idx_stage_field_configs_field ON stage_field_configurations(custom_field_id);
```

#### 4.1. `field_validation_rules`

Defines validation rules for custom fields that are checked during stage transitions.

```sql
CREATE TABLE field_validation_rules (
    id VARCHAR(255) PRIMARY KEY,
    custom_field_id VARCHAR(255) NOT NULL REFERENCES workflow_custom_fields(id) ON DELETE CASCADE,
    stage_id VARCHAR(255) NOT NULL REFERENCES workflow_stages(id) ON DELETE CASCADE,

    -- Validation configuration
    rule_type VARCHAR(50) NOT NULL,           -- 'compare_position_field' | 'range' | 'pattern' | 'custom'
    comparison_operator VARCHAR(50),          -- 'gt' | 'gte' | 'lt' | 'lte' | 'eq' | 'neq' | 'in_range' | 'out_range'
    position_field_path VARCHAR(255),         -- JSON path to position field (e.g., 'max_salary', 'location.city')
    comparison_value JSONB,                   -- Static value to compare (if not comparing with position)

    -- Validation result
    severity VARCHAR(50) NOT NULL,            -- 'warning' | 'error'
    validation_message TEXT NOT NULL,         -- Message to show user (supports variables)

    -- Optional: Auto-reject on error
    auto_reject BOOLEAN DEFAULT FALSE,
    rejection_reason TEXT,

    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_field_validation_rules_field ON field_validation_rules(custom_field_id);
CREATE INDEX idx_field_validation_rules_stage ON field_validation_rules(stage_id);
CREATE INDEX idx_field_validation_rules_active ON field_validation_rules(is_active) WHERE is_active = TRUE;
```

**Example data:**
```sql
-- Salary validation (Error)
INSERT INTO field_validation_rules VALUES (
    'rule_001',
    'field_salary_expectation',
    'stage_negotiation',
    'compare_position_field',
    'gt',
    'max_salary',
    NULL,
    'error',
    'Candidate expects ${candidate_value}, but position max is ${position_value}. Cannot proceed.',
    TRUE,
    'Salary expectation exceeds position budget',
    TRUE,
    NOW(),
    NOW()
);

-- Location validation (Warning)
INSERT INTO field_validation_rules VALUES (
    'rule_002',
    'field_location',
    'stage_screening',
    'compare_position_field',
    'neq',
    'location',
    NULL,
    'warning',
    'Candidate is in ${candidate_value}, position is in ${position_value}. Consider relocation needs.',
    FALSE,
    NULL,
    TRUE,
    NOW(),
    NOW()
);

-- Experience validation (Error)
INSERT INTO field_validation_rules VALUES (
    'rule_003',
    'field_years_experience',
    'stage_screening',
    'compare_position_field',
    'lt',
    'minimum_experience',
    NULL,
    'error',
    'Candidate has ${candidate_value} years, position requires minimum ${position_value} years.',
    TRUE,
    'Does not meet minimum experience requirement',
    TRUE,
    NOW(),
    NOW()
);
```

#### 5. `job_positions`

```sql
ALTER TABLE job_positions ADD COLUMN workflow_id VARCHAR(255) REFERENCES company_workflows(id);

CREATE INDEX idx_job_positions_workflow ON job_positions(workflow_id);
```

#### 6. `position_stage_assignments`

Maps users to specific stages of a position.

```sql
CREATE TABLE position_stage_assignments (
    id VARCHAR(255) PRIMARY KEY,
    position_id VARCHAR(255) NOT NULL REFERENCES job_positions(id) ON DELETE CASCADE,
    stage_id VARCHAR(255) NOT NULL REFERENCES workflow_stages(id),
    assigned_user_ids JSONB NOT NULL DEFAULT '[]', -- Array of CompanyUser IDs
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_position_stage UNIQUE(position_id, stage_id)
);

CREATE INDEX idx_position_stage_assignments_position ON position_stage_assignments(position_id);
CREATE INDEX idx_position_stage_assignments_stage ON position_stage_assignments(stage_id);
```

#### 7. `candidate_applications`

```sql
ALTER TABLE candidate_applications
ADD COLUMN workflow_id VARCHAR(255) REFERENCES company_workflows(id),
ADD COLUMN current_stage_id VARCHAR(255) REFERENCES workflow_stages(id),
ADD COLUMN application_data JSONB DEFAULT '{}',      -- Data captured during process
ADD COLUMN shared_data JSONB DEFAULT '{}',            -- Data candidate authorized to share
ADD COLUMN stage_entered_at TIMESTAMP,                -- When entered current stage
ADD COLUMN stage_deadline TIMESTAMP,                  -- Current stage deadline
ADD COLUMN task_status VARCHAR(50) DEFAULT 'pending'; -- 'pending' | 'in_progress' | 'completed' | 'blocked'

CREATE INDEX idx_candidate_applications_workflow ON candidate_applications(workflow_id);
CREATE INDEX idx_candidate_applications_stage ON candidate_applications(current_stage_id);
CREATE INDEX idx_candidate_applications_deadline ON candidate_applications(stage_deadline);
CREATE INDEX idx_candidate_applications_task_status ON candidate_applications(task_status);
```

**Structure of `application_data`:**
```json
{
    "custom_field_key_1": "value",
    "custom_field_key_2": ["multiple", "values"],
    "salary_expectation": 120000,
    "available_start_date": "2025-02-01",
    "technical_test_score": 85,
    "interview_notes": "Excellent communication skills",
    "stage_history": [
        {
            "stage_id": "stage_1",
            "stage_name": "Screening",
            "entered_at": "2025-01-15T10:00:00Z",
            "exited_at": "2025-01-17T14:30:00Z",
            "duration_hours": 52.5,
            "changed_by": "user_id_1",
            "data_snapshot": {}
        }
    ]
}
```

**Structure of `shared_data`:**
```json
{
    "include_education": true,
    "include_experience": true,
    "include_projects": false,
    "include_skills": true,
    "include_languages": true,
    "resume_ids": ["resume_1", "resume_2"],
    "portfolio_url": "https://example.com/portfolio"
}
```

#### 8. `company_talent_pool`

```sql
CREATE TABLE company_talent_pool (
    id VARCHAR(255) PRIMARY KEY,
    company_id VARCHAR(255) NOT NULL REFERENCES companies(id),
    company_candidate_id VARCHAR(255) NOT NULL REFERENCES company_candidates(id),
    comments TEXT,
    tags JSONB DEFAULT '[]',
    added_at TIMESTAMP NOT NULL DEFAULT NOW(),
    added_by_user_id VARCHAR(255) REFERENCES company_users(id),

    CONSTRAINT unique_talent_pool_candidate UNIQUE(company_id, company_candidate_id)
);

CREATE INDEX idx_talent_pool_company ON company_talent_pool(company_id);
CREATE INDEX idx_talent_pool_candidate ON company_talent_pool(company_candidate_id);
```

#### 9. `email_templates`

```sql
CREATE TABLE email_templates (
    id VARCHAR(255) PRIMARY KEY,
    company_id VARCHAR(255) NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,                 -- HTML with placeholders
    variables JSONB DEFAULT '[]',       -- Available variables
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_company_template_name UNIQUE(company_id, name)
);

CREATE INDEX idx_email_templates_company ON email_templates(company_id);
```

**Supported variables:**
- `{{candidate_name}}`: Candidate's full name
- `{{candidate_first_name}}`: First name
- `{{position_title}}`: Position title
- `{{company_name}}`: Company name
- `{{stage_name}}`: Stage name
- `{{custom_text}}`: Additional custom text

#### 10. `company_users` (extension)

```sql
ALTER TABLE company_users ADD COLUMN roles JSONB DEFAULT '[]';

-- Common roles:
-- ["HR Manager", "Tech Lead", "Recruiter", "Hiring Manager", "Interviewer", "Department Head"]
```

---

## Workflows

### Workflow Types

#### 1. Prospecting (Sourcing)

**Purpose**: Lead management and candidates who haven't yet applied to specific positions.

**Fixed stages** (not customizable for now):
1. `Pending`: Newly entered candidate
2. `Screening`: Initial review
3. `Discarded`: Rejected
4. `On Hold`: On hold
5. `To Talent Pool`: Move to talent pool

**Flow:**
```
Pending → Screening → {
    ✅ To Talent Pool → Save in company_talent_pool
    ❌ Discarded → Mark as discarded
    ⏸️ On Hold → Keep on hold
}
```

**Transition to Evaluation:**
When a candidate is accepted in Screening, they can:
- Apply to a specific position (create `CandidateApplication`)
- Move to `selection` type workflow

#### 2. Selection (Evaluation)

**Purpose**: Formal selection process for a specific position.

**Customizable stages:**
- Company defines stages according to their process
- Can have between 2 and 20 stages (recommended: 4-8)

**Example stages:**
- HR Interview
- Technical Test
- Technical Interview
- Team Lead Interview
- Reference Check
- Offer
- Hired

#### 3. Offer and Pre-Onboarding

**Purpose**: Offer formalization and onboarding preparation.

**Suggested stages (customizable):**
1. `Offer Proposal`: Offer preparation
2. `Negotiation`: Terms negotiation
3. `Document Submission`: Document submission
4. `Document Verification`: Document verification
5. `Contract Signing`: Contract signing
6. `Hired`: Hired (final)

### WorkflowStage Entity

```python
@dataclass
class WorkflowStage:
    id: WorkflowStageId
    workflow_id: WorkflowId
    name: str
    description: Optional[str]
    stage_type: StageType  # initial, intermediate, final, custom
    order: int
    is_active: bool

    # Advanced configuration
    required_outcome: Optional[str]
    estimated_duration_days: Optional[int]
    deadline_days: Optional[int]
    estimated_cost: Optional[Decimal]

    # Assignment defaults
    default_roles: List[str]
    default_assigned_users: List[str]

    # Email configuration
    email_template_id: Optional[EmailTemplateId]
    custom_email_text: Optional[str]

    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        workflow_id: WorkflowId,
        name: str,
        stage_type: StageType,
        order: int,
        description: Optional[str] = None,
        estimated_duration_days: Optional[int] = None,
        deadline_days: Optional[int] = None,
        estimated_cost: Optional[Decimal] = None,
        default_roles: Optional[List[str]] = None,
        default_assigned_users: Optional[List[str]] = None,
        email_template_id: Optional[EmailTemplateId] = None,
        custom_email_text: Optional[str] = None
    ) -> "WorkflowStage":
        """Factory method to create a new stage"""

        # Validations
        if deadline_days and deadline_days < 1:
            raise ValueError("deadline_days must be positive")

        if estimated_cost and estimated_cost < 0:
            raise ValueError("estimated_cost must be non-negative")

        if estimated_duration_days and estimated_duration_days < 1:
            raise ValueError("estimated_duration_days must be positive")

        return cls(
            id=WorkflowStageId.generate(),
            workflow_id=workflow_id,
            name=name,
            description=description,
            stage_type=stage_type,
            order=order,
            is_active=True,
            required_outcome=None,
            estimated_duration_days=estimated_duration_days,
            deadline_days=deadline_days,
            estimated_cost=estimated_cost,
            default_roles=default_roles or [],
            default_assigned_users=default_assigned_users or [],
            email_template_id=email_template_id,
            custom_email_text=custom_email_text,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        estimated_duration_days: Optional[int] = None,
        deadline_days: Optional[int] = None,
        estimated_cost: Optional[Decimal] = None,
        default_roles: Optional[List[str]] = None,
        default_assigned_users: Optional[List[str]] = None,
        email_template_id: Optional[EmailTemplateId] = None,
        custom_email_text: Optional[str] = None
    ) -> None:
        """Update stage fields"""

        if name:
            self.name = name
        if description is not None:
            self.description = description
        if estimated_duration_days:
            self.estimated_duration_days = estimated_duration_days
        if deadline_days:
            if deadline_days < 1:
                raise ValueError("deadline_days must be positive")
            self.deadline_days = deadline_days
        if estimated_cost is not None:
            if estimated_cost < 0:
                raise ValueError("estimated_cost must be non-negative")
            self.estimated_cost = estimated_cost
        if default_roles is not None:
            self.default_roles = default_roles
        if default_assigned_users is not None:
            self.default_assigned_users = default_assigned_users
        if email_template_id is not None:
            self.email_template_id = email_template_id
        if custom_email_text is not None:
            self.custom_email_text = custom_email_text

        self.updated_at = datetime.now(UTC)
```

---

## Custom Fields

### CustomField Entity

```python
@dataclass
class CustomField:
    id: CustomFieldId
    workflow_id: WorkflowId
    field_key: str              # Unique identifier (snake_case)
    field_name: str             # Display name
    field_type: FieldType
    field_config: Dict[str, Any]
    order: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        workflow_id: WorkflowId,
        field_key: str,
        field_name: str,
        field_type: FieldType,
        field_config: Dict[str, Any],
        order: int
    ) -> "CustomField":
        """Factory method"""

        # Validate field_key
        if not re.match(r'^[a-z][a-z0-9_]*$', field_key):
            raise ValueError("field_key must be snake_case")

        # Validate field_config based on field_type
        cls._validate_config(field_type, field_config)

        return cls(
            id=CustomFieldId.generate(),
            workflow_id=workflow_id,
            field_key=field_key,
            field_name=field_name,
            field_type=field_type,
            field_config=field_config,
            order=order,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

    @staticmethod
    def _validate_config(field_type: FieldType, config: Dict[str, Any]) -> None:
        """Validate configuration based on type"""

        if field_type in [FieldType.DROPDOWN, FieldType.CHECKBOX, FieldType.RADIO]:
            if "options" not in config or not config["options"]:
                raise ValueError("options required for choice fields")

        if field_type == FieldType.CURRENCY:
            if "currency" not in config:
                raise ValueError("currency required for currency field")

        if field_type == FieldType.FILE:
            if "allowed_extensions" not in config:
                raise ValueError("allowed_extensions required for file field")
```

### FieldConfiguration Entity

Defines field visibility in a specific stage.

```python
@dataclass
class FieldConfiguration:
    id: FieldConfigurationId
    stage_id: WorkflowStageId
    custom_field_id: CustomFieldId
    visibility: FieldVisibility  # hidden, mandatory, recommended, optional
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        stage_id: WorkflowStageId,
        custom_field_id: CustomFieldId,
        visibility: FieldVisibility
    ) -> "FieldConfiguration":
        return cls(
            id=FieldConfigurationId.generate(),
            stage_id=stage_id,
            custom_field_id=custom_field_id,
            visibility=visibility,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
```

### Field Types

```python
class FieldType(Enum):
    TEXT_SHORT = "text_short"
    TEXT_LONG = "text_long"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    FILE = "file"
    CURRENCY = "currency"
    INTEGER = "integer"
    FLOAT = "float"
    PERCENTAGE = "percentage"

class FieldVisibility(Enum):
    HIDDEN = "hidden"
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"
```

---

## Field Validation System

### Validation Rules

The system allows defining validation rules for custom fields that are automatically checked when attempting to move a candidate to the next stage.

#### ValidationRule Entity

```python
@dataclass
class ValidationRule:
    id: ValidationRuleId
    custom_field_id: CustomFieldId
    stage_id: WorkflowStageId
    rule_type: ValidationRuleType
    comparison_operator: Optional[ComparisonOperator]
    position_field_path: Optional[str]  # JSON path to position field
    comparison_value: Optional[Any]     # Static value if not comparing with position
    severity: ValidationSeverity
    validation_message: str
    auto_reject: bool
    rejection_reason: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        custom_field_id: CustomFieldId,
        stage_id: WorkflowStageId,
        rule_type: ValidationRuleType,
        severity: ValidationSeverity,
        validation_message: str,
        comparison_operator: Optional[ComparisonOperator] = None,
        position_field_path: Optional[str] = None,
        comparison_value: Optional[Any] = None,
        auto_reject: bool = False,
        rejection_reason: Optional[str] = None
    ) -> "ValidationRule":
        """Factory method to create a validation rule"""

        # Validate that comparison rules have necessary fields
        if rule_type == ValidationRuleType.COMPARE_POSITION_FIELD:
            if not comparison_operator or not position_field_path:
                raise ValueError(
                    "comparison_operator and position_field_path required "
                    "for COMPARE_POSITION_FIELD rule type"
                )

        # Auto-reject only makes sense for error severity
        if auto_reject and severity != ValidationSeverity.ERROR:
            raise ValueError("auto_reject can only be True for ERROR severity")

        return cls(
            id=ValidationRuleId.generate(),
            custom_field_id=custom_field_id,
            stage_id=stage_id,
            rule_type=rule_type,
            comparison_operator=comparison_operator,
            position_field_path=position_field_path,
            comparison_value=comparison_value,
            severity=severity,
            validation_message=validation_message,
            auto_reject=auto_reject,
            rejection_reason=rejection_reason,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

    def evaluate(
        self,
        candidate_value: Any,
        position: Position
    ) -> ValidationResult:
        """Evaluate this validation rule"""

        if not self.is_active:
            return ValidationResult.passed()

        # Get comparison value
        if self.rule_type == ValidationRuleType.COMPARE_POSITION_FIELD:
            position_value = self._get_position_field_value(
                position,
                self.position_field_path
            )
        else:
            position_value = self.comparison_value

        # Perform comparison
        passed = self._perform_comparison(
            candidate_value,
            position_value,
            self.comparison_operator
        )

        if passed:
            return ValidationResult.passed()
        else:
            # Build message with variable substitution
            message = self._build_message(candidate_value, position_value)
            return ValidationResult.failed(
                severity=self.severity,
                message=message,
                auto_reject=self.auto_reject,
                rejection_reason=self.rejection_reason
            )

    def _get_position_field_value(self, position: Position, path: str) -> Any:
        """Extract value from position using JSON path"""
        # Example: "max_salary" -> position.max_salary
        # Example: "location.city" -> position.location.city
        parts = path.split('.')
        value = position
        for part in parts:
            value = getattr(value, part, None)
            if value is None:
                return None
        return value

    def _perform_comparison(
        self,
        candidate_value: Any,
        comparison_value: Any,
        operator: ComparisonOperator
    ) -> bool:
        """Perform the comparison operation"""

        if candidate_value is None or comparison_value is None:
            return True  # Skip validation if values missing

        if operator == ComparisonOperator.GREATER_THAN:
            return not (candidate_value > comparison_value)
        elif operator == ComparisonOperator.GREATER_THAN_OR_EQUAL:
            return not (candidate_value >= comparison_value)
        elif operator == ComparisonOperator.LESS_THAN:
            return not (candidate_value < comparison_value)
        elif operator == ComparisonOperator.LESS_THAN_OR_EQUAL:
            return not (candidate_value <= comparison_value)
        elif operator == ComparisonOperator.EQUAL:
            return candidate_value == comparison_value
        elif operator == ComparisonOperator.NOT_EQUAL:
            return candidate_value != comparison_value
        elif operator == ComparisonOperator.IN_RANGE:
            # comparison_value should be [min, max]
            min_val, max_val = comparison_value
            return min_val <= candidate_value <= max_val
        elif operator == ComparisonOperator.OUT_OF_RANGE:
            # comparison_value should be [min, max]
            min_val, max_val = comparison_value
            return not (min_val <= candidate_value <= max_val)

        return True

    def _build_message(self, candidate_value: Any, position_value: Any) -> str:
        """Build message with variable substitution"""
        message = self.validation_message
        message = message.replace('${candidate_value}', str(candidate_value))
        message = message.replace('${position_value}', str(position_value))
        return message


class ValidationRuleType(Enum):
    COMPARE_POSITION_FIELD = "compare_position_field"  # Compare with position field
    RANGE = "range"                                     # Check if in range
    PATTERN = "pattern"                                 # Regex pattern match
    CUSTOM = "custom"                                   # Custom validation logic


class ComparisonOperator(Enum):
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    EQUAL = "eq"
    NOT_EQUAL = "neq"
    IN_RANGE = "in_range"
    OUT_OF_RANGE = "out_range"


class ValidationSeverity(Enum):
    WARNING = "warning"  # Shows warning but allows proceeding
    ERROR = "error"      # Blocks stage transition


@dataclass
class ValidationResult:
    passed: bool
    severity: Optional[ValidationSeverity]
    message: Optional[str]
    auto_reject: bool
    rejection_reason: Optional[str]

    @classmethod
    def passed(cls) -> "ValidationResult":
        return cls(
            passed=True,
            severity=None,
            message=None,
            auto_reject=False,
            rejection_reason=None
        )

    @classmethod
    def failed(
        cls,
        severity: ValidationSeverity,
        message: str,
        auto_reject: bool = False,
        rejection_reason: Optional[str] = None
    ) -> "ValidationResult":
        return cls(
            passed=False,
            severity=severity,
            message=message,
            auto_reject=auto_reject,
            rejection_reason=rejection_reason
        )
```

### FieldValidationService

Service to validate all fields during stage transition.

```python
class FieldValidationService:
    def __init__(
        self,
        validation_rule_repo: ValidationRuleRepository,
        custom_field_repo: CustomFieldRepository
    ):
        self.validation_rule_repo = validation_rule_repo
        self.custom_field_repo = custom_field_repo

    def validate_stage_transition(
        self,
        application: CandidateApplication,
        from_stage_id: WorkflowStageId,
        to_stage_id: WorkflowStageId,
        position: Position
    ) -> StageTransitionValidationResult:
        """Validate all fields before allowing stage transition"""

        # Get all validation rules for the current stage
        rules = self.validation_rule_repo.get_by_stage(from_stage_id)

        if not rules:
            return StageTransitionValidationResult.allow()

        errors = []
        warnings = []
        auto_reject_triggered = False
        rejection_reason = None

        # Evaluate each rule
        for rule in rules:
            # Get candidate value from application_data
            field = self.custom_field_repo.get_by_id(rule.custom_field_id)
            candidate_value = application.application_data.get(field.field_key)

            # Evaluate rule
            result = rule.evaluate(candidate_value, position)

            if not result.passed:
                if result.severity == ValidationSeverity.ERROR:
                    errors.append(result.message)
                    if result.auto_reject:
                        auto_reject_triggered = True
                        rejection_reason = result.rejection_reason
                elif result.severity == ValidationSeverity.WARNING:
                    warnings.append(result.message)

        # Determine result
        if errors:
            return StageTransitionValidationResult.block(
                errors=errors,
                warnings=warnings,
                auto_reject=auto_reject_triggered,
                rejection_reason=rejection_reason
            )
        elif warnings:
            return StageTransitionValidationResult.warn(warnings=warnings)
        else:
            return StageTransitionValidationResult.allow()


@dataclass
class StageTransitionValidationResult:
    can_proceed: bool
    has_warnings: bool
    errors: List[str]
    warnings: List[str]
    auto_reject: bool
    rejection_reason: Optional[str]

    @classmethod
    def allow(cls) -> "StageTransitionValidationResult":
        """Validation passed, allow transition"""
        return cls(
            can_proceed=True,
            has_warnings=False,
            errors=[],
            warnings=[],
            auto_reject=False,
            rejection_reason=None
        )

    @classmethod
    def warn(cls, warnings: List[str]) -> "StageTransitionValidationResult":
        """Validation has warnings but can proceed"""
        return cls(
            can_proceed=True,
            has_warnings=True,
            errors=[],
            warnings=warnings,
            auto_reject=False,
            rejection_reason=None
        )

    @classmethod
    def block(
        cls,
        errors: List[str],
        warnings: List[str],
        auto_reject: bool = False,
        rejection_reason: Optional[str] = None
    ) -> "StageTransitionValidationResult":
        """Validation failed, block transition"""
        return cls(
            can_proceed=False,
            has_warnings=len(warnings) > 0,
            errors=errors,
            warnings=warnings,
            auto_reject=auto_reject,
            rejection_reason=rejection_reason
        )
```

### Integration with ChangeStageCommand

```python
class ChangeStageCommandHandler:
    def __init__(
        self,
        application_repo: CandidateApplicationRepository,
        position_repo: PositionRepository,
        permission_service: StagePermissionService,
        validation_service: FieldValidationService,
        event_bus: EventBus
    ):
        self.application_repo = application_repo
        self.position_repo = position_repo
        self.permission_service = permission_service
        self.validation_service = validation_service
        self.event_bus = event_bus

    def execute(self, command: ChangeStageCommand) -> ChangeStageResult:
        # Get application and position
        application = self.application_repo.get_by_id(command.application_id)
        position = self.position_repo.get_by_id(application.position_id)

        # Check permission
        if not self.permission_service.can_user_process_stage(
            user_id=command.user_id,
            application=application
        ):
            raise PermissionDeniedError("User not assigned to current stage")

        # Validate stage transition
        validation_result = self.validation_service.validate_stage_transition(
            application=application,
            from_stage_id=application.current_stage_id,
            to_stage_id=command.new_stage_id,
            position=position
        )

        # If validation blocks transition
        if not validation_result.can_proceed:
            # Check if auto-reject triggered
            if validation_result.auto_reject:
                # Automatically reject candidate
                application.reject(
                    reason=validation_result.rejection_reason,
                    rejected_by=command.user_id
                )
                self.application_repo.save(application)

                return ChangeStageResult.rejected(
                    errors=validation_result.errors,
                    warnings=validation_result.warnings,
                    rejection_reason=validation_result.rejection_reason
                )
            else:
                # Return validation errors
                return ChangeStageResult.validation_failed(
                    errors=validation_result.errors,
                    warnings=validation_result.warnings
                )

        # If has warnings but user must confirm
        if validation_result.has_warnings and not command.force_with_warnings:
            return ChangeStageResult.needs_confirmation(
                warnings=validation_result.warnings
            )

        # Validation passed, proceed with stage change
        previous_stage_id = application.current_stage_id
        application.move_to_stage(
            new_stage_id=command.new_stage_id,
            changed_by=command.user_id
        )

        # Save
        self.application_repo.save(application)

        # Emit event
        event = ApplicationStageChangedEvent(
            application_id=application.id,
            previous_stage_id=previous_stage_id,
            new_stage_id=command.new_stage_id,
            changed_by_user_id=command.user_id,
            changed_at=datetime.now(UTC)
        )
        self.event_bus.publish(event)

        return ChangeStageResult.success()


@dataclass
class ChangeStageCommand:
    application_id: str
    new_stage_id: str
    user_id: str
    force_with_warnings: bool = False  # User confirmed despite warnings


@dataclass
class ChangeStageResult:
    success: bool
    status: str  # 'success' | 'validation_failed' | 'needs_confirmation' | 'rejected'
    errors: List[str]
    warnings: List[str]
    rejection_reason: Optional[str]

    @classmethod
    def success(cls) -> "ChangeStageResult":
        return cls(
            success=True,
            status='success',
            errors=[],
            warnings=[],
            rejection_reason=None
        )

    @classmethod
    def validation_failed(
        cls,
        errors: List[str],
        warnings: List[str]
    ) -> "ChangeStageResult":
        return cls(
            success=False,
            status='validation_failed',
            errors=errors,
            warnings=warnings,
            rejection_reason=None
        )

    @classmethod
    def needs_confirmation(cls, warnings: List[str]) -> "ChangeStageResult":
        return cls(
            success=False,
            status='needs_confirmation',
            errors=[],
            warnings=warnings,
            rejection_reason=None
        )

    @classmethod
    def rejected(
        cls,
        errors: List[str],
        warnings: List[str],
        rejection_reason: str
    ) -> "ChangeStageResult":
        return cls(
            success=True,  # Command succeeded (candidate was rejected)
            status='rejected',
            errors=errors,
            warnings=warnings,
            rejection_reason=rejection_reason
        )
```

### Example Usage

```python
# Example 1: Salary validation blocks transition
application = get_application("app_123")
position = get_position(application.position_id)

# Application data has salary_expectation = 150000
# Position has max_salary = 120000
# Validation rule: salary_expectation > max_salary (ERROR)

result = change_stage_handler.execute(
    ChangeStageCommand(
        application_id="app_123",
        new_stage_id="stage_interview",
        user_id="user_1"
    )
)

# Result:
# success=False
# status='validation_failed'
# errors=['Candidate expects $150,000, but position max is $120,000. Cannot proceed.']

# Example 2: Location validation shows warning
# Application data has location = "New York"
# Position has location = "San Francisco"
# Validation rule: location != position.location (WARNING)

result = change_stage_handler.execute(
    ChangeStageCommand(
        application_id="app_124",
        new_stage_id="stage_interview",
        user_id="user_1"
    )
)

# Result:
# success=False
# status='needs_confirmation'
# warnings=['Candidate is in New York, position is in San Francisco. Consider relocation needs.']

# User confirms and retries with force flag
result = change_stage_handler.execute(
    ChangeStageCommand(
        application_id="app_124",
        new_stage_id="stage_interview",
        user_id="user_1",
        force_with_warnings=True
    )
)

# Result:
# success=True
# status='success'
```

---

## Roles and Task System

### CompanyUser Roles

Roles are stored in `company_users.roles` as JSONB array.

**Common roles:**
- `HR Manager`: Manages HR process
- `Tech Lead`: Leads technical assessments
- `Recruiter`: Recruiter
- `Hiring Manager`: Hiring manager
- `Interviewer`: General interviewer
- `Department Head`: Department head

### Task Priority System

```python
@dataclass
class TaskPriority:
    base_priority: int = 100
    deadline_weight: int = 0
    position_weight: int = 0
    candidate_weight: int = 0

    @property
    def total_score(self) -> int:
        return (
            self.base_priority +
            self.deadline_weight +
            self.position_weight +
            self.candidate_weight
        )

    @classmethod
    def calculate(
        cls,
        application: CandidateApplication,
        current_date: datetime
    ) -> "TaskPriority":
        """Calculate application priority"""

        deadline_weight = cls._calculate_deadline_weight(
            application.stage_deadline,
            current_date
        )

        position_weight = application.position.priority * 10  # 0-5 stars → 0-50
        candidate_weight = application.candidate.priority * 5  # 0-5 stars → 0-25

        return cls(
            deadline_weight=deadline_weight,
            position_weight=position_weight,
            candidate_weight=candidate_weight
        )

    @staticmethod
    def _calculate_deadline_weight(deadline: Optional[datetime], now: datetime) -> int:
        """Calculate weight by deadline"""

        if not deadline:
            return 0

        days_until_deadline = (deadline - now).days

        if days_until_deadline < 0:  # Overdue
            return 50
        elif days_until_deadline == 0:  # Due today
            return 30
        elif days_until_deadline <= 2:  # Due in 1-2 days
            return 20
        elif days_until_deadline <= 5:  # Due in 3-5 days
            return 10
        else:  # Due in 6+ days
            return 0
```

### Task Assignment

```python
@dataclass
class TaskAssignment:
    application: CandidateApplication
    priority: TaskPriority
    assignment_type: AssignmentType  # direct, role_based

class AssignmentType(Enum):
    DIRECT = "direct"          # User specifically assigned
    ROLE_BASED = "role_based"  # User has matching role
```

### Task Queries

#### GetMyAssignedTasksQuery

Returns applications where user is directly assigned to current stage.

```python
@dataclass
class GetMyAssignedTasksQuery:
    user_id: str
    filters: Optional[TaskFilters] = None

class GetMyAssignedTasksQueryHandler:
    def handle(self, query: GetMyAssignedTasksQuery) -> List[TaskDto]:
        """
        SELECT ca.*
        FROM candidate_applications ca
        JOIN position_stage_assignments psa
            ON psa.position_id = ca.position_id
            AND psa.stage_id = ca.current_stage_id
        WHERE ca.task_status = 'pending'
            AND psa.assigned_user_ids @> jsonb_build_array(query.user_id)
        ORDER BY ca.priority DESC, ca.stage_entered_at ASC
        """
        pass
```

#### GetAvailableTasksQuery

Returns applications in stages matching user's roles but without assigned user.

```python
@dataclass
class GetAvailableTasksQuery:
    user_id: str
    filters: Optional[TaskFilters] = None

class GetAvailableTasksQueryHandler:
    def handle(self, query: GetAvailableTasksQuery) -> List[TaskDto]:
        """
        1. Get user roles
        2. Find stages whose default_roles match any user role
        3. Filter applications in those stages without specific assigned user
        4. Sort by priority
        """
        pass
```

---

## Email System

### EmailTemplate Entity

```python
@dataclass
class EmailTemplate:
    id: EmailTemplateId
    company_id: CompanyId
    name: str
    subject: str
    body: str  # HTML
    variables: List[str]
    created_at: datetime
    updated_at: datetime

    def render(
        self,
        context: Dict[str, Any],
        custom_text: Optional[str] = None
    ) -> str:
        """Render template with variables"""

        rendered = self.body

        # Replace variables
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))

        # Add custom text
        if custom_text:
            custom_placeholder = "{{custom_text}}"
            if custom_placeholder in rendered:
                rendered = rendered.replace(custom_placeholder, custom_text)
            else:
                # Add at end if no placeholder
                rendered += f"\n\n{custom_text}"

        return rendered
```

### Email Variables

```python
class EmailVariables:
    CANDIDATE_NAME = "candidate_name"
    CANDIDATE_FIRST_NAME = "candidate_first_name"
    POSITION_TITLE = "position_title"
    COMPANY_NAME = "company_name"
    STAGE_NAME = "stage_name"
    CUSTOM_TEXT = "custom_text"

    @classmethod
    def build_context(
        cls,
        candidate: Candidate,
        position: Position,
        company: Company,
        stage: WorkflowStage,
        custom_text: Optional[str] = None
    ) -> Dict[str, Any]:
        return {
            cls.CANDIDATE_NAME: candidate.full_name,
            cls.CANDIDATE_FIRST_NAME: candidate.first_name,
            cls.POSITION_TITLE: position.title,
            cls.COMPANY_NAME: company.name,
            cls.STAGE_NAME: stage.name,
            cls.CUSTOM_TEXT: custom_text or ""
        }
```

### SendStageTransitionEmailHandler

Event handler that sends email when stage changes.

```python
class SendStageTransitionEmailHandler:
    def __init__(
        self,
        email_template_repository: EmailTemplateRepository,
        email_service: EmailService,
        workflow_repository: WorkflowRepository
    ):
        self.email_template_repo = email_template_repository
        self.email_service = email_service
        self.workflow_repo = workflow_repository

    def handle(self, event: ApplicationStageChangedEvent) -> None:
        """
        1. Get new stage
        2. Check if has email_template_id
        3. If yes, render template
        4. Add custom_email_text if exists
        5. Send email to candidate
        6. Record in history
        """

        # Get stage
        stage = self.workflow_repo.get_stage_by_id(event.new_stage_id)

        if not stage.email_template_id:
            return  # No template configured

        # Get template
        template = self.email_template_repo.get_by_id(stage.email_template_id)

        # Build context
        context = EmailVariables.build_context(
            candidate=event.candidate,
            position=event.position,
            company=event.company,
            stage=stage,
            custom_text=stage.custom_email_text
        )

        # Render
        body = template.render(context, stage.custom_email_text)
        subject = self._render_subject(template.subject, context)

        # Send
        self.email_service.send(
            to=event.candidate.email,
            subject=subject,
            body=body
        )

        # TODO: Record in application history
```

---

## Permission System

### Stage Permission Service

```python
class StagePermissionService:
    def __init__(
        self,
        position_assignment_repo: PositionStageAssignmentRepository,
        company_user_repo: CompanyUserRepository
    ):
        self.assignment_repo = position_assignment_repo
        self.user_repo = company_user_repo

    def can_user_process_stage(
        self,
        user_id: str,
        application: CandidateApplication
    ) -> bool:
        """Check if user can process this application"""

        # Check if company admin
        user = self.user_repo.get_by_id(user_id)
        if user.is_admin:
            return True

        # Check if assigned to current stage
        assignment = self.assignment_repo.get_by_position_and_stage(
            position_id=application.position_id,
            stage_id=application.current_stage_id
        )

        if not assignment:
            return False

        return user_id in assignment.assigned_user_ids

    def get_assigned_users_for_stage(
        self,
        position_id: str,
        stage_id: str
    ) -> List[str]:
        """Get users assigned to a stage"""

        assignment = self.assignment_repo.get_by_position_and_stage(
            position_id=position_id,
            stage_id=stage_id
        )

        if not assignment:
            return []

        return assignment.assigned_user_ids
```

### Permission Checks in Commands

```python
class ChangeStageCommandHandler:
    def __init__(
        self,
        application_repo: CandidateApplicationRepository,
        permission_service: StagePermissionService,
        event_bus: EventBus
    ):
        self.application_repo = application_repo
        self.permission_service = permission_service
        self.event_bus = event_bus

    def execute(self, command: ChangeStageCommand) -> None:
        # Get application
        application = self.application_repo.get_by_id(command.application_id)

        # Check permission
        if not self.permission_service.can_user_process_stage(
            user_id=command.user_id,
            application=application
        ):
            raise PermissionDeniedError(
                "User not assigned to current stage"
            )

        # Validate transition
        self._validate_transition(application, command.new_stage_id)

        # Move to new stage
        previous_stage_id = application.current_stage_id
        application.move_to_stage(
            new_stage_id=command.new_stage_id,
            changed_by=command.user_id
        )

        # Save
        self.application_repo.save(application)

        # Emit event
        event = ApplicationStageChangedEvent(
            application_id=application.id,
            previous_stage_id=previous_stage_id,
            new_stage_id=command.new_stage_id,
            changed_by_user_id=command.user_id,
            changed_at=datetime.now(UTC)
        )
        self.event_bus.publish(event)
```

---

## APIs

### Workflow Management

```
GET    /api/company/{company_id}/workflows
POST   /api/company/{company_id}/workflows
GET    /api/workflows/{workflow_id}
PUT    /api/workflows/{workflow_id}
DELETE /api/workflows/{workflow_id}
POST   /api/workflows/{workflow_id}/activate
POST   /api/workflows/{workflow_id}/deactivate
POST   /api/workflows/{workflow_id}/archive

GET    /api/workflows/{workflow_id}/stages
POST   /api/workflows/{workflow_id}/stages
GET    /api/stages/{stage_id}
PUT    /api/stages/{stage_id}
DELETE /api/stages/{stage_id}
POST   /api/stages/{stage_id}/move-up
POST   /api/stages/{stage_id}/move-down
```

### Custom Fields

```
GET    /api/workflows/{workflow_id}/custom-fields
POST   /api/workflows/{workflow_id}/custom-fields
PUT    /api/custom-fields/{field_id}
DELETE /api/custom-fields/{field_id}

GET    /api/stages/{stage_id}/field-configurations
PUT    /api/stages/{stage_id}/fields/{field_id}/visibility
```

### Field Validation Rules

```
GET    /api/custom-fields/{field_id}/validation-rules
POST   /api/custom-fields/{field_id}/validation-rules
GET    /api/validation-rules/{rule_id}
PUT    /api/validation-rules/{rule_id}
DELETE /api/validation-rules/{rule_id}
POST   /api/validation-rules/{rule_id}/activate
POST   /api/validation-rules/{rule_id}/deactivate

GET    /api/stages/{stage_id}/validation-rules          (all rules for stage)
POST   /api/applications/{app_id}/validate-stage-transition  (preview validation)
```

### Position Stage Assignments

```
GET    /api/positions/{position_id}/stage-assignments
POST   /api/positions/{position_id}/stage-assignments      (batch)
PUT    /api/positions/{position_id}/stages/{stage_id}/users
POST   /api/positions/{position_id}/stages/{stage_id}/users/{user_id}
DELETE /api/positions/{position_id}/stages/{stage_id}/users/{user_id}
GET    /api/positions/{position_id}/stages/{stage_id}/can-process
```

### Application Processing

```
GET    /api/company/{company_id}/applications
GET    /api/positions/{position_id}/applications
GET    /api/applications/{application_id}
POST   /api/applications/{application_id}/change-stage
GET    /api/applications/{application_id}/can-change-stage
GET    /api/applications/{application_id}/history

POST   /api/applications/{application_id}/comments
GET    /api/applications/{application_id}/comments

POST   /api/applications/{application_id}/messages
GET    /api/applications/{application_id}/messages
```

### Task Management

```
GET    /api/company-users/{user_id}/tasks/assigned
GET    /api/company-users/{user_id}/tasks/available
GET    /api/company-users/{user_id}/tasks/all
POST   /api/applications/{app_id}/claim
POST   /api/applications/{app_id}/unclaim
PUT    /api/applications/{app_id}/task-status
```

### Email Templates

```
GET    /api/company/{company_id}/email-templates
POST   /api/company/{company_id}/email-templates
GET    /api/email-templates/{template_id}
PUT    /api/email-templates/{template_id}
DELETE /api/email-templates/{template_id}
POST   /api/email-templates/{template_id}/preview
POST   /api/email-templates/{template_id}/test-send
```

### Analytics

```
GET    /api/workflows/{workflow_id}/analytics
GET    /api/workflows/{workflow_id}/bottlenecks
GET    /api/workflows/{workflow_id}/cost-analysis
GET    /api/positions/{position_id}/hiring-metrics
```

---

## Domain Events

### ApplicationStageChangedEvent

```python
@dataclass
class ApplicationStageChangedEvent(DomainEvent):
    application_id: str
    previous_stage_id: str
    new_stage_id: str
    changed_by_user_id: str
    changed_at: datetime

    # Additional context for event handlers
    candidate: Candidate
    position: Position
    company: Company
```

**Event Handlers:**
- `SendStageTransitionEmailHandler`: Sends automatic email if configured
- `UpdateApplicationHistoryHandler`: Records change in history
- `RecalculateDeadlineHandler`: Recalculates new stage deadline
- `NotifyAssignedUsersHandler`: Notifies users of new stage

### PositionCreatedEvent

```python
@dataclass
class PositionCreatedEvent(DomainEvent):
    position_id: str
    company_id: str
    workflow_id: Optional[str]
    created_by_user_id: str
    created_at: datetime
```

**Event Handlers:**
- `CreateDefaultStageAssignmentsHandler`: Creates default assignments based on workflow

### CandidateApplicationCreatedEvent

```python
@dataclass
class CandidateApplicationCreatedEvent(DomainEvent):
    application_id: str
    candidate_id: str
    position_id: str
    workflow_id: str
    initial_stage_id: str
    created_at: datetime
```

**Event Handlers:**
- `SendApplicationConfirmationEmailHandler`: Sends confirmation email to candidate
- `NotifyRecruitersHandler`: Notifies assigned recruiters

---

## Frontend Implementation

### Component Structure

```
client-vite/src/
├── pages/
│   └── company/
│       ├── WorkflowsSettingsPage.tsx       # Workflow list
│       ├── CreateWorkflowPage.tsx          # Create workflow
│       ├── EditWorkflowPage.tsx            # Edit workflow
│       ├── PositionsPage.tsx               # Position list
│       ├── CreatePositionPage.tsx          # Create position with workflow
│       ├── EditPositionPage.tsx            # Edit position
│       ├── ApplicationsKanbanPage.tsx      # Kanban board
│       ├── ApplicationDetailPage.tsx       # Application detail
│       ├── MyTasksPage.tsx                 # Task dashboard
│       └── WorkflowAnalyticsPage.tsx       # Analytics
│
├── components/
│   └── company/
│       ├── workflow/
│       │   ├── WorkflowCard.tsx
│       │   ├── WorkflowStageList.tsx
│       │   ├── StageForm.tsx
│       │   ├── CustomFieldEditor.tsx
│       │   └── FieldVisibilityMatrix.tsx
│       ├── position/
│       │   ├── WorkflowSelector.tsx
│       │   ├── StageAssignmentEditor.tsx
│       │   └── UserMultiSelect.tsx
│       ├── application/
│       │   ├── ApplicationCard.tsx
│       │   ├── KanbanColumn.tsx
│       │   ├── StageTransitionButton.tsx
│       │   ├── ApplicationHistory.tsx
│       │   └── CustomFieldsForm.tsx
│       ├── tasks/
│       │   ├── TaskCard.tsx
│       │   ├── TaskFilters.tsx
│       │   ├── PriorityBadge.tsx
│       │   └── DeadlineIndicator.tsx
│       └── email/
│           ├── EmailTemplateEditor.tsx
│           ├── TemplateVariables.tsx
│           └── EmailPreview.tsx
│
└── services/
    ├── workflowService.ts
    ├── stageService.ts
    ├── customFieldService.ts
    ├── positionStageAssignmentService.ts
    ├── applicationService.ts
    ├── taskService.ts
    └── emailTemplateService.ts
```

### API Services

#### workflowService.ts

```typescript
export const workflowService = {
    listWorkflows: (companyId: string) =>
        api.get(`/company/${companyId}/workflows`),

    createWorkflow: (companyId: string, data: CreateWorkflowRequest) =>
        api.post(`/company/${companyId}/workflows`, data),

    getWorkflow: (workflowId: string) =>
        api.get(`/workflows/${workflowId}`),

    updateWorkflow: (workflowId: string, data: UpdateWorkflowRequest) =>
        api.put(`/workflows/${workflowId}`, data),

    deleteWorkflow: (workflowId: string) =>
        api.delete(`/workflows/${workflowId}`),

    activateWorkflow: (workflowId: string) =>
        api.post(`/workflows/${workflowId}/activate`),

    deactivateWorkflow: (workflowId: string) =>
        api.post(`/workflows/${workflowId}/deactivate`),
};
```

### TypeScript Types

```typescript
// Validation Rule types
export interface ValidationRule {
    id: string;
    custom_field_id: string;
    stage_id: string;
    rule_type: 'compare_position_field' | 'range' | 'pattern' | 'custom';
    comparison_operator?: 'gt' | 'gte' | 'lt' | 'lte' | 'eq' | 'neq' | 'in_range' | 'out_range';
    position_field_path?: string;
    comparison_value?: any;
    severity: 'warning' | 'error';
    validation_message: string;
    auto_reject: boolean;
    rejection_reason?: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface CreateValidationRuleRequest {
    custom_field_id: string;
    stage_id: string;
    rule_type: 'compare_position_field' | 'range' | 'pattern' | 'custom';
    comparison_operator?: 'gt' | 'gte' | 'lt' | 'lte' | 'eq' | 'neq' | 'in_range' | 'out_range';
    position_field_path?: string;
    comparison_value?: any;
    severity: 'warning' | 'error';
    validation_message: string;
    auto_reject?: boolean;
    rejection_reason?: string;
}

export interface ValidationResult {
    passed: boolean;
    severity?: 'warning' | 'error';
    message?: string;
    auto_reject: boolean;
    rejection_reason?: string;
}

export interface StageTransitionValidationResult {
    can_proceed: boolean;
    has_warnings: boolean;
    errors: string[];
    warnings: string[];
    auto_reject: boolean;
    rejection_reason?: string;
}

export interface ChangeStageResult {
    success: boolean;
    status: 'success' | 'validation_failed' | 'needs_confirmation' | 'rejected';
    errors: string[];
    warnings: string[];
    rejection_reason?: string;
}

// Workflow types
export interface Workflow {
    id: string;
    company_id: string;
    name: string;
    description?: string;
    workflow_type: 'prospecting' | 'selection';
    status: 'active' | 'inactive' | 'archived';
    is_default: boolean;
    stages: WorkflowStage[];
    active_candidates_count: number;
    active_positions_count: number;
    created_at: string;
    updated_at: string;
}

export interface WorkflowStage {
    id: string;
    workflow_id: string;
    name: string;
    description?: string;
    stage_type: 'initial' | 'intermediate' | 'final' | 'custom';
    order: number;
    is_active: boolean;
    required_outcome?: string;
    estimated_duration_days?: number;
    deadline_days?: number;
    estimated_cost?: number;
    default_roles: string[];
    default_assigned_users: string[];
    email_template_id?: string;
    custom_email_text?: string;
    created_at: string;
    updated_at: string;
}

// Custom field types
export interface CustomField {
    id: string;
    workflow_id: string;
    field_key: string;
    field_name: string;
    field_type: FieldType;
    field_config: Record<string, any>;
    order: number;
    created_at: string;
    updated_at: string;
}

export type FieldType =
    | 'text_short'
    | 'text_long'
    | 'dropdown'
    | 'checkbox'
    | 'radio'
    | 'date'
    | 'datetime'
    | 'time'
    | 'file'
    | 'currency'
    | 'integer'
    | 'float'
    | 'percentage';

export type FieldVisibility =
    | 'hidden'
    | 'mandatory'
    | 'recommended'
    | 'optional';

// Application types
export interface CandidateApplication {
    id: string;
    candidate_id: string;
    position_id: string;
    workflow_id: string;
    current_stage_id: string;
    application_data: Record<string, any>;
    shared_data: SharedData;
    stage_entered_at: string;
    stage_deadline?: string;
    task_status: 'pending' | 'in_progress' | 'completed' | 'blocked';
    status: string;
    priority: number;
    created_at: string;
    updated_at: string;
}

export interface SharedData {
    include_education: boolean;
    include_experience: boolean;
    include_projects: boolean;
    include_skills: boolean;
    include_languages: boolean;
    resume_ids: string[];
    portfolio_url?: string;
}

// Task types
export interface Task {
    application: CandidateApplication;
    candidate_name: string;
    candidate_photo?: string;
    position_title: string;
    current_stage_name: string;
    priority_score: number;
    deadline?: string;
    days_in_stage: number;
    assignment_type: 'direct' | 'role_based';
    can_process: boolean;
}

// Assignment types
export interface PositionStageAssignment {
    id: string;
    position_id: string;
    stage_id: string;
    assigned_user_ids: string[];
    created_at: string;
    updated_at: string;
}
```

---

## Migrations

### Execution Order

1. `add_workflow_type_to_company_workflows.sql`
2. `add_stage_configuration_fields.sql`
3. `create_workflow_custom_fields.sql`
4. `create_stage_field_configurations.sql`
5. `create_field_validation_rules.sql` ⭐ **NEW**
6. `add_workflow_id_to_positions.sql`
7. `create_position_stage_assignments.sql`
8. `add_workflow_fields_to_candidate_applications.sql`
9. `create_company_talent_pool.sql`
10. `create_email_templates.sql`
11. `add_roles_to_company_users.sql`

---

## Testing Strategy

### Unit Tests

```python
# Test WorkflowStage entity
def test_create_workflow_stage_with_valid_data():
    stage = WorkflowStage.create(
        workflow_id=WorkflowId("wf_123"),
        name="Technical Interview",
        stage_type=StageType.INTERMEDIATE,
        order=2,
        deadline_days=5,
        estimated_cost=Decimal("100.00")
    )

    assert stage.name == "Technical Interview"
    assert stage.deadline_days == 5
    assert stage.estimated_cost == Decimal("100.00")

def test_create_stage_with_negative_deadline_fails():
    with pytest.raises(ValueError):
        WorkflowStage.create(
            workflow_id=WorkflowId("wf_123"),
            name="Test",
            stage_type=StageType.INTERMEDIATE,
            order=1,
            deadline_days=-1
        )

# Test ValidationRule entity
def test_create_validation_rule_with_position_comparison():
    rule = ValidationRule.create(
        custom_field_id=CustomFieldId("field_salary"),
        stage_id=WorkflowStageId("stage_123"),
        rule_type=ValidationRuleType.COMPARE_POSITION_FIELD,
        comparison_operator=ComparisonOperator.GREATER_THAN,
        position_field_path="max_salary",
        severity=ValidationSeverity.ERROR,
        validation_message="Salary too high",
        auto_reject=True,
        rejection_reason="Exceeds budget"
    )

    assert rule.comparison_operator == ComparisonOperator.GREATER_THAN
    assert rule.position_field_path == "max_salary"
    assert rule.severity == ValidationSeverity.ERROR
    assert rule.auto_reject is True

def test_validation_rule_evaluate_salary_exceeds_max():
    rule = ValidationRule.create(
        custom_field_id=CustomFieldId("field_salary"),
        stage_id=WorkflowStageId("stage_123"),
        rule_type=ValidationRuleType.COMPARE_POSITION_FIELD,
        comparison_operator=ComparisonOperator.GREATER_THAN,
        position_field_path="max_salary",
        severity=ValidationSeverity.ERROR,
        validation_message="Expected ${candidate_value}, max ${position_value}"
    )

    position = Position(max_salary=120000)
    result = rule.evaluate(candidate_value=150000, position=position)

    assert result.passed is False
    assert result.severity == ValidationSeverity.ERROR
    assert "150000" in result.message
    assert "120000" in result.message

def test_validation_rule_evaluate_salary_within_range():
    rule = ValidationRule.create(
        custom_field_id=CustomFieldId("field_salary"),
        stage_id=WorkflowStageId("stage_123"),
        rule_type=ValidationRuleType.COMPARE_POSITION_FIELD,
        comparison_operator=ComparisonOperator.GREATER_THAN,
        position_field_path="max_salary",
        severity=ValidationSeverity.ERROR,
        validation_message="Salary too high"
    )

    position = Position(max_salary=120000)
    result = rule.evaluate(candidate_value=100000, position=position)

    assert result.passed is True

def test_field_validation_service_blocks_on_errors():
    # Setup
    service = FieldValidationService(validation_rule_repo, custom_field_repo)
    application = create_test_application(
        application_data={"salary_expectation": 150000}
    )
    position = create_test_position(max_salary=120000)

    # Mock validation rule
    rule = create_salary_validation_rule(severity="error")
    validation_rule_repo.get_by_stage.return_value = [rule]

    # Execute
    result = service.validate_stage_transition(
        application=application,
        from_stage_id=application.current_stage_id,
        to_stage_id="next_stage",
        position=position
    )

    # Assert
    assert result.can_proceed is False
    assert len(result.errors) > 0

def test_field_validation_service_warns_but_allows():
    # Setup
    service = FieldValidationService(validation_rule_repo, custom_field_repo)
    application = create_test_application(
        application_data={"location": "New York"}
    )
    position = create_test_position(location="San Francisco")

    # Mock validation rule
    rule = create_location_validation_rule(severity="warning")
    validation_rule_repo.get_by_stage.return_value = [rule]

    # Execute
    result = service.validate_stage_transition(
        application=application,
        from_stage_id=application.current_stage_id,
        to_stage_id="next_stage",
        position=position
    )

    # Assert
    assert result.can_proceed is True
    assert result.has_warnings is True
    assert len(result.warnings) > 0
```

### Integration Tests

```python
def test_create_position_with_workflow_creates_assignments():
    # Arrange
    workflow = create_test_workflow_with_stages()

    # Act
    position = create_position(workflow_id=workflow.id)

    # Assert
    assignments = position_assignment_repo.list_by_position(position.id)
    assert len(assignments) == len(workflow.stages)

def test_change_stage_without_permission_fails():
    # Arrange
    application = create_test_application()
    unauthorized_user = create_test_user()

    # Act & Assert
    with pytest.raises(PermissionDeniedError):
        change_stage_command_handler.execute(
            ChangeStageCommand(
                application_id=application.id,
                new_stage_id="next_stage",
                user_id=unauthorized_user.id
            )
        )
```

### E2E Tests

```typescript
describe('Complete Hiring Workflow', () => {
    it('should process candidate through all stages', async () => {
        // 1. Create workflow
        const workflow = await createWorkflow({
            name: 'Test Hiring',
            stages: [
                { name: 'Screening', order: 0 },
                { name: 'Interview', order: 1 },
                { name: 'Hired', order: 2 }
            ]
        });

        // 2. Create position with workflow
        const position = await createPosition({
            title: 'Developer',
            workflow_id: workflow.id
        });

        // 3. Assign users to stages
        await assignUsersToStages(position.id, [
            { stage_id: workflow.stages[0].id, user_ids: [recruiter.id] },
            { stage_id: workflow.stages[1].id, user_ids: [manager.id] }
        ]);

        // 4. Candidate applies
        const application = await candidateApplies(position.id);

        // 5. Recruiter moves to interview
        await loginAs(recruiter);
        await moveToNextStage(application.id);

        // 6. Manager moves to hired
        await loginAs(manager);
        await moveToNextStage(application.id);

        // 7. Verify final state
        const finalApp = await getApplication(application.id);
        expect(finalApp.current_stage_id).toBe(workflow.stages[2].id);
    });
});
```

---

## Performance Considerations

### Database Indexes

```sql
-- For frequent searches
CREATE INDEX idx_applications_stage_deadline ON candidate_applications(stage_deadline)
    WHERE task_status = 'pending';

CREATE INDEX idx_applications_workflow_stage ON candidate_applications(workflow_id, current_stage_id);

CREATE INDEX idx_stage_assignments_lookup ON position_stage_assignments(position_id, stage_id);

-- For task queries
CREATE INDEX idx_applications_task_priority ON candidate_applications(
    (application_data->>'priority_score')::int DESC,
    stage_entered_at ASC
) WHERE task_status = 'pending';
```

### Caching Strategy

```python
# Cache workflow + stages for 1 hour (changes infrequently)
@cache(ttl=3600)
def get_workflow_with_stages(workflow_id: str) -> WorkflowWithStagesDto:
    pass

# Cache user permissions for 5 minutes
@cache(ttl=300)
def get_user_stage_permissions(user_id: str, stage_id: str) -> bool:
    pass

# Cache user roles for 10 minutes
@cache(ttl=600)
def get_user_roles(user_id: str) -> List[str]:
    pass
```

### Query Optimization

```python
# Eager loading to avoid N+1 queries
def list_tasks_for_user(user_id: str) -> List[TaskDto]:
    return (
        session.query(CandidateApplication)
        .options(
            joinedload(CandidateApplication.candidate),
            joinedload(CandidateApplication.position),
            joinedload(CandidateApplication.current_stage)
        )
        .join(PositionStageAssignment)
        .filter(...)
        .all()
    )
```

---

## Security Considerations

### Authorization

```python
# Always check permissions before sensitive operations
class ChangeStageController:
    @require_auth
    def change_stage(self, application_id: str, request: ChangeStageRequest):
        # Verify user belongs to same company
        application = self.app_repo.get_by_id(application_id)
        if application.company_id != current_user.company_id:
            raise ForbiddenError()

        # Verify specific stage permission
        if not self.permission_service.can_user_process_stage(
            user_id=current_user.id,
            application=application
        ):
            raise ForbiddenError("Not assigned to current stage")

        # Proceed with command
        self.command_bus.execute(...)
```

### Data Privacy

```python
# Only share data authorized by candidate
class ApplicationDto:
    @staticmethod
    def from_entity(
        application: CandidateApplication,
        include_candidate_data: bool = False
    ) -> "ApplicationDto":
        dto = ApplicationDto(
            id=application.id.value,
            position_id=application.position_id.value,
            status=application.status,
            # ...
        )

        if include_candidate_data:
            # Filter according to shared_data
            dto.candidate_data = filter_shared_data(
                candidate=application.candidate,
                shared_data=application.shared_data
            )

        return dto

def filter_shared_data(candidate: Candidate, shared_data: SharedData) -> Dict:
    result = {}

    if shared_data.include_education:
        result['education'] = candidate.education

    if shared_data.include_experience:
        result['experience'] = candidate.experience

    # ... more fields according to authorization

    return result
```

---

## Deployment Checklist

### Backend

- [ ] Execute all migrations in order
- [ ] Verify indexes created
- [ ] Seed default email templates
- [ ] Seed example workflows
- [ ] Configure email service (SMTP)
- [ ] Verify event bus configured
- [ ] Verify dependency injection container updated
- [ ] Run integration tests
- [ ] Verify error logs

### Frontend

- [ ] Production build
- [ ] Verify environment variables
- [ ] Verify routes configured
- [ ] Verify access permissions by role
- [ ] E2E testing
- [ ] Verify responsive design

---

## Conclusion

This technical design implements a complete workflow system that is flexible and scalable:

1. Allows total customization of selection processes
2. Handles granular permissions per user and stage
3. Supports custom fields with dynamic validations
4. **Field validation system with warnings and errors** ⭐ **NEW**
   - Automatic validation during stage transitions
   - Compare candidate data with position requirements
   - Warning vs. Error severity levels
   - Auto-reject capability for critical mismatches
   - Rich validation messages with variable substitution
5. Automates candidate communication
6. Prioritizes tasks intelligently
7. Provides metrics and analytics
8. Maintains clean architecture and CQRS
9. Scales horizontally

### Key Features of Validation System

The validation system is a powerful feature that helps companies:

- **Save Time**: Automatically catch mismatches early in the process
- **Improve Quality**: Ensure candidates meet minimum requirements
- **Increase Consistency**: Apply the same criteria to all candidates
- **Enable Flexibility**: Warnings allow exceptions when appropriate
- **Maintain Control**: Errors block unsuitable candidates from progressing
- **Automate Decisions**: Auto-reject feature handles obvious mismatches

**Example Use Cases**:
- Salary expectations exceeding budget → **Error** (blocks progression)
- Candidate location differs from office → **Warning** (shows alert, allows proceeding)
- Missing required years of experience → **Error** (auto-rejects if configured)
- Availability date later than needed → **Warning** (user decides if acceptable)

Phased implementation allows delivering value incrementally while maintaining code quality and architecture.
