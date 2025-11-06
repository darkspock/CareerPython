# Job Position View - Comments & Activity Implementation - Analysis

## Purpose
Allow stakeholders to **review, refine, and approve** requirements for a job position before it is published. The view facilitates collaboration through comments, tracks all interactions, and provides visibility into the position's evolution through its workflow stages.

---

## Requirements Summary

Based on `JobPositionViewRequirements.md`, the view must display:

1. **Custom Fields** - Dynamic fields defined in the job position workflow
2. **Common Fields** - Standard fields (title, description, category, etc.)
3. **Interactions** - All edits, stage moves, and other activities
4. **Comments System**:
   - Users can add comments **globally** (not tied to a stage) or **per-stage**
   - Users can mark comments as **pending** or **reviewed**
   - **Critical**: Comments from other stages should NOT appear directly in the current view
   - **Only show**: Global comments + Current stage comments

### Proposed UI Structure

#### **Upper Card (Tabbed Interface)**
- **Tab 1: Global** - Overview of the position (common fields)
- **Tab 2: Comments** - All comments (historical log across all stages + global)
- **Tab 3: History** - Activity log (edits, stage moves, status changes, etc.)

#### **Lower Card**
- **Section 1: Custom Fields** - Display custom fields for current workflow stage
- **Section 2: Current Comments** - Only comments for current stage + global comments

---

## Current State - Candidate Comments (Reference)

The candidate comments system provides a baseline, but differs in key aspects:

### Key Differences from Candidate Comments

| Aspect | Candidate Comments | Job Position Comments (New) |
|--------|-------------------|----------------------------|
| **Parent Entity** | `CompanyCandidate` | `JobPosition` |
| **Stage Filtering** | Shows all stage comments | **Only current stage + global** |
| **Global Comments** | Not supported | **New feature: stage_id = NULL** |
| **Activity Log** | Not implemented | **New feature: interaction history** |
| **UI Structure** | Single comments section | **Tabbed UI + separated sections** |
| **Purpose** | Track candidate evaluation | **Collaborative approval workflow** |

---

## Job Position Comments - Implementation Plan

### Key Concepts

1. **Global Comments** (`stage_id = NULL`):
   - Visible at all stages
   - Apply to the entire position
   - Use for general feedback, approval decisions, etc.

2. **Stage-Specific Comments** (`stage_id != NULL`):
   - Only visible when position is in that stage
   - Use for stage-specific refinements

3. **Review Status**:
   - `PENDING` - Requires action/response
   - `REVIEWED` - Acknowledged/resolved

4. **Activity History**:
   - Track position edits (who changed what field, when)
   - Track stage transitions (moved from X to Y, when, by whom)
   - Track status changes (draft → active, etc.)

---

## Implementation Tasks

### Phase 1: Backend - Domain Layer

**1.1. Create Value Object**
- File: `src/job_position/domain/value_objects/job_position_comment_id.py`
- Inherit from `BaseId`

**1.2. Create Entity - JobPositionComment**
- File: `src/job_position/domain/entities/job_position_comment.py`
- Fields:
  ```python
  id: JobPositionCommentId
  job_position_id: JobPositionId
  comment: str
  workflow_id: Optional[JobPositionWorkflowId]
  stage_id: Optional[JobPositionWorkflowStageId]  # NULL = global comment
  created_by_user_id: CompanyUserId
  review_status: CommentReviewStatusEnum  # PENDING | REVIEWED
  visibility: CommentVisibilityEnum  # PRIVATE | SHARED_WITH_CANDIDATE (future)
  created_at: datetime
  updated_at: datetime
  ```
- Methods:
  - `create()` - factory (default: review_status=REVIEWED, visibility=PRIVATE)
  - `update(comment, visibility)` - update comment content
  - `mark_as_pending()` - change status to PENDING
  - `mark_as_reviewed()` - change status to REVIEWED
  - `is_global()` - returns True if stage_id is None

