# Job Posting & Publishing Flow - Frontend Implementation Tasks

**Reference Documents:**
- `jobposting.md` - PRD v2.1
- `jobposting_analysis.md` - Technical Analysis
- `jobposting_tasks.md` - Backend Tasks

---

## Phase 1: Types & Services

### 1.1 TypeScript Types

- [ ] **1.1.1** Create/update `JobPositionStatus` enum
  ```typescript
  enum JobPositionStatus {
    DRAFT = 'draft',
    PENDING_APPROVAL = 'pending_approval',
    CONTENT_REVIEW = 'content_review',
    PUBLISHED = 'published',
    ON_HOLD = 'on_hold',
    CLOSED = 'closed',
    ARCHIVED = 'archived'
  }
  ```

- [ ] **1.1.2** Create `ClosedReason` enum
  ```typescript
  enum ClosedReason {
    FILLED = 'filled',
    CANCELLED = 'cancelled',
    BUDGET_CUT = 'budget_cut',
    DUPLICATE = 'duplicate',
    OTHER = 'other'
  }
  ```

- [ ] **1.1.3** Create `EmploymentType` enum

- [ ] **1.1.4** Create `ExperienceLevel` enum

- [ ] **1.1.5** Create `WorkLocationType` enum

- [ ] **1.1.6** Create `SalaryPeriod` enum

- [ ] **1.1.7** Create `LanguageRequirement` interface
  ```typescript
  interface LanguageRequirement {
    language: string;
    level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2' | 'Native';
  }
  ```

- [ ] **1.1.8** Create `CustomFieldDefinition` interface
  ```typescript
  interface CustomFieldDefinition {
    field_key: string;
    label: string;
    field_type: 'TEXT' | 'NUMBER' | 'SELECT' | 'MULTISELECT' | 'DATE' | 'BOOLEAN' | 'URL';
    options?: string[];
    is_required: boolean;
    candidate_visible: boolean;
    validation_rules?: Record<string, any>;
    sort_order: number;
    is_active: boolean;
  }
  ```

- [ ] **1.1.9** Update `JobPosition` interface with all new fields
  ```typescript
  interface JobPosition {
    id: string;
    company_id: string;
    requisition_id?: string;

    // Publishing Flow
    status: JobPositionStatus;
    closed_reason?: ClosedReason;
    closed_at?: string;

    // Financial
    salary_currency?: string;
    salary_min?: number;
    salary_max?: number;
    salary_period?: SalaryPeriod;
    show_salary: boolean;
    budget_max?: number;
    approved_budget_max?: number;
    financial_approver_id?: string;
    approved_at?: string;

    // Content
    title: string;
    description_html?: string;
    skills: string[];
    languages?: LanguageRequirement[];

    // Standard Fields
    department_id?: string;
    employment_type?: EmploymentType;
    experience_level?: ExperienceLevel;
    work_location_type?: WorkLocationType;
    office_locations: string[];
    remote_restrictions?: string;
    number_of_openings: number;

    // Ownership
    hiring_manager_id?: string;
    recruiter_id?: string;
    created_by_id?: string;

    // Publishing
    visibility: 'hidden' | 'internal' | 'public';
    public_slug?: string;
    open_at?: string;
    application_deadline?: string;
    published_at?: string;

    // Pipeline
    candidate_pipeline_id?: string;
    phase_pipelines?: Record<string, string>;
    stage_assignments: Record<string, string[]>;

    // Custom Fields (Snapshot)
    custom_fields_config: CustomFieldDefinition[];
    custom_fields_values: Record<string, any>;
    source_workflow_id?: string;

    // Screening
    screening_template_id?: string;

    // Timestamps
    created_at: string;
    updated_at: string;
  }
  ```

### 1.2 API Service

- [ ] **1.2.1** Update `jobPositionService.ts` with new methods:

  ```typescript
  // Status transitions
  requestApproval(positionId: string): Promise<JobPosition>
  approve(positionId: string): Promise<JobPosition>
  reject(positionId: string, reason: string): Promise<JobPosition>
  publish(positionId: string): Promise<JobPosition>
  hold(positionId: string): Promise<JobPosition>
  resume(positionId: string): Promise<JobPosition>
  close(positionId: string, reason: ClosedReason, note?: string): Promise<JobPosition>
  archive(positionId: string): Promise<JobPosition>
  clone(positionId: string): Promise<JobPosition>
  ```

- [ ] **1.2.2** Update `create()` method to accept all new fields

- [ ] **1.2.3** Update `update()` method to accept all new fields

