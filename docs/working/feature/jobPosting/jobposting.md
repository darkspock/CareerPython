# Job Posting & Publishing Flow

**Version:** 2.1
**Module:** Job Management

---

## 1. Overview

The goal is to allow companies to create, approve, and publish job openings efficiently. The system must be adaptable to support two distinct realities:

1. **Quick Mode (SMB/Startup):** "Write & Publish" in seconds.
2. **Controlled Mode (Enterprise):** A strict flow requiring financial approval and quality review before publishing.

Companies hiring few people won't need all the advanced features, but they will benefit from a simple and intuitive interface to get their job postings live quickly.

---

## 2. Job Publishing Flow (State Machine)

We use a linear **State Machine** called the **Job Publishing Flow** to manage the job requisition *before* any candidate applies. This flow is configurable per company.

### 2.1 The Lifecycle States

| State | UI Name | Description | Allowed Actions |
|-------|---------|-------------|-----------------|
| **DRAFT** | Draft | Hiring Manager defines needs and salary range. | Edit all fields. Request Approval. |
| **PENDING_APPROVAL** | Pending Approval | Finance/Execs review the cost (Budget Gate). | **Read-only.** Approve or Reject (with notes). |
| **CONTENT_REVIEW** | Content Review | (Optional) HR polishes text, media, and tone. | Edit descriptions/media. **Cannot touch salary/budget.** |
| **PUBLISHED** | Published | Job is live and visible to candidates. | Receive candidates. Put on hold. Close job. |
| **ON_HOLD** | On Hold | Temporarily paused (hiring freeze, etc.). | Resume to Published. Close job. |
| **CLOSED** | Closed | No longer hiring. | Archive. Reopen (returns to Draft). |
| **ARCHIVED** | Archived | Historical record. | View only. Clone to new position. |

```
DRAFT → PENDING_APPROVAL → CONTENT_REVIEW → PUBLISHED → CLOSED → ARCHIVED
                                               ↓
                                            ON_HOLD
```

### 2.2 Operation Modes (Company Setting)

#### Quick Mode (Default for SMBs)
- User creates the job and clicks "Publish"
- System internally performs: `DRAFT` → `PUBLISHED`
- Approval and Content Review steps are skipped automatically
- Implementation: Configure workflow with only 2 stages (Draft, Published)

#### Controlled Mode (Enterprise)
- User clicks "Request Approval"
- System transitions to `PENDING_APPROVAL`
- The approval chain is notified
- The "Publish" button remains disabled until the flow completes
- Sensitive fields become read-only after leaving DRAFT

### 2.3 Close Reasons

When closing a position, require a reason:
| Reason | Description |
|--------|-------------|
| FILLED | Position was filled (hired someone) |
| CANCELLED | Position no longer needed |
| BUDGET_CUT | Budget constraints |
| DUPLICATE | Duplicate of another position |
| OTHER | Other reason (requires note) |

---

## 3. Job Position Attributes

### 3.1 Standard Fields (Core)

These are common fields that recruiters expect in every ATS:

| Field | Type | Candidate Visible | Notes |
|-------|------|-------------------|-------|
| **Title** | string | Yes | Required |
| **Description** | HTML | Yes | Rich text editor |
| **Department** | reference | Yes | Link to company departments |
| **Employment Type** | enum | Yes | Full-time, Part-time, Contract, Internship, Temporary, Freelance |
| **Experience Level** | enum | Yes | Internship, Entry, Mid, Senior, Lead, Executive |
| **Work Location** | enum | Yes | On-site, Hybrid, Remote |
| **Office Locations** | list | Yes | Cities/addresses for on-site/hybrid |
| **Remote Restrictions** | string | Optional | "US only", timezone requirements |
| **Skills / Tags** | list | Yes | Vital for matching (e.g., "Python", "Sales") |
| **Languages** | list | Optional | E.g., `[{lang: "English", level: "C1"}]` |
| **Number of Openings** | int | No | Default 1 |
| **Requisition ID** | string | No | Internal job code |
| **Application Deadline** | date | Yes | Optional |

### 3.2 Financial Fields (The Gatekeeper)

Critical fields for budget control and salary transparency:

