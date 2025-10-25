# Workflow System Implementation Tasks

**Last Updated**: 2025-01-25
**Related Documents**:
- WORKFLOW_SYSTEM_ARCHITECTURE.md
- WORKFLOW2.md

## Overview

This document tracks the implementation of the complete workflow system with role-based task management, email automation, and analytics.

---

## Phase 1: Basic Workflows ✅ COMPLETED

**Status**: All core workflow functionality is working

- ✅ CompanyWorkflow entity and CRUD operations
- ✅ WorkflowStage entity and CRUD operations
- ✅ Basic workflow UI (Create/Edit/List workflows)
- ✅ Stage ordering with up/down buttons
- ✅ Set default workflow per company
- ✅ Workflow status management (Active/Inactive/Archived)
- ✅ Stage type support (initial, intermediate, final, custom)
- ✅ Active Candidates and Active Open Positions counters on workflow cards

**Partially Complete**:
- ⚠️ `required_outcome` and `estimated_duration_days` exist in DB but not in UI

---

## Phase 2: Enhanced Stage Configuration

**Goal**: Expose existing fields and add new fields for roles, emails, deadlines, and costs

**Priority**: HIGH
**Estimated Effort**: 2-3 days

### Backend Tasks

#### 2.1 Database Schema Updates
- [ ] **Migration**: Add new fields to `workflow_stages` table
  ```sql
  ALTER TABLE workflow_stages ADD COLUMN default_roles JSONB;
  ALTER TABLE workflow_stages ADD COLUMN default_assigned_users JSONB;
  ALTER TABLE workflow_stages ADD COLUMN email_template_id VARCHAR(255);
  ALTER TABLE workflow_stages ADD COLUMN custom_email_text TEXT;
  ALTER TABLE workflow_stages ADD COLUMN deadline_days INTEGER;
  ALTER TABLE workflow_stages ADD COLUMN estimated_cost DECIMAL(10,2);
  ```
- [ ] Create and run migration: `make revision m="add_stage_configuration_fields"`

#### 2.2 Domain Layer Updates
- [ ] Update `WorkflowStage` entity with new properties:
  - `default_roles: List[str]`
  - `default_assigned_users: List[str]`
  - `email_template_id: Optional[str]`
  - `custom_email_text: Optional[str]`
  - `deadline_days: Optional[int]`
  - `estimated_cost: Optional[Decimal]`
- [ ] Update `WorkflowStage.create()` factory method
- [ ] Update `WorkflowStage.update()` method
- [ ] Add validation: `deadline_days` must be positive if provided
- [ ] Add validation: `estimated_cost` must be non-negative if provided

#### 2.3 Application Layer Updates
- [ ] Update `WorkflowStageDto` with new fields
- [ ] Update `WorkflowStageMapper.entity_to_dto()`
- [ ] Update `CreateStageCommand` with new fields
- [ ] Update `UpdateStageCommand` with new fields
- [ ] Update command handlers to process new fields

#### 2.4 Infrastructure Layer Updates
- [ ] Update `WorkflowStageModel` with new columns
- [ ] Update `WorkflowStageRepository._to_domain()` mapper
- [ ] Update `WorkflowStageRepository._to_model()` mapper

#### 2.5 Presentation Layer Updates
- [ ] Update `CreateStageRequest` schema with new fields
- [ ] Update `UpdateStageRequest` schema with new fields
- [ ] Update `WorkflowStageResponse` schema with new fields
- [ ] Update controller to handle new fields

### Frontend Tasks

#### 2.6 Update Stage Forms
- [ ] **File**: `EditWorkflowPage.tsx` - Update `StageFormData` interface
- [ ] **File**: `EditWorkflowPage.tsx` - Add form fields:
  - Required Outcome dropdown (use existing enum)
  - Estimated Duration (days) - number input
  - Deadline (days) - number input
  - Estimated Cost - currency input with $ symbol
  - Default Roles - tag input or multi-select
  - Email Template - dropdown (nullable, fetch from API)
  - Custom Email Text - textarea (conditional, only if template selected)
- [ ] **File**: `CreateWorkflowPage.tsx` - Same updates as EditWorkflowPage
- [ ] Add field validations
- [ ] Update API service calls to include new fields
- [ ] Add tooltips/help text for each new field

#### 2.7 Update Workflow Display
- [ ] **File**: `WorkflowsSettingsPage.tsx` - Show stage count, total estimated cost
- [ ] Create new component: `WorkflowStageDetailCard` showing all stage info
- [ ] Add estimated timeline calculation (sum of estimated_duration_days)
- [ ] Add total cost calculation (sum of estimated_cost)

