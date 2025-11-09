# Stage Tracking Standardization - Implementation Tasks

## Overview
This document contains the detailed, executable tasks to standardize stage tracking between `CandidateApplication` and `JobPosition` by creating a `JobPositionStage` entity.

**Reference**: See `docs/stage_tracking_standardization_analysis.md` for the full analysis.

---

## Phase 1: Domain Layer

### Task 1.1: Create Value Object
- **File**: `src/job_position/domain/value_objects/job_position_stage_id.py`
- **Action**: Create `JobPositionStageId` value object
- **Details**:
  - Inherit from `BaseId`
  - Follow same pattern as `CandidateApplicationStageId`
- **Dependencies**: None

### Task 1.2: Create Entity
- **File**: `src/job_position/domain/entities/job_position_stage.py`
- **Action**: Create `JobPositionStage` entity
- **Details**:
  - Fields: `id`, `job_position_id`, `phase_id`, `workflow_id`, `stage_id`, `started_at`, `completed_at`, `deadline`, `estimated_cost`, `actual_cost`, `comments`, `data`, `created_at`, `updated_at`
  - Methods: `create()`, `complete()`, `update_data()`, `is_completed()`, `is_overdue()`
  - Follow same pattern as `CandidateApplicationStage`
  - Use Value Objects for IDs
- **Dependencies**: Task 1.1

### Task 1.3: Create Repository Interface
- **File**: `src/job_position/domain/infrastructure/job_position_stage_repository_interface.py`
- **Action**: Create abstract repository interface
- **Details**:
  - Methods: `save()`, `get_by_id()`, `get_by_job_position()`, `get_current_by_job_position()`, `list_by_job_position()`, `delete()`
  - Follow same pattern as `CandidateApplicationStageRepositoryInterface`
- **Dependencies**: Task 1.2

### Task 1.4: Update Domain Exports
- **File**: `src/job_position/domain/__init__.py` and related `__init__.py` files
- **Action**: Export new entity and value object
- **Dependencies**: Tasks 1.1, 1.2, 1.3

---

## Phase 2: Infrastructure Layer

### Task 2.1: Create SQLAlchemy Model
- **File**: `src/job_position/infrastructure/models/job_position_stage_model.py`
- **Action**: Create `JobPositionStageModel`
- **Details**:
  - Table: `job_position_stages`
  - Columns matching entity fields
  - Foreign keys: `job_position_id`, `phase_id`, `workflow_id`, `stage_id`
  - Indexes: `job_position_id`, `stage_id`, `started_at`, `completed_at`
  - Use `JSON` for `data` field
- **Dependencies**: Task 1.2

### Task 2.2: Create Repository Implementation
- **File**: `src/job_position/infrastructure/repositories/job_position_stage_repository.py`
- **Action**: Implement `JobPositionStageRepositoryInterface`
- **Details**:
  - Implement all interface methods
  - `_to_domain()` and `_to_model()` conversion methods
  - Handle `None` values for optional fields
- **Dependencies**: Tasks 1.3, 2.1

### Task 2.3: Create Alembic Migration
- **File**: `alembic/versions/XXXXX_add_job_position_stages_table.py`
- **Action**: Create migration for `job_position_stages` table
- **Details**:
  - Create table with all columns
  - Add foreign key constraints
  - Add indexes
  - Use `make revision m="add job_position_stages table"`
- **Dependencies**: Task 2.1

### Task 2.4: Update JobPositionComment Model
- **File**: `src/job_position/infrastructure/models/job_position_comment_model.py`
- **Action**: Add `job_position_stage_id` field
- **Details**:
  - Add `job_position_stage_id: Mapped[Optional[str]]` column
  - Foreign key to `job_position_stages.id` with `ON DELETE SET NULL`
  - Add index
  - Keep existing `stage_id` field for backward compatibility
- **Dependencies**: Task 2.1

