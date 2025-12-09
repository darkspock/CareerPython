# Job Posting & Publishing Flow - Implementation Tasks

**Reference Documents:**
- `jobposting.md` - PRD v2.1
- `jobposting_analysis.md` - Technical Analysis

---

## Phase 1: Core Fields & Enums

### 1.1 Create New Enums

- [ ] **1.1.1** Create `JobPositionStatusEnum` in `src/company_bc/job_position/domain/enums/`
  ```python
  DRAFT, PENDING_APPROVAL, CONTENT_REVIEW, PUBLISHED, ON_HOLD, CLOSED, ARCHIVED
  ```

- [ ] **1.1.2** Create `ClosedReasonEnum` in `src/company_bc/job_position/domain/enums/`
  ```python
  FILLED, CANCELLED, BUDGET_CUT, DUPLICATE, OTHER
  ```

- [ ] **1.1.3** Create `ExperienceLevelEnum` in `src/company_bc/job_position/domain/enums/`
  ```python
  INTERNSHIP, ENTRY, MID, SENIOR, LEAD, EXECUTIVE
  ```

- [ ] **1.1.4** Create `SalaryPeriodEnum` in `src/company_bc/job_position/domain/enums/`
  ```python
  HOURLY, MONTHLY, YEARLY
  ```

- [ ] **1.1.5** Verify existing enums: `EmploymentType`, `WorkLocationTypeEnum`
  - Check if they exist and have correct values
  - Update if needed

- [ ] **1.1.6** Update `src/company_bc/job_position/domain/enums/__init__.py` to export all enums

### 1.2 Create Value Objects

- [ ] **1.2.1** Create `LanguageRequirement` value object
  ```python
  @dataclass
  class LanguageRequirement:
      language: str  # "English", "Spanish"
      level: str     # "A1", "A2", "B1", "B2", "C1", "C2", "Native"
  ```

- [ ] **1.2.2** Create `CustomFieldDefinition` value object
  ```python
  @dataclass
  class CustomFieldDefinition:
      field_key: str
      label: str
      field_type: str
      options: Optional[List[str]]
      is_required: bool
      candidate_visible: bool
      validation_rules: Optional[Dict[str, Any]]
      sort_order: int
      is_active: bool
  ```

### 1.3 Update JobPosition Entity

- [ ] **1.3.1** Add financial fields to `JobPosition` entity
  - `salary_currency: Optional[str]`
  - `salary_min: Optional[Decimal]`
  - `salary_max: Optional[Decimal]`
  - `salary_period: Optional[SalaryPeriodEnum]`
  - `show_salary: bool`
  - `budget_max: Optional[Decimal]`
  - `approved_budget_max: Optional[Decimal]`
  - `financial_approver_id: Optional[CompanyUserId]`
  - `approved_at: Optional[datetime]`

- [ ] **1.3.2** Add standard fields to `JobPosition` entity
  - `department_id: Optional[str]`
  - `employment_type: Optional[EmploymentTypeEnum]`
  - `experience_level: Optional[ExperienceLevelEnum]`
  - `work_location_type: Optional[WorkLocationTypeEnum]`
  - `office_locations: List[str]`
  - `remote_restrictions: Optional[str]`
  - `number_of_openings: int` (default 1)
  - `requisition_id: Optional[str]`

- [ ] **1.3.3** Add ownership fields to `JobPosition` entity
  - `hiring_manager_id: Optional[CompanyUserId]`
  - `recruiter_id: Optional[CompanyUserId]`
  - `created_by_id: Optional[CompanyUserId]`

- [ ] **1.3.4** Add content fields to `JobPosition` entity
  - `skills: List[str]`
  - `languages: Optional[List[LanguageRequirement]]`

- [ ] **1.3.5** Add lifecycle fields to `JobPosition` entity
  - `status: JobPositionStatusEnum` (default DRAFT)
  - `closed_reason: Optional[ClosedReasonEnum]`
  - `closed_at: Optional[datetime]`
  - `published_at: Optional[datetime]`

- [ ] **1.3.6** Add custom fields snapshot to `JobPosition` entity
  - `custom_fields_config: List[CustomFieldDefinition]`
  - `source_workflow_id: Optional[str]`

- [ ] **1.3.7** Add pipeline reference to `JobPosition` entity
  - `candidate_pipeline_id: Optional[str]`
  - `phase_pipelines: Optional[Dict[str, str]]`

- [ ] **1.3.8** Add screening reference to `JobPosition` entity
  - `screening_template_id: Optional[str]`

- [ ] **1.3.9** Update `JobPosition.create()` factory method with new fields

- [ ] **1.3.10** Update `JobPosition._from_repository()` method with new fields

### 1.4 Update Database Model

