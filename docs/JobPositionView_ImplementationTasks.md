# Job Position View - Implementation Tasks

## Overview
Implementation of comments and activity tracking system for Job Positions with tabbed UI interface.

**Total Estimated Effort**: 18-24 hours

---

## Phase 1: Backend - Domain Layer (Comments)

### Task 1.1: Create Value Object - JobPositionCommentId
**File**: `src/job_position/domain/value_objects/job_position_comment_id.py`
- [ ] Create `JobPositionCommentId` class inheriting from `BaseId`
- [ ] Follow same pattern as `CandidateCommentId`

**Estimated Time**: 15 minutes

---

### Task 1.2: Create Entity - JobPositionComment
**File**: `src/job_position/domain/entities/job_position_comment.py`
- [ ] Create `JobPositionComment` dataclass with fields:
  - `id: JobPositionCommentId`
  - `job_position_id: JobPositionId`
  - `comment: str`
  - `workflow_id: Optional[JobPositionWorkflowId]`
  - `stage_id: Optional[JobPositionWorkflowStageId]` (NULL = global comment)
  - `created_by_user_id: CompanyUserId`
  - `review_status: CommentReviewStatusEnum`
  - `visibility: CommentVisibilityEnum`
  - `created_at: datetime`
  - `updated_at: datetime`
- [ ] Implement `create()` factory method (default: review_status=REVIEWED)
- [ ] Implement `update(comment, visibility)` method
- [ ] Implement `mark_as_pending()` method
- [ ] Implement `mark_as_reviewed()` method
- [ ] Implement `is_global()` property (returns True if stage_id is None)
- [ ] Add validation: comment cannot be empty

**Estimated Time**: 45 minutes

---

### Task 1.3: Reuse Enums from Candidate Comments
**Files**: 
- `src/company_candidate/domain/enums/__init__.py`
- Update imports in job_position module

- [ ] Confirm `CommentReviewStatusEnum` is accessible (PENDING, REVIEWED)
- [ ] Confirm `CommentVisibilityEnum` is accessible (PRIVATE, SHARED_WITH_CANDIDATE)
- [ ] Add imports to job_position module if needed

**Estimated Time**: 10 minutes

---

### Task 1.4: Create Repository Interface - JobPositionComment
**File**: `src/job_position/domain/infrastructure/job_position_comment_repository_interface.py`
- [ ] Create `JobPositionCommentRepositoryInterface` abstract class
- [ ] Define abstract methods:
  - `save(comment: JobPositionComment) -> None`
  - `get_by_id(comment_id: JobPositionCommentId) -> Optional[JobPositionComment]`
  - `list_by_job_position(job_position_id: JobPositionId) -> List[JobPositionComment]`
  - `list_by_stage_and_global(job_position_id: JobPositionId, stage_id: Optional[JobPositionWorkflowStageId]) -> List[JobPositionComment]` ⭐
  - `list_global_only(job_position_id: JobPositionId) -> List[JobPositionComment]`
  - `delete(comment_id: JobPositionCommentId) -> None`
  - `count_pending_by_job_position(job_position_id: JobPositionId) -> int`

**Estimated Time**: 30 minutes

---

## Phase 2: Backend - Domain Layer (Activities)

### Task 2.1: Create Value Object - JobPositionActivityId
**File**: `src/job_position/domain/value_objects/job_position_activity_id.py`
- [ ] Create `JobPositionActivityId` class inheriting from `BaseId`

**Estimated Time**: 10 minutes

---

### Task 2.2: Create Enum - ActivityTypeEnum
**File**: `src/job_position/domain/enums/activity_type_enum.py`
- [ ] Create enum with values:
  - `CREATED`
  - `EDITED`
  - `STAGE_MOVED`
  - `STATUS_CHANGED`
  - `COMMENT_ADDED`
- [ ] Add `__init__.py` export

**Estimated Time**: 15 minutes

---