- [ ] **1.2.4** Add filter parameters to `list()` method
  - `status?: JobPositionStatus`
  - `hiring_manager_id?: string`
  - `recruiter_id?: string`

---

## Phase 2: Job Position List Page

### 2.1 Status Filters & Display

- [ ] **2.1.1** Add status filter dropdown to list page
  - All, Draft, Pending Approval, Content Review, Published, On Hold, Closed, Archived

- [ ] **2.1.2** Create `StatusBadge` component
  - Different colors per status
  - DRAFT: gray
  - PENDING_APPROVAL: yellow
  - CONTENT_REVIEW: blue
  - PUBLISHED: green
  - ON_HOLD: orange
  - CLOSED: red
  - ARCHIVED: gray (muted)

- [ ] **2.1.3** Add status column to positions table/grid

- [ ] **2.1.4** Add ownership filters
  - Filter by Hiring Manager
  - Filter by Recruiter

### 2.2 Quick Actions

- [ ] **2.2.1** Add context menu / action dropdown per position
  - Edit (if allowed)
  - View
  - Request Approval (if DRAFT)
  - Publish (if allowed)
  - Hold (if PUBLISHED)
  - Resume (if ON_HOLD)
  - Close (if PUBLISHED or ON_HOLD)
  - Archive (if CLOSED)
  - Clone

- [ ] **2.2.2** Create `ClosePositionModal` component
  - Reason dropdown (required)
  - Note textarea (optional for FILLED, required for OTHER)
  - Confirm button

- [ ] **2.2.3** Create `RejectPositionModal` component
  - Reason textarea (required)
  - Confirm button

### 2.3 Bulk Actions (Optional)

- [ ] **2.3.1** Add checkbox selection to list
- [ ] **2.3.2** Add bulk close action
- [ ] **2.3.3** Add bulk archive action

---

## Phase 3: Job Position Create/Edit Form

### 3.1 Form Structure

- [ ] **3.1.1** Create multi-step form or tabbed form:
  - Tab 1: Basic Info (title, description, department)
  - Tab 2: Job Details (employment type, experience, location, skills)
  - Tab 3: Compensation (salary, budget - if permission)
  - Tab 4: Pipeline & Screening
  - Tab 5: Custom Fields
  - Tab 6: Team Assignment

### 3.2 Basic Info Tab

- [ ] **3.2.1** Title input (required)

- [ ] **3.2.2** Rich text editor for description
  - Use existing rich text component or add one (TipTap, Quill, etc.)

- [ ] **3.2.3** Department dropdown
  - Fetch from company departments

- [ ] **3.2.4** Requisition ID input (optional, internal code)

### 3.3 Job Details Tab

- [ ] **3.3.1** Employment Type dropdown
  - Full-time, Part-time, Contract, Internship, Temporary, Freelance

- [ ] **3.3.2** Experience Level dropdown
  - Internship, Entry, Mid, Senior, Lead, Executive

- [ ] **3.3.3** Work Location section
  - Location Type: On-site, Hybrid, Remote
  - Office Locations: Multi-input for cities/addresses (show if On-site or Hybrid)
  - Remote Restrictions: Text input (show if Hybrid or Remote)

- [ ] **3.3.4** Skills/Tags input
  - Tag input component (comma-separated or chips)
  - Autocomplete from existing skills in company

- [ ] **3.3.5** Languages section
  - Add/remove language requirements
  - Language dropdown + Level dropdown per row

- [ ] **3.3.6** Number of Openings input (default 1)

- [ ] **3.3.7** Application Deadline date picker

### 3.4 Compensation Tab

- [ ] **3.4.1** Salary section
  - Currency dropdown (USD, EUR, etc.)
  - Salary Min input
  - Salary Max input
  - Period dropdown (Yearly, Monthly, Hourly)
  - Show to Candidates checkbox

- [ ] **3.4.2** Budget section (only if user has finance permission)
  - Budget Max input (internal only)
  - Helper text: "This will never be shown to candidates"

- [ ] **3.4.3** Validation: salary_max ≤ budget_max
  - Show error if violated

### 3.5 Pipeline & Screening Tab

- [ ] **3.5.1** Candidate Pipeline dropdown
  - Fetch available pipelines
  - Show pipeline stages preview when selected

- [ ] **3.5.2** Screening Template section
  - Option 1: Select existing template (scope=APPLICATION)
  - Option 2: Create inline (see 3.5.3)
  - Option 3: No screening