### Task 2.5: Update JobPositionComment Entity
- **File**: `src/job_position/domain/entities/job_position_comment.py`
- **Action**: Add `job_position_stage_id` field
- **Details**:
  - Add `job_position_stage_id: Optional[JobPositionStageId]` field
  - Update `create()` method to accept optional `job_position_stage_id`
  - Keep existing `stage_id` field
- **Dependencies**: Tasks 1.1, 2.4

### Task 2.6: Create Migration for JobPositionComment Update
- **File**: `alembic/versions/XXXXX_add_job_position_stage_id_to_comments.py`
- **Action**: Add `job_position_stage_id` column to `job_position_comments` table
- **Details**:
  - Add column with foreign key constraint
  - Add index
  - Backfill: Try to match existing comments with `stage_id` to `JobPositionStage` records
- **Dependencies**: Tasks 2.3, 2.4

### Task 2.7: Register Repository in DI Container
- **File**: `core/container.py`
- **Action**: Register `job_position_stage_repository`
- **Details**:
  - Add import
  - Register as `providers.Factory`
- **Dependencies**: Task 2.2

### Task 2.8: Update JobPositionComment Repository
- **File**: `src/job_position/infrastructure/repositories/job_position_comment_repository.py`
- **Action**: Update to handle `job_position_stage_id`
- **Details**:
  - Update `_to_domain()` and `_to_model()` methods
  - Add query method: `list_by_job_position_stage(job_position_stage_id)`
- **Dependencies**: Tasks 2.5, 2.4

---

## Phase 3: Application Layer

### Task 3.1: Create DTO
- **File**: `src/job_position/application/dtos/job_position_stage_dto.py`
- **Action**: Create `JobPositionStageDto`
- **Details**:
  - Fields matching entity
  - `from_entity()` static method
  - Convert Value Objects to strings
- **Dependencies**: Task 1.2

### Task 3.2: Create Create Command
- **File**: `src/job_position/application/commands/create_job_position_stage_command.py`
- **Action**: Create `CreateJobPositionStageCommand` and handler
- **Details**:
  - Command with all required fields (use Value Objects for IDs)
  - Handler creates entity and saves via repository
  - Handler is void (no return)
- **Dependencies**: Tasks 1.2, 2.2, 3.1

### Task 3.3: Create Complete Command
- **File**: `src/job_position/application/commands/complete_job_position_stage_command.py`
- **Action**: Create `CompleteJobPositionStageCommand` and handler
- **Details**:
  - Command: `job_position_stage_id`, `completed_at` (optional), `actual_cost` (optional), `comments` (optional)
  - Handler loads entity, calls `complete()`, saves
- **Dependencies**: Tasks 1.2, 2.2, 3.1

### Task 3.4: Create Get Stages Query
- **File**: `src/job_position/application/queries/get_job_position_stages_query.py`
- **Action**: Create `GetJobPositionStagesQuery` and handler
- **Details**:
  - Query: `job_position_id: JobPositionId`
  - Handler returns `List[JobPositionStageDto]`
  - Order by `started_at DESC`
- **Dependencies**: Tasks 1.2, 2.2, 3.1

### Task 3.5: Create Get Current Stage Query
- **File**: `src/job_position/application/queries/get_current_job_position_stage_query.py`
- **Action**: Create `GetCurrentJobPositionStageQuery` and handler
- **Details**:
  - Query: `job_position_id: JobPositionId`
  - Handler returns `Optional[JobPositionStageDto]` (where `completed_at IS NULL`)
- **Dependencies**: Tasks 1.2, 2.2, 3.1

### Task 3.6: Update Create Comment Command
- **File**: `src/job_position/application/commands/create_job_position_comment_command.py`
- **Action**: Update to accept `job_position_stage_id`
- **Details**:
  - Add optional `job_position_stage_id: Optional[JobPositionStageId]` to command
  - Update handler to set the field when creating comment
- **Dependencies**: Tasks 2.5, 3.1

