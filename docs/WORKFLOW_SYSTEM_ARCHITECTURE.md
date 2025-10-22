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
- `stage_type`: Type of stage (screening, interview, assessment, offer, final)
- `order`: Position in workflow (0, 1, 2, ...)
- `required_outcome`: What outcome is needed to proceed? (optional)
- `estimated_duration_days`: How long candidates typically stay here
- `is_active`: Can candidates be in this stage?

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

**Key Behavior**:
- Created when candidate applies or company adds candidate to position
- Inherits workflow from position
- Current stage determines who can process
- Only data in `shared_data` is visible to company
- Candidate can withdraw anytime
- Company can move through stages (if assigned)

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

### Phase 1.5 Tasks

1. **Backend**:
   - Add `workflow_id` to Position entity and model
   - Add `default_workflow_id` to Company entity
   - Create PositionStageAssignment entity + full module
   - Update CompanyApplication with permission checks
   - Create seeder for predefined workflows
   - API endpoints for stage assignments

2. **Frontend**:
   - Position form: workflow selector + stage assignment editor
   - Application kanban: permission-aware stage transitions
   - Settings page: manage workflows and templates
   - User assignment UI components

3. **Migrations**:
   - Add workflow_id to positions table
   - Add default_workflow_id to companies table
   - Create position_stage_assignments table
   - Seed predefined workflows

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