### Task 2.3: Create Entity - JobPositionActivity
**File**: `src/job_position/domain/entities/job_position_activity.py`
- [ ] Create `JobPositionActivity` dataclass with fields:
  - `id: JobPositionActivityId`
  - `job_position_id: JobPositionId`
  - `activity_type: ActivityTypeEnum`
  - `description: str`
  - `performed_by_user_id: CompanyUserId`
  - `metadata: Dict[str, Any]`
  - `created_at: datetime`
- [ ] Implement `create()` factory method
- [ ] Implement static factory `from_edit(job_position_id, user_id, changed_fields, old_values, new_values)`
- [ ] Implement static factory `from_stage_move(job_position_id, user_id, old_stage, new_stage)`
- [ ] Implement static factory `from_status_change(job_position_id, user_id, old_status, new_status)`
- [ ] Implement static factory `from_comment_added(job_position_id, user_id, comment_id)`

**Estimated Time**: 1 hour

---

### Task 2.4: Create Repository Interface - JobPositionActivity
**File**: `src/job_position/domain/infrastructure/job_position_activity_repository_interface.py`
- [ ] Create `JobPositionActivityRepositoryInterface` abstract class
- [ ] Define abstract methods:
  - `save(activity: JobPositionActivity) -> None`
  - `list_by_job_position(job_position_id: JobPositionId, limit: int = 50) -> List[JobPositionActivity]`

**Estimated Time**: 20 minutes

---

## Phase 3: Backend - Infrastructure Layer

### Task 3.1: Create Database Model - JobPositionComment
**File**: `src/job_position/infrastructure/models/job_position_comment_model.py`
- [ ] Create `JobPositionCommentModel` class
- [ ] Define table name: `job_position_comments`
- [ ] Add columns:
  - `id: Mapped[str]` (PK)
  - `job_position_id: Mapped[str]` (FK to job_positions, CASCADE)
  - `comment: Mapped[str]` (Text)
  - `workflow_id: Mapped[Optional[str]]` (FK to job_position_workflows, SET NULL)
  - `stage_id: Mapped[Optional[str]]` (FK to job_position_workflow_stages, SET NULL) ⭐
  - `created_by_user_id: Mapped[str]` (FK to company_users, SET NULL)
  - `review_status: Mapped[str]` (Enum)
  - `visibility: Mapped[str]` (Enum)
  - `created_at: Mapped[datetime]`
  - `updated_at: Mapped[datetime]`
- [ ] Add indexes on: id, job_position_id, stage_id, review_status, created_at

**Estimated Time**: 45 minutes

---

### Task 3.2: Create Database Model - JobPositionActivity
**File**: `src/job_position/infrastructure/models/job_position_activity_model.py`
- [ ] Create `JobPositionActivityModel` class
- [ ] Define table name: `job_position_activities`
- [ ] Add columns:
  - `id: Mapped[str]` (PK)
  - `job_position_id: Mapped[str]` (FK to job_positions, CASCADE)
  - `activity_type: Mapped[str]` (Enum)
  - `description: Mapped[str]` (Text)
  - `performed_by_user_id: Mapped[str]` (FK to company_users, SET NULL)
  - `metadata: Mapped[dict]` (JSON)
  - `created_at: Mapped[datetime]`
- [ ] Add indexes on: id, job_position_id, activity_type, created_at

**Estimated Time**: 30 minutes

---

### Task 3.3: Create Alembic Migration - Comments Table
**Command**: `cd /Users/juanmacias/Projects/CareerPython && make revision m="add job_position_comments table"`
- [ ] Generate migration
- [ ] Review generated migration
- [ ] Adjust if needed (FKs, indexes)
- [ ] Test upgrade/downgrade

**Estimated Time**: 30 minutes

---

### Task 3.4: Create Alembic Migration - Activities Table
**Command**: `cd /Users/juanmacias/Projects/CareerPython && make revision m="add job_position_activities table"`
- [ ] Generate migration
- [ ] Review generated migration
- [ ] Adjust if needed (FKs, indexes)
- [ ] Test upgrade/downgrade

**Estimated Time**: 30 minutes

---