**1.3. Create Entity - JobPositionActivity** (NEW)
- File: `src/job_position/domain/entities/job_position_activity.py`
- Purpose: Track all interactions with the position
- Fields:
  ```python
  id: JobPositionActivityId
  job_position_id: JobPositionId
  activity_type: ActivityTypeEnum  # CREATED, EDITED, STAGE_MOVED, STATUS_CHANGED, etc.
  description: str  # Human-readable description
  performed_by_user_id: CompanyUserId
  metadata: Dict[str, Any]  # JSON with details (old/new values, etc.)
  created_at: datetime
  ```
- Methods:
  - `create()` - factory
  - `from_edit(job_position_id, user_id, changed_fields)` - static factory
  - `from_stage_move(job_position_id, user_id, old_stage, new_stage)` - static factory

**1.4. Create Enums** (Reuse + New)
- **Reuse from candidate comments**:
  - `CommentReviewStatusEnum`: PENDING, REVIEWED
  - `CommentVisibilityEnum`: PRIVATE, SHARED_WITH_CANDIDATE
- **New**:
  - `ActivityTypeEnum`: CREATED, EDITED, STAGE_MOVED, STATUS_CHANGED, COMMENT_ADDED

**1.5. Create Repository Interfaces**
- `JobPositionCommentRepositoryInterface`:
  - `save(comment: JobPositionComment) -> None`
  - `get_by_id(comment_id: JobPositionCommentId) -> Optional[JobPositionComment]`
  - `list_by_job_position(job_position_id: JobPositionId) -> List[JobPositionComment]`
  - **`list_by_stage_and_global(job_position_id: JobPositionId, stage_id: Optional[JobPositionWorkflowStageId]) -> List[JobPositionComment]`** ✨ (NEW: returns global + stage comments)
  - `list_global_only(job_position_id: JobPositionId) -> List[JobPositionComment]` ✨ (NEW)
  - `delete(comment_id: JobPositionCommentId) -> None`
  - `count_pending_by_job_position(job_position_id: JobPositionId) -> int`
  
- `JobPositionActivityRepositoryInterface`: ✨ (NEW)
  - `save(activity: JobPositionActivity) -> None`
  - `list_by_job_position(job_position_id: JobPositionId, limit: int) -> List[JobPositionActivity]`

---

### Phase 2: Backend - Infrastructure Layer

**2.1. Create Database Model - JobPositionComment**
- File: `src/job_position/infrastructure/models/job_position_comment_model.py`
- Table: `job_position_comments`
- Columns:
  - `id`: String (PK)
  - `job_position_id`: String (FK to job_positions, CASCADE)
  - `comment`: Text
  - `workflow_id`: String (FK to job_position_workflows, SET NULL) - optional
  - **`stage_id`: String (FK to job_position_workflow_stages, SET NULL) - **NULL = global comment** ✨**
  - `created_by_user_id`: String (FK to company_users, SET NULL)
  - `review_status`: Enum (CommentReviewStatusEnum)
  - `visibility`: Enum (CommentVisibilityEnum)
  - `created_at`: DateTime
  - `updated_at`: DateTime
- Indexes: 
  - `job_position_id`
  - `stage_id` (allows NULL)
  - `review_status`
  - `created_at` (for ordering)

**2.2. Create Database Model - JobPositionActivity** ✨ (NEW)
- File: `src/job_position/infrastructure/models/job_position_activity_model.py`
- Table: `job_position_activities`
- Columns:
  - `id`: String (PK)
  - `job_position_id`: String (FK to job_positions, CASCADE)
  - `activity_type`: Enum (ActivityTypeEnum)
  - `description`: Text
  - `performed_by_user_id`: String (FK to company_users, SET NULL)
  - `metadata`: JSON (details about the activity)
  - `created_at`: DateTime
- Indexes:
  - `job_position_id`
  - `activity_type`
  - `created_at` (for ordering)