### Testing

#### 2.8 Backend Tests
- [ ] Unit test: `WorkflowStage.create()` with new fields
- [ ] Unit test: `WorkflowStage.update()` validation
- [ ] Unit test: Field validation (negative costs, etc.)
- [ ] Integration test: Create stage with all fields via API
- [ ] Integration test: Update stage fields via API

#### 2.9 Frontend Tests
- [ ] Test stage form with new fields
- [ ] Test form validation
- [ ] Test API integration

---

## Phase 3: Position-Workflow Integration

**Goal**: Connect workflows to job positions and implement user assignments to stages

**Priority**: HIGH
**Estimated Effort**: 4-5 days

### Backend Tasks

#### 3.1 Update Position Entity
- [ ] Add `workflow_id` field to `Position` entity (optional)
- [ ] Add `workflow_id` column to `job_positions` table (FK to company_workflows)
- [ ] Add validation: workflow must belong to same company as position
- [ ] Add business logic: use company's `default_workflow_id` if position workflow not specified
- [ ] Update `CreatePositionCommand` to accept `workflow_id`
- [ ] Update `UpdatePositionCommand` to allow changing workflow
- [ ] Create migration

#### 3.2 Create PositionStageAssignment Module

**File Structure**:
```
src/position_stage_assignment/
├── domain/
│   ├── entities/
│   │   └── position_stage_assignment.py
│   ├── value_objects/
│   │   └── position_stage_assignment_id.py
│   └── infrastructure/
│       └── position_stage_assignment_repository_interface.py
├── application/
│   ├── commands/
│   │   ├── assign_users_to_stage_command.py
│   │   ├── remove_user_from_stage_command.py
│   │   └── copy_workflow_assignments_command.py
│   ├── queries/
│   │   ├── list_stage_assignments_query.py
│   │   └── get_assigned_users_query.py
│   └── dtos/
│       └── position_stage_assignment_dto.py
├── infrastructure/
│   ├── models/
│   │   └── position_stage_assignment_model.py
│   └── repositories/
│       └── position_stage_assignment_repository.py
└── presentation/
    ├── controllers/
    │   └── position_stage_assignment_controller.py
    ├── schemas/
    │   ├── assign_users_request.py
    │   └── position_stage_assignment_response.py
    └── mappers/
        └── position_stage_assignment_mapper.py
```

**Tasks**:
- [ ] Create domain entity `PositionStageAssignment`
  ```python
  class PositionStageAssignment:
      id: PositionStageAssignmentId
      position_id: PositionId
      stage_id: WorkflowStageId
      assigned_user_ids: List[CompanyUserId]
      created_at: datetime
      updated_at: datetime
  ```
- [ ] Create value object `PositionStageAssignmentId`
- [ ] Create repository interface
- [ ] Create repository implementation
- [ ] Create commands:
  - `AssignUsersToStageCommand` - bulk assign users to a stage
  - `RemoveUserFromStageCommand` - remove single user
  - `CopyWorkflowAssignmentsCommand` - copy default assignments from workflow
- [ ] Create queries:
  - `ListStageAssignmentsQuery` - get all assignments for a position
  - `GetAssignedUsersQuery` - get users assigned to specific stage
- [ ] Create command/query handlers
- [ ] Create DTOs and mappers
- [ ] Create controller with methods:
  - `assign_users_to_stage()`
  - `remove_user_from_stage()`
  - `list_assignments()`
  - `copy_workflow_defaults()`
- [ ] Create router with endpoints
- [ ] Add to dependency injection container
- [ ] Create database table migration:
  ```sql
  CREATE TABLE position_stage_assignments (
      id VARCHAR(255) PRIMARY KEY,
      position_id VARCHAR(255) NOT NULL REFERENCES job_positions(id),
      stage_id VARCHAR(255) NOT NULL REFERENCES workflow_stages(id),
      assigned_user_ids JSONB NOT NULL DEFAULT '[]',
      created_at TIMESTAMP NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
      UNIQUE(position_id, stage_id)
  );
  CREATE INDEX idx_position_stage_assignments_position ON position_stage_assignments(position_id);
  CREATE INDEX idx_position_stage_assignments_stage ON position_stage_assignments(stage_id);
  ```

#### 3.3 Auto-Assignment on Position Creation
- [ ] Update `CreatePositionCommandHandler`
- [ ] After position created, if workflow specified:
  - Fetch workflow stages
  - For each stage with `default_assigned_users`, create PositionStageAssignment