- [ ] **1.4.1** Update `JobPositionModel` in `src/company_bc/job_position/infrastructure/models/`
  - Add all new columns matching entity fields
  - Use appropriate SQLAlchemy types (String, Numeric, JSON, etc.)

- [ ] **1.4.2** Create database migration
  ```bash
  make revision m="add_job_position_publishing_flow_fields"
  ```

- [ ] **1.4.3** Run migration
  ```bash
  make migrate
  ```

### 1.5 Update Repository

- [ ] **1.5.1** Update `JobPositionRepository._to_domain()` to handle new fields

- [ ] **1.5.2** Update `JobPositionRepository._to_model()` to handle new fields

### 1.6 Update DTOs

- [ ] **1.6.1** Update `JobPositionDto` with all new fields

- [ ] **1.6.2** Create `JobPositionPublicDto` (candidate-facing, excludes budget fields)

---

## Phase 2: Publishing Flow State Machine

### 2.1 Status Transition Logic

- [ ] **2.1.1** Add `JobPosition.can_transition_to(new_status)` method
  - Define valid transitions:
    - DRAFT → PENDING_APPROVAL, PUBLISHED (quick mode)
    - PENDING_APPROVAL → CONTENT_REVIEW, PUBLISHED, DRAFT (rejected)
    - CONTENT_REVIEW → PUBLISHED, DRAFT (rejected)
    - PUBLISHED → ON_HOLD, CLOSED
    - ON_HOLD → PUBLISHED, CLOSED
    - CLOSED → ARCHIVED, DRAFT (reopen)

- [ ] **2.1.2** Add `JobPosition.transition_to(new_status)` method
  - Validate transition is allowed
  - Update status
  - Set timestamps (published_at, closed_at, etc.)
  - Raise exception if invalid transition

- [ ] **2.1.3** Create `JobPositionStatusTransitionError` exception

### 2.2 Field Locking Logic

- [ ] **2.2.1** Add `JobPosition.can_edit_field(field_name)` method
  - DRAFT: All fields editable
  - PENDING_APPROVAL: No fields editable
  - CONTENT_REVIEW: Only description, skills, custom_fields_values
  - PUBLISHED: Only description, deadline, custom_fields_values
  - ON_HOLD, CLOSED, ARCHIVED: No fields editable

- [ ] **2.2.2** Add `JobPosition.get_locked_fields()` method
  - Returns list of field names that are locked in current status

- [ ] **2.2.3** Update `JobPosition.update_details()` to check field locking
  - Raise `JobPositionFieldLockedError` if attempting to edit locked field

### 2.3 Create Status Transition Commands

- [ ] **2.3.1** Create `RequestJobPositionApprovalCommand`
  - Validates required fields are filled
  - Validates salary_max ≤ budget_max
  - Transitions DRAFT → PENDING_APPROVAL
  - Notifies approvers (future: notification system)

- [ ] **2.3.2** Create `ApproveJobPositionCommand`
  - Captures `approved_budget_max = budget_max`
  - Sets `financial_approver_id`
  - Sets `approved_at`
  - Transitions to CONTENT_REVIEW or PUBLISHED

- [ ] **2.3.3** Create `RejectJobPositionCommand`
  - Stores rejection reason
  - Transitions back to DRAFT
  - Unlocks all fields

- [ ] **2.3.4** Create `PublishJobPositionCommand`
  - Validates approval chain completed (if controlled mode)
  - Freezes `custom_fields_config`
  - Sets `visibility = PUBLIC`
  - Sets `published_at`
  - Generates `public_slug` if not set

- [ ] **2.3.5** Create `HoldJobPositionCommand`
  - Transitions PUBLISHED → ON_HOLD

- [ ] **2.3.6** Create `ResumeJobPositionCommand`
  - Transitions ON_HOLD → PUBLISHED

- [ ] **2.3.7** Create `CloseJobPositionCommand`
  - Requires `closed_reason`
  - Sets `closed_at`
  - Transitions to CLOSED

- [ ] **2.3.8** Create `ArchiveJobPositionCommand`
  - Transitions CLOSED → ARCHIVED

- [ ] **2.3.9** Create `CloneJobPositionCommand`
  - Creates new position in DRAFT from existing
  - Copies all fields except: id, status, timestamps, slug

---

## Phase 3: Custom Fields Snapshot

### 3.1 Workflow Custom Fields Config

- [ ] **3.1.1** Check if `Workflow` entity has `custom_fields_config`
  - If not, add `custom_fields_config: List[CustomFieldDefinition]` field

- [ ] **3.1.2** Update workflow model and migration if needed

### 3.2 Copy Logic on Position Creation

- [ ] **3.2.1** Update `CreateJobPositionCommand` to accept `workflow_id`