**2.3. Create Repository Implementations**
- `JobPositionCommentRepository`:
  - Implement all interface methods
  - **`list_by_stage_and_global()`** query:
    ```sql
    WHERE job_position_id = ? AND (stage_id = ? OR stage_id IS NULL)
    ORDER BY created_at DESC
    ```
  - Include expanded data in queries (JOIN for user name, workflow name, stage name)

- `JobPositionActivityRepository`: ✨ (NEW)
  - Implement interface methods
  - Include user name in expanded data

**2.4. Create Alembic Migrations**
1. **Migration 1**: `add_job_position_comments_table`
   - Create `job_position_comments` table with all columns, FKs, indexes
   
2. **Migration 2**: `add_job_position_activities_table` ✨
   - Create `job_position_activities` table with all columns, FKs, indexes

---

### Phase 3: Backend - Application Layer

**3.1. Create DTOs**
- `JobPositionCommentDto`:
  - All entity fields + expanded data:
    - `workflow_name`, `stage_name`
    - `created_by_user_name`, `created_by_user_email`
    - **`is_global`**: boolean (computed from stage_id)

- `JobPositionActivityDto`: ✨ (NEW)
  - All entity fields + expanded data:
    - `performed_by_user_name`, `performed_by_user_email`

**3.2. Create Mappers**
- `JobPositionCommentMapper`: Entity ↔ DTO
- `JobPositionActivityMapper`: Entity ↔ DTO ✨

**3.3. Create Commands - Comments**
- `CreateJobPositionCommentCommand` + Handler
  - When creating comment, also create activity record: `COMMENT_ADDED`
- `UpdateJobPositionCommentCommand` + Handler
- `DeleteJobPositionCommentCommand` + Handler
- `MarkJobPositionCommentAsPendingCommand` + Handler
- `MarkJobPositionCommentAsReviewedCommand` + Handler

**3.4. Create Commands - Activities** ✨ (NEW)
- `CreateJobPositionActivityCommand` + Handler
  - Used internally by other commands to log activities

**3.5. Update Existing Commands** ✨
- **`UpdateJobPositionCommand`**:
  - After updating, create activity: `EDITED`
  - Log which fields changed in metadata
  
- **`MoveJobPositionToStageCommand`**:
  - After moving stage, create activity: `STAGE_MOVED`
  - Log old/new stage in metadata

**3.6. Create Queries - Comments**
- `GetJobPositionCommentByIdQuery` + Handler
- `ListJobPositionCommentsByJobPositionQuery` + Handler (all comments, for tab view)
- **`ListJobPositionCommentsCurrentAndGlobalQuery` + Handler** ✨ (NEW: current stage + global only)
- `CountPendingJobPositionCommentsQuery` + Handler

**3.7. Create Queries - Activities** ✨ (NEW)
- `ListJobPositionActivitiesQuery` + Handler
  - Returns activities ordered by created_at DESC
  - Optional limit parameter (default: 50)

---

### Phase 4: Backend - Presentation Layer

**4.1. Create Request/Response Schemas - Comments**
- `CreateJobPositionCommentRequest`:
  ```python
  comment: str
  stage_id: Optional[str] = None  # NULL = global comment ✨
  workflow_id: Optional[str] = None
  visibility: str = "private"
  review_status: str = "reviewed"
  ```
- `UpdateJobPositionCommentRequest`
- `JobPositionCommentResponse` (all fields + expanded data + `is_global`)

**4.2. Create Response Schemas - Activities** ✨
- `JobPositionActivityResponse`:
  ```python
  id: str
  job_position_id: str
  activity_type: str
  description: str
  performed_by_user_id: str
  performed_by_user_name: str
  performed_by_user_email: str
  metadata: Dict[str, Any]
  created_at: datetime
  ```