- [ ] Add domain event: `PositionCreatedEvent`
- [ ] Create event handler: `CreateDefaultStageAssignmentsHandler`

### Frontend Tasks

#### 3.4 Position Form Updates
- [ ] **File**: Create `components/company/WorkflowSelector.tsx`
  - Dropdown to select workflow
  - Display workflow stages preview
  - Show stage count and estimated timeline
- [ ] **File**: Update `CreatePositionPage.tsx`
  - Add workflow selection step after basic info
  - Add stage assignment step after workflow selection
- [ ] **File**: Create `components/company/StageAssignmentEditor.tsx`
  - For each stage in workflow, show multi-select of company users
  - Pre-populate with `default_assigned_users` from workflow
  - Allow adding/removing users
  - Show role suggestions based on `default_roles`

#### 3.5 Position Management UI
- [ ] **File**: Update `PositionDetailPage.tsx`
  - Display assigned workflow name
  - Display workflow stages with assigned users
  - Add "Edit Stage Assignments" button
- [ ] **File**: Create `EditStageAssignmentsModal.tsx`
  - Modal showing all stages
  - Multi-select for users per stage
  - Save/Cancel actions
  - API integration

#### 3.6 API Service
- [ ] **File**: Create `services/positionStageAssignmentService.ts`
  ```typescript
  export const positionStageAssignmentService = {
    listAssignments: (positionId: string) => Promise<Assignment[]>,
    assignUsers: (positionId: string, stageId: string, userIds: string[]) => Promise<void>,
    removeUser: (positionId: string, stageId: string, userId: string) => Promise<void>,
    copyWorkflowDefaults: (positionId: string) => Promise<void>
  }
  ```

### Testing

#### 3.7 Backend Tests
- [ ] Unit test: PositionStageAssignment entity
- [ ] Unit test: Assignment commands
- [ ] Integration test: Create position with workflow
- [ ] Integration test: Auto-create assignments from defaults
- [ ] Integration test: Assign/remove users via API
- [ ] Integration test: Validate same company constraint

#### 3.8 Frontend Tests
- [ ] Test workflow selector component
- [ ] Test stage assignment editor
- [ ] Test position creation with workflow
- [ ] Test editing stage assignments

---

## Phase 4: Application Processing with Permissions

**Goal**: Implement permission checks and deadline tracking for applications

**Priority**: MEDIUM
**Estimated Effort**: 3-4 days

### Backend Tasks

#### 4.1 Update CompanyApplication/CandidateApplication Entity
- [ ] Add `stage_entered_at: datetime` field
- [ ] Add `stage_deadline: Optional[datetime]` field (computed)
- [ ] Add method: `calculate_stage_deadline()` - fetches stage's deadline_days and adds to stage_entered_at
- [ ] Add method: `move_to_stage(new_stage, current_user)` - validates permission, updates stage, recalculates deadline
- [ ] Update `ChangeStageCommand` to update these fields
- [ ] Create migration

#### 4.2 Permission Service
- [ ] Create service: `StagePermissionService`
  ```python
  class StagePermissionService:
      def can_user_process_stage(self, user_id: str, application_id: str) -> bool
      def get_assigned_users_for_stage(self, position_id: str, stage_id: str) -> List[str]
      def is_user_company_admin(self, user_id: str, company_id: str) -> bool
  ```
- [ ] Permission logic:
  - Company admins can always process
  - User must be in assigned_user_ids for current stage
- [ ] Integrate into `ChangeStageCommandHandler`
- [ ] Return 403 if permission denied

#### 4.3 Domain Events
- [ ] Create event: `ApplicationStageChangedEvent`
  ```python
  class ApplicationStageChangedEvent:
      application_id: str
      previous_stage_id: str
      new_stage_id: str
      changed_by_user_id: str
      changed_at: datetime
  ```
- [ ] Emit event from `ChangeStageCommandHandler`
- [ ] Create event handler stub for future email notifications

### Frontend Tasks

#### 4.4 Workflow Board/Kanban Updates
- [ ] **File**: Update `WorkflowBoardPage.tsx`
- [ ] Before rendering "Move" button, call permission check API
- [ ] Disable button if user not authorized
- [ ] Show tooltip: "You are not assigned to this stage" when disabled
- [ ] Handle 403 responses with user-friendly error message
- [ ] Add visual indicator showing who is assigned to current stage

