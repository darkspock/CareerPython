# Job Posting & Publishing Flow - Technical Analysis

## 1. Executive Summary

This document analyzes the Job Posting & Publishing Flow PRD (v2.1) against the current implementation to identify gaps and recommend implementation approach.

**Key Concepts:**
- **Publishing Flow:** Job requisition lifecycle (Draft → Approval → Published) - internal process
- **Candidate Pipeline:** Candidate journey through stages (Screening → Interview → Offer) - candidate-facing

**Key Finding:** The current implementation has foundational elements (workflows, stages, visibility) but needs significant enhancements for the full state machine, financial controls, and approval flow.

---

## 2. Current Implementation Status

### 2.1 What We Have (Implemented)

| Feature | Status | Location |
|---------|--------|----------|
| **Basic Job Position** | ✅ Complete | `JobPosition` entity |
| Title, Description | ✅ | Core fields |
| Job Category | ✅ | `JobCategoryEnum` |
| Company association | ✅ | `company_id` |
| Visibility levels | ✅ | `HIDDEN`, `INTERNAL`, `PUBLIC` |
| Public slug for URLs | ✅ | `public_slug` field |
| Application deadline | ✅ | `application_deadline` field |
| Open date | ✅ | `open_at` field |
| **Workflow Integration** | ✅ Complete | |
| Workflow assignment | ✅ | `job_position_workflow_id` |
| Phase-specific workflows | ✅ | `phase_workflows` dict |
| Stage tracking | ✅ | `stage_id` |
| Stage user assignments | ✅ | `stage_assignments` |
| **Custom Fields** | ⚠️ Partial | |
| Custom field values | ✅ | `custom_fields_values` JSON |
| Custom field config (snapshot) | ❌ | Need `custom_fields_config` |
| Candidate visibility control | ✅ | `get_visible_custom_fields_for_candidate()` |
| **Public Job Board** | ✅ Complete | |
| List public positions | ✅ | `/public/positions` |
| Get position by slug/id | ✅ | `/public/positions/{slug_or_id}` |
| Submit application | ✅ | `/public/positions/{slug_or_id}/apply` |
| **Interview Templates** | ✅ Complete | |
| Screening type templates | ✅ | `InterviewTemplateTypeEnum.SCREENING` |
| Scoring modes | ✅ | `DISTANCE`, `ABSOLUTE` |

### 2.2 Predefined Workflows (Already Implemented in Onboarding)

The company onboarding process (`InitializeCompanyPhasesCommand`) already creates:

**Candidate Application Pipelines (3 phases):**
| Phase | Pipeline | Stages |
|-------|----------|--------|
| Sourcing | Sourcing Pipeline | Pending → Screening → Qualified / Not Suitable / On Hold |
| Evaluation | Evaluation Pipeline | HR Interview → Manager → Assessment → Executive → Selected / Rejected |
| Offer | Offer Pipeline | Proposal → Negotiation → Documents → Verification / Lost |

**Job Position Publishing Flow (1 phase):**
| Phase | Workflow | Stages |
|-------|----------|--------|
| Job Positions | Job Positions Workflow | Draft → Under Review → Approved → Published → Closed / Cancelled |

**Also created during onboarding:**
- 7 default roles (HR Manager, Recruiter, Tech Lead, Hiring Manager, Interviewer, Department Head, CTO)
- 5 default pages (About Company, Job Position Description, Data Protection, Terms of Use, Thank You)

### 2.3 What's Missing (From PRD v2.1)

| Feature | Priority | Notes |
|---------|----------|-------|
| **Publishing Flow State Machine** | High | Full lifecycle with PENDING_APPROVAL, CONTENT_REVIEW states |
| **Financial Fields** | High | budget_max, approved_budget_max, salary_min/max, currency |
| **Financial Approval Flow** | High | Approver assignment, lock fields after approval |
| **Double Gatekeeper Logic** | High | Budget check at publish AND at offer |
| **Custom Fields Snapshot** | High | Copy config from workflow at creation |
| **Skills/Tags Field** | Medium | List of strings for SEO/matching |
| **Languages Field** | Medium | Structured language requirements |
| **Quick/Controlled Mode** | ❌ Removed | Solved via workflow configuration (2-stage vs multi-stage workflow) |
| **Interview Template Scope** | Medium | PIPELINE vs APPLICATION vs STANDALONE |
| **Inline Screening Creation** | Medium | Create template without leaving job form |

---

## 3. Architecture Decisions