**4.3. Create Controllers**
- `JobPositionCommentController`:
  - `create_comment(job_position_id, request, created_by_user_id)`
  - `list_all_comments(job_position_id)` - for "Comments" tab
  - **`list_current_and_global_comments(job_position_id, stage_id)` ✨** - for "Current Comments" section
  - `count_pending_comments(job_position_id)`
  - `update_comment(comment_id, request)`
  - `delete_comment(comment_id)`
  - `mark_as_pending(comment_id)`
  - `mark_as_reviewed(comment_id)`

- `JobPositionActivityController`: ✨ (NEW)
  - `list_activities(job_position_id, limit=50)` - for "History" tab

**4.4. Create Response Mappers**
- `JobPositionCommentResponseMapper`: DTO → Response
- `JobPositionActivityResponseMapper`: DTO → Response ✨

**4.5. Create Router/Endpoints**
Base path: `/api/company/positions/{job_position_id}`

**Comment Endpoints:**
- `POST /comments` - Create comment (global if stage_id=null)
- `GET /comments` - List all comments (for Comments tab)
- **`GET /comments/current` - List current stage + global comments** ✨
- `GET /comments/{comment_id}` - Get single comment
- `PUT /comments/{comment_id}` - Update comment
- `DELETE /comments/{comment_id}` - Delete comment
- `POST /comments/{comment_id}/mark-pending` - Mark as pending
- `POST /comments/{comment_id}/mark-reviewed` - Mark as reviewed
- `GET /comments/pending/count` - Count pending comments

**Activity Endpoints:** ✨ (NEW)
- `GET /activities` - List activities (history log)

**4.6. Register in Container**
- Register repositories
- Register all command/query handlers
- Register controllers

---

### Phase 5: Frontend - Types & Services

**5.1. Create Types**
- File: `client-vite/src/types/jobPositionComment.ts`
  ```typescript
  export type CommentReviewStatus = 'pending' | 'reviewed';
  export type CommentVisibility = 'private' | 'shared_with_candidate';

  export interface JobPositionComment {
    id: string;
    job_position_id: string;
    comment: string;
    workflow_id: string | null;
    stage_id: string | null;  // NULL = global comment ✨
    created_by_user_id: string;
    review_status: CommentReviewStatus;
    visibility: CommentVisibility;
    created_at: string;
    updated_at: string;
    // Expanded data
    workflow_name?: string;
    stage_name?: string;
    created_by_user_name?: string;
    created_by_user_email?: string;
    is_global: boolean;  // Computed field ✨
  }

  export interface CreateJobPositionCommentRequest {
    comment: string;
    stage_id?: string | null;  // Omit or null for global ✨
    workflow_id?: string;
    visibility?: CommentVisibility;
    review_status?: CommentReviewStatus;
  }
  ```

- File: `client-vite/src/types/jobPositionActivity.ts` ✨ (NEW)
  ```typescript
  export type ActivityType = 
    | 'created' 
    | 'edited' 
    | 'stage_moved' 
    | 'status_changed' 
    | 'comment_added';

  export interface JobPositionActivity {
    id: string;
    job_position_id: string;
    activity_type: ActivityType;
    description: string;
    performed_by_user_id: string;
    performed_by_user_name: string;
    performed_by_user_email: string;
    metadata: Record<string, any>;
    created_at: string;
  }
  ```

**5.2. Create Services**
- File: `client-vite/src/services/jobPositionCommentService.ts`
  ```typescript
  class JobPositionCommentService {
    async createComment(jobPositionId: string, data: CreateJobPositionCommentRequest)
    async getAllComments(jobPositionId: string) // For Comments tab
    async getCurrentAndGlobalComments(jobPositionId: string, stageId: string) ✨
    async getPendingCount(jobPositionId: string)
    async updateComment(commentId: string, data: UpdateJobPositionCommentRequest)
    async deleteComment(commentId: string)
    async markAsPending(commentId: string)
    async markAsReviewed(commentId: string)
  }
  ```

