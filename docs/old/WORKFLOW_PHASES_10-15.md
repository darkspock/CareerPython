# Workflow System - Phases 10-15 Implementation Plan

**Version**: 1.0
**Date**: 2025-10-26
**Status**: Ready for Implementation

---

## Table of Contents

1. [Phase 10: Candidate Application System](#phase-10-candidate-application-system)
2. [Phase 11: Communication System](#phase-11-communication-system)
3. [Phase 12: Sourcing Flow](#phase-12-sourcing-flow)
4. [Phase 13: Advanced Task Features](#phase-13-advanced-task-features)
5. [Phase 14: Document Management](#phase-14-document-management)
6. [Phase 15: Advanced Analytics](#phase-15-advanced-analytics)

---

## Phase 10: Candidate Application System

**Goal**: Allow candidates to apply to positions from a public portal and track their application status.

**Priority**: 🔴 CRITICAL
**Estimated Time**: 3-4 days
**Dependencies**: Phase 3 (Position-Workflow Integration)

### Backend Tasks

#### 10.1 Database Schema

- [ ] Create migration `add_candidate_public_access.sql`
  - Add `is_public` boolean to `job_positions` table
  - Add `public_slug` string to `job_positions` table (for SEO-friendly URLs)
  - Add indexes for public queries
  - Time: 1 hour

#### 10.2 Domain Layer

- [ ] Update `JobPosition` entity
  - Add `is_public` property
  - Add `public_slug` property
  - Add `make_public()` method
  - Add `make_private()` method
  - Time: 2 hours

#### 10.3 Application Layer

- [ ] Create `SubmitApplicationCommand`
  - Properties: position_id, candidate_id, cover_letter, referral_source
  - Handler creates CompanyCandidate with workflow assignment
  - Time: 3 hours

- [ ] Create `ListPublicPositionsQuery`
  - Filter: is_public=True, status=Active
  - Return: PositionDto with company info
  - Time: 2 hours

- [ ] Create `GetPublicPositionQuery`
  - By public_slug
  - Return: Full position details
  - Time: 2 hours

- [ ] Create `GetCandidateApplicationsQuery`
  - By candidate_id
  - Return: List of applications with current stage
  - Time: 2 hours

#### 10.4 Presentation Layer

- [ ] Create REST endpoints
  - GET `/api/public/positions` - List public positions
  - GET `/api/public/positions/{slug}` - Get position details
  - POST `/api/public/positions/{slug}/apply` - Submit application
  - GET `/api/candidates/me/applications` - My applications
  - Time: 4 hours

### Frontend Tasks

#### 10.5 Public Pages

- [ ] Create `PublicPositionsPage.tsx`
  - List of open positions
  - Search and filters
  - Time: 4 hours

- [ ] Create `PublicPositionDetailPage.tsx`
  - Position details
  - Apply button
  - Application form modal
  - Time: 4 hours

- [ ] Create `CandidateApplicationsPage.tsx`
  - List of candidate's applications
  - Status tracking
  - Application history
  - Time: 4 hours

- [ ] Create `ApplicationForm` component
  - Cover letter textarea
  - File upload (CV)
  - Referral source
  - Time: 3 hours

#### 10.6 Company Admin

- [ ] Add "Make Public" toggle to Position form
  - Toggle in CreatePositionPage
  - Toggle in EditPositionPage
  - Auto-generate slug
  - Time: 2 hours

---

## Phase 11: Communication System

**Goal**: Bidirectional messaging between company and candidates.

**Priority**: 🔴 CRITICAL
**Estimated Time**: 3-4 days
**Dependencies**: Phase 10 (for candidate authentication)

### Backend Tasks

#### 11.1 Database Schema

- [ ] Create migration `create_candidate_messages.sql`
  - Table: `candidate_messages`
    - id (ULID)
    - application_id (FK to company_candidates)
    - sender_type (enum: company, candidate)
    - sender_id (user_id or candidate_id)
    - message_text
    - is_read
    - created_at
  - Time: 1 hour

#### 11.2 Domain Layer

- [ ] Create `CandidateMessage` entity
  - Properties: id, application_id, sender_type, sender_id, message_text, is_read
  - Factory: create()
  - Method: mark_as_read()
  - Time: 3 hours

- [ ] Create `SenderType` enum
  - Values: COMPANY, CANDIDATE
  - Time: 30 minutes

- [ ] Create value objects
  - `CandidateMessageId`
  - Time: 1 hour

- [ ] Create repository interface
  - Methods: save, get_by_id, list_by_application, count_unread
  - Time: 2 hours

#### 11.3 Infrastructure Layer

- [ ] Create `CandidateMessageModel`
  - SQLAlchemy model
  - Time: 2 hours

- [ ] Create `CandidateMessageRepository`
  - Implement interface
  - Time: 3 hours

#### 11.4 Application Layer

- [ ] Create commands
  - `SendMessageToCandidateCommand` (company → candidate, sends email)
  - `SendMessageToCompanyCommand` (candidate → company, no email)
  - `MarkMessageAsReadCommand`
  - Time: 4 hours

- [ ] Create queries
  - `GetConversationQuery` (all messages for application)
  - `GetUnreadCountQuery`
  - Time: 3 hours

- [ ] Create event handler
  - `MessageSentToCandidate` → Send email notification
  - Time: 2 hours

#### 11.5 Presentation Layer

- [ ] Create REST endpoints
  - POST `/api/applications/{id}/messages` - Send message
  - GET `/api/applications/{id}/messages` - Get conversation
  - POST `/api/applications/{id}/messages/{message_id}/read` - Mark as read
  - GET `/api/candidates/me/unread-count` - Unread count
  - Time: 4 hours

### Frontend Tasks

#### 11.6 Components

- [ ] Create `ConversationView` component
  - Message list with sender indication
  - Company messages styled differently
  - Time: 4 hours

- [ ] Create `MessageComposer` component
  - Textarea for message
  - Send button
  - Character count
  - Time: 3 hours

- [ ] Create `MessagesPage` component
  - Conversation view + composer
  - For both company and candidate
  - Time: 4 hours

- [ ] Add unread badge to navigation
  - Show count of unread messages
  - Time: 2 hours

---

## Phase 12: Phase System Architecture

**Goal**: Implement the Phase system that organizes workflows into higher-level phases with default configurations on company onboarding.

**Priority**: 🔴 CRITICAL
**Estimated Time**: 4-5 days
**Dependencies**: Phase 3 (Workflow System)

**Concept**:
Companies configure **Phases**, and each Phase contains one or more **Workflows**:
- Phase = High-level stage (Sourcing, Evaluation, Offer & Pre-Onboarding)
- Workflow = Belongs to a Phase, contains Stages
- candidate_application has: phase_id, workflow_id, stage_id

**Flow**:
1. Company onboarding → Auto-create 3 default Phases with default Workflows
2. Create Position → Select workflow per phase (auto-select if only 1 active)
3. Stage configuration → If stage type is SUCCESS or FAIL, optionally configure next_phase_id
4. When candidate reaches SUCCESS/FAIL stage with next_phase_id → Auto-move to configured Phase

### Backend Tasks

#### 12.1 Database Schema

- [ ] Create migration `create_phases_table.sql`
  - Table: `company_phases`
    - id (ULID, PK)
    - company_id (FK)
    - name (string) - "Sourcing", "Evaluation", etc.
    - sort_order (int) - Display order
    - default_view (enum: KANBAN, LIST)
    - objective (text) - Description for AI assistance
    - created_at, updated_at
  - Time: 1 hour

- [ ] Create migration `update_workflows_table.sql`
  - Add column `phase_id` (FK to company_phases) to `workflows` table
  - Change `WorkflowStatusEnum`: Remove old values, add DRAFT, ACTIVE, ARCHIVED
  - Time: 1 hour

- [ ] Create migration `update_candidate_applications_table.sql`
  - Add column `phase_id` (FK to company_phases) to `candidate_applications` table
  - Note: workflow_id and stage_id already exist
  - Time: 30 minutes

- [ ] Create migration `update_stage_type_enum.sql`
  - Remove: CUSTOM
  - Change: FINAL → SUCCESS
  - Add: FAIL
  - Time: 30 minutes

- [ ] Create migration `add_next_phase_to_stages.sql`
  - Add column `next_phase_id` (FK to company_phases, nullable) to `workflow_stages` table
  - This field is only used when stage_type is SUCCESS or FAIL
  - Time: 30 minutes

#### 12.2 Domain Layer

- [ ] Create `Phase` entity
  - Location: `src/phase/domain/entities/phase.py`
  - Properties: id, company_id, name, sort_order, default_view, objective
  - Factory: create()
  - Method: update_details()
  - Time: 3 hours

- [ ] Create `PhaseId` value object
  - Location: `src/phase/domain/value_objects/phase_id.py`
  - Time: 1 hour

- [ ] Create `DefaultView` enum
  - Location: `src/phase/domain/enums/default_view_enum.py`
  - Values: KANBAN, LIST
  - Time: 30 minutes

- [ ] Update `WorkflowStatusEnum`
  - Location: `src/workflow/domain/enums/workflow_status_enum.py`
  - New values: DRAFT, ACTIVE, ARCHIVED
  - Time: 30 minutes

- [ ] Update `StageTypeEnum`
  - Location: `src/workflow/domain/enums/stage_type_enum.py`
  - Remove CUSTOM, change FINAL to SUCCESS, add FAIL
  - Time: 30 minutes

- [ ] Update `WorkflowStage` entity
  - Add field: `next_phase_id: Optional[PhaseId]`
  - Validation: next_phase_id can only be set if stage_type is SUCCESS or FAIL
  - Update create() and update_details() methods
  - Time: 2 hours

- [ ] Update `Workflow` entity
  - Add field: `phase_id: PhaseId`
  - Update create() and update_details() to include phase_id
  - Time: 2 hours

- [ ] Update `CandidateApplication` entity
  - Add field: `phase_id: PhaseId`
  - Method: `move_to_next_phase(next_phase_id, workflow_id, stage_id)` - Auto transition
  - Time: 2 hours

- [ ] Create `PhaseModel` (SQLAlchemy)
  - Location: `src/phase/infrastructure/models/phase_model.py`
  - Time: 2 hours

- [ ] Create `PhaseRepository` interface and implementation
  - Location: `src/phase/domain/infrastructure/phase_repository_interface.py`
  - Location: `src/phase/infrastructure/repositories/phase_repository.py`
  - Time: 3 hours

#### 12.3 Application Layer

- [ ] Create `PhaseDto`
  - Location: `src/phase/application/queries/phase_dto.py`
  - Time: 1 hour

- [ ] Create `InitializeCompanyPhasesCommand`
  - Creates 3 default phases on company activation:
    1. **Sourcing** (sort_order: 1, default_view: LIST)
       - Default Workflow: "Sourcing Workflow" (status: ACTIVE) with stages:
         - Pending (STANDARD)
         - Screening (STANDARD)
         - Cualificado (SUCCESS, next_phase_id: Evaluation Phase)
         - No apto (FAIL)
         - On Hold (STANDARD)
    2. **Evaluation** (sort_order: 2, default_view: KANBAN)
       - Default Workflow: "Evaluation Workflow" (status: ACTIVE) with stages:
         - Entrevista RRHH (STANDARD)
         - Entrevista Manager (STANDARD)
         - Prueba (STANDARD)
         - Entrevista Directivo (STANDARD)
         - Seleccionado (SUCCESS, next_phase_id: Offer Phase)
         - Descartado (FAIL)
    3. **Offer & Pre-Onboarding** (sort_order: 3, default_view: KANBAN)
       - Default Workflow: "Offer Workflow" (status: ACTIVE) with stages:
         - Offer Proposal (STANDARD)
         - Negotiation (STANDARD)
         - Document Submission (STANDARD)
         - Document Verification (STANDARD)
         - Accepted (SUCCESS)
         - Lost (FAIL)
  - Time: 6 hours

- [ ] Create Phase commands
  - `CreatePhaseCommand` - Create custom phase
  - `UpdatePhaseCommand` - Update phase details
  - `DeletePhaseCommand` - Delete phase (if no workflows attached)
  - Time: 4 hours

- [ ] Create Phase queries
  - `ListPhasesQuery` - List all phases for company (ordered by sort_order)
  - `GetPhaseByIdQuery` - Get phase details
  - Time: 3 hours

- [ ] Update Workflow commands
  - Update `CreateWorkflowCommand` to require phase_id
  - Update `UpdateWorkflowCommand` to allow changing phase_id
  - Time: 2 hours

- [ ] Create event handler for stage transitions
  - Listen to `StageCompletedEvent` (when candidate moves to SUCCESS or FAIL stage)
  - If stage.next_phase_id is set → Auto-move candidate to next phase
  - Call candidate_application.move_to_next_phase(next_phase_id, initial_workflow_id, initial_stage_id)
  - Time: 3 hours

- [ ] Update Stage commands
  - Update `CreateStageCommand` to include optional next_phase_id
  - Update `UpdateStageCommand` to allow setting/changing next_phase_id
  - Validation: next_phase_id only valid if stage_type is SUCCESS or FAIL
  - Time: 2 hours

#### 12.4 Presentation Layer

- [ ] Create Phase endpoints
  - GET `/api/companies/{company_id}/phases` - List phases
  - GET `/api/phases/{phase_id}` - Get phase
  - POST `/api/companies/{company_id}/phases` - Create phase
  - PUT `/api/phases/{phase_id}` - Update phase
  - DELETE `/api/phases/{phase_id}` - Delete phase
  - POST `/api/companies/{company_id}/phases/initialize` - Initialize default phases
  - Time: 4 hours

- [ ] Update Workflow endpoints
  - Update POST `/api/workflows` to require phase_id
  - Update PUT `/api/workflows/{id}` to allow phase_id change
  - GET `/api/phases/{phase_id}/workflows` - List workflows in phase
  - Time: 2 hours

- [ ] Update Position endpoints
  - Update POST `/api/positions` to include workflow selection per phase
  - Response should include phase_workflow_config: {phase_id: workflow_id}
  - Time: 2 hours

### Frontend Tasks

#### 12.5 Types and Services

- [ ] Create Phase types
  - Location: `client-vite/src/types/phase.ts`
  - Interfaces: Phase, CreatePhaseRequest, UpdatePhaseRequest
  - Enum: DefaultView
  - Time: 1 hour

- [ ] Create Phase service
  - Location: `client-vite/src/services/phaseService.ts`
  - Methods: list, get, create, update, delete, initialize
  - Time: 2 hours

#### 12.6 Phase Management Pages

- [ ] Create `PhasesPage.tsx`
  - Location: `client-vite/src/pages/company/PhasesPage.tsx`
  - List all phases with sort_order, default_view
  - Drag to reorder phases
  - Button: "Add Phase"
  - Show workflows count per phase
  - Time: 4 hours

- [ ] Create `PhaseFormModal.tsx`
  - Form for create/edit phase
  - Fields: name, default_view (dropdown), objective (textarea)
  - Time: 3 hours

#### 12.7 Workflow and Stage Updates

- [ ] Update `CreateWorkflowPage.tsx`
  - Add dropdown to select Phase
  - Time: 2 hours

- [ ] Update `WorkflowListPage.tsx`
  - Group workflows by Phase
  - Show phase name and default_view
  - Time: 2 hours

- [ ] Update `StageForm.tsx` (or wherever stages are created/edited)
  - When stage_type is SUCCESS or FAIL, show dropdown "Next Phase" (optional)
  - Dropdown options: All available phases for the company
  - Label: "Auto-move to phase (optional)"
  - Time: 3 hours

#### 12.8 Position Configuration

- [ ] Update `CreatePositionPage.tsx` / `EditPositionPage.tsx`
  - Section: "Workflow Configuration"
  - For each phase, show dropdown to select workflow
  - If only 1 active workflow in phase → auto-select, show as read-only
  - If all phases have only 1 workflow → hide section, store config silently
  - Time: 4 hours

#### 12.9 Candidate Application Views

- [ ] Update `CandidateApplicationPage.tsx`
  - Show current Phase prominently
  - Show phase progress indicator (Phase 1 of 3)
  - Time: 2 hours

- [ ] Create phase-specific views
  - Use phase.default_view to render KANBAN or LIST
  - Sourcing Phase → LIST view by default
  - Evaluation/Offer Phases → KANBAN view by default
  - Time: 3 hours

---

## Summary of Phase 12 Changes

**Key Points:**
1. ✅ New entity: `Phase` (company_phases table)
2. ✅ Workflow belongs to Phase (phase_id FK)
3. ✅ Stage can have optional next_phase_id (only for SUCCESS/FAIL types)
4. ✅ When candidate reaches SUCCESS/FAIL stage with next_phase_id → auto-transition
5. ✅ 3 default phases created on company onboarding (NOT 4, removed Talent Pool)
6. ✅ StageTypeEnum updated: Remove CUSTOM, FINAL→SUCCESS, Add FAIL
7. ✅ WorkflowStatusEnum updated: DRAFT, ACTIVE, ARCHIVED
8. ✅ Phase configuration is customizable per stage (not automatic for all SUCCESS stages)

---

## Phase 13: Advanced Task Features

**Goal**: Enhance task management with better filters and bulk operations.

**Priority**: 🟡 IMPORTANT
**Estimated Time**: 2 days
**Dependencies**: Phase 6 (Task System)

### Backend Tasks

#### 13.1 Application Layer

- [ ] Enhance `GetMyTasksQuery`
  - Add filter parameters: deadline_range, priority_min, workflow_id, stage_id
  - Add sorting options
  - Time: 3 hours

- [ ] Create `BulkAssignTasksCommand`
  - Assign multiple applications to user
  - Time: 2 hours

- [ ] Create `BulkMoveStageCommand`
  - Move multiple candidates to next stage
  - Time: 3 hours

#### 13.2 Presentation Layer

- [ ] Update endpoints
  - Add query parameters to `/api/tasks/my-tasks`
  - POST `/api/tasks/bulk-assign` - Bulk assign
  - POST `/api/tasks/bulk-move` - Bulk move
  - Time: 3 hours

### Frontend Tasks

#### 13.3 Components

- [ ] Enhance `TaskDashboard`
  - Add filter panel (deadline, priority, workflow, stage)
  - Add bulk selection checkboxes
  - Add bulk action buttons
  - Time: 4 hours

- [ ] Create `TaskFilters` component
  - Filter UI
  - Time: 3 hours

---

## Phase 14: Document Management

**Goal**: Allow candidates to upload required documents and companies to verify them.

**Priority**: 🟢 OPTIONAL
**Estimated Time**: 3-4 days
**Dependencies**: Phase 10 (Candidate Application)

### Backend Tasks

#### 14.1 Database Schema

- [ ] Create migration `create_application_documents.sql`
  - Table: `application_documents`
    - id (ULID)
    - application_id (FK to company_candidates)
    - document_type (string: cv, id_card, diploma, etc.)
    - file_name
    - file_path
    - file_size
    - mime_type
    - status (enum: pending, approved, rejected)
    - uploaded_at
    - reviewed_at
    - reviewed_by
  - Time: 1 hour

- [ ] Create migration `add_required_documents_to_positions.sql`
  - Add `required_documents` JSON column to `job_positions`
  - Time: 30 minutes

#### 14.2 Domain Layer

- [ ] Create `ApplicationDocument` entity
  - Time: 3 hours

- [ ] Create `DocumentStatus` enum
  - Values: PENDING, APPROVED, REJECTED
  - Time: 30 minutes

#### 14.3 Application Layer

- [ ] Create commands
  - `UploadDocumentCommand`
  - `ApproveDocumentCommand`
  - `RejectDocumentCommand`
  - Time: 4 hours

- [ ] Create queries
  - `ListApplicationDocumentsQuery`
  - `GetDocumentQuery`
  - Time: 2 hours

#### 14.4 Infrastructure

- [ ] Implement file storage service
  - Local storage or S3
  - Time: 4 hours

#### 14.5 Presentation Layer

- [ ] Create REST endpoints
  - POST `/api/applications/{id}/documents` - Upload
  - GET `/api/applications/{id}/documents` - List
  - POST `/api/applications/{id}/documents/{doc_id}/approve` - Approve
  - POST `/api/applications/{id}/documents/{doc_id}/reject` - Reject
  - Time: 4 hours

### Frontend Tasks

#### 14.6 Components

- [ ] Create `DocumentUpload` component
  - Drag & drop file upload
  - Progress indicator
  - Time: 4 hours

- [ ] Create `DocumentList` component
  - List of uploaded documents
  - Status badges
  - Download/preview
  - Time: 4 hours

- [ ] Create `DocumentReview` component
  - For company users to approve/reject
  - Time: 3 hours

---

## Phase 15: Advanced Analytics

**Goal**: Enhanced analytics with real time tracking and cost analysis.

**Priority**: 🟢 OPTIONAL
**Estimated Time**: 3-4 days
**Dependencies**: Phase 9 (Basic Analytics)

### Backend Tasks

#### 15.1 Database Schema

- [ ] Create migration `add_stage_history_tracking.sql`
  - Table: `company_candidate_stage_history`
    - id (ULID)
    - application_id
    - stage_id
    - entered_at
    - exited_at
    - duration_hours (calculated)
  - Time: 1 hour

#### 15.2 Application Layer

- [ ] Create stage history tracking
  - Event handler for stage changes
  - Calculate time in stage
  - Time: 3 hours

- [ ] Enhance analytics queries
  - Add real time calculations (avg, median, min, max)
  - Add cost per hire calculation
  - Time: 4 hours

- [ ] Create export service
  - Export to CSV
  - Export to PDF (using ReportLab)
  - Time: 6 hours

#### 15.3 Presentation Layer

- [ ] Create export endpoints
  - GET `/api/analytics/{workflow_id}/export/csv`
  - GET `/api/analytics/{workflow_id}/export/pdf`
  - Time: 3 hours

### Frontend Tasks

#### 15.4 Enhanced UI

- [ ] Add time metrics to analytics page
  - Average time per stage (actual data)
  - Median time
  - Min/max time
  - Time: 3 hours

- [ ] Add cost analysis section
  - Cost per hire
  - ROI calculation
  - Time: 3 hours

- [ ] Add export buttons
  - Download CSV
  - Download PDF
  - Time: 2 hours

---

## Implementation Order

### Week 1: Critical Features
1. **Day 1-2**: Phase 10 Backend (Candidate Application System)
2. **Day 3-4**: Phase 10 Frontend (Public portal + Application tracking)
3. **Day 5**: Testing Phase 10

### Week 2: Communication
4. **Day 6-7**: Phase 11 Backend (Communication System)
5. **Day 8-9**: Phase 11 Frontend (Messages + Conversation UI)
6. **Day 10**: Testing Phase 11

### Week 3: Sourcing + Tasks
7. **Day 11-12**: Phase 12 Backend (Sourcing Flow)
8. **Day 13**: Phase 12 Frontend (Sourcing Kanban)
9. **Day 14-15**: Phase 13 (Advanced Task Features)

### Week 4: Optional Features
10. **Day 16-18**: Phase 14 (Document Management) - If needed
11. **Day 19-20**: Phase 15 (Advanced Analytics) - If needed
12. **Day 21**: Final testing and deployment

---

## Success Criteria

### Phase 10
- ✅ Candidates can view open positions
- ✅ Candidates can apply to positions
- ✅ Candidates can track their application status
- ✅ Applications automatically enter correct workflow

### Phase 11
- ✅ Company can send messages to candidates
- ✅ Candidates receive email notifications
- ✅ Candidates can reply in platform
- ✅ Conversation history is preserved

### Phase 12
- ✅ Fixed sourcing workflow with 5 stages
- ✅ Candidates can move through sourcing stages
- ✅ Accepted candidates move to talent pool
- ✅ Kanban board visualization

### Phase 13
- ✅ Advanced task filtering works
- ✅ Bulk operations complete successfully
- ✅ Performance improved

### Phase 14
- ✅ Candidates can upload documents
- ✅ Companies can review documents
- ✅ Document checklist tracks progress

### Phase 15
- ✅ Real time metrics calculated
- ✅ Cost per hire displayed
- ✅ Reports export successfully

---

## Notes

- All phases follow Clean Architecture principles
- All phases include proper error handling
- All phases include unit tests
- All phases include proper logging
- All phases follow CQRS pattern