### 3.1 Snapshot Pattern for Custom Fields

**Decision:** When creating a job position, custom field definitions are **COPIED** from the workflow, not referenced.

```
❌ Reference Pattern (problematic):
JobPosition → references → Workflow.custom_fields
                              ↓
                    If workflow changes, ALL positions change

✅ Snapshot Pattern (chosen):
Workflow.custom_fields_config (template)
         ↓ COPY at creation
JobPosition.custom_fields_config (frozen snapshot)
         ↓
JobPosition.custom_fields_values (recruiter fills these)
```

**Benefits:**
1. **Immutability after publish** - Published positions don't change unexpectedly
2. **Historical integrity** - Audit trail shows exactly what candidates saw
3. **Independence** - Position can be modified without affecting workflow
4. **Predictability** - Recruiters won't see live postings change

### 3.2 Publishing Flow vs Candidate Pipeline

**Clear Separation:**

| Concept | Purpose | States/Stages | Who Interacts |
|---------|---------|---------------|---------------|
| **Publishing Flow** | Job requisition approval | DRAFT → PENDING_APPROVAL → CONTENT_REVIEW → PUBLISHED | Internal team (HR, Finance, Hiring Manager) |
| **Candidate Pipeline** | Candidate evaluation | Screening → Interview → Offer | Candidates + Recruiters |

**Implementation:** These are independent systems. A job has:
- One `status` (publishing flow state)
- One `candidate_pipeline_id` (which pipeline candidates go through)

### 3.3 Double Gatekeeper Logic

**Gatekeeper 1: At Publishing**
- During `PENDING_APPROVAL`, system captures `approved_budget_max`
- Financial approver signs off
- This becomes ceiling for offers

**Gatekeeper 2: At Offer**
- When generating offer letter, compare `offer_amount` vs `approved_budget_max`
- If exceeds: Block and force exception re-approval
- Creates audit trail

---

## 4. Data Model Changes Required

### 4.1 Updated JobPosition Entity

```python
@dataclass
class JobPosition:
    # Identity
    id: JobPositionId
    company_id: CompanyId
    requisition_id: Optional[str]  # Internal job code

    # Publishing Flow (State Machine) - ENHANCED
    status: JobPositionStatusEnum  # DRAFT, PENDING_APPROVAL, CONTENT_REVIEW, PUBLISHED, ON_HOLD, CLOSED, ARCHIVED
    closed_reason: Optional[ClosedReasonEnum]
    closed_at: Optional[datetime]

    # Financial Control (NEW - The Gatekeeper)
    salary_currency: Optional[str]  # "USD", "EUR"
    salary_min: Optional[Decimal]
    salary_max: Optional[Decimal]
    salary_period: Optional[SalaryPeriodEnum]  # YEARLY, MONTHLY, HOURLY
    show_salary: bool  # Whether to display to candidates
    budget_max: Optional[Decimal]  # Internal limit - NEVER exposed
    approved_budget_max: Optional[Decimal]  # Snapshot captured upon approval
    financial_approver_id: Optional[CompanyUserId]
    approved_at: Optional[datetime]

    # Content
    title: str
    description_html: Optional[str]  # Rich text
    skills: List[str]  # NEW - Tags for matching/SEO
    languages: Optional[List[LanguageRequirement]]  # NEW

    # Standard Fields (NEW)
    department_id: Optional[str]
    employment_type: EmploymentTypeEnum
    experience_level: ExperienceLevelEnum
    work_location_type: WorkLocationTypeEnum
    office_locations: List[str]
    remote_restrictions: Optional[str]
    number_of_openings: int  # Default 1

    # Ownership (NEW)
    hiring_manager_id: Optional[CompanyUserId]
    recruiter_id: Optional[CompanyUserId]
    created_by_id: Optional[CompanyUserId]

    # Publishing
    visibility: VisibilityEnum  # HIDDEN, INTERNAL, PUBLIC
    public_slug: Optional[str]
    open_at: Optional[datetime]
    application_deadline: Optional[date]
    published_at: Optional[datetime]

    # Candidate Pipeline Configuration
    candidate_pipeline_id: Optional[str]  # Reference to chosen Pipeline
    phase_pipelines: Optional[Dict[str, str]]  # phase_id -> pipeline_id
    stage_assignments: Dict[str, List[str]]  # stage_id -> [user_ids]

    # Custom Fields (SNAPSHOT PATTERN)
    custom_fields_config: List[CustomFieldDefinition]  # Frozen structure
    custom_fields_values: Dict[str, Any]  # Editable values
    source_workflow_id: Optional[str]  # Track origin

    # Screening
    screening_template_id: Optional[str]

    # Timestamps
    created_at: datetime
    updated_at: datetime


@dataclass
class CustomFieldDefinition:
    """Field definition copied from workflow - immutable after publish"""
    field_key: str
    label: str
    field_type: str  # TEXT, NUMBER, SELECT, MULTISELECT, DATE, BOOLEAN, URL
    options: Optional[List[str]]
    is_required: bool
    candidate_visible: bool
    validation_rules: Optional[Dict[str, Any]]
    sort_order: int
    is_active: bool  # Recruiter can deactivate per position


@dataclass
class LanguageRequirement:
    language: str  # "English", "Spanish"
    level: str  # "A1", "A2", "B1", "B2", "C1", "C2", "Native"
```