### Task 3.5: Create Repository Implementation - JobPositionComment
**File**: `src/job_position/infrastructure/repositories/job_position_comment_repository.py`
- [ ] Create `JobPositionCommentRepository` class implementing interface
- [ ] Implement `save()` with model ↔ entity conversion
- [ ] Implement `get_by_id()` with expanded data (JOIN user, workflow, stage)
- [ ] Implement `list_by_job_position()` with expanded data, order by created_at DESC
- [ ] Implement `list_by_stage_and_global()` ⭐:
  ```sql
  WHERE job_position_id = ? AND (stage_id = ? OR stage_id IS NULL)
  ORDER BY created_at DESC
  ```
- [ ] Implement `list_global_only()`:
  ```sql
  WHERE job_position_id = ? AND stage_id IS NULL
  ORDER BY created_at DESC
  ```
- [ ] Implement `delete()`
- [ ] Implement `count_pending_by_job_position()`:
  ```sql
  WHERE job_position_id = ? AND review_status = 'pending'
  ```
- [ ] Add `_to_domain()` method (Model → Entity)
- [ ] Add `_to_model()` method (Entity → Model)

**Estimated Time**: 2 hours

---

### Task 3.6: Create Repository Implementation - JobPositionActivity
**File**: `src/job_position/infrastructure/repositories/job_position_activity_repository.py`
- [ ] Create `JobPositionActivityRepository` class implementing interface
- [ ] Implement `save()` with model ↔ entity conversion
- [ ] Implement `list_by_job_position()` with:
  - JOIN to get user name/email
  - ORDER BY created_at DESC
  - LIMIT parameter
- [ ] Add `_to_domain()` method (Model → Entity)
- [ ] Add `_to_model()` method (Entity → Model)

**Estimated Time**: 1 hour

---

## Phase 4: Backend - Application Layer (Comments)

### Task 4.1: Create DTO - JobPositionCommentDto
**File**: `src/job_position/application/dtos/job_position_comment_dto.py`
- [ ] Create dataclass with all entity fields
- [ ] Add expanded data fields:
  - `workflow_name: Optional[str]`
  - `stage_name: Optional[str]`
  - `created_by_user_name: Optional[str]`
  - `created_by_user_email: Optional[str]`
  - `is_global: bool` (computed from stage_id)

**Estimated Time**: 20 minutes

---

### Task 4.2: Create Mapper - JobPositionComment
**File**: `src/job_position/application/mappers/job_position_comment_mapper.py`
- [ ] Create `JobPositionCommentMapper` class
- [ ] Implement `entity_to_dto()` static method
- [ ] Calculate `is_global` field (stage_id is None)

**Estimated Time**: 15 minutes

---

### Task 4.3: Create Command - CreateJobPositionComment
**File**: `src/job_position/application/commands/create_job_position_comment_command.py`
- [ ] Create `CreateJobPositionCommentCommand` dataclass
- [ ] Create `CreateJobPositionCommentCommandHandler`
- [ ] Handler logic:
  - Create comment entity
  - Save via repository
  - Create activity: COMMENT_ADDED
  - Dispatch activity command

**Estimated Time**: 45 minutes

---

### Task 4.4: Create Command - UpdateJobPositionComment
**File**: `src/job_position/application/commands/update_job_position_comment_command.py`
- [ ] Create `UpdateJobPositionCommentCommand` dataclass
- [ ] Create `UpdateJobPositionCommentCommandHandler`
- [ ] Handler logic:
  - Load comment
  - Update comment
  - Save via repository

**Estimated Time**: 30 minutes

---

### Task 4.5: Create Command - DeleteJobPositionComment
**File**: `src/job_position/application/commands/delete_job_position_comment_command.py`
- [ ] Create `DeleteJobPositionCommentCommand` dataclass
- [ ] Create `DeleteJobPositionCommentCommandHandler`
- [ ] Handler logic: Delete via repository

**Estimated Time**: 20 minutes

---