- File: `client-vite/src/services/jobPositionActivityService.ts` ✨ (NEW)
  ```typescript
  class JobPositionActivityService {
    async getActivities(jobPositionId: string, limit?: number)
  }
  ```

---

### Phase 6: Frontend - Components & Integration

**6.1. Modify PositionDetailPage - Add Tabbed Upper Card** ✨

File: `client-vite/src/pages/company/PositionDetailPage.tsx`

**Structure:**
```tsx
<PositionDetailPage>
  {/* Header with title, status, actions */}
  
  {/* Upper Card - Tabbed Interface */}
  <Card>
    <Tabs value={activeTab} onValueChange={setActiveTab}>
      <TabsList>
        <TabsTrigger value="global">Global</TabsTrigger>
        <TabsTrigger value="comments">
          Comments
          {pendingCount > 0 && <Badge>{pendingCount}</Badge>}
        </TabsTrigger>
        <TabsTrigger value="history">History</TabsTrigger>
      </TabsList>
      
      <TabsContent value="global">
        {/* Common fields display */}
        <GlobalInfoTab position={position} />
      </TabsContent>
      
      <TabsContent value="comments">
        {/* All comments (historical log) */}
        <AllCommentsTab 
          comments={allComments} 
          onTogglePending={handleTogglePending}
        />
      </TabsContent>
      
      <TabsContent value="history">
        {/* Activity log */}
        <ActivityHistoryTab activities={activities} />
      </TabsContent>
    </Tabs>
  </Card>
  
  {/* Lower Section */}
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
    {/* Left: Custom Fields */}
    <Card>
      <CustomFieldsSection 
        workflow={workflow}
        position={position}
      />
    </Card>
    
    {/* Right: Current Comments */}
    <Card>
      <CurrentCommentsSection 
        jobPositionId={position.id}
        stageId={position.stage_id}
        workflowId={position.job_position_workflow_id}
        onCommentChange={loadAllComments}
      />
    </Card>
  </div>
</PositionDetailPage>
```

**State Management:**
```typescript
// Tabs
const [activeTab, setActiveTab] = useState<'global' | 'comments' | 'history'>('global');

// Comments
const [allComments, setAllComments] = useState<JobPositionComment[]>([]);
const [currentComments, setCurrentComments] = useState<JobPositionComment[]>([]);
const [pendingCount, setPendingCount] = useState(0);

// Activities
const [activities, setActivities] = useState<JobPositionActivity[]>([]);
```

**6.2. Create Component: GlobalInfoTab** ✨
- File: `client-vite/src/components/jobPosition/GlobalInfoTab.tsx`
- Display common fields: title, description, category, dates, visibility, etc.
- Read-only view

**6.3. Create Component: AllCommentsTab** ✨
- File: `client-vite/src/components/jobPosition/AllCommentsTab.tsx`
- Display all comments across all stages + global
- Group by stage (with "Global" as a separate group)
- Show stage name badge for stage-specific comments
- Show "Global" badge for global comments
- Mark as pending/reviewed
- Highlight pending comments (yellow background)

**6.4. Create Component: ActivityHistoryTab** ✨ (NEW)
- File: `client-vite/src/components/jobPosition/ActivityHistoryTab.tsx`
- Display activity timeline
- Show icon for each activity type
- Format description
- Show user, timestamp
- Display metadata details if available

**6.5. Create Component: CurrentCommentsSection** ✨
- File: `client-vite/src/components/jobPosition/CurrentCommentsSection.tsx`
- **Critical**: Only shows current stage comments + global comments
- Add new comment form with checkbox: "Make this a global comment" (sets stage_id to null)
- Toggle pending/reviewed
- Visual distinction for global vs stage comments

**Props:**
```typescript
interface CurrentCommentsSectionProps {
  jobPositionId: string;
  stageId: string | null;
  workflowId: string | null;
  onCommentChange: () => void;
}
```

