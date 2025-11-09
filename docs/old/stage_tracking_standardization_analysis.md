# Stage Tracking Standardization Analysis

## Current State

### CandidateApplication - Has Dedicated Stage Tracking

**Entity: `CandidateApplicationStage`**
- **Purpose**: Tracks a candidate's progression through a phase/workflow/stage
- **Location**: `src/candidate_application_stage/domain/entities/candidate_application_stage.py`
- **Fields**:
  - `id`: CandidateApplicationStageId
  - `candidate_application_id`: CandidateApplicationId
  - `phase_id`: Optional[PhaseId]
  - `workflow_id`: Optional[WorkflowId]
  - `stage_id`: Optional[WorkflowStageId]
  - `started_at`: datetime
  - `completed_at`: Optional[datetime]
  - `deadline`: Optional[datetime]
  - `estimated_cost`: Optional[Decimal]
  - `actual_cost`: Optional[Decimal]
  - `comments`: Optional[str]
  - `data`: Optional[Dict[str, Any]]
  - `created_at`: datetime
  - `updated_at`: datetime

**Key Features**:
- Tracks time spent in each stage (`started_at`, `completed_at`)
- Tracks deadlines and overdue status
- Tracks costs (estimated vs actual)
- Has a `comments` field for stage-specific notes
- Has a `data` field for custom JSON data
- Methods: `create()`, `complete()`, `update_data()`, `is_completed()`, `is_overdue()`

**Database Table**: `candidate_application_stages`

---

### JobPosition - Uses Activity Log + Comments

**Entity 1: `JobPositionActivity`**
- **Purpose**: Tracks general activities/interactions on a job position
- **Location**: `src/job_position/domain/entities/job_position_activity.py`
- **Fields**:
  - `id`: JobPositionActivityId
  - `job_position_id`: JobPositionId
  - `activity_type`: ActivityTypeEnum (CREATED, EDITED, STAGE_MOVED, STATUS_CHANGED, COMMENT_ADDED)
  - `description`: str
  - `performed_by_user_id`: CompanyUserId
  - `metadata`: Dict[str, Any]
  - `created_at`: datetime

**Key Features**:
- Generic activity tracking (not stage-specific)
- Tracks who did what and when
- Uses `metadata` JSON for additional details
- Factory methods: `from_edit()`, `from_stage_move()`, `from_status_change()`, `from_comment_added()`

**Database Table**: `job_position_activities`

**Entity 2: `JobPositionComment`**
- **Purpose**: Structured comments on job positions
- **Location**: `src/job_position/domain/entities/job_position_comment.py`
- **Fields**:
  - `id`: JobPositionCommentId
  - `job_position_id`: JobPositionId
  - `comment`: str
  - `workflow_id`: Optional[JobPositionWorkflowId]
  - `stage_id`: Optional[str] (NULL = global comment)
  - `created_by_user_id`: CompanyUserId
  - `review_status`: CommentReviewStatusEnum
  - `visibility`: CommentVisibilityEnum
  - `created_at`: datetime
  - `updated_at`: datetime

**Key Features**:
- Supports global comments (`stage_id = NULL`) and stage-specific comments
- Has review status (PENDING, REVIEWED)
- Has visibility settings (PRIVATE, SHARED)

**Database Table**: `job_position_comments`

---

## Problem Statement