- [ ] **3.2.2** Update `CreateJobPositionCommandHandler`:
  - Fetch workflow by ID
  - Deep copy `workflow.custom_fields_config` to position
  - Set `source_workflow_id`
  - Initialize `custom_fields_values` as empty dict

### 3.3 Freeze Logic on Publish

- [ ] **3.3.1** In `PublishJobPositionCommand`:
  - Mark `custom_fields_config` as frozen (structure immutable)
  - Only `custom_fields_values` can be updated after publish

- [ ] **3.3.2** Update `JobPosition.can_edit_field()` to block `custom_fields_config` after publish

---

## Phase 4: Financial Controls

### 4.1 Budget Validation

- [ ] **4.1.1** Add `JobPosition.validate_salary_within_budget()` method
  - If `budget_max` is set, ensure `salary_max ≤ budget_max`
  - Raise `JobPositionBudgetExceededError` if violated

- [ ] **4.1.2** Call validation in `RequestJobPositionApprovalCommand`

### 4.2 Capture Approved Budget

- [ ] **4.2.1** In `ApproveJobPositionCommand`:
  - Set `approved_budget_max = budget_max`
  - This becomes the ceiling for offers

### 4.3 Offer Gatekeeper (Future Phase)

- [ ] **4.3.1** (Future) In Offer module, before generating offer letter:
  - Compare `offer_amount` vs `approved_budget_max`
  - If exceeds, block and require exception approval

---

## Phase 5: API Endpoints

### 5.1 New Endpoints

- [ ] **5.1.1** Create `POST /api/company/positions/{id}/request-approval`
  - Calls `RequestJobPositionApprovalCommand`
  - Returns updated position

- [ ] **5.1.2** Create `POST /api/company/positions/{id}/approve`
  - Requires approver permission
  - Calls `ApproveJobPositionCommand`
  - Returns updated position

- [ ] **5.1.3** Create `POST /api/company/positions/{id}/reject`
  - Requires approver permission
  - Body: `{ "reason": "string" }`
  - Calls `RejectJobPositionCommand`
  - Returns updated position

- [ ] **5.1.4** Create `POST /api/company/positions/{id}/publish`
  - Calls `PublishJobPositionCommand`
  - Returns updated position

- [ ] **5.1.5** Create `POST /api/company/positions/{id}/hold`
  - Calls `HoldJobPositionCommand`
  - Returns updated position

- [ ] **5.1.6** Create `POST /api/company/positions/{id}/resume`
  - Calls `ResumeJobPositionCommand`
  - Returns updated position

- [ ] **5.1.7** Create `POST /api/company/positions/{id}/close`
  - Body: `{ "reason": "filled|cancelled|budget_cut|duplicate|other", "note": "optional" }`
  - Calls `CloseJobPositionCommand`
  - Returns updated position

- [ ] **5.1.8** Create `POST /api/company/positions/{id}/archive`
  - Calls `ArchiveJobPositionCommand`
  - Returns updated position

- [ ] **5.1.9** Create `POST /api/company/positions/{id}/clone`
  - Calls `CloneJobPositionCommand`
  - Returns new position in DRAFT

### 5.2 Update Existing Endpoints

- [ ] **5.2.1** Update `POST /api/company/positions` (create)
  - Accept all new fields
  - Accept `workflow_id` to copy custom fields from
  - Set `created_by_id` from auth context

- [ ] **5.2.2** Update `PUT /api/company/positions/{id}` (update)
  - Enforce field locking based on status
  - Return 400 with locked fields list if attempting to edit locked field

- [ ] **5.2.3** Update `GET /api/company/positions/{id}` (get)
  - Return all new fields

- [ ] **5.2.4** Update `GET /api/company/positions` (list)
  - Add filter by `status`
  - Add filter by `hiring_manager_id`
  - Add filter by `recruiter_id`

### 5.3 Public API Security

- [ ] **5.3.1** Update `GET /public/positions/{slug_or_id}`
  - NEVER return: `budget_max`, `approved_budget_max`, `financial_approver_id`, `stage_assignments`, `created_by_id`
  - Only return `salary_min/max` if `show_salary = true`
  - Only return custom fields where `candidate_visible = true`

- [ ] **5.3.2** Update `GET /public/positions` (list)
  - Same security rules as above
  - Only return positions with `status = PUBLISHED` and `visibility = PUBLIC`

### 5.4 Request/Response Schemas

- [ ] **5.4.1** Create `JobPositionCreateRequest` with all fields

- [ ] **5.4.2** Create `JobPositionUpdateRequest` with all fields

- [ ] **5.4.3** Create `JobPositionResponse` (internal, all fields)

- [ ] **5.4.4** Create `JobPositionPublicResponse` (candidate-facing, filtered fields)

- [ ] **5.4.5** Create `CloseJobPositionRequest` with reason and note