**Features:**
- Load comments via `getCurrentAndGlobalComments(jobPositionId, stageId)`
- Show badge: "Global" or stage name
- Add comment form with:
  - Text area
  - Checkbox: "Global comment (visible at all stages)"
  - Submit button
- Mark as pending/reviewed
- Visual: Yellow background for pending, white for reviewed

**6.6. Update PositionsListPage** (Optional Enhancement)
- Show pending comments count badge on position cards
- Visual indicator for positions with pending comments

---

## Key Implementation Details

### 1. **Global Comments Logic**

**Backend:**
```python
# Creating a global comment
comment = JobPositionComment.create(
    id=comment_id,
    job_position_id=job_position_id,
    comment=text,
    created_by_user_id=user_id,
    workflow_id=workflow_id,
    stage_id=None,  # NULL = global ✨
    review_status=CommentReviewStatusEnum.REVIEWED
)
```

**Query for current + global:**
```sql
SELECT * FROM job_position_comments
WHERE job_position_id = ? 
  AND (stage_id = ? OR stage_id IS NULL)
ORDER BY created_at DESC
```

**Frontend:**
```typescript
// Add comment with global flag
const createComment = async (text: string, isGlobal: boolean) => {
  const request: CreateJobPositionCommentRequest = {
    comment: text,
    stage_id: isGlobal ? null : currentStageId,
    workflow_id: currentWorkflowId,
    review_status: 'reviewed',
  };
  await jobPositionCommentService.createComment(jobPositionId, request);
};
```

### 2. **Activity Logging**

**When to Log:**
- Position created
- Position edited (log changed fields)
- Stage moved (log old/new stage)
- Status changed (log old/new status)
- Comment added (reference comment ID)

**Metadata Examples:**
```json
// Edit activity
{
  "changed_fields": ["title", "description"],
  "old_values": {"title": "Old Title"},
  "new_values": {"title": "New Title"}
}

// Stage move activity
{
  "old_stage_id": "stage_123",
  "old_stage_name": "Draft",
  "new_stage_id": "stage_456",
  "new_stage_name": "Review"
}
```

### 3. **Comment Filtering in UI**

**AllCommentsTab** (Comments tab):
- Fetches ALL comments
- Groups by stage + "Global"
- Shows historical view

**CurrentCommentsSection** (Lower card):
- Fetches ONLY current stage + global comments
- Live, actionable view
- Users add comments here

### 4. **Pending Comments Badge**

Show count in:
- "Comments" tab trigger
- Position cards in list view (optional)

Count query: `WHERE review_status = 'pending'`

---

## File Structure Summary

### Backend (New Files)

```
src/job_position/
├── domain/
│   ├── entities/
│   │   ├── job_position_comment.py
│   │   └── job_position_activity.py ✨
│   ├── value_objects/
│   │   ├── job_position_comment_id.py
│   │   └── job_position_activity_id.py ✨
│   ├── enums/
│   │   └── activity_type_enum.py ✨ (NEW)
│   └── infrastructure/
│       ├── job_position_comment_repository_interface.py
│       └── job_position_activity_repository_interface.py ✨
├── infrastructure/
│   ├── models/
│   │   ├── job_position_comment_model.py
│   │   └── job_position_activity_model.py ✨
│   └── repositories/
│       ├── job_position_comment_repository.py
│       └── job_position_activity_repository.py ✨
├── application/
│   ├── dtos/
│   │   ├── job_position_comment_dto.py
│   │   └── job_position_activity_dto.py ✨
│   ├── mappers/
│   │   ├── job_position_comment_mapper.py
│   │   └── job_position_activity_mapper.py ✨
│   ├── commands/
│   │   ├── create_job_position_comment_command.py
│   │   ├── update_job_position_comment_command.py
│   │   ├── delete_job_position_comment_command.py
│   │   ├── mark_job_position_comment_as_pending_command.py
│   │   ├── mark_job_position_comment_as_reviewed_command.py
│   │   └── create_job_position_activity_command.py ✨
│   └── queries/
│       ├── get_job_position_comment_by_id.py
│       ├── list_job_position_comments_by_job_position.py
│       ├── list_job_position_comments_current_and_global.py ✨
│       ├── count_pending_job_position_comments_query.py
│       └── list_job_position_activities_query.py ✨
└── presentation/
    ├── controllers/
    │   ├── job_position_comment_controller.py
    │   └── job_position_activity_controller.py ✨
    ├── mappers/
    │   ├── job_position_comment_mapper.py
    │   └── job_position_activity_mapper.py ✨
    └── schemas/
        ├── create_job_position_comment_request.py
        ├── update_job_position_comment_request.py
        ├── job_position_comment_response.py
        └── job_position_activity_response.py ✨

alembic/versions/
├── XXXX_add_job_position_comments_table.py
└── XXXX_add_job_position_activities_table.py ✨
```