- [ ] **3.5.3** Inline Screening Creation
  - Expandable section (don't navigate away)
  - Default name = position title (editable)
  - Add questions inline
  - Save creates template with scope=APPLICATION
  - Transparent UX: user shouldn't feel they left the form

### 3.6 Custom Fields Tab

- [ ] **3.6.1** Display copied custom fields from workflow
  - Show field label, type, required status
  - Toggle to activate/deactivate per field
  - Read-only structure (can't change field definitions)

- [ ] **3.6.2** Custom field value inputs
  - Render appropriate input per field_type
  - TEXT: text input
  - NUMBER: number input
  - SELECT: dropdown
  - MULTISELECT: multi-select
  - DATE: date picker
  - BOOLEAN: checkbox
  - URL: URL input with validation

- [ ] **3.6.3** Add Position-Specific Field button
  - Modal to define new field (key, label, type, options, required, candidate_visible)
  - Add to custom_fields_config

### 3.7 Team Assignment Tab

- [ ] **3.7.1** Hiring Manager dropdown
  - Search/select company user

- [ ] **3.7.2** Recruiter dropdown
  - Search/select company user

- [ ] **3.7.3** Stage Assignments section (optional)
  - Show stages from selected pipeline
  - For each stage, assign users
  - User multi-select per stage

### 3.8 Form Actions & Field Locking

- [ ] **3.8.1** Implement field locking based on status
  - Disable fields that are locked in current status
  - Show lock icon on locked fields
  - Show tooltip explaining why locked

- [ ] **3.8.2** Save as Draft button (always available in DRAFT)

- [ ] **3.8.3** Request Approval button (if DRAFT and controlled mode)

- [ ] **3.8.4** Publish button
  - If Quick Mode: Show in DRAFT
  - If Controlled Mode: Show only after approval

- [ ] **3.8.5** Show status banner at top of form
  - Current status with color
  - Available actions

---

## Phase 4: Job Position Detail/View Page

### 4.1 Header Section

- [ ] **4.1.1** Title + Status badge

- [ ] **4.1.2** Action buttons based on status
  - Edit (if allowed)
  - Request Approval / Approve / Reject
  - Publish
  - Hold / Resume
  - Close
  - Clone

- [ ] **4.1.3** Meta info: Created by, Created at, Last updated

### 4.2 Info Sections

- [ ] **4.2.1** Basic Info card
  - Title, Description, Department, Requisition ID

- [ ] **4.2.2** Job Details card
  - Employment type, Experience level, Location, Skills, Languages

- [ ] **4.2.3** Compensation card (internal view)
  - Salary range, Budget (if permission)
  - Approved budget (if approved)
  - Approver name, Approved date

- [ ] **4.2.4** Pipeline card
  - Pipeline name, Stages preview
  - Screening template (if any)

- [ ] **4.2.5** Custom Fields card
  - List of active custom fields with values

- [ ] **4.2.6** Team card
  - Hiring Manager, Recruiter
  - Stage assignments summary

### 4.3 Activity/History Section (Optional)

- [ ] **4.3.1** Show status change history
  - Who changed, When, From status → To status

---

## Phase 5: Approval Flow UI

### 5.1 Pending Approval View

- [ ] **5.1.1** Create "Pending My Approval" section/page
  - List positions awaiting current user's approval
  - Show requester, requested date, budget info

- [ ] **5.1.2** Approval detail modal/page
  - Show all position details (read-only)
  - Highlight financial info (salary, budget)
  - Approve button
  - Reject button (opens reason modal)

### 5.2 Notifications

- [ ] **5.2.1** Show notification badge for pending approvals

- [ ] **5.2.2** Notification when position is approved/rejected

### 5.3 Content Review View

- [ ] **5.3.1** Content Review mode
  - Only description, skills, custom_fields_values editable
  - Salary/budget fields shown but disabled
  - "Finish Review & Publish" button

---

## Phase 6: Public Job Board Updates

### 6.1 Public Position Card

- [ ] **6.1.1** Update public position card to show:
  - Salary range (if show_salary = true)
  - Employment type badge
  - Location type badge
  - Experience level

- [ ] **6.1.2** Skills/tags display as chips

### 6.2 Public Position Detail Page

- [ ] **6.2.1** Update public detail page:
  - All candidate-visible fields
  - Custom fields (only candidate_visible = true)
  - Languages required
  - Never show: budget, internal fields, stage assignments

- [ ] **6.2.2** Apply button behavior
  - If has screening template: Show screening questions after apply
  - If no screening: Direct to application confirmation

---

## Phase 7: Dashboard Widgets

### 7.1 Position Stats Widget

- [ ] **7.1.1** Create widget showing:
  - Total positions by status
  - DRAFT: X
  - PENDING_APPROVAL: X
  - PUBLISHED: X
  - etc.

- [ ] **7.1.2** Click to filter list by status

### 7.2 My Pending Approvals Widget

- [ ] **7.2.1** Show count of positions pending user's approval
- [ ] **7.2.2** Quick link to approval queue

### 7.3 My Positions Widget

- [ ] **7.3.1** Show positions where user is:
  - Hiring Manager
  - Recruiter
  - Created By

---

## Phase 8: Components Library

### 8.1 Shared Components

- [ ] **8.1.1** `StatusBadge` - Position status with color

- [ ] **8.1.2** `EmploymentTypeBadge` - Employment type display

- [ ] **8.1.3** `LocationTypeBadge` - Work location with icon

- [ ] **8.1.4** `SalaryRange` - Formatted salary display

- [ ] **8.1.5** `SkillsChips` - Skills as chips/tags

- [ ] **8.1.6** `LanguagesList` - Languages with levels

- [ ] **8.1.7** `CustomFieldInput` - Dynamic input based on field_type

- [ ] **8.1.8** `UserSelect` - Company user search/select

- [ ] **8.1.9** `PipelinePreview` - Visual stages preview

- [ ] **8.1.10** `LockedFieldIndicator` - Lock icon with tooltip

### 8.2 Form Components

- [ ] **8.2.1** `RichTextEditor` - For description (if not exists)

- [ ] **8.2.2** `TagInput` - For skills

- [ ] **8.2.3** `LanguageRequirementInput` - Language + level row

- [ ] **8.2.4** `MultiLocationInput` - Multiple office locations

---

## Phase 9: Translations (i18n)

### 9.1 English Translations

- [ ] **9.1.1** Add translations for all new status values
- [ ] **9.1.2** Add translations for closed reasons
- [ ] **9.1.3** Add translations for employment types
- [ ] **9.1.4** Add translations for experience levels
- [ ] **9.1.5** Add translations for form labels
- [ ] **9.1.6** Add translations for action buttons
- [ ] **9.1.7** Add translations for error messages
- [ ] **9.1.8** Add translations for validation messages

### 9.2 Spanish Translations

- [ ] **9.2.1** Translate all new keys to Spanish

---

## Phase 10: Testing

### 10.1 Component Tests

- [ ] **10.1.1** Test StatusBadge renders correctly for each status
- [ ] **10.1.2** Test form field locking based on status
- [ ] **10.1.3** Test CustomFieldInput renders correct input type
- [ ] **10.1.4** Test salary validation (max ≤ budget)

### 10.2 Integration Tests

- [ ] **10.2.1** Test create position flow
- [ ] **10.2.2** Test edit position with locked fields
- [ ] **10.2.3** Test approval flow
- [ ] **10.2.4** Test publish flow
- [ ] **10.2.5** Test close flow with reason

### 10.3 E2E Tests (Optional)

- [ ] **10.3.1** Full publishing flow: Create → Approve → Publish
- [ ] **10.3.2** Quick mode: Create → Publish directly

---

## Summary

| Phase | Focus | Tasks |
|-------|-------|-------|
| Phase 1 | Types & Services | 13 |
| Phase 2 | List Page | 9 |
| Phase 3 | Create/Edit Form | 28 |
| Phase 4 | Detail/View Page | 9 |
| Phase 5 | Approval Flow UI | 6 |
| Phase 6 | Public Job Board | 4 |
| Phase 7 | Dashboard Widgets | 5 |
| Phase 8 | Components Library | 14 |
| Phase 9 | Translations | 10 |
| Phase 10 | Testing | 10 |

**Total: ~108 frontend tasks**

**Recommended Order:**
1. Phase 1 (Types & Services) - Foundation
2. Phase 8 (Components Library) - Reusable components
3. Phase 3 (Create/Edit Form) - Main functionality
4. Phase 2 (List Page) - Display positions
5. Phase 4 (Detail/View Page) - View details
6. Phase 5 (Approval Flow) - Enterprise feature
7. Phase 6 (Public Job Board) - Candidate experience
8. Phase 9 (Translations) - i18n
9. Phase 7 (Dashboard Widgets) - Nice to have
10. Phase 10 (Testing) - Quality assurance

**Dependencies:**
- Backend Phase 1-2 must be complete before Frontend Phase 1
- Backend Phase 5 must be complete before Frontend Phase 3-5