| Field | Type | Candidate Visible | Notes |
|-------|------|-------------------|-------|
| **Salary Currency** | string | Configurable | "USD", "EUR", etc. |
| **Salary Min** | decimal | Configurable | Public-facing minimum |
| **Salary Max** | decimal | Configurable | Public-facing maximum |
| **Salary Period** | enum | Configurable | Yearly, Monthly, Hourly |
| **Show Salary** | boolean | N/A | Whether to display salary to candidates |
| **Budget Max** | decimal | **Never** | Internal approved limit. Hidden from candidates. |
| **Financial Approver ID** | reference | No | Who signed off on the budget |
| **Approved At** | datetime | No | When budget was approved |

**Validation Rule:** `salary_max` must be ≤ `budget_max` (if budget approval is enabled)

### 3.3 Ownership Fields

| Field | Type | Notes |
|-------|------|-------|
| **Hiring Manager** | reference | Makes final hiring decisions, approves offers |
| **Recruiter** | reference | Day-to-day management, candidate communication |
| **Created By** | reference | User who created the position (audit) |

### 3.4 Custom Fields (Snapshot Pattern)

**Architecture Decision:** When creating a job position, custom field definitions are **COPIED** from the workflow/template, not referenced. This ensures immutability.

**Why Snapshot Pattern:**
- If the company changes global policies tomorrow, historical job data remains intact
- Reports don't break when field definitions change
- Audit trail shows exactly what was published

**Flow:**
```
Workflow.custom_fields_config (template)
         ↓ COPY at creation
JobPosition.custom_fields_config (frozen snapshot)
         ↓
JobPosition.custom_fields_values (filled by recruiter)
```

**Custom Field Definition Structure:**
- `field_key`: Unique identifier
- `label`: Display name for recruiters/candidates
- `field_type`: TEXT, NUMBER, SELECT, MULTISELECT, DATE, BOOLEAN, URL
- `options`: For SELECT/MULTISELECT types
- `is_required`: Whether field must be filled
- `candidate_visible`: Whether candidates see this field
- `validation_rules`: Min/max, patterns, etc.
- `sort_order`: Display order

**Behavior:**
- When selecting workflow, its custom fields are copied to position
- Recruiter can activate/deactivate copied fields for this position
- Recruiter can add new position-specific fields
- Once published, field definitions are frozen (structure immutable, values editable)

---

## 4. Candidate Pipeline (Separate from Publishing Flow)

To avoid naming confusion, we distinguish clearly:

- **Publishing Flow:** The states of the Job Requisition (Draft → Published)
- **Candidate Pipeline:** The steps the candidate walks through (Screening → Interview → Offer)

### 4.1 Pipeline Selection

When creating the Job, the user selects **ONE** Candidate Pipeline (e.g., "Standard Tech Pipeline").

**Predefined Pipelines (Created on Company Onboarding):**

| Phase | Default Pipeline | Stages |
|-------|------------------|--------|
| Sourcing | Sourcing Pipeline | Pending → Screening → Qualified / Not Suitable / On Hold |
| Evaluation | Evaluation Pipeline | HR Interview → Manager → Assessment → Executive → Selected / Rejected |
| Offer | Offer Pipeline | Proposal → Negotiation → Documents → Verification / Lost |

### 4.2 Stage Overrides

The user can customize *who* conducts the interview at each stage for this specific job:

| Configuration | Inherited From | Can Override |
|---------------|----------------|--------------|
| Interview Templates | Pipeline Stage | Yes - add/remove per position |
| Required Roles | Pipeline Stage | Yes - add/remove per position |
| Assigned Users | Pipeline Stage defaults | Yes - specific users per position |
| Email Templates | Pipeline Stage | Yes - per position |

**Note:** Cannot alter the structural pipeline stages themselves (in MVP).

---

## 5. Screening / Application Questions

### 5.1 Interview Template Scope

Interview templates have a `scope` field to differentiate usage:
- `PIPELINE` - Used in candidate pipeline stages (triggered during progression)
- `APPLICATION` - Used as post-application screening (triggered after apply)
- `STANDALONE` - Reusable anywhere

### 5.2 Screening Flow

1. Candidate submits application
2. System presents screening interview (if configured)
3. Candidate completes screening questions
4. Answers are scored automatically (if scoring enabled)
5. Candidate enters pipeline at initial stage