### 4.2 New Enums Required

```python
class JobPositionStatusEnum(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    CONTENT_REVIEW = "content_review"
    PUBLISHED = "published"
    ON_HOLD = "on_hold"
    CLOSED = "closed"
    ARCHIVED = "archived"

class ClosedReasonEnum(str, Enum):
    FILLED = "filled"
    CANCELLED = "cancelled"
    BUDGET_CUT = "budget_cut"
    DUPLICATE = "duplicate"
    OTHER = "other"

class EmploymentTypeEnum(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"
    FREELANCE = "freelance"

class ExperienceLevelEnum(str, Enum):
    INTERNSHIP = "internship"
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class WorkLocationTypeEnum(str, Enum):
    ON_SITE = "on_site"
    HYBRID = "hybrid"
    REMOTE = "remote"

class SalaryPeriodEnum(str, Enum):
    HOURLY = "hourly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class InterviewTemplateScopeEnum(str, Enum):
    PIPELINE = "pipeline"      # Used in candidate pipeline stages
    APPLICATION = "application"  # Post-application screening
    STANDALONE = "standalone"   # Reusable anywhere
```

---

## 5. Database Migration Plan

### 5.1 Phase 1: Add New Columns (Non-Breaking)

```sql
-- Add financial fields
ALTER TABLE job_positions ADD COLUMN salary_currency VARCHAR(3);
ALTER TABLE job_positions ADD COLUMN salary_min DECIMAL(12,2);
ALTER TABLE job_positions ADD COLUMN salary_max DECIMAL(12,2);
ALTER TABLE job_positions ADD COLUMN salary_period VARCHAR(20);
ALTER TABLE job_positions ADD COLUMN show_salary BOOLEAN DEFAULT false;
ALTER TABLE job_positions ADD COLUMN budget_max DECIMAL(12,2);
ALTER TABLE job_positions ADD COLUMN approved_budget_max DECIMAL(12,2);
ALTER TABLE job_positions ADD COLUMN financial_approver_id VARCHAR;
ALTER TABLE job_positions ADD COLUMN approved_at TIMESTAMP;

-- Add standard fields
ALTER TABLE job_positions ADD COLUMN department_id VARCHAR;
ALTER TABLE job_positions ADD COLUMN employment_type VARCHAR(20);
ALTER TABLE job_positions ADD COLUMN experience_level VARCHAR(20);
ALTER TABLE job_positions ADD COLUMN work_location_type VARCHAR(20);
ALTER TABLE job_positions ADD COLUMN office_locations JSON DEFAULT '[]';
ALTER TABLE job_positions ADD COLUMN remote_restrictions VARCHAR;
ALTER TABLE job_positions ADD COLUMN number_of_openings INTEGER DEFAULT 1;
ALTER TABLE job_positions ADD COLUMN requisition_id VARCHAR;

-- Add ownership fields
ALTER TABLE job_positions ADD COLUMN hiring_manager_id VARCHAR;
ALTER TABLE job_positions ADD COLUMN recruiter_id VARCHAR;
ALTER TABLE job_positions ADD COLUMN created_by_id VARCHAR;

-- Add new content fields
ALTER TABLE job_positions ADD COLUMN skills JSON DEFAULT '[]';
ALTER TABLE job_positions ADD COLUMN languages JSON;

-- Add lifecycle fields
ALTER TABLE job_positions ADD COLUMN status VARCHAR(30) DEFAULT 'draft';
ALTER TABLE job_positions ADD COLUMN closed_reason VARCHAR(20);
ALTER TABLE job_positions ADD COLUMN closed_at TIMESTAMP;
ALTER TABLE job_positions ADD COLUMN published_at TIMESTAMP;

-- Add custom fields snapshot
ALTER TABLE job_positions ADD COLUMN custom_fields_config JSON DEFAULT '[]';
ALTER TABLE job_positions ADD COLUMN source_workflow_id VARCHAR;

-- Add pipeline reference
ALTER TABLE job_positions ADD COLUMN candidate_pipeline_id VARCHAR;
ALTER TABLE job_positions ADD COLUMN phase_pipelines JSON;

-- Add screening
ALTER TABLE job_positions ADD COLUMN screening_template_id VARCHAR;

-- Create indexes
CREATE INDEX ix_job_positions_status ON job_positions(status);
CREATE INDEX ix_job_positions_company_status ON job_positions(company_id, status);
CREATE INDEX ix_job_positions_hiring_manager ON job_positions(hiring_manager_id);
CREATE INDEX ix_job_positions_recruiter ON job_positions(recruiter_id);
```

