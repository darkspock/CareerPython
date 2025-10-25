# Workflow System Architecture

**Date**: 2025-01-22
**Version**: 2.0

## Overview

The CareerPython ATS implements a flexible workflow system that allows companies to manage candidates through customizable hiring stages with granular user permissions.

## Core Concepts

### 1. **CompanyWorkflow**
A template that defines the stages of a hiring process.

**Examples**:
- "Standard Hiring Process": Screening → HR Interview → Technical Interview → Final Interview → Offer → Hired
- "Technical Hiring": HR Screen → Technical Test → Tech Interview → Team Lead Interview → CTO Meeting → Offer → Hired
- "Quick Hiring": Interview → Offer → Hired

**Properties**:
- `id`: Unique identifier
- `company_id`: Owner company
- `name`: Workflow name
- `description`: What this workflow is for
- `is_default`: Is this the company's default workflow?
- `is_active`: Can be assigned to new positions?
- `workflow_type`: prospecting (Lead management) or selection (Hiring process)

### 2. **WorkflowStage**
Individual stage within a workflow.

**Properties**:
- `id`: Unique identifier
- `workflow_id`: Parent workflow
- `name`: Stage name (e.g., "HR Interview", "Technical Test")
- `description`: What happens in this stage
- `stage_type`: Type of stage (initial, intermediate, final, custom)
- `order`: Position in workflow (0, 1, 2, ...)
- `required_outcome`: What outcome is needed to proceed? (optional)
- `estimated_duration_days`: How long candidates typically stay here
- `is_active`: Can candidates be in this stage?
- **`default_roles`**: Array of role names that should be assigned to this stage (e.g., ["Tech Lead", "HR Manager"])
- **`default_assigned_users`**: Array of user IDs that are always assigned to this stage (optional)
- **`email_template_id`**: Default email template to use when candidate enters stage (optional)
- **`custom_email_text`**: Additional text to include in email template (optional)
- **`deadline_days`**: Number of days to complete this stage (optional, for task priority)
- **`estimated_cost`**: Estimated cost for completing this stage (optional, for ROI tracking)

### 3. **Position** (Job Posting)
A job opening with assigned workflow.

**Properties**:
- `id`: Unique identifier
- `company_id`: Owner company
- **`workflow_id`**: Which workflow to use for applications (NEW)
- `title`, `description`, `location`, etc.
- `status`: draft, active, paused, closed

**Key Behavior**:
- When creating a position, company selects a workflow
- All applications to this position follow that workflow
- Workflow can be changed anytime (affects new applications)

### 4. **PositionStageAssignment** (NEW)
Maps CompanyUsers to specific workflow stages for a position.

**Properties**:
- `id`: Unique identifier
- `position_id`: The job position
- `stage_id`: The workflow stage
- `assigned_user_ids`: List of CompanyUser IDs who can process this stage
- `created_at`, `updated_at`

**Example**:
```
Position: "Senior Python Developer"
Workflow: "Technical Hiring" (6 stages)

Assignments:
- Stage 1 (HR Screen)      → [Alice (HR Manager)]
- Stage 2 (Technical Test) → [Bob (Tech Lead), Carol (Senior Dev)]
- Stage 3 (Tech Interview) → [Bob (Tech Lead), Carol (Senior Dev)]
- Stage 4 (Team Lead)      → [Bob (Tech Lead)]
- Stage 5 (CTO Meeting)    → [David (CTO)]
- Stage 6 (Offer)          → [Alice (HR Manager), David (CTO)]
```