### Task 4.6: Create Command - MarkJobPositionCommentAsPending
**File**: `src/job_position/application/commands/mark_job_position_comment_as_pending_command.py`
- [ ] Create `MarkJobPositionCommentAsPendingCommand` dataclass
- [ ] Create handler
- [ ] Handler logic:
  - Load comment
  - Call `mark_as_pending()`
  - Save

**Estimated Time**: 25 minutes

---

### Task 4.7: Create Command - MarkJobPositionCommentAsReviewed
**File**: `src/job_position/application/commands/mark_job_position_comment_as_reviewed_command.py`
- [ ] Create `MarkJobPositionCommentAsReviewedCommand` dataclass
- [ ] Create handler
- [ ] Handler logic:
  - Load comment
  - Call `mark_as_reviewed()`
  - Save

**Estimated Time**: 25 minutes

---

### Task 4.8: Create Query - GetJobPositionCommentById
**File**: `src/job_position/application/queries/get_job_position_comment_by_id.py`
- [ ] Create `GetJobPositionCommentByIdQuery` dataclass
- [ ] Create handler returning `Optional[JobPositionCommentDto]`
- [ ] Use repository, map to DTO

**Estimated Time**: 20 minutes

---

### Task 4.9: Create Query - ListJobPositionCommentsByJobPosition
**File**: `src/job_position/application/queries/list_job_position_comments_by_job_position.py`
- [ ] Create query dataclass
- [ ] Create handler returning `List[JobPositionCommentDto]`
- [ ] For "Comments" tab (all comments)

**Estimated Time**: 20 minutes

---

### Task 4.10: Create Query - ListJobPositionCommentsCurrentAndGlobal ⭐
**File**: `src/job_position/application/queries/list_job_position_comments_current_and_global.py`
- [ ] Create query dataclass with `job_position_id` and `stage_id`
- [ ] Create handler returning `List[JobPositionCommentDto]`
- [ ] Use `list_by_stage_and_global()` repository method
- [ ] For "Current Comments" section

**Estimated Time**: 25 minutes

---

### Task 4.11: Create Query - CountPendingJobPositionComments
**File**: `src/job_position/application/queries/count_pending_job_position_comments_query.py`
- [ ] Create query dataclass
- [ ] Create handler returning `int`
- [ ] Use repository count method

**Estimated Time**: 15 minutes

---

## Phase 5: Backend - Application Layer (Activities)

### Task 5.1: Create DTO - JobPositionActivityDto
**File**: `src/job_position/application/dtos/job_position_activity_dto.py`
- [ ] Create dataclass with all entity fields
- [ ] Add expanded data fields:
  - `performed_by_user_name: Optional[str]`
  - `performed_by_user_email: Optional[str]`

**Estimated Time**: 15 minutes

---

### Task 5.2: Create Mapper - JobPositionActivity
**File**: `src/job_position/application/mappers/job_position_activity_mapper.py`
- [ ] Create `JobPositionActivityMapper` class
- [ ] Implement `entity_to_dto()` static method

**Estimated Time**: 15 minutes

---

### Task 5.3: Create Command - CreateJobPositionActivity
**File**: `src/job_position/application/commands/create_job_position_activity_command.py`
- [ ] Create `CreateJobPositionActivityCommand` dataclass
- [ ] Create handler
- [ ] Handler logic: Create and save activity

**Estimated Time**: 30 minutes

---

### Task 5.4: Create Query - ListJobPositionActivities
**File**: `src/job_position/application/queries/list_job_position_activities_query.py`
- [ ] Create query dataclass with `job_position_id` and optional `limit`
- [ ] Create handler returning `List[JobPositionActivityDto]`
- [ ] Default limit: 50

**Estimated Time**: 20 minutes

---

### Task 5.5: Update Existing Commands - Activity Logging
**Files to update**:
1. `src/job_position/application/commands/update_job_position.py`
2. `src/job_position/application/commands/move_job_position_to_stage.py` (if exists)

- [ ] In `UpdateJobPositionCommand` handler:
  - After update, create activity: EDITED
  - Track changed fields in metadata
  - Dispatch `CreateJobPositionActivityCommand`
  