#### 4.5 Application Detail View
- [ ] **File**: Update `CandidateDetailPage.tsx` or `ApplicationDetailPage.tsx`
- [ ] Display current stage deadline
- [ ] Add deadline indicator:
  - Red badge: Overdue
  - Orange badge: Due today
  - Yellow badge: Due in 1-2 days
  - Gray badge: Due in 3+ days
- [ ] Display list of assigned users for current stage
- [ ] Add stage history timeline with timestamps

#### 4.6 Permission Check API
- [ ] **File**: Update `companyApplicationService.ts`
  ```typescript
  canUserProcessStage: (applicationId: string) => Promise<boolean>
  getAssignedUsers: (applicationId: string, stageId: string) => Promise<User[]>
  ```

### Testing

#### 4.7 Backend Tests
- [ ] Unit test: Permission service logic
- [ ] Unit test: Deadline calculation
- [ ] Integration test: Change stage with permission
- [ ] Integration test: Change stage without permission (expect 403)
- [ ] Integration test: Admin can always process

#### 4.8 Frontend Tests
- [ ] Test permission check integration
- [ ] Test disabled button states
- [ ] Test deadline indicators
- [ ] Test error handling

---

## Phase 5: Task Management System

**Goal**: Create task dashboard for users to see their assigned work

**Priority**: MEDIUM
**Estimated Effort**: 5-6 days

### Backend Tasks

#### 5.1 CompanyUser Roles System
- [ ] Add `roles: List[str]` field to `CompanyUser` entity (stored as JSONB)
- [ ] Common role values:
  - "HR Manager"
  - "Tech Lead"
  - "Recruiter"
  - "Hiring Manager"
  - "Interviewer"
  - "Department Head"
- [ ] Create command: `AssignRolesToUserCommand`
- [ ] Create query: `GetUserRolesQuery`
- [ ] Update user management UI to assign roles
- [ ] Create migration

#### 5.2 Task Priority System
- [ ] Add method to `CandidateApplication`: `calculate_priority()` returning int
  ```python
  def calculate_priority(self) -> int:
      base = 100
      deadline_weight = self._calculate_deadline_weight()
      position_weight = self.position.priority * 10
      candidate_weight = self.candidate.priority * 5
      return base + deadline_weight + position_weight + candidate_weight
  ```
- [ ] Add `task_status` field to `CandidateApplication`:
  - Values: `pending`, `in_progress`, `completed`, `blocked`
- [ ] Create commands:
  - `ClaimTaskCommand` - user claims an application
  - `UnclaimTaskCommand` - user releases an application
  - `UpdateTaskStatusCommand` - update task status
- [ ] Create migration

#### 5.3 Task Queries
- [ ] Create query: `GetMyAssignedTasksQuery`
  - Returns applications where user is in assigned_user_ids for current stage
  - Sorted by priority desc, stage_entered_at asc
- [ ] Create query: `GetAvailableTasksQuery`
  - Returns applications where:
    - Current stage's default_roles contains any of user's roles
    - User is not in assigned_user_ids (unassigned)
  - Sorted by priority desc
- [ ] Create query: `GetAllMyTasksQuery`
  - Combines both assigned and available
  - Sorted by assigned first, then priority
- [ ] Add filters:
  - By stage
  - By priority range
  - By deadline (overdue, due today, due this week)
  - By position

#### 5.4 Task API Endpoints
- [ ] Create router: `/api/company-users/{user_id}/tasks`
  - `GET /assigned` - directly assigned tasks
  - `GET /available` - role-based available tasks
  - `GET /all` - combined view
- [ ] Create endpoints for task actions:
  - `POST /api/applications/{app_id}/claim`
  - `POST /api/applications/{app_id}/unclaim`
  - `PUT /api/applications/{app_id}/task-status`

### Frontend Tasks

#### 5.5 User Task Dashboard
- [ ] **File**: Create `pages/company/MyTasksPage.tsx`
  - Header with filters and search
  - Two sections:
    1. "My Assigned Tasks" (directly assigned)
    2. "Available Tasks" (role-based, can claim)
  - Each task card shows:
    - Candidate name and photo
    - Position title
    - Current stage name
    - Priority indicator (color-coded badge)
    - Deadline with urgency indicator
    - Quick actions: View, Claim (if available), Move to Next Stage
  - Pagination
- [ ] **File**: Create `components/company/TaskCard.tsx`
  - Reusable task card component
  - Shows all task info
  - Quick action buttons