### 5.3 Inline Creation

From the job posting form, recruiter can:
- Select existing screening template from library
- Create new screening template inline (saved to library with scope=APPLICATION)
- Preview how candidates will see it
- The neme of the screening template is the same as the job title by default, but editable
- Make it transparent for the user when creating in the job posting flow, do not make go to another screen an go back.

---

## 6. The "Double Gatekeeper" Logic

To solve the "hiring without budget" problem:

### Gatekeeper 1: At Publishing (Budget Gate)

During `PENDING_APPROVAL` phase:
- System captures and locks the `approved_budget_max`
- Financial approver reviews and signs off
- This becomes the ceiling for any future offer

### Gatekeeper 2: At Offer (Offer Gate)

When a Manager tries to generate an Offer Letter:
- System compares: `Final Offer Amount` vs. `approved_budget_max`
- If Offer > Budget: System **blocks** PDF generation
- Forces an "Exception Re-approval" flow
- Creates audit trail of budget exceptions

```
Job Created → Budget Approved ($80k) → Candidate Selected → Offer $85k
                                                              ↓
                                              ❌ BLOCKED: Exceeds approved budget
                                                              ↓
                                              Request Exception Approval
                                                              ↓
                                              Finance approves new limit ($85k)
                                                              ↓
                                              ✅ Offer generated
```

---

## 7. Data Model Summary