- [ ] In stage move handler:
  - After move, create activity: STAGE_MOVED
  - Track old/new stage in metadata
  - Dispatch `CreateJobPositionActivityCommand`

**Estimated Time**: 1 hour

---

## Phase 6: Backend - Presentation Layer

### Task 6.1: Create Request Schema - CreateJobPositionComment
**File**: `src/job_position/presentation/schemas/create_job_position_comment_request.py`
- [ ] Create Pydantic model with fields:
  - `comment: str`
  - `stage_id: Optional[str] = None` ⭐ (NULL = global)
  - `workflow_id: Optional[str] = None`
  - `visibility: str = "private"`
  - `review_status: str = "reviewed"`
- [ ] Add validation
- [ ] Add example in Config

**Estimated Time**: 20 minutes

---

### Task 6.2: Create Request Schema - UpdateJobPositionComment
**File**: `src/job_position/presentation/schemas/update_job_position_comment_request.py`
- [ ] Create Pydantic model with fields:
  - `comment: str`
  - `visibility: str`

**Estimated Time**: 15 minutes

---

### Task 6.3: Create Response Schema - JobPositionComment
**File**: `src/job_position/presentation/schemas/job_position_comment_response.py`
- [ ] Create Pydantic model with all DTO fields
- [ ] Include expanded data
- [ ] Include `is_global: bool`

**Estimated Time**: 20 minutes

---

### Task 6.4: Create Response Schema - JobPositionActivity
**File**: `src/job_position/presentation/schemas/job_position_activity_response.py`
- [ ] Create Pydantic model with all DTO fields
- [ ] Include expanded data

**Estimated Time**: 15 minutes

---

### Task 6.5: Create Response Mapper - JobPositionComment
**File**: `src/job_position/presentation/mappers/job_position_comment_mapper.py`
- [ ] Create `JobPositionCommentResponseMapper` class
- [ ] Implement `dto_to_response()` static method

**Estimated Time**: 15 minutes

---

### Task 6.6: Create Response Mapper - JobPositionActivity
**File**: `src/job_position/presentation/mappers/job_position_activity_mapper.py`
- [ ] Create `JobPositionActivityResponseMapper` class
- [ ] Implement `dto_to_response()` static method

**Estimated Time**: 15 minutes

---

### Task 6.7: Create Controller - JobPositionComment
**File**: `src/job_position/presentation/controllers/job_position_comment_controller.py`
- [ ] Create controller class with `__init__(command_bus, query_bus)`
- [ ] Implement methods:
  - `create_comment(job_position_id, request, created_by_user_id)` → Response
  - `get_comment_by_id(comment_id)` → Optional[Response]
  - `list_all_comments(job_position_id)` → List[Response]
  - `list_current_and_global_comments(job_position_id, stage_id)` → List[Response] ⭐
  - `count_pending_comments(job_position_id)` → int
  - `update_comment(comment_id, request)` → Optional[Response]
  - `delete_comment(comment_id)` → None
  - `mark_as_pending(comment_id)` → Response
  - `mark_as_reviewed(comment_id)` → Response

**Estimated Time**: 1.5 hours

---

### Task 6.8: Create Controller - JobPositionActivity
**File**: `src/job_position/presentation/controllers/job_position_activity_controller.py`
- [ ] Create controller class
- [ ] Implement method:
  - `list_activities(job_position_id, limit=50)` → List[Response]

**Estimated Time**: 30 minutes

---

### Task 6.9: Create Router Endpoints - Comments
**File**: `adapters/http/admin/job_position_routes.py` (or new file)
- [ ] Add comment endpoints under `/api/company/positions/{job_position_id}/comments`:
  - `POST /` - Create comment
  - `GET /` - List all comments
  - `GET /current` - List current + global ⭐
  - `GET /pending/count` - Count pending
  - `GET /{comment_id}` - Get single
  - `PUT /{comment_id}` - Update
  - `DELETE /{comment_id}` - Delete
  - `POST /{comment_id}/mark-pending` - Mark as pending
  - `POST /{comment_id}/mark-reviewed` - Mark as reviewed