- [ ] **File**: Create `components/company/TaskFilters.tsx`
  - Filter by stage
  - Filter by priority
  - Filter by deadline
  - Filter by position
- [ ] **File**: Create `components/company/PriorityBadge.tsx`
  - Color-coded priority indicator
  - Red: 175+ (high priority)
  - Orange: 150-174 (medium-high)
  - Yellow: 125-149 (medium)
  - Gray: <125 (normal)

#### 5.6 Navigation Updates
- [ ] Add "My Tasks" link to company navigation
- [ ] Add badge showing count of assigned tasks
- [ ] Update on real-time when new tasks assigned

#### 5.7 API Service
- [ ] **File**: Create `services/taskService.ts`
  ```typescript
  export const taskService = {
    getAssignedTasks: (userId: string, filters?: TaskFilters) => Promise<Task[]>,
    getAvailableTasks: (userId: string, filters?: TaskFilters) => Promise<Task[]>,
    getAllTasks: (userId: string, filters?: TaskFilters) => Promise<Task[]>,
    claimTask: (applicationId: string) => Promise<void>,
    unclaimTask: (applicationId: string) => Promise<void>,
    updateTaskStatus: (applicationId: string, status: TaskStatus) => Promise<void>
  }
  ```

### Testing

#### 5.8 Backend Tests
- [ ] Unit test: Priority calculation
- [ ] Unit test: Task queries with different user roles
- [ ] Integration test: Get assigned tasks API
- [ ] Integration test: Claim/unclaim task
- [ ] Integration test: Filter tasks by various criteria

#### 5.9 Frontend Tests
- [ ] Test task dashboard rendering
- [ ] Test task filters
- [ ] Test claim/unclaim actions
- [ ] Test priority sorting

---

## Phase 6: Email Integration

**Goal**: Auto-send emails when candidates move to stages with configured templates

**Priority**: LOW
**Estimated Effort**: 4-5 days

### Backend Tasks

#### 6.1 Email Template System (if not exists)
- [ ] Create `EmailTemplate` entity
  ```python
  class EmailTemplate:
      id: EmailTemplateId
      company_id: CompanyId
      name: str
      subject: str
      body: str  # HTML with placeholders
      variables: List[str]  # Available placeholders
      created_at: datetime
      updated_at: datetime
  ```
- [ ] Create full CQRS module for email templates
- [ ] Create migration
- [ ] Seed default templates:
  - "Stage Transition" - generic
  - "Interview Invitation"
  - "Offer Letter"
  - "Rejection Notice"

#### 6.2 Template Rendering Service
- [ ] Create service: `EmailTemplateService`
  ```python
  class EmailTemplateService:
      def render_template(
          self,
          template_id: str,
          custom_text: Optional[str],
          variables: Dict[str, Any]
      ) -> str
  ```
- [ ] Support variables:
  - `{{candidate_name}}`
  - `{{candidate_first_name}}`
  - `{{position_title}}`
  - `{{company_name}}`
  - `{{stage_name}}`
  - `{{custom_text}}` (if provided)

#### 6.3 Email on Stage Change
- [ ] Create event handler: `SendStageTransitionEmailHandler`
- [ ] Listens to: `ApplicationStageChangedEvent`
- [ ] Logic:
  1. Fetch new stage details
  2. If stage has `email_template_id`:
     - Render template with variables
     - Append `custom_email_text` if exists
     - Send email to candidate
     - Log email sent in application history
- [ ] Integrate with existing email service (Mailpit for dev)

### Frontend Tasks

#### 6.4 Email Template Management
- [ ] **File**: Create `pages/company/EmailTemplatesPage.tsx`
- [ ] CRUD operations for templates
- [ ] Template editor with:
  - Rich text editor
  - Variable helper buttons (insert placeholders)
  - Subject line editor
- [ ] **File**: Create `components/company/TemplateEditor.tsx`
  - WYSIWYG editor
  - Variable palette
  - Preview functionality
  - Test send button

#### 6.5 Workflow Stage Email Configuration
- [ ] **File**: Update `EditWorkflowPage.tsx` and `CreateWorkflowPage.tsx`
- [ ] In stage form, add:
  - Email Template dropdown (fetch from API)
  - Preview button to see template
  - Custom Email Text textarea
  - Preview of final email with custom text merged

### Testing

#### 6.6 Backend Tests
- [ ] Unit test: Template rendering with variables
- [ ] Unit test: Custom text appending
- [ ] Integration test: Send email on stage change
- [ ] Integration test: No email if template not configured