### Frontend (New Files)

```
client-vite/src/
├── types/
│   ├── jobPositionComment.ts
│   └── jobPositionActivity.ts ✨
├── services/
│   ├── jobPositionCommentService.ts
│   └── jobPositionActivityService.ts ✨
└── components/
    └── jobPosition/
        ├── GlobalInfoTab.tsx ✨
        ├── AllCommentsTab.tsx ✨
        ├── ActivityHistoryTab.tsx ✨
        └── CurrentCommentsSection.tsx ✨
```

### Frontend (Modified Files)

```
client-vite/src/pages/company/
└── PositionDetailPage.tsx 
    - Add tabbed interface (Global, Comments, History)
    - Add activity loading
    - Add CurrentCommentsSection
    - Restructure layout (upper/lower cards)
```

---

## Testing Strategy

### Backend Tests

1. **Unit Tests** (Domain Layer):
   - Test global vs stage comments
   - Test activity creation
   - Test comment filtering logic

2. **Integration Tests** (Application Layer):
   - Test `list_current_and_global` query
   - Test activity logging on edits/moves
   - Test pending count calculation

3. **API Tests** (Presentation Layer):
   - Test creating global comments (stage_id=null)
   - Test filtering current + global comments
   - Test activity log endpoint

### Frontend Tests

1. **Component Tests**:
   - Test tab switching
   - Test global comment checkbox
   - Test activity timeline rendering

2. **Integration Tests**:
   - Test comment filtering (current vs all)
   - Test activity loading

---

## Estimated Effort

- **Backend - Comments**: ~3-4 hours
- **Backend - Activities**: ~3-4 hours (new feature)
- **Backend - Integration** (update existing commands): ~2 hours
- **Frontend - Tabs & Layout**: ~3-4 hours
- **Frontend - Components**: ~4-5 hours
- **Testing**: ~3-4 hours
- **Total**: ~18-24 hours

---

## Rollout Plan

1. **Phase 1-2** (Backend Foundation): Domain + Infrastructure (comments + activities)
2. **Phase 3** (Backend Logic): Application layer (commands, queries)
3. **Phase 4** (Backend API): Presentation layer + migrations
4. **Phase 5** (Frontend Types/Services)
5. **Phase 6** (Frontend UI): Tabs, components, integration
6. **Testing**: End-to-end verification
7. **Deployment**: Run migrations, deploy

---

## Success Criteria

✅ Users can add **global comments** (visible at all stages)
✅ Users can add **stage-specific comments**
✅ **Current Comments section** only shows current stage + global comments
✅ **Comments tab** shows all historical comments grouped by stage
✅ **History tab** shows activity log (edits, moves, status changes)
✅ Pending comments are visually distinct and counted
✅ Tabbed UI provides clear separation of concerns
✅ Activity log tracks all interactions with the position
✅ No performance issues with comment/activity loading
✅ System follows DDD architecture

---

## Next Steps

1. Review this analysis
2. Confirm approach
3. Begin Phase 1 implementation
4. Iterate through phases
5. Test at each phase
6. Deploy when complete