**Estimated Time**: 1.5 hours

---

### Task 6.10: Create Router Endpoints - Activities
**File**: Same as above or new file
- [ ] Add activity endpoint:
  - `GET /api/company/positions/{job_position_id}/activities` - List activities

**Estimated Time**: 20 minutes

---

### Task 6.11: Register in Container
**File**: `core/container.py`
- [ ] Register `JobPositionCommentRepository`
- [ ] Register `JobPositionActivityRepository`
- [ ] Register all comment command handlers
- [ ] Register all comment query handlers
- [ ] Register activity command handler
- [ ] Register activity query handler
- [ ] Register `JobPositionCommentController`
- [ ] Register `JobPositionActivityController`

**Estimated Time**: 45 minutes

---

## Phase 7: Frontend - Types & Services

### Task 7.1: Create Types - JobPositionComment
**File**: `client-vite/src/types/jobPositionComment.ts`
- [ ] Create interfaces:
  - `JobPositionComment`
  - `CreateJobPositionCommentRequest`
  - `UpdateJobPositionCommentRequest`
- [ ] Create types:
  - `CommentReviewStatus = 'pending' | 'reviewed'`
  - `CommentVisibility = 'private' | 'shared_with_candidate'`

**Estimated Time**: 30 minutes

---

### Task 7.2: Create Types - JobPositionActivity
**File**: `client-vite/src/types/jobPositionActivity.ts`
- [ ] Create interface: `JobPositionActivity`
- [ ] Create type: `ActivityType` (union of all activity types)

**Estimated Time**: 20 minutes

---

### Task 7.3: Create Service - JobPositionComment
**File**: `client-vite/src/services/jobPositionCommentService.ts`
- [ ] Create service class with methods:
  - `createComment(jobPositionId, data)`
  - `getAllComments(jobPositionId)`
  - `getCurrentAndGlobalComments(jobPositionId, stageId)` ⭐
  - `getCommentById(commentId)`
  - `getPendingCount(jobPositionId)`
  - `updateComment(commentId, data)`
  - `deleteComment(commentId)`
  - `markAsPending(commentId)`
  - `markAsReviewed(commentId)`
- [ ] Export singleton instance

**Estimated Time**: 1 hour

---

### Task 7.4: Create Service - JobPositionActivity
**File**: `client-vite/src/services/jobPositionActivityService.ts`
- [ ] Create service class with method:
  - `getActivities(jobPositionId, limit?)`
- [ ] Export singleton instance

**Estimated Time**: 20 minutes

---

## Phase 8: Frontend - Components

### Task 8.1: Create Component - GlobalInfoTab
**File**: `client-vite/src/components/jobPosition/GlobalInfoTab.tsx`
- [ ] Create component displaying position common fields:
  - Title
  - Description (HTML)
  - Category
  - Visibility
  - Dates (open_at, application_deadline)
  - Public slug (if public)
- [ ] Read-only view
- [ ] Use Card/shadcn components

**Estimated Time**: 45 minutes

---

### Task 8.2: Create Component - AllCommentsTab
**File**: `client-vite/src/components/jobPosition/AllCommentsTab.tsx`
- [ ] Create component accepting props:
  - `comments: JobPositionComment[]`
  - `onTogglePending: (comment) => void`
- [ ] Group comments by stage + "Global"
- [ ] Display each comment with:
  - Author name
  - Timestamp
  - Comment text
  - Stage badge (or "Global" badge)
  - Workflow name
  - Toggle pending/reviewed button
- [ ] Highlight pending (yellow background)
- [ ] Empty state if no comments

**Estimated Time**: 1.5 hours

---

### Task 8.3: Create Component - ActivityHistoryTab
**File**: `client-vite/src/components/jobPosition/ActivityHistoryTab.tsx`
- [ ] Create component accepting props:
  - `activities: JobPositionActivity[]`
  - `loading: boolean`
- [ ] Display timeline of activities
- [ ] Show icon for each activity type:
  - CREATED: Plus
  - EDITED: Edit
  - STAGE_MOVED: ArrowRight
  - STATUS_CHANGED: RefreshCw
  - COMMENT_ADDED: MessageSquare
