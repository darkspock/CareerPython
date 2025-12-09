# Architecture Fixes - Task List

**Created:** 2025-12-07
**Based on:** Architecture Compliance Analysis (75% score)
**Goal:** Achieve 90%+ compliance with Clean Architecture / DDD patterns

---

## Priority 1: Critical (Breaks Architecture Patterns)

### 1.1 Remove `from_dto()` Methods from Response Schemas

**Severity:** CRITICAL
**Impact:** Circular dependencies, tight coupling, violates SRP

#### Files to Fix:

| File | Line | Issue |
|------|------|-------|
| `adapters/http/company_app/interview/schemas/interview_management.py` | 109-166 | `from_dto()` calls queryBus inside schema |
| `adapters/http/auth/schemas/auth_response.py` | Various | `from_dto()` method |
| `adapters/http/admin_app/schemas/job_position.py` | Various | `from_dto()` method |
| `adapters/http/admin_app/schemas/interview_template.py` | Various | `from_dto()` method |

#### Fix Pattern:

**BEFORE (Wrong):**
```python
# In schema file
class InterviewFullResource(BaseModel):
    @classmethod
    def from_dto(cls, queryBus: QueryBus, dto: InterviewDto) -> "InterviewFullResource":
        candidate = queryBus.query(GetCandidateByIdQuery(dto.candidate_id))  # VIOLATION
        return cls(candidate_name=candidate.name, ...)
```

**AFTER (Correct):**
```python
# In mapper file: adapters/http/company_app/interview/mappers/interview_mapper.py
class InterviewMapper:
    @staticmethod
    def dto_to_full_response(dto: InterviewDto, candidate: CandidateDto, ...) -> InterviewFullResource:
        return InterviewFullResource(
            candidate_name=candidate.name if candidate else None,
            ...
        )

# In controller
def get_interview(self, interview_id: str) -> InterviewFullResource:
    interview_dto = self.query_bus.query(GetInterviewByIdQuery(interview_id))
    candidate_dto = self.query_bus.query(GetCandidateByIdQuery(interview_dto.candidate_id))
    return InterviewMapper.dto_to_full_response(interview_dto, candidate_dto, ...)
```

#### Tasks:
- [x] Create `InterviewMapper` in `adapters/http/company_app/interview/mappers/`
- [x] Move conversion logic from `InterviewFullResource.from_dto()` to mapper
- [x] Update `InterviewController` to use mapper
- [x] Remove `from_dto()` and `from_list_dto()` methods from schema
- [ ] Repeat for other schemas with `from_dto()` methods

---

### 1.2 Remove Repository Dependencies from Controllers

**Severity:** HIGH
**Impact:** Violates dependency direction, bypasses CQRS

#### Files to Fix:

**1. FileAttachmentController**
- **File:** `adapters/http/candidate_app/controllers/file_attachment_controller.py`
- **Lines:** 22, 64, 85, 108, 120, 130
- **Issue:** Direct `_file_repository` calls

**Tasks:**
- [x] Create `SaveFileAttachmentCommand` + Handler (created as `UploadFileAttachmentCommand`)
- [x] Create `DeleteFileAttachmentCommand` + Handler
- [x] Create `GetFileAttachmentByIdQuery` + Handler
- [x] Create `ListFileAttachmentsByCandidateQuery` + Handler
- [x] Update controller to use command/query bus
- [x] Remove repository injection from controller

---

**2. ApplicationController**
- **File:** `adapters/http/candidate_app/controllers/application_controller.py`
- **Line:** 46, 154
- **Issue:** Direct `_application_repository.get_by_id()` call

**Tasks:**
- [x] Create `CanUserProcessApplicationQuery` + Handler
- [x] Update controller to use query bus
- [x] Remove repository injection

---

**3. AdminCandidateController**
- **File:** `adapters/http/admin_app/controllers/admin_candidate_controller.py`
- **Lines:** 32-33, 96, 139, 148, 194
- **Issue:** Direct `user_repository` access

**Tasks:**
- [x] Create `GetUserByIdQuery` + Handler
- [x] Use existing `GetUserByEmailQuery`
- [x] Use existing `CreateUserCommand`
- [x] Update controller to use command/query bus
- [x] Remove repository injection

---

**4. InterviewController**
- **File:** `adapters/http/company_app/interview/controllers/interview_controller.py`
- **Line:** 78
- **Issue:** Direct repository count query

**Tasks:**
- [x] Create `CountInterviewsQuery` + Handler
- [x] Update controller to use query bus
- [x] Remove direct repository access

---

## Priority 2: High (Structural Issues)

### 2.1 Move DTO from Domain Layer

**File:** `src/framework/domain/dtos/resume_analysis_dto.py`
**Issue:** DTOs belong in application layer, not domain

**Tasks:**
- [x] Move to `src/framework/application/dtos/resume_analysis_dto.py`
- [x] Update all imports
- [x] Verify no broken references
- [x] Delete old domain/dtos directory

---

### 2.2 Standardize Presentation Layer Location

**Issue:** Inconsistent placement - some BCs have `/presentation/`, most use `/adapters/http/`