```python
class JobPosition:
    # Identity
    id: UUID
    company_id: CompanyId
    requisition_id: Optional[str]  # Internal job code

    # Publishing Flow (State Machine)
    status: JobPositionStatusEnum  # DRAFT, PENDING_APPROVAL, CONTENT_REVIEW, PUBLISHED, ON_HOLD, CLOSED, ARCHIVED
    closed_reason: Optional[ClosedReasonEnum]
    closed_at: Optional[datetime]

    # Financial Control (The Gatekeeper)
    salary_currency: Optional[str]
    salary_min: Optional[Decimal]
    salary_max: Optional[Decimal]
    salary_period: Optional[SalaryPeriodEnum]
    show_salary: bool
    budget_max: Optional[Decimal]  # Internal limit - NEVER exposed to candidates
    approved_budget_max: Optional[Decimal]  # Snapshot captured upon approval
    financial_approver_id: Optional[CompanyUserId]
    approved_at: Optional[datetime]

    # Content
    title: str
    description_html: Optional[str]
    skills: List[str]  # Tags for matching/SEO
    languages: Optional[List[LanguageRequirement]]

    # Standard Fields
    department_id: Optional[str]
    employment_type: EmploymentTypeEnum
    experience_level: ExperienceLevelEnum
    work_location_type: WorkLocationTypeEnum
    office_locations: List[str]
    remote_restrictions: Optional[str]
    number_of_openings: int  # Default 1

    # Ownership
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
    candidate_pipeline_id: Optional[UUID]  # Reference to the chosen Pipeline
    phase_pipelines: Optional[Dict[str, str]]  # phase_id -> pipeline_id mapping
    stage_assignments: Dict[str, List[str]]  # stage_id -> [user_ids] - Overrides

    # Custom Fields (Snapshot Pattern)
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
    """Field definition copied from workflow - immutable after position is published"""
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

---

## 8. Risk Analysis & Mitigations

### Risk A: The "Backdoor Edit" (Post-Approval Drift)

**Scenario:** Finance approves the job in `PENDING_APPROVAL`. The job moves to `CONTENT_REVIEW`. The Recruiter, while "polishing" the text, secretly changes the Salary from 40k to 50k and publishes it.

**Solution:**
- Sensitive fields (Salary, Budget, Contract Type) become **Read-Only** once the state leaves `DRAFT`
- If they need to be changed, the system forces an "Edit Conditions" action that automatically reverts the status back to `PENDING_APPROVAL`
- Audit log captures all field changes with timestamps and user IDs

### Risk B: The Approver Bottleneck

**Scenario:** In Enterprise mode, if the VP of Finance goes on vacation, no jobs can be published. The system halts.

**Solution:**
- Implement a "Delegate Approver" feature
- Allow multiple approvers per level (any one can approve)
- Allow a "Global Admin" (Superuser) to force-approve a requisition, bypassing the flow (logged in audit trails)
- Optional: Auto-escalation after N days without response

### Risk C: Salary Privacy Leak

**Scenario:** The Manager sets the `Budget Max` (internal info). The Recruiter publishes the job. If careless, internal budget data might leak into the public API response.

**Solution:**
- Strictly separate `salary_range` (candidate view) from `budget_max` (finance view) in the database
- API serializers have separate DTOs for public vs internal views
- Never include budget fields in public endpoints
- Code review checklist item: "No internal financial data in public responses"

### Risk D: Transitioning from Quick to Controlled Mode

**Scenario:** A startup begins in Quick Mode. They grow and switch to Controlled Mode. What happens to old jobs that have no `approved_budget_max`?

**Solution:**
- Data Migration strategy required
- Jobs created in Quick Mode get flag `legacy_approval = True`
- Auto-fill `approved_budget_max = salary_max` at transition
- Dashboard shows "Legacy jobs without budget approval" for audit

### Risk E: Custom Fields Breaking After Publish

**Scenario:** Company changes workflow custom fields. What happens to published positions?

**Solution:**
- Snapshot Pattern ensures published positions are immutable
- `custom_fields_config` is copied at creation, not referenced
- Changes to workflow don't affect existing positions
- `source_workflow_id` tracks origin for reporting

---

## 9. API Considerations

### 9.1 Create Position Endpoint

When creating position:
1. Validate user has permission to create positions
2. COPY custom_fields_config from selected workflow
3. Initialize custom_fields_values as empty
4. Copy stage default assignments if any
5. Set status = DRAFT
6. Set created_by_id = current user

### 9.2 Request Approval Endpoint

Before requesting approval:
1. Validate required fields are filled (title, description, salary, etc.)
2. Validate salary_max ≤ budget_max (if budget enabled)
3. Set status = PENDING_APPROVAL
4. Notify approvers
5. Lock salary/budget fields from editing

### 9.3 Approve/Reject Endpoint

On approval:
1. Capture `approved_budget_max` = current `budget_max`
2. Set `financial_approver_id` = current user
3. Set `approved_at` = now
4. Transition to next state (CONTENT_REVIEW or PUBLISHED)

On rejection:
1. Set status = DRAFT
2. Unlock all fields for editing
3. Store rejection reason
4. Notify hiring manager

### 9.4 Publish Position Endpoint

Before publishing:
1. Validate required fields are filled
2. Validate required custom fields have values
3. Validate approval chain completed (if Controlled Mode)
4. Freeze custom_fields_config (no more changes to definitions)
5. Set visibility = PUBLIC (or INTERNAL)
6. Set published_at = now
7. Generate public_slug if not set

### 9.5 Update Published Position

After publishing, limited updates allowed:
- ✅ Can update: description, custom_fields_values, deadline
- ❌ Cannot change: salary, budget, workflow, custom_fields_config structure
- ⚠️ Salary changes require: Re-approval flow (status → PENDING_APPROVAL)

### 9.6 Public API (Candidate View)

Public endpoints must NEVER return:
- `budget_max`
- `approved_budget_max`
- `financial_approver_id`
- Internal custom fields (`candidate_visible = false`)
- `stage_assignments`
- Any audit/internal fields

---

## 10. Implementation Notes

### 10.1 Existing Infrastructure

The following is already implemented and can be reused:
- Workflow/Phase system with stages
- Custom fields on workflow stages
- Position stage assignments
- Visibility levels (HIDDEN, INTERNAL, PUBLIC)
- Public position API with slug support

### 10.2 What Needs Implementation

| Feature | Priority | Notes |
|---------|----------|-------|
| Status state machine | High | Replace simple visibility with full lifecycle |
| Budget fields | High | salary_min/max, budget_max, approved_budget_max |
| Financial approval flow | High | Approver assignment, notifications |
| Field locking after approval | High | Prevent post-approval edits |
| Skills/Tags field | Medium | List of strings for SEO/matching |
| Languages field | Medium | Structured language requirements |
| Double Gatekeeper at Offer | Medium | Block offers exceeding budget |
| Quick/Controlled mode toggle | Medium | Company setting |
| Delegate approver feature | Low | For approver availability |