- [ ] Display:
  - Description
  - User name
  - Timestamp
  - Metadata details (if available)
- [ ] Empty state if no activities

**Estimated Time**: 1.5 hours

---

### Task 8.4: Create Component - CurrentCommentsSection
**File**: `client-vite/src/components/jobPosition/CurrentCommentsSection.tsx`
- [ ] Create component accepting props:
  - `jobPositionId: string`
  - `stageId: string | null`
  - `workflowId: string | null`
  - `onCommentChange: () => void`
- [ ] Load comments via `getCurrentAndGlobalComments()` ⭐
- [ ] Display existing comments:
  - Badge: "Global" or stage name
  - Author, timestamp
  - Comment text
  - Toggle pending/reviewed
- [ ] Add comment form:
  - Textarea
  - Checkbox: "Global comment (visible at all stages)" ⭐
  - Submit button
- [ ] When submitting:
  - If checkbox checked: `stage_id = null`
  - Otherwise: `stage_id = currentStageId`
- [ ] Highlight pending comments (yellow)
- [ ] Call `onCommentChange` after add/update

**Estimated Time**: 2 hours

---

## Phase 9: Frontend - Integration

### Task 9.1: Update PositionDetailPage - Add State Management
**File**: `client-vite/src/pages/company/PositionDetailPage.tsx`
- [ ] Add state:
  ```typescript
  const [activeTab, setActiveTab] = useState<'global' | 'comments' | 'history'>('global');
  const [allComments, setAllComments] = useState<JobPositionComment[]>([]);
  const [pendingCount, setPendingCount] = useState(0);
  const [activities, setActivities] = useState<JobPositionActivity[]>([]);
  const [loadingComments, setLoadingComments] = useState(false);
  const [loadingActivities, setLoadingActivities] = useState(false);
  ```

**Estimated Time**: 15 minutes

---

### Task 9.2: Update PositionDetailPage - Add Data Loading
**File**: Same as above
- [ ] Create `loadAllComments()` function:
  - Call `jobPositionCommentService.getAllComments()`
  - Set `allComments` state
- [ ] Create `loadPendingCount()` function:
  - Call `jobPositionCommentService.getPendingCount()`
  - Set `pendingCount` state
- [ ] Create `loadActivities()` function:
  - Call `jobPositionActivityService.getActivities()`
  - Set `activities` state
- [ ] Call these on mount and when tab changes

**Estimated Time**: 30 minutes

---

### Task 9.3: Update PositionDetailPage - Add Tabbed Interface
**File**: Same as above
- [ ] Replace current layout with:
  - Header (keep existing)
  - **Upper Card with Tabs**:
    ```tsx
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
          <GlobalInfoTab position={position} />
        </TabsContent>
        <TabsContent value="comments">
          <AllCommentsTab 
            comments={allComments}
            onTogglePending={handleTogglePending}
          />
        </TabsContent>
        <TabsContent value="history">
          <ActivityHistoryTab 
            activities={activities}
            loading={loadingActivities}
          />
        </TabsContent>
      </Tabs>
    </Card>
    ```
  - **Lower Section (2 columns)**:
    ```tsx
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card>
        <CardHeader>Custom Fields</CardHeader>
        <CardContent>
          <DynamicCustomFields ... />
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>Current Comments</CardHeader>
        <CardContent>
          <CurrentCommentsSection 
            jobPositionId={position.id}
            stageId={position.stage_id}
            workflowId={position.job_position_workflow_id}
            onCommentChange={loadAllComments}
          />
        </CardContent>
      </Card>
    </div>
    ```

**Estimated Time**: 1.5 hours

---

### Task 9.4: Update PositionDetailPage - Add Event Handlers
**File**: Same as above
- [ ] Implement `handleTogglePending(comment)`:
  - Call `markAsPending()` or `markAsReviewed()`
  - Reload all comments
  - Reload pending count
- [ ] Ensure `onCommentChange` callback reloads data