**Key Behavior**:
- Multiple users can be assigned to same stage (collaboration)
- Users can be changed anytime
- Only assigned users can move candidates to next stage
- Company admins can always see all stages (but can't move unless assigned)

### 5. **CompanyCandidate**
A person in the company's database (not yet applied to specific position).

**Properties**:
- `id`, `company_id`, `candidate_id` (nullable)
- Basic info: name, email, phone, country, linkedin
- `source`: how they entered system (manual_entry, direct_application, referral)
- `resume_url`: Path to uploaded CV (via storage service)
- `workflow_id`, `current_stage_id`: For lead prospecting (future Head Hunting feature)
- `status`: lead, contacted, in_process, etc.
- Tags, notes, priority

**Key Behavior**:
- Can exist without candidate_id (company added manually)
- Can have resume uploaded by company
- NOT tied to specific position (general candidate pool)

### 6. **CompanyApplication**
A formal application to a specific position.

**Properties**:
- `id`: Unique identifier
- `company_candidate_id`: Link to candidate in company's database
- `candidate_id`: The registered candidate (required)
- `company_id`: Owner company
- **`position_id`**: The job position (determines workflow)
- **`workflow_id`**: Copy of position's workflow at time of application
- **`current_stage_id`**: Where candidate is in the process
- `shared_data`: JSON with authorization of what candidate data to share
- `status`: active, offer_made, accepted, rejected, withdrawn
- `applied_at`, `tags`, `internal_notes`, `priority`
- **`stage_entered_at`**: When candidate entered current stage (for deadline tracking)
- **`stage_deadline`**: Calculated deadline for current stage (stage_entered_at + deadline_days)

**Key Behavior**:
- Created when candidate applies or company adds candidate to position
- Inherits workflow from position
- Current stage determines who can process
- Only data in `shared_data` is visible to company
- Candidate can withdraw anytime
- Company can move through stages (if assigned)
- When moving to new stage, `stage_entered_at` is updated and deadline is recalculated

### 7. **Task Management System**
A system for tracking user assignments and work items.

**Concepts**:
- **Task**: A candidate application in a stage that requires action from a user
- **Task Priority**: Calculated based on multiple factors
- **Task Assignment**: Can be direct (specific user) or indirect (any user with matching role)

**Priority Calculation**:
```
Priority Score = Base Priority + Deadline Weight + Position Weight + Candidate Weight

Where:
- Base Priority = 100
- Deadline Weight =
  * Overdue (past deadline): +50
  * Due today: +30
  * Due in 1-2 days: +20
  * Due in 3-5 days: +10
  * Due in 6+ days: 0
- Position Weight = position.priority * 10 (0-50)
- Candidate Weight = candidate.priority * 5 (0-25)

Maximum Priority = 225
```

**Task States**:
- `pending`: Waiting for user action
- `in_progress`: User has started working on it
- `completed`: Moved to next stage or final outcome
- `blocked`: Cannot proceed (missing info, etc.)

**User Task Dashboard**:
Users see tasks in this order:
1. **Directly Assigned**: Applications where user is specifically assigned to current stage
2. **Role-Based**: Applications in stages matching user's roles, not yet assigned to specific person
3. Sorted by: Priority (desc), then Stage Entered Date (asc)

---

## Permission Model

### Stage Transition Rules

**Rule 1: Only assigned users can move candidates**
```python
def can_change_stage(application: CompanyApplication, user: CompanyUser) -> bool:
    # Get assignments for current stage
    assignments = get_stage_assignments(
        position_id=application.position_id,
        stage_id=application.current_stage_id
    )

    # Check if user is assigned to this stage
    return user.id in assignments.assigned_user_ids or user.is_admin()
```

**Rule 2: Can only move to adjacent stages**
- Current stage order: 2
- Can move to: stage order 3 (next) or 1 (previous)
- Cannot skip stages

**Rule 3: Final stages are terminal**
- Stages marked as `is_final=True` cannot transition forward
- Example: "Hired", "Rejected", "Withdrawn"

### Visibility Rules

**Company Users**:
- ✅ Can see all applications to positions in their company
- ✅ Can see all stages in workflow
- ✅ Can view application in any stage
- ❌ Can only MOVE applications in stages they're assigned to

**Candidates**:
- ✅ Can see their own applications
- ✅ Can see current stage name
- ✅ Can see stage history
- ❌ Cannot see internal notes or comments
- ❌ Cannot see who is assigned to stages

---

## User Flows

### Flow 1: Company Creates Position with Workflow

```
1. Company creates new job position
   POST /api/company/{company_id}/positions
   Body: {
     title: "Senior Python Developer",
     workflow_id: "workflow_123",  // Select from company's workflows
     ...
   }

2. Company assigns users to each stage
   POST /api/positions/{position_id}/stage-assignments
   Body: {
     assignments: [
       { stage_id: "stage_1", user_ids: ["alice_id"] },
       { stage_id: "stage_2", user_ids: ["bob_id", "carol_id"] },
       ...
     ]
   }

3. Company publishes position
   POST /api/positions/{position_id}/publish
```

### Flow 2: Candidate Applies to Position

```
1. Candidate views public position
   GET /api/public/positions/{position_id}

2. Candidate clicks "Apply"
   - System checks if candidate is logged in
   - If not, redirects to register/login

3. Candidate selects data to share
   UI shows checkboxes:
   □ Education history
   □ Work experience
   □ Projects
   □ Skills
   □ Languages
   [x] Selected CV to share

4. Candidate submits application
   POST /api/positions/{position_id}/apply
   Body: {
     candidate_id: "candidate_123",
     shared_data: {
       include_education: true,
       include_experience: true,
       include_projects: false,
       include_skills: true,
       resume_id: "resume_456"
     }
   }

5. System creates CompanyApplication
   - Copies workflow from position
   - Sets current_stage_id to first stage (order=0)
   - Creates CompanyCandidate if doesn't exist
   - Links everything together

6. System creates notification (future)
   - Notifies assigned users for first stage
```

### Flow 3: Company Processes Application

```
1. Alice (HR Manager, assigned to "HR Screen" stage) logs in
   - Dashboard shows applications in "HR Screen" stage
   - She can see her assigned applications

2. Alice reviews candidate
   GET /api/applications/{application_id}
   - Sees candidate data according to shared_data
   - Sees uploaded CV
   - Can download resume

3. Alice adds internal comment
   POST /api/applications/{application_id}/comments
   Body: {
     comment: "Strong Python skills, good cultural fit"
   }

4. Alice moves candidate to next stage
   POST /api/applications/{application_id}/change-stage
   Body: {
     new_stage_id: "stage_2"  // Technical Test
   }

   System validates:
   - Is Alice assigned to current stage? ✓
   - Is new_stage_id adjacent? ✓
   - Is new_stage_id valid in workflow? ✓

5. Bob (Tech Lead, assigned to "Technical Test") gets notified (future)
   - Dashboard now shows this application
   - He can process it when ready

6. Process continues through all stages until:
   - Offer stage: Company makes offer
   - Final stage: Hired, Rejected, or Withdrawn
```

### Flow 4: Company Communicates with Candidate (Pseudo-Chat)

**Important**: This is a pseudo-chat system:
- Company sends message → Saved in DB + Email notification sent to candidate
- Candidate receives email with link → Clicks → Logs in → Sees conversation → Replies in-app
- Candidate reply → Saved in DB → Company sees in dashboard (NO email to company)
- **All replies must happen in-app, NOT via email**

```
1. Bob (assigned to current stage) sends message
   POST /api/applications/{application_id}/messages
   Body: {
     message: "Hi John, we'd like to schedule your technical interview. Are you available next Tuesday at 2pm?"
   }

   System actions:
   - Saves message to DB
   - Sends email to candidate:
     Subject: "New message from TechCorp regarding Senior Python Developer"
     Body: Preview + button "View Conversation"
     Link: https://app.careerpython.com/candidate/applications/app_123/messages

2. Candidate receives email notification
   - Clicks "View Conversation" button
   - Redirected to login (if not logged in)
   - After login, sees conversation page

3. Candidate views conversation
   GET /api/applications/{application_id}/messages
   Returns: [{
     id: "msg_1",
     sender_type: "COMPANY",
     sender_name: "Bob (Tech Lead)",
     message: "Hi John, we'd like to schedule...",
     created_at: "2025-01-22T10:30:00Z",
     is_read: false
   }]

4. Candidate replies in-app
   POST /api/applications/{application_id}/messages
   Body: {
     message: "Yes, Tuesday at 2pm works perfectly!"
   }

   System actions:
   - Saves message to DB
   - NO email sent to company
   - Company user sees notification in dashboard next time they log in

5. Bob sees reply in dashboard
   GET /api/company/{company_id}/messages/unread
   Returns: [{
     application_id: "app_123",
     candidate_name: "John Doe",
     position_title: "Senior Python Developer",
     unread_count: 1,
     last_message: "Yes, Tuesday at 2pm works perfectly!",
     last_message_at: "2025-01-22T11:15:00Z"
   }]

6. Bob opens conversation
   GET /api/applications/{application_id}/messages
   - Marks messages as read automatically
   - Sees full conversation history
   - Can reply (sends email to candidate again)
```

### Flow 5: Company Changes User Assignments

```
1. Scenario: Carol (Senior Dev) leaves team
   - Need to remove her from Technical Test and Tech Interview stages

2. HR Admin updates assignments
   DELETE /api/positions/{position_id}/stages/{stage_2}/users/{carol_id}
   DELETE /api/positions/{position_id}/stages/{stage_3}/users/{carol_id}

3. HR Admin adds replacement
   POST /api/positions/{position_id}/stages/{stage_2}/users/{dave_id}
   POST /api/positions/{position_id}/stages/{stage_3}/users/{dave_id}

4. Immediate effect:
   - Carol can no longer move candidates in those stages
   - Dave can now process candidates in those stages
   - Existing applications in those stages aren't affected
```

---

## Database Schema

### Tables

```sql
-- Existing tables (with additions)
companies
  + default_workflow_id UUID (nullable, FK to company_workflows)

positions
  + workflow_id UUID (nullable, FK to company_workflows)

-- New table
position_stage_assignments
  id UUID PRIMARY KEY
  position_id UUID NOT NULL (FK to positions)
  stage_id UUID NOT NULL (FK to workflow_stages)
  assigned_user_ids UUID[] NOT NULL (array of company_user IDs)
  created_at TIMESTAMP
  updated_at TIMESTAMP

  UNIQUE(position_id, stage_id)
  INDEX(position_id)
  INDEX(stage_id)
```

### Relationships

```
Company 1---* CompanyWorkflow
CompanyWorkflow 1---* WorkflowStage
Company 1---* Position
Position *---1 CompanyWorkflow (which workflow to use)
Position 1---* PositionStageAssignment (user assignments)
WorkflowStage 1---* PositionStageAssignment (which stage)
Position 1---* CompanyApplication
CompanyApplication *---1 WorkflowStage (current position)
CompanyApplication *---1 CompanyWorkflow (copy of position's workflow)
```

---

## API Endpoints

### Workflow Management

```
GET    /api/company/{company_id}/workflows
POST   /api/company/{company_id}/workflows
GET    /api/workflows/{workflow_id}
PUT    /api/workflows/{workflow_id}
DELETE /api/workflows/{workflow_id}

GET    /api/workflows/{workflow_id}/stages
POST   /api/workflows/{workflow_id}/stages
PUT    /api/stages/{stage_id}
DELETE /api/stages/{stage_id}
```

### Position Stage Assignments

```
POST   /api/positions/{position_id}/stage-assignments       (batch assign)
GET    /api/positions/{position_id}/stage-assignments       (get all)
PUT    /api/positions/{position_id}/stages/{stage_id}/users (update assigned users)
POST   /api/positions/{position_id}/stages/{stage_id}/users/{user_id}   (add user)
DELETE /api/positions/{position_id}/stages/{stage_id}/users/{user_id}   (remove user)
GET    /api/positions/{position_id}/stages/{stage_id}/can-process       (check permission)
```

### Application Processing

```
GET    /api/company/{company_id}/applications
GET    /api/positions/{position_id}/applications
GET    /api/applications/{application_id}
POST   /api/applications/{application_id}/change-stage
POST   /api/applications/{application_id}/comments
GET    /api/applications/{application_id}/comments
POST   /api/applications/{application_id}/messages
GET    /api/applications/{application_id}/messages
```

---

## Frontend Integration

### Position Creation Form

```typescript
// Step 1: Basic Info
{
  title: string,
  description: string,
  ...
}

// Step 2: Select Workflow
{
  workflow_id: string  // Dropdown of company's workflows
}

// Step 3: Assign Users to Stages
{
  stage_assignments: [
    {
      stage_id: string,
      stage_name: string,      // Display only
      assigned_user_ids: string[]  // Multi-select of company users
    },
    ...
  ]
}

// Submit all together
POST /api/company/{company_id}/positions
```

### Application Kanban Board

```typescript
// Kanban columns = Workflow stages
// Cards = Applications

// Only show "Move to next stage" button if:
const canMoveStage = (application: Application): boolean => {
  const currentStage = getCurrentStage(application);
  const assignments = getStageAssignments(application.position_id, currentStage.id);
  return assignments.assigned_user_ids.includes(currentUser.id) || currentUser.isAdmin;
}

// Drag & drop validation
onDrop = (application: Application, newStageId: string) => {
  if (!canMoveStage(application)) {
    showError("You are not assigned to this stage");
    return;
  }

  // Call API
  changeStage(application.id, newStageId);
}
```

### Stage Assignment Editor

```typescript
// For each stage, show multi-select of users
<WorkflowStageList>
  {stages.map(stage => (
    <StageCard key={stage.id}>
      <StageName>{stage.name}</StageName>
      <UserMultiSelect
        value={getAssignedUsers(stage.id)}
        options={companyUsers}
        onChange={(users) => updateAssignment(stage.id, users)}
      />
    </StageCard>
  ))}
</WorkflowStageList>
```

---

## Predefined Workflow Templates

### 1. Standard Hiring Process

```yaml
name: "Standard Hiring Process"
description: "General purpose hiring workflow for most positions"
stages:
  - name: "Application Review"
    order: 0
    type: screening
    estimated_duration: 2 days

  - name: "HR Phone Screen"
    order: 1
    type: interview
    estimated_duration: 3 days

  - name: "Technical Interview"
    order: 2
    type: interview
    estimated_duration: 5 days

  - name: "Final Interview"
    order: 3
    type: interview
    estimated_duration: 5 days

  - name: "Offer"
    order: 4
    type: offer
    estimated_duration: 3 days

  - name: "Hired"
    order: 5
    type: final
    is_final: true
```

### 2. Technical Hiring

```yaml
name: "Technical Hiring"
description: "Engineering and technical positions with coding assessment"
stages:
  - name: "Resume Review"
    order: 0
    type: screening

  - name: "Technical Test"
    order: 1
    type: assessment
    estimated_duration: 7 days

  - name: "Technical Interview"
    order: 2
    type: interview
    estimated_duration: 5 days

  - name: "Team Lead Interview"
    order: 3
    type: interview
    estimated_duration: 5 days

  - name: "CTO Meeting"
    order: 4
    type: interview
    estimated_duration: 5 days

  - name: "Offer"
    order: 5
    type: offer

  - name: "Hired"
    order: 6
    type: final
    is_final: true
```

### 3. Quick Hiring

```yaml
name: "Quick Hiring"
description: "Simplified process for junior or time-sensitive positions"
stages:
  - name: "Initial Interview"
    order: 0
    type: interview
    estimated_duration: 3 days

  - name: "Offer"
    order: 1
    type: offer
    estimated_duration: 2 days

  - name: "Hired"
    order: 2
    type: final
    is_final: true
```

---

## Implementation Notes

### Current Status (Phase 1 - Basic Workflows)

**Completed**:
- ✅ CompanyWorkflow entity and CRUD operations
- ✅ WorkflowStage entity and CRUD operations
- ✅ Basic workflow UI (Create/Edit/List workflows)
- ✅ Stage ordering with up/down buttons
- ✅ Set default workflow per company
- ✅ Workflow status management (Active/Inactive/Archived)

**Partially Completed**:
- ⚠️ WorkflowStage has `required_outcome` and `estimated_duration_days` fields in DB but not exposed in UI
- ⚠️ No connection between workflows and positions yet
- ⚠️ No user assignments to stages

### Phase 2: Enhanced Stage Configuration

**Backend Tasks**:
1. **Add new fields to WorkflowStage**:
   - [ ] Add `default_roles` (JSONB array) - roles that should be assigned
   - [ ] Add `default_assigned_users` (JSONB array) - user IDs always assigned
   - [ ] Add `email_template_id` (FK to email_templates, nullable)
   - [ ] Add `custom_email_text` (TEXT, nullable)
   - [ ] Add `deadline_days` (INTEGER, nullable) - days to complete stage
   - [ ] Add `estimated_cost` (DECIMAL, nullable) - cost tracking
   - [ ] Create migration for new fields

2. **Update WorkflowStage entity**:
   - [ ] Add new properties to domain entity
   - [ ] Update factory methods to handle new fields
   - [ ] Update mapper to include new fields in DTO
   - [ ] Update repository to persist new fields

3. **Create/Update Commands**:
   - [ ] Update CreateStageCommand with new fields
   - [ ] Update UpdateStageCommand with new fields
   - [ ] Update command handlers

**Frontend Tasks**:
1. **Update Stage Form (Create/Edit)**:
   - [ ] Add "Required Outcome" field (dropdown)
   - [ ] Add "Estimated Duration (days)" field (number input)
   - [ ] Add "Deadline (days)" field (number input)
   - [ ] Add "Estimated Cost" field (currency input)
   - [ ] Add "Default Roles" field (multi-select or tags)
   - [ ] Add "Email Template" field (dropdown, optional)
   - [ ] Add "Custom Email Text" field (textarea, optional)
   - [ ] Update form validation
   - [ ] Update API calls to include new fields

2. **Update Workflow Display**:
   - [ ] Show additional stage details in workflow view
   - [ ] Display costs summary for entire workflow
   - [ ] Display estimated timeline for workflow

### Phase 3: Position-Workflow Integration

**Backend Tasks**:
1. **Update Position Entity**:
   - [ ] Add `workflow_id` field (FK to company_workflows)
   - [ ] Add validation: workflow must belong to same company
   - [ ] Add default: use company's default_workflow if not specified
   - [ ] Create migration

2. **Create PositionStageAssignment Module**:
   - [ ] Create domain entity `PositionStageAssignment`
   - [ ] Create value objects (PositionStageAssignmentId)
   - [ ] Create repository interface and implementation
   - [ ] Create commands: AssignUsersToStageCommand, RemoveUserFromStageCommand
   - [ ] Create queries: ListStageAssignmentsQuery, GetAssignedUsersQuery
   - [ ] Create command/query handlers
   - [ ] Create DTOs and mappers
   - [ ] Create API controller
   - [ ] Create router with endpoints
   - [ ] Add to dependency injection container
   - [ ] Create migration for table

3. **Update Position Creation Flow**:
   - [ ] Modify CreatePositionCommand to accept workflow_id
   - [ ] When position created with workflow, auto-create stage assignments based on `default_assigned_users`
   - [ ] Create command: CopyWorkflowToPositionCommand (creates initial assignments)

**Frontend Tasks**:
1. **Position Form Updates**:
   - [ ] Add "Workflow" selector in position creation form
   - [ ] Load company workflows for dropdown
   - [ ] Add stage assignment step after basic info
   - [ ] Show workflow stages with user multi-select for each
   - [ ] Pre-populate with default_assigned_users from workflow
   - [ ] Allow editing assignments before creating position

2. **Position Management**:
   - [ ] Display assigned workflow in position detail view
   - [ ] Add "Edit Stage Assignments" button in position detail
   - [ ] Create stage assignments editor modal/page
   - [ ] Show current assignments with ability to add/remove users

### Phase 4: Application Processing with Permissions

**Backend Tasks**:
1. **Update CompanyApplication Entity**:
   - [ ] Add `stage_entered_at` (DATETIME)
   - [ ] Add `stage_deadline` (DATETIME, calculated)
   - [ ] Add method: `calculate_stage_deadline()` using workflow stage's deadline_days
   - [ ] Add method: `move_to_stage()` that updates stage_entered_at and recalculates deadline
   - [ ] Create migration

2. **Create Permission System**:
   - [ ] Create service: StagePermissionService
   - [ ] Method: `can_user_process_stage(user_id, application_id)` → bool
   - [ ] Method: `get_assigned_users_for_stage(position_id, stage_id)` → List[UserId]
   - [ ] Integrate permission checks in ChangeStageCommand handler
   - [ ] Return 403 Forbidden if user not authorized

3. **Update ChangeStageCommand**:
   - [ ] Add permission validation before allowing stage change
   - [ ] Update stage_entered_at when stage changes
   - [ ] Recalculate stage_deadline
   - [ ] Emit domain event: ApplicationStageChangedEvent

**Frontend Tasks**:
1. **Workflow Board/Kanban**:
   - [ ] Check permissions before showing "Move" button
   - [ ] Call permission check API endpoint
   - [ ] Disable stage transitions if user not assigned
   - [ ] Show tooltip explaining why action is disabled
   - [ ] Handle 403 errors gracefully with user-friendly message

2. **Application Detail View**:
   - [ ] Display stage deadline
   - [ ] Show visual indicator if deadline approaching/overdue
   - [ ] Display assigned users for current stage
   - [ ] Show stage history with timestamps

### Phase 5: Task Management System

**Backend Tasks**:
1. **Create Task Domain**:
   - [ ] Create entity: Task (or use CompanyApplication directly)
   - [ ] Add computed property: `priority_score` (calculated)
   - [ ] Add method: `calculate_priority()` based on deadline, position, candidate
   - [ ] Add field to CompanyApplication: `task_status` (pending/in_progress/completed/blocked)

2. **Create Task Queries**:
   - [ ] Query: GetMyTasksQuery (returns applications assigned to user)
   - [ ] Query: GetRoleTasksQuery (returns applications matching user's roles, unassigned)
   - [ ] Sort by priority, then stage_entered_at
   - [ ] Add filters: priority range, stage, position
   - [ ] Create query handler with optimized SQL

3. **Create CompanyUser Role System** (if not exists):
   - [ ] Add `roles` field to CompanyUser (JSONB array)
   - [ ] Common roles: "HR Manager", "Tech Lead", "Recruiter", "Hiring Manager"
   - [ ] Create role assignment commands
   - [ ] Update user management to assign roles

4. **Task API Endpoints**:
   - [ ] GET /api/company-users/{user_id}/tasks/assigned (direct assignments)
   - [ ] GET /api/company-users/{user_id}/tasks/available (role-based, unassigned)
   - [ ] GET /api/company-users/{user_id}/tasks/all (combined view)
   - [ ] POST /api/applications/{app_id}/claim (user claims task)
   - [ ] POST /api/applications/{app_id}/unclaim (user releases task)
   - [ ] PUT /api/applications/{app_id}/task-status (update status)

**Frontend Tasks**:
1. **User Dashboard**:
   - [ ] Create "My Tasks" page
   - [ ] Section 1: Directly Assigned (applications in stages where I'm assigned)
   - [ ] Section 2: Available Tasks (applications in stages matching my roles)
   - [ ] Display priority indicator (color coded)
   - [ ] Display deadline with urgency indicator
   - [ ] Display position and candidate name
   - [ ] Quick actions: View, Claim, Move to Next Stage
   - [ ] Filters: by stage, by priority, by deadline
   - [ ] Sort options

2. **Task Indicators**:
   - [ ] Badge showing task count in navigation
   - [ ] Highlight overdue tasks in red
   - [ ] Highlight due-today tasks in orange
   - [ ] Show estimated time remaining

### Phase 6: Email Integration

**Backend Tasks**:
1. **Create Email Template System** (if not exists):
   - [ ] Entity: EmailTemplate (id, company_id, name, subject, body, variables)
   - [ ] Templates can have placeholders: {{candidate_name}}, {{position_title}}, etc.
   - [ ] CRUD operations for email templates
   - [ ] Default templates seeded for common scenarios

2. **Stage Transition Email**:
   - [ ] When application moves to new stage, check if stage has email_template_id
   - [ ] If yes, render template with custom_email_text appended
   - [ ] Send email to candidate
   - [ ] Log email sent in application history
   - [ ] Create event handler: OnApplicationStageChanged → SendStageEmailHandler

**Frontend Tasks**:
1. **Email Template Management**:
   - [ ] Create email templates CRUD UI
   - [ ] Template editor with variable helpers
   - [ ] Preview functionality
   - [ ] Test send feature

2. **Workflow Stage Email Configuration**:
   - [ ] In stage edit form, show email template selector
   - [ ] Preview selected template
   - [ ] Add custom text field
   - [ ] Preview final email with custom text

### Phase 7: Analytics & Reporting

**Backend Tasks**:
1. **Workflow Analytics Queries**:
   - [ ] Average time per stage
   - [ ] Conversion rate per stage
   - [ ] Total applications per workflow
   - [ ] Bottleneck detection (stages taking longest)
   - [ ] Cost per hire calculation (sum of stage costs)

**Frontend Tasks**:
1. **Analytics Dashboard**:
   - [ ] Workflow performance metrics
   - [ ] Stage conversion funnel visualization
   - [ ] Time-in-stage charts
   - [ ] Cost tracking per workflow
   - [ ] Export reports

### Testing Strategy

1. **Unit Tests**:
   - PositionStageAssignment entity methods
   - Permission check logic
   - Workflow template creation

2. **Integration Tests**:
   - Stage assignment CRUD operations
   - Permission validation on stage changes
   - Application flow with multiple users

3. **E2E Tests**:
   - Complete hiring workflow
   - User assignment changes mid-process
   - Permission denial scenarios

---

## Future Enhancements (V2+)

- **Workflow Analytics**: Time in each stage, conversion rates
- **Automated Transitions**: Auto-advance based on rules
- **Email Notifications**: Notify assigned users when candidate enters their stage
- **Stage Templates**: Reusable stage configurations
- **Conditional Workflows**: Different paths based on criteria
- **Stage SLAs**: Alerts when candidate stuck too long
- **Bulk Operations**: Move multiple candidates at once
- **Workflow Versioning**: Track changes to workflows over time