### 5.2 Phase 2: Data Migration

```sql
-- Migrate visibility to status
UPDATE job_positions
SET status = CASE
    WHEN visibility = 'public' THEN 'published'
    WHEN visibility = 'internal' THEN 'published'
    ELSE 'draft'
END
WHERE status IS NULL;

-- Set published_at for existing public positions
UPDATE job_positions
SET published_at = created_at
WHERE visibility = 'public' AND published_at IS NULL;
```

### 5.3 Phase 3: Add Interview Template Scope

```sql
-- Add scope to interview_templates
ALTER TABLE interview_templates ADD COLUMN scope VARCHAR(20) DEFAULT 'pipeline';

-- Migrate existing screening templates
UPDATE interview_templates
SET scope = 'application'
WHERE template_type = 'SCREENING';
```

---

## 6. API Changes Required

### 6.1 New Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/positions/{id}/request-approval` | POST | Transition DRAFT → PENDING_APPROVAL |
| `/positions/{id}/approve` | POST | Approve and capture budget |
| `/positions/{id}/reject` | POST | Reject with reason, return to DRAFT |
| `/positions/{id}/publish` | POST | Transition to PUBLISHED |
| `/positions/{id}/hold` | POST | Transition to ON_HOLD |
| `/positions/{id}/close` | POST | Close with reason |
| `/positions/{id}/archive` | POST | Archive closed position |
| `/positions/{id}/clone` | POST | Clone to new draft |

### 6.2 Modified Endpoints

| Endpoint | Changes |
|----------|---------|
| `POST /positions` | Accept all new fields, copy custom_fields_config from workflow |
| `PUT /positions/{id}` | Enforce field locking based on status |
| `GET /positions/{id}` | Return all new fields |
| `GET /public/positions/{id}` | NEVER return budget fields |

### 6.3 Field Locking Rules

| Status | Editable Fields | Locked Fields |
|--------|-----------------|---------------|
| DRAFT | All | None |
| PENDING_APPROVAL | None (read-only) | All |
| CONTENT_REVIEW | description, skills, custom_fields_values | salary, budget, workflow |
| PUBLISHED | description, deadline, custom_fields_values | salary, budget, workflow, custom_fields_config |
| ON_HOLD | None | All |
| CLOSED | None | All |

---

## 7. Risk Mitigations Implementation

### 7.1 Risk A: Backdoor Edit (Post-Approval Drift)

**Implementation:**
```python
class JobPosition:
    def can_edit_field(self, field_name: str) -> bool:
        """Check if field can be edited in current status"""
        LOCKED_AFTER_DRAFT = ['salary_min', 'salary_max', 'budget_max', 'salary_currency']
        LOCKED_AFTER_APPROVAL = ['candidate_pipeline_id', 'custom_fields_config']

        if self.status == JobPositionStatusEnum.DRAFT:
            return True
        if self.status in [JobPositionStatusEnum.PENDING_APPROVAL, JobPositionStatusEnum.ON_HOLD]:
            return False  # All locked
        if field_name in LOCKED_AFTER_DRAFT:
            return False
        if self.status == JobPositionStatusEnum.PUBLISHED and field_name in LOCKED_AFTER_APPROVAL:
            return False
        return True
```

### 7.2 Risk C: Salary Privacy Leak