**Estimated Time**: 30 minutes

---

## Phase 10: Testing & Deployment

### Task 10.1: Backend Unit Tests
- [ ] Test `JobPositionComment` entity methods
- [ ] Test `JobPositionActivity` entity methods
- [ ] Test `is_global()` property
- [ ] Test activity factory methods

**Estimated Time**: 1.5 hours

---

### Task 10.2: Backend Integration Tests
- [ ] Test comment repository methods
- [ ] Test `list_by_stage_and_global()` query ⭐
- [ ] Test activity repository
- [ ] Test command handlers
- [ ] Test query handlers

**Estimated Time**: 2 hours

---

### Task 10.3: Backend API Tests
- [ ] Test all comment endpoints
- [ ] Test activity endpoint
- [ ] Test creating global comment (stage_id=null)
- [ ] Test filtering current + global comments
- [ ] Test pending/reviewed status changes

**Estimated Time**: 1.5 hours

---

### Task 10.4: Frontend Component Tests
- [ ] Test `CurrentCommentsSection` rendering
- [ ] Test global comment checkbox
- [ ] Test tab switching
- [ ] Test activity timeline

**Estimated Time**: 1 hour

---

### Task 10.5: End-to-End Testing
- [ ] Test complete flow:
  - Add global comment
  - Add stage comment
  - Move to different stage
  - Verify only current + global visible in lower section
  - Verify all visible in Comments tab
  - Verify activities logged
  - Mark comment as pending
  - Verify pending count updates

**Estimated Time**: 1 hour

---

### Task 10.6: Run Migrations
- [ ] Run `make migrate` in dev/staging
- [ ] Verify tables created correctly
- [ ] Verify indexes exist
- [ ] Verify FKs work

**Estimated Time**: 30 minutes

---

### Task 10.7: Deploy Backend
- [ ] Deploy backend changes
- [ ] Verify API endpoints work
- [ ] Check logs for errors

**Estimated Time**: 30 minutes

---

### Task 10.8: Deploy Frontend
- [ ] Build frontend: `npm run build`
- [ ] Deploy
- [ ] Verify UI renders correctly
- [ ] Test all interactions

**Estimated Time**: 30 minutes

---

## Summary Checklist

### Backend
- [ ] Phase 1: Domain Layer - Comments (4 tasks) - **~2 hours**
- [ ] Phase 2: Domain Layer - Activities (4 tasks) - **~2 hours**
- [ ] Phase 3: Infrastructure Layer (6 tasks) - **~5 hours**
- [ ] Phase 4: Application Layer - Comments (11 tasks) - **~5 hours**
- [ ] Phase 5: Application Layer - Activities (5 tasks) - **~2.5 hours**
- [ ] Phase 6: Presentation Layer (11 tasks) - **~6.5 hours**

**Backend Total**: ~23 hours

### Frontend
- [ ] Phase 7: Types & Services (4 tasks) - **~2.5 hours**
- [ ] Phase 8: Components (4 tasks) - **~5.5 hours**
- [ ] Phase 9: Integration (4 tasks) - **~2.5 hours**

**Frontend Total**: ~10.5 hours

### Testing & Deployment
- [ ] Phase 10: Testing & Deployment (8 tasks) - **~8.5 hours**

**Testing Total**: ~8.5 hours

---

## Grand Total: ~42 hours

**Note**: Original estimate was 18-24 hours. Revised estimate with detailed breakdown is ~42 hours. This is more realistic accounting for:
- Complete activity logging system
- Comprehensive testing
- All CRUD operations
- Proper error handling
- UI polish

---

## Next Steps

1. ✅ Review this task list
2. ✅ Confirm approach
3. ⏸️ Begin Phase 1 implementation
4. ⏸️ Iterate through phases sequentially
5. ⏸️ Test at each phase completion
6. ⏸️ Deploy when all phases complete

---

## Notes

⭐ = Critical/unique features
- Global comments (stage_id = NULL)
- Filtering current + global comments
- Activity logging system
- Tabbed UI interface