### Task 3.7: Update Move to Stage Command
- **File**: `src/job_position/application/commands/move_job_position_to_stage_command.py`
- **Action**: Update to create/complete `JobPositionStage` records
- **Details**:
  - When moving to a new stage:
    1. Get current `JobPositionStage` (if exists)
    2. Complete it (if exists)
    3. Create new `JobPositionStage` for new stage
  - Use `CommandBus` to dispatch `CompleteJobPositionStageCommand` and `CreateJobPositionStageCommand`
- **Dependencies**: Tasks 3.2, 3.3

### Task 3.8: Register Handlers in DI Container
- **File**: `core/container.py`
- **Action**: Register all command and query handlers
- **Details**:
  - Register `create_job_position_stage_command_handler`
  - Register `complete_job_position_stage_command_handler`
  - Register `get_job_position_stages_query_handler`
  - Register `get_current_job_position_stage_query_handler`
- **Dependencies**: Tasks 3.2, 3.3, 3.4, 3.5

---

## Phase 4: Presentation Layer

### Task 4.1: Create Response Schema
- **File**: `adapters/http/job_position/schemas/job_position_stage_schemas.py`
- **Action**: Create `JobPositionStageResponse` schema
- **Details**:
  - Fields matching DTO
  - Use Pydantic models
  - Include examples
- **Dependencies**: Task 3.1

### Task 4.2: Create Request Schemas
- **File**: `adapters/http/job_position/schemas/job_position_stage_schemas.py`
- **Action**: Create request schemas
- **Details**:
  - `CreateJobPositionStageRequest`
  - `CompleteJobPositionStageRequest`
  - Validation rules
- **Dependencies**: Task 3.1

### Task 4.2b: Update Comment Request Schema
- **File**: `adapters/http/job_position/schemas/job_position_comment_schemas.py` (or similar)
- **Action**: Add `job_position_stage_id` to `CreateJobPositionCommentRequest`
- **Details**:
  - Add optional `job_position_stage_id: Optional[str]` field
  - Update validation if needed
- **Dependencies**: Task 3.6

### Task 4.3: Create Controller
- **File**: `adapters/http/job_position/controllers/job_position_stage_controller.py`
- **Action**: Create `JobPositionStageController`
- **Details**:
  - Methods:
    - `create_stage(request)` - Create new stage
    - `complete_stage(stage_id, request)` - Complete a stage
    - `get_stages(job_position_id)` - List all stages
    - `get_current_stage(job_position_id)` - Get current stage
  - Use `CommandBus` and `QueryBus`
  - Convert DTOs to responses
- **Dependencies**: Tasks 3.2, 3.3, 3.4, 3.5, 4.1, 4.2

### Task 4.4: Create Router
- **File**: `adapters/http/job_position/routers/job_position_stage_router.py`
- **Action**: Create FastAPI router
- **Details**:
  - Endpoints:
    - `POST /api/job-positions/{job_position_id}/stages` - Create stage
    - `POST /api/job-positions/stages/{stage_id}/complete` - Complete stage
    - `GET /api/job-positions/{job_position_id}/stages` - List stages
    - `GET /api/job-positions/{job_position_id}/stages/current` - Get current stage
  - Use dependency injection for controller
- **Dependencies**: Task 4.3

### Task 4.5: Register Router in Main App
- **File**: `adapters/http/main.py` or similar
- **Action**: Include router in FastAPI app
- **Details**:
  - `app.include_router(job_position_stage_router)`
- **Dependencies**: Task 4.4

### Task 4.6: Register Controller in DI Container
- **File**: `core/container.py`
- **Action**: Register `job_position_stage_controller`
- **Details**:
  - Register as `providers.Factory`
- **Dependencies**: Task 4.3

---

## Phase 5: Data Migration

### Task 5.1: Create Backfill Script
- **File**: `scripts/backfill_job_position_stages.py`
- **Action**: Create script to populate `job_position_stages` from existing data
- **Details**:
  - Read `JobPositionActivity` records with `STAGE_MOVED` type
  - For each position, create `JobPositionStage` records:
    - Use `metadata` to get `old_stage_id` and `new_stage_id`
    - Use `created_at` as `started_at`
    - If there's a next stage move, use that `created_at` as `completed_at`
    - For current stage (no next move), create record with `completed_at = NULL`
  - Handle positions that are already in a stage (create current record)