**Implementation:**
```python
# In public position serializer - NEVER include these fields
class PublicJobPositionResponse(BaseModel):
    id: str
    title: str
    description_html: str
    # ... public fields only

    # EXCLUDED:
    # budget_max
    # approved_budget_max
    # financial_approver_id
    # stage_assignments
    # created_by_id

    @classmethod
    def from_dto(cls, dto: JobPositionDto) -> 'PublicJobPositionResponse':
        return cls(
            id=dto.id,
            title=dto.title,
            # Only map public fields
            salary_min=dto.salary_min if dto.show_salary else None,
            salary_max=dto.salary_max if dto.show_salary else None,
        )
```

---

## 8. Implementation Priority

### Phase 1: Core Fields & Status (High Priority)

| Task | Complexity | Dependencies |
|------|------------|--------------|
| Add status field with enum | Low | None |
| Add financial fields (salary, budget) | Low | None |
| Add ownership fields | Low | None |
| Add skills/languages fields | Low | None |
| Database migration | Medium | Above tasks |
| Update entity and DTOs | Medium | Migration |

### Phase 2: Publishing Flow (High Priority)

| Task | Complexity | Dependencies |
|------|------------|--------------|
| Status transition logic | Medium | Phase 1 |
| Field locking per status | Medium | Status transitions |
| Approval endpoints | Medium | Status transitions |
| Notifications for approvers | Medium | Approval endpoints |

### Phase 3: Custom Fields Snapshot (High Priority)

| Task | Complexity | Dependencies |
|------|------------|--------------|
| Add custom_fields_config field | Low | None |
| Copy logic on position creation | Medium | Field added |
| Freeze logic on publish | Low | Copy logic |

### Phase 4: Financial Controls (Medium Priority)

| Task | Complexity | Dependencies |
|------|------------|--------------|
| Budget validation (salary ≤ budget) | Low | Financial fields |
| Capture approved_budget_max on approval | Low | Approval flow |
| Offer gatekeeper (Phase 2 - Offer module) | Medium | Budget fields |

### Phase 5: Screening Integration (Medium Priority)

| Task | Complexity | Dependencies |
|------|------------|--------------|
| Add scope to InterviewTemplate | Low | None |
| Inline creation from job form | Medium | Scope field |
| Link screening_template_id to position | Low | Scope field |

### ~~Phase 6: Quick/Controlled Mode~~ (REMOVED)

> **Note:** This phase has been removed. The Quick/Controlled mode can be achieved through workflow configuration:
> - **Quick Mode:** Configure a 2-stage workflow (Draft → Published)
> - **Controlled Mode:** Configure a multi-stage workflow (Draft → Pending Approval → Content Review → Published)
>
> This approach leverages the existing workflow system and eliminates the need for a separate company setting.

---

## 9. Testing Checklist

### Unit Tests
- [ ] Status transitions (all valid paths)
- [ ] Status transitions (invalid paths - should fail)
- [ ] Field locking per status
- [ ] Budget validation (salary ≤ budget)
- [ ] Custom fields snapshot on creation
- [ ] Custom fields freeze on publish

### Integration Tests
- [ ] Full publishing flow: Draft → Approval → Published (multi-stage workflow)
- [ ] Simple publishing flow: Draft → Published (2-stage workflow)
- [ ] Rejection flow: Draft → Pending → Rejected → Draft
- [ ] Close with reason
- [ ] Clone position

### Security Tests
- [ ] Public API never returns budget fields
- [ ] Public API never returns internal custom fields
- [ ] Only approvers can approve
- [ ] Only owners can edit

---

## 10. Summary

The Job Posting & Publishing Flow feature requires:

1. **New Fields:** 20+ new columns on job_positions table
2. **State Machine:** 7-state publishing flow with transition rules
3. **Field Locking:** Status-dependent editability
4. **Financial Controls:** Budget approval and offer gatekeeper
5. **Snapshot Pattern:** Custom fields copied at creation
6. **API Changes:** 8 new endpoints, modifications to existing

**Estimated Effort:**
- Phase 1-2 (Core + Flow): High priority, foundational
- Phase 3-4 (Snapshot + Financial): High priority, critical for Enterprise
- Phase 5 (Screening): Medium priority, enhances UX
- ~~Phase 6 (Quick/Controlled Mode)~~: Removed - solved via workflow configuration

The existing workflow/stage infrastructure provides a solid foundation. Main work is extending the JobPosition entity and adding the publishing flow logic. The Quick/Controlled mode is inherently supported by configuring different workflows (2-stage for quick, multi-stage for controlled).