- [ ] **5.4.6** Create `RejectJobPositionRequest` with reason

---

## Phase 6: Screening Integration

### 6.1 Interview Template Scope

- [ ] **6.1.1** Add `scope` field to `InterviewTemplate` entity
  ```python
  scope: InterviewTemplateScopeEnum  # PIPELINE, APPLICATION, STANDALONE
  ```

- [ ] **6.1.2** Update `InterviewTemplateModel` with `scope` column

- [ ] **6.1.3** Create migration for `scope` field

- [ ] **6.1.4** Migrate existing SCREENING templates to `scope = APPLICATION`

### 6.2 Link Screening to Position

- [ ] **6.2.1** Position already has `screening_template_id` field (from Phase 1)

- [ ] **6.2.2** Update create/update commands to accept `screening_template_id`

- [ ] **6.2.3** Validate template exists and has `scope = APPLICATION`

### 6.3 Inline Screening Creation (Frontend-Heavy)

- [ ] **6.3.1** Create endpoint to create screening template inline
  - `POST /api/company/positions/{id}/screening-template`
  - Creates template with `scope = APPLICATION`
  - Default name = position title
  - Links to position automatically

---

## Phase 7: Quick/Controlled Mode

### 7.1 Company Setting

- [ ] **7.1.1** Add `job_approval_mode` to Company settings
  ```python
  job_approval_mode: Enum  # QUICK, CONTROLLED
  ```

- [ ] **7.1.2** Update Company model and migration

### 7.2 Conditional Approval Bypass

- [ ] **7.2.1** In `PublishJobPositionCommand`:
  - Check company's `job_approval_mode`
  - If QUICK: Allow direct DRAFT → PUBLISHED
  - If CONTROLLED: Require PENDING_APPROVAL step

---

## Phase 8: Testing

### 8.1 Unit Tests

- [ ] **8.1.1** Test status transitions (valid paths)
- [ ] **8.1.2** Test status transitions (invalid paths - should fail)
- [ ] **8.1.3** Test field locking per status
- [ ] **8.1.4** Test budget validation (salary ≤ budget)
- [ ] **8.1.5** Test custom fields snapshot on creation
- [ ] **8.1.6** Test custom fields freeze on publish

### 8.2 Integration Tests

- [ ] **8.2.1** Test full publishing flow: Draft → Approval → Published
- [ ] **8.2.2** Test quick mode: Draft → Published (skip approval)
- [ ] **8.2.3** Test rejection flow: Draft → Pending → Rejected → Draft
- [ ] **8.2.4** Test close with reason
- [ ] **8.2.5** Test clone position
- [ ] **8.2.6** Test screening template link

### 8.3 Security Tests

- [ ] **8.3.1** Test public API never returns budget fields
- [ ] **8.3.2** Test public API never returns internal custom fields
- [ ] **8.3.3** Test only approvers can approve
- [ ] **8.3.4** Test only owners can edit

### 8.4 Run All Tests

- [ ] **8.4.1** Run `make test`
- [ ] **8.4.2** Run `make mypy`
- [ ] **8.4.3** Run `make lint`

---

## Phase 9: Documentation & Cleanup

### 9.1 API Documentation

- [ ] **9.1.1** Update OpenAPI/Swagger docs for new endpoints
- [ ] **9.1.2** Add request/response examples

### 9.2 Code Cleanup

- [ ] **9.2.1** Remove deprecated fields/methods if any
- [ ] **9.2.2** Update enum exports in `__init__.py` files
- [ ] **9.2.3** Verify all imports are correct

---

## Summary

| Phase | Tasks | Priority |
|-------|-------|----------|
| Phase 1: Core Fields & Enums | 25 tasks | High |
| Phase 2: Publishing Flow | 12 tasks | High |
| Phase 3: Custom Fields Snapshot | 5 tasks | High |
| Phase 4: Financial Controls | 4 tasks | Medium |
| Phase 5: API Endpoints | 17 tasks | High |
| Phase 6: Screening Integration | 6 tasks | Medium |
| Phase 7: Quick/Controlled Mode | 3 tasks | Low |
| Phase 8: Testing | 14 tasks | High |
| Phase 9: Documentation | 4 tasks | Low |

**Total: ~90 tasks**

**Recommended Order:**
1. Phase 1 (Core Fields) - Foundation
2. Phase 2 (Publishing Flow) - State machine
3. Phase 5 (API Endpoints) - Expose functionality
4. Phase 3 (Custom Fields Snapshot) - Data integrity
5. Phase 8 (Testing) - Validation
6. Phase 4 (Financial Controls) - Enterprise feature
7. Phase 6 (Screening Integration) - UX enhancement
8. Phase 7 (Quick/Controlled Mode) - Company setting
9. Phase 9 (Documentation) - Final polish