#### 6.7 Frontend Tests
- [ ] Test template CRUD
- [ ] Test template editor
- [ ] Test preview functionality

---

## Phase 7: Analytics & Reporting

**Goal**: Provide insights into workflow performance

**Priority**: LOW
**Estimated Effort**: 5-6 days

### Backend Tasks

#### 7.1 Analytics Queries
- [ ] Create query: `GetWorkflowAnalyticsQuery`
  - Returns:
    - Average time in each stage
    - Conversion rate per stage
    - Total applications
    - Active applications
    - Completed applications
    - Rejected applications
- [ ] Create query: `GetStageBottlenecksQuery`
  - Returns stages taking longest on average
- [ ] Create query: `GetCostPerHireQuery`
  - Sums `estimated_cost` of all stages for hired candidates
  - Groups by position or workflow

#### 7.2 Analytics API
- [ ] Create controller: `WorkflowAnalyticsController`
- [ ] Endpoints:
  - `GET /api/workflows/{id}/analytics`
  - `GET /api/workflows/{id}/bottlenecks`
  - `GET /api/workflows/{id}/cost-analysis`

### Frontend Tasks

#### 7.3 Analytics Dashboard
- [ ] **File**: Create `pages/company/WorkflowAnalyticsPage.tsx`
- [ ] Sections:
  1. Workflow performance metrics (cards)
  2. Stage conversion funnel (chart)
  3. Time-in-stage breakdown (bar chart)
  4. Cost per hire (line chart over time)
  5. Bottleneck detection (table)
- [ ] Add date range picker
- [ ] Add export to CSV/PDF button
- [ ] Use charting library (recharts or Chart.js)

### Testing

#### 7.4 Backend Tests
- [ ] Integration test: Analytics queries with real data
- [ ] Test date range filtering
- [ ] Test performance with large datasets

#### 7.5 Frontend Tests
- [ ] Test analytics dashboard rendering
- [ ] Test chart interactions
- [ ] Test export functionality

---

## Implementation Priority Order

1. **Phase 2** (Enhanced Stage Configuration) - Quick win, exposes existing fields
2. **Phase 3** (Position-Workflow Integration) - Core functionality, enables workflow usage
3. **Phase 4** (Application Processing with Permissions) - Critical for security
4. **Phase 5** (Task Management System) - High value for users
5. **Phase 6** (Email Integration) - Automation, nice-to-have
6. **Phase 7** (Analytics & Reporting) - Business intelligence, can wait

---

## Technical Debt & Considerations

### Database Performance
- [ ] Add indexes on frequently queried columns:
  - `candidate_applications.current_stage_id`
  - `candidate_applications.stage_entered_at`
  - `position_stage_assignments.position_id`
  - `position_stage_assignments.stage_id`
- [ ] Consider materialized view for task queries if performance degrades

### Caching Strategy
- [ ] Cache workflow + stages for position (changes infrequently)
- [ ] Cache user permissions for stage (invalidate on assignment change)
- [ ] Cache role-to-stage mappings

### API Rate Limiting
- [ ] Implement rate limiting on task queries (users might refresh frequently)
- [ ] Implement rate limiting on email sends (prevent spam)

### Audit Trail
- [ ] Log all stage transitions with user_id and timestamp
- [ ] Log all permission checks (for debugging)
- [ ] Log all email sends

### Error Handling
- [ ] Graceful degradation if email service down
- [ ] Clear error messages for permission denials
- [ ] Validate workflow integrity before allowing position creation

---

## Success Metrics

### Phase 2
- All workflow stages have complete configuration
- Average time to create workflow: < 5 minutes

### Phase 3
- All positions have assigned workflows
- Average time to assign users to stages: < 2 minutes

### Phase 4
- Zero unauthorized stage transitions
- 100% deadline visibility for applications

### Phase 5
- Average task assignment per user: 5-10
- Task dashboard load time: < 1 second
- Task claim rate: > 70%

### Phase 6
- Email delivery rate: > 95%
- Email open rate: > 40%
- Template usage rate: > 60% of stages

### Phase 7
- Dashboard load time: < 2 seconds
- Report generation time: < 5 seconds
- User engagement with analytics: > 30% weekly

---

## Notes

- All phases follow Clean Architecture and CQRS patterns
- All database changes require migrations
- All new features require tests (unit + integration)
- Frontend components should be reusable where possible
- API endpoints follow RESTful conventions
- Use TypeScript strict mode
- Follow existing naming conventions

---

**Document Version**: 1.0
**Status**: Ready for implementation