**Inconsistency**: 
- `CandidateApplication` has a dedicated `CandidateApplicationStage` entity that tracks detailed stage information (time, costs, deadlines, comments)
- `JobPosition` does NOT have a similar `JobPositionStage` entity
- Instead, `JobPosition` uses:
  - `JobPositionActivity` for general activity tracking (but doesn't track stage-specific metrics like time, costs, deadlines)
  - `JobPositionComment` for comments (but comments are separate from stage tracking)

**Missing in JobPosition**:
1. ❌ No tracking of time spent in each stage (`started_at`, `completed_at`)
2. ❌ No tracking of stage deadlines
3. ❌ No tracking of estimated vs actual costs per stage
4. ❌ No dedicated stage-specific data storage
5. ❌ No way to query "all stages this position has been through" easily

**Current Workaround**:
- `JobPositionActivity` with `STAGE_MOVED` type tracks stage transitions, but:
  - Only records the transition event (who moved it, when, from/to)
  - Doesn't track time spent in each stage
  - Doesn't track costs or deadlines
  - Doesn't provide easy querying of "current stage history"

---

## Proposed Solution: Create `JobPositionStage`

### Goal
Standardize stage tracking across both `CandidateApplication` and `JobPosition` by creating a `JobPositionStage` entity that mirrors `CandidateApplicationStage`.

### Benefits
1. ✅ **Consistency**: Both entities use the same pattern for stage tracking
2. ✅ **Complete History**: Track full stage progression history for job positions
3. ✅ **Time Tracking**: Know how long a position spent in each stage
4. ✅ **Cost Tracking**: Track estimated vs actual costs per stage
5. ✅ **Deadline Management**: Track deadlines per stage
6. ✅ **Analytics**: Better analytics on stage performance (average time, bottlenecks, etc.)
7. ✅ **Query Simplicity**: Easy to query "all stages this position has been through"

### Entity Design

**New Entity: `JobPositionStage`**
- **Location**: `src/job_position/domain/entities/job_position_stage.py`
- **Fields** (mirroring `CandidateApplicationStage`):
  ```python
  id: JobPositionStageId
  job_position_id: JobPositionId
  phase_id: Optional[PhaseId]
  workflow_id: Optional[WorkflowId]
  stage_id: Optional[WorkflowStageId]
  started_at: datetime
  completed_at: Optional[datetime]
  deadline: Optional[datetime]
  estimated_cost: Optional[Decimal]
  actual_cost: Optional[Decimal]
  comments: Optional[str]  # Stage-specific notes
  data: Optional[Dict[str, Any]]  # Custom JSON data
  created_at: datetime
  updated_at: datetime
  ```

**Methods**:
- `create()` - Factory method
- `complete()` - Mark stage as completed
- `update_data()` - Update custom data
- `is_completed()` - Check if completed
- `is_overdue()` - Check if overdue

**Database Table**: `job_position_stages`

---

## Migration Strategy

### Phase 1: Create New Entity (Non-Breaking)

1. **Domain Layer**:
   - Create `JobPositionStageId` value object
   - Create `JobPositionStage` entity
   - Create `JobPositionStageRepositoryInterface`

2. **Infrastructure Layer**:
   - Create `JobPositionStageModel` (SQLAlchemy)
   - Create `JobPositionStageRepository` implementation
   - Create Alembic migration for `job_position_stages` table

3. **Application Layer**:
   - Create DTOs for `JobPositionStage`
   - Create Commands: `CreateJobPositionStageCommand`, `CompleteJobPositionStageCommand`
   - Create Queries: `GetJobPositionStagesQuery`, `GetCurrentJobPositionStageQuery`

### Phase 2: Integrate with Existing Workflows

1. **Update Stage Movement Logic**:
   - When a `JobPosition` moves to a new stage:
     - Complete the previous `JobPositionStage` (if exists)
     - Create a new `JobPositionStage` for the new stage
   - Update `MoveJobPositionToStageCommand` to handle this

2. **Backfill Existing Data**:
   - Create a migration script to backfill `job_position_stages` from:
     - `JobPositionActivity` records with `STAGE_MOVED` type
     - Current `JobPosition.stage_id` to create "current" stage record

### Phase 3: Update APIs and Frontend

1. **API Endpoints**:
   - `GET /api/job-positions/{id}/stages` - List all stages
   - `GET /api/job-positions/{id}/stages/current` - Get current stage
   - `POST /api/job-positions/{id}/stages/{stage_id}/complete` - Complete a stage

2. **Frontend Updates**:
   - Display stage history timeline
   - Show time spent in each stage
   - Show costs per stage
   - Show deadlines and overdue status

### Phase 4: Deprecate/Refactor (Optional)

1. **Keep `JobPositionActivity`**:
   - Still useful for general activity tracking (CREATED, EDITED, STATUS_CHANGED, COMMENT_ADDED)
   - `STAGE_MOVED` activities can reference `JobPositionStage` records

2. **Keep `JobPositionComment`**:
   - Still useful for structured comments with review status and visibility
   - `JobPositionStage.comments` is for quick stage-specific notes
   - Can link comments to stages via `stage_id`

---

## Relationship Between Entities

### After Standardization

**JobPosition** has:
1. **`JobPositionStage`** (NEW):
   - Detailed stage tracking (time, costs, deadlines)
   - Stage-specific notes (`comments` field)
   - Custom data (`data` field)

2. **`JobPositionActivity`** (KEEP):
   - General activity log (CREATED, EDITED, STATUS_CHANGED, COMMENT_ADDED)
   - `STAGE_MOVED` activities can reference `JobPositionStage.id` in metadata

3. **`JobPositionComment`** (KEEP):
   - Structured comments with review status and visibility
   - Can be global (`stage_id = NULL`) or stage-specific (`stage_id != NULL`)
   - More formal than `JobPositionStage.comments`

**Usage Guidelines**:
- Use `JobPositionStage` for: time tracking, cost tracking, deadlines, stage progression history
- Use `JobPositionActivity` for: general activity log, audit trail
- Use `JobPositionComment` for: formal comments requiring review/visibility controls

---

## Database Schema

### New Table: `job_position_stages`

```sql
CREATE TABLE job_position_stages (
    id VARCHAR(26) PRIMARY KEY,
    job_position_id VARCHAR(26) NOT NULL REFERENCES job_positions(id) ON DELETE CASCADE,
    phase_id VARCHAR(26) REFERENCES company_phases(id) ON DELETE SET NULL,
    workflow_id VARCHAR(26) REFERENCES workflows(id) ON DELETE SET NULL,
    stage_id VARCHAR(26) REFERENCES workflow_stages(id) ON DELETE SET NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    deadline TIMESTAMP,
    estimated_cost NUMERIC(10, 2),
    actual_cost NUMERIC(10, 2),
    comments TEXT,
    data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Indexes
    INDEX idx_job_position_stages_job_position_id (job_position_id),
    INDEX idx_job_position_stages_stage_id (stage_id),
    INDEX idx_job_position_stages_started_at (started_at),
    INDEX idx_job_position_stages_completed_at (completed_at)
);
```

---

## Implementation Checklist

### Domain Layer
- [ ] Create `JobPositionStageId` value object
- [ ] Create `JobPositionStage` entity with all methods
- [ ] Create `JobPositionStageRepositoryInterface`

### Infrastructure Layer
- [ ] Create `JobPositionStageModel` (SQLAlchemy)
- [ ] Create `JobPositionStageRepository` implementation
- [ ] Create Alembic migration for `job_position_stages` table
- [ ] Register repository in DI container

### Application Layer
- [ ] Create `JobPositionStageDto`
- [ ] Create `CreateJobPositionStageCommand` and handler
- [ ] Create `CompleteJobPositionStageCommand` and handler
- [ ] Create `GetJobPositionStagesQuery` and handler
- [ ] Create `GetCurrentJobPositionStageQuery` and handler
- [ ] Update `MoveJobPositionToStageCommand` to create/complete stages

### Presentation Layer
- [ ] Create `JobPositionStageResponse` schema
- [ ] Create `CreateJobPositionStageRequest` schema
- [ ] Create `CompleteJobPositionStageRequest` schema
- [ ] Create `JobPositionStageController`
- [ ] Create `JobPositionStageRouter` with endpoints
- [ ] Register controller in DI container

### Data Migration
- [ ] Create backfill script to populate `job_position_stages` from:
  - `JobPositionActivity` records (STAGE_MOVED)
  - Current `JobPosition.stage_id`

### Testing
- [ ] Unit tests for `JobPositionStage` entity
- [ ] Unit tests for repository
- [ ] Integration tests for commands/queries
- [ ] API endpoint tests
- [ ] Frontend integration tests

---

## Update: JobPositionComment Relationship

**IMPORTANT**: `JobPositionComment` should be updated to reference `JobPositionStage`:

### Current Structure
- `JobPositionComment.stage_id`: Points to `workflow_stages.id` (stage type, not instance)

### Updated Structure
- `JobPositionComment.job_position_stage_id`: NEW - Points to `job_position_stages.id` (specific stage instance)
- `JobPositionComment.stage_id`: KEEP - Points to `workflow_stages.id` (for global comments or comments that apply to any instance)

### Benefits
1. **Historical Accuracy**: Know exactly which stage instance the comment belongs to
2. **Better Context**: Link comments to specific time periods, costs, and deadlines
3. **Flexibility**: Still support global comments and stage-type comments

### Migration
- Add `job_position_stage_id` column to `job_position_comments` table
- Update entity, model, and repository
- Backfill: For existing comments with `stage_id`, try to find matching `JobPositionStage` record

---

## Open Questions

1. **Should we migrate existing `JobPositionActivity` STAGE_MOVED records to `JobPositionStage`?**
   - **Recommendation**: Yes, create a backfill script

2. **Should `JobPositionStage.comments` replace `JobPositionComment` for stage-specific comments?**
   - **Recommendation**: No, keep both:
     - `JobPositionStage.comments`: Quick notes, informal
     - `JobPositionComment`: Formal comments with review status and visibility
   - **UPDATE**: `JobPositionComment` should reference `JobPositionStage` via `job_position_stage_id`

3. **Should we track costs for job positions?**
   - **Recommendation**: Yes, for consistency and future analytics (e.g., cost per hire)

4. **Should we track deadlines for job positions?**
   - **Recommendation**: Yes, useful for SLA tracking and workflow management

5. **How to handle positions that are already in a stage?**
   - **Recommendation**: Create a "current" `JobPositionStage` record with `completed_at = NULL` during backfill

6. **Should `JobPositionComment` have both `job_position_stage_id` and `stage_id`?**
   - **Recommendation**: Yes:
     - `job_position_stage_id`: For comments specific to a stage instance
     - `stage_id`: For comments that apply to any instance of that stage type (or global if both NULL)

---

## Next Steps

1. Review and approve this analysis
2. Create implementation task list
3. Begin Phase 1 implementation (Domain Layer)
4. Test with sample data
5. Proceed with remaining phases