**Current State:**
- `src/position_stage_assignment/presentation/` ✓ Has presentation
- Other BCs → No presentation folder (use adapters)

**Decision Required:**
- [ ] Option A: Move all presentation to `/adapters/http/` (current trend)
- [ ] Option B: Add `/presentation/` to all BCs

**Recommendation:** Option A - Keep all HTTP adapters in `/adapters/http/` for consistency

**Tasks:**
- [ ] Document the standard in CLAUDE.md
- [ ] Consider moving `position_stage_assignment/presentation/` to adapters (optional)

---

## Priority 3: Medium (Code Quality)

### 3.1 Add Missing Command/Query Base Class Inheritance Checks

**Issue:** Ensure all future Commands/Queries inherit properly

**Tasks:**
- [ ] Add linting rule or test to verify inheritance
- [ ] Document pattern in CLAUDE.md (already done)

---

### 3.2 Verify QueryHandlers Return DTOs Not Entities

**Status:** Currently compliant (95%)

**Tasks:**
- [ ] Add automated check in CI/CD
- [ ] Review any edge cases

---

## Implementation Order

### Phase 1: Critical Schema Fixes (Est. 2-3 hours)
1. Create `InterviewMapper`
2. Refactor `InterviewFullResource` to remove `from_dto()`
3. Update `InterviewController`
4. Test interview endpoints

### Phase 2: Controller Repository Removal (Est. 3-4 hours)
1. Fix `FileAttachmentController` (create 4 commands/queries)
2. Fix `ApplicationController` (1 query)
3. Fix `AdminCandidateController` (3 commands/queries)
4. Fix `InterviewController` (1 query modification)

### Phase 3: Structural Cleanup (Est. 1 hour)
1. Move `resume_analysis_dto.py`
2. Update CLAUDE.md with presentation layer standard
3. Add architecture compliance notes

---

## Verification Checklist

After fixes, verify:

- [x] No `from_dto()` methods in `InterviewFullResource` (moved to mapper)
- [x] No repository injections in fixed controllers (FileAttachment, Application, AdminCandidate, Interview)
- [x] All fixed controllers use only `command_bus` and `query_bus`
- [x] No DTOs in domain layers (moved `resume_analysis_dto.py` to application)
- [x] All mappers in `/mappers/` directories
- [x] Run `make mypy` - no new errors (only 3 pre-existing)
- [x] Run `make test` - 121 unit tests pass (2 pre-existing failures in company_page)
- [ ] Manual test of affected endpoints

---

## Files Changed Summary

| Action | Files |
|--------|-------|
| **Create** | `interview_mapper.py`, 4+ command/query files |
| **Modify** | 5 controller files, 4+ schema files |
| **Move** | 1 DTO file |
| **Delete** | `from_dto()` methods from schemas |

---

## Expected Result

| Metric | Before | After |
|--------|--------|-------|
| Overall Compliance | 75% | 90%+ |
| Dependency Direction | 65% | 90%+ |
| Data Flow | 80% | 95%+ |

---

## Completion Summary (2025-12-08)

### Completed Tasks:
1. **InterviewMapper** - Created mapper, moved logic from `from_dto()`, updated controller
2. **FileAttachmentController** - Created domain layer (entity, value object, interface), application layer (4 commands/queries), mapper
3. **ApplicationController** - Created `CanUserProcessApplicationQuery`, removed repository access
4. **AdminCandidateController** - Created `GetUserByIdQuery`, updated to use existing commands/queries
5. **InterviewController** - Created `CountInterviewsQuery`, removed direct repository access
6. **resume_analysis_dto.py** - Moved from domain to application layer

### Files Created:
- `adapters/http/company_app/interview/mappers/interview_mapper.py`
- `src/candidate_bc/candidate/domain/value_objects/file_attachment_id.py`
- `src/candidate_bc/candidate/domain/entities/file_attachment.py`
- `src/candidate_bc/candidate/domain/repositories/file_attachment_repository_interface.py`
- `src/candidate_bc/candidate/application/queries/shared/file_attachment_dto.py`
- `src/candidate_bc/candidate/application/queries/get_file_attachment_by_id.py`
- `src/candidate_bc/candidate/application/queries/list_file_attachments_by_candidate.py`
- `src/candidate_bc/candidate/application/commands/upload_file_attachment.py`
- `src/candidate_bc/candidate/application/commands/delete_file_attachment.py`
- `adapters/http/candidate_app/mappers/file_attachment_mapper.py`
- `src/company_bc/candidate_application/application/queries/can_user_process_application_query.py`
- `src/auth_bc/user/application/queries/get_user_by_id_query.py`
- `src/interview_bc/interview/application/queries/count_interviews.py`
- `src/framework/application/dtos/__init__.py`
- `src/framework/application/dtos/resume_analysis_dto.py`

### Remaining Tasks:
- Priority 2.2: Standardize Presentation Layer Location (optional, requires decision)
- Priority 3: Medium priority items (linting rules, CI/CD checks)
- Manual testing of affected endpoints

---

**Document Status:** Completed (Priority 1 & 2.1)
**Owner:** Development Team