- **Dependencies**: Tasks 2.3, 3.2

### Task 5.2: Test Backfill Script
- **Action**: Test script on development database
- **Details**:
  - Verify all positions have stage records
  - Verify current stages are marked correctly
  - Verify historical stages are created correctly
- **Dependencies**: Task 5.1

### Task 5.3: Backfill Comment Relationships
- **File**: `scripts/backfill_job_position_comment_stage_relationships.py`
- **Action**: Update existing comments to reference `JobPositionStage`
- **Details**:
  - For comments with `stage_id`, find matching `JobPositionStage` records
  - Update `job_position_stage_id` where possible
  - Keep `stage_id` for comments that can't be matched (global or historical)
- **Dependencies**: Tasks 2.6, 5.1

---

## Phase 6: Testing

### Task 6.1: Unit Tests - Entity
- **File**: `tests/job_position/domain/entities/test_job_position_stage.py`
- **Action**: Write unit tests for `JobPositionStage`
- **Details**:
  - Test `create()`
  - Test `complete()`
  - Test `update_data()`
  - Test `is_completed()`
  - Test `is_overdue()`
- **Dependencies**: Task 1.2

### Task 6.2: Unit Tests - Repository
- **File**: `tests/job_position/infrastructure/repositories/test_job_position_stage_repository.py`
- **Action**: Write unit tests for repository
- **Details**:
  - Test all repository methods
  - Use test database
- **Dependencies**: Task 2.2

### Task 6.3: Integration Tests - Commands/Queries
- **File**: `tests/job_position/application/test_job_position_stage_commands_queries.py`
- **Action**: Write integration tests
- **Details**:
  - Test `CreateJobPositionStageCommand`
  - Test `CompleteJobPositionStageCommand`
  - Test `GetJobPositionStagesQuery`
  - Test `GetCurrentJobPositionStageQuery`
- **Dependencies**: Tasks 3.2, 3.3, 3.4, 3.5

### Task 6.4: API Tests
- **File**: `tests/api/job_position/test_job_position_stage_endpoints.py`
- **Action**: Write API endpoint tests
- **Details**:
  - Test all endpoints
  - Test authentication/authorization
  - Test validation
- **Dependencies**: Task 4.4

---

## Phase 7: Frontend Integration (Optional - Future)

### Task 7.1: Create Frontend Types
- **File**: `client-vite/src/types/jobPositionStage.ts`
- **Action**: Create TypeScript types
- **Details**:
  - Interface matching `JobPositionStageResponse`
- **Dependencies**: Task 4.1

### Task 7.2: Create Frontend Service
- **File**: `client-vite/src/services/jobPositionStageService.ts`
- **Action**: Create service for API calls
- **Details**:
  - Methods for all endpoints
- **Dependencies**: Task 4.4, 7.1

### Task 7.3: Update UI Components
- **Files**: Various frontend components
- **Action**: Display stage history
- **Details**:
  - Show timeline of stages
  - Show time spent in each stage
  - Show costs and deadlines
- **Dependencies**: Tasks 7.1, 7.2

---

## Implementation Order

1. **Phase 1** (Domain Layer) - Foundation
2. **Phase 2** (Infrastructure Layer) - Persistence
3. **Phase 3** (Application Layer) - Business Logic
4. **Phase 4** (Presentation Layer) - API
5. **Phase 5** (Data Migration) - Backfill existing data
6. **Phase 6** (Testing) - Quality assurance
7. **Phase 7** (Frontend) - Optional, can be done later

---

## Notes

- Follow the same patterns as `CandidateApplicationStage`
- Use Value Objects for all IDs
- Ensure mutability (methods modify instance, return `None`)
- Register all components in DI container
- Write tests as you go
- Update documentation as needed

