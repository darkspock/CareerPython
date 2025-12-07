# Pending Tasks & Priorities

**Last Updated:** 2025-12-07 (Added Application Questions feature)
**Document Type:** Development Roadmap

---

## Priority Matrix

| Priority | Description | Timeline Focus |
|----------|-------------|----------------|
| **P0 - Critical** | Blocking issues, security, data integrity | Immediate |
| **P1 - High** | Core functionality gaps | Short-term |
| **P2 - Medium** | Feature completion | Medium-term |
| **P3 - Low** | Nice-to-have, optimization | Long-term |

---

## P0 - Critical Tasks

### 1. Permission System Implementation ✅ COMPLETED

**Status**: Implemented on 2025-12-05

**Files Modified**:
- `src/company_bc/candidate_application/application/services/stage_permission_service.py`
- `src/company_bc/job_position/domain/entities/job_position.py`
- `core/containers/workflow_container.py`
- `core/container.py`

**Completed Tasks**:
- [x] Implement `can_receive_applications()` logic - checks visibility (PUBLIC) and stage type (INITIAL/PROGRESS)
- [x] Implement `is_user_company_admin()` logic - queries company_users table, checks ADMIN role and ACTIVE status
- [x] Add role-based permission checks - integrated CompanyUserRepository
- [ ] Add feature flag support for billing tiers - Future enhancement
- [ ] Write unit tests for permission logic - Pending

**Implementation Notes**:
- `is_user_company_admin()`: Queries `company_users` table via `CompanyUserRepositoryInterface`, returns true only if user has `ADMIN` role and `ACTIVE` status
- `can_receive_applications()`: Accepts optional `stage_type` parameter, returns true when visibility is `PUBLIC` and stage is `INITIAL` or `PROGRESS`

---

### 2. JsonLogic Validation Engine ✅ COMPLETED

**Status**: Implemented on 2025-12-05

**Files Created/Modified**:
- `src/shared_bc/customization/field_validation/domain/services/jsonlogic_evaluator.py` (NEW)
- `src/company_bc/job_position/application/commands/move_job_position_to_stage.py`

**Completed Tasks**:
- [x] Custom JsonLogic evaluator implementation (no external dependency)
- [x] Implement rule evaluation in `_validate_with_jsonlogic()`
- [x] Add validation error messages with field mapping
- [ ] Create validation rule builder UI component - Future frontend task
- [ ] Write comprehensive test cases - Pending

**Supported JsonLogic Operators**:
- Comparison: `==`, `!=`, `===`, `!==`, `>`, `<`, `>=`, `<=`
- Logic: `and`, `or`, `!`, `!!`, `if`
- Data access: `var` (with dot notation for nested access)
- Array: `in`, `all`, `some`, `none`, `merge`
- String: `cat`, `substr`
- Numeric: `+`, `-`, `*`, `/`, `%`, `min`, `max`
- Type: `missing`, `missing_some`

**Validation Rules Format**:
```json
{
    "rules": [
        {
            "rule": {">=": [{"var": "salary"}, 50000]},
            "field": "salary",
            "message": "Salary must be at least 50,000"
        }
    ]
}
```

**Impact**: Stage transitions now enforce JsonLogic validation rules configured on stages.

---

## P1 - High Priority Tasks

### 3. Enable Talent Pool Routes ✅ COMPLETED

**Status**: Implemented on 2025-12-05

**Files Created/Modified**:
- `client-vite/src/pages/company/TalentPoolPageWrapper.tsx` (NEW)
- `client-vite/src/App.tsx` - Added route `/company/talent-pool`
- `client-vite/src/components/company/CompanyLayout.tsx` - Added navigation link with Star icon
- `client-vite/src/locales/en/translation.json` - Added translation key
- `client-vite/src/locales/es/translation.json` - Added translation key

**Completed Tasks**:
- [x] Add route: `/company/talent-pool` → `TalentPoolPageWrapper`
- [x] Add navigation link in sidebar with Star icon
- [x] Add translations (EN: "Talent Pool", ES: "Pool de Talento")
- [ ] Test full flow end-to-end - Pending

---

### 4. Enable Workflow Analytics Routes ✅ COMPLETED

**Status**: Implemented on 2025-12-05

**Files Created/Modified**:
- `client-vite/src/pages/company/WorkflowAnalyticsPageWrapper.tsx` (NEW)
- `client-vite/src/App.tsx` - Added route `/company/analytics/workflow`
- `client-vite/src/components/company/CompanyLayout.tsx` - Added navigation link with BarChart2 icon
- `client-vite/src/locales/en/translation.json` - Added translation key
- `client-vite/src/locales/es/translation.json` - Added translation key

**Completed Tasks**:
- [x] Add route: `/company/analytics/workflow` → `WorkflowAnalyticsPageWrapper`
- [x] Add analytics section in sidebar with BarChart2 icon
- [x] Connect to real backend data (via WorkflowAnalyticsService)
- [x] Add date range filters (all time, 30 days, 90 days, custom)
- [x] Add translations (EN: "Analytics", ES: "Analíticas")

---

### 5. Candidate Report Generation ✅ COMPLETED

**Status**: Implemented on 2025-12-07

**Files Created/Modified**:
- `client-vite/src/services/candidateReportService.ts` (NEW) - Frontend service for report API
- `client-vite/src/components/candidate/CandidateReportModal.tsx` (NEW) - Report generation modal
- `client-vite/src/components/candidate/CandidateHeader.tsx` - Added "Report" button
- `src/company_bc/company_candidate/application/queries/generate_candidate_report_query.py` (NEW) - Backend query/handler
- `adapters/http/company_app/company_candidate/routers/company_candidate_router.py` - Added `/reports/generate` endpoint
- `core/containers/company_container.py` - Registered query handler

**Completed Tasks**:
- [x] Create `CandidateReportModal` component (generate, view, download)
- [x] Add "Report" button to CandidateHeader
- [x] Implement backend query handler with mock AI analysis
- [x] Add API endpoint for report generation
- [x] Implement markdown download functionality
- [ ] Connect real AI service (Anthropic/OpenAI) - Future enhancement
- [ ] Add PDF export with proper formatting - Future enhancement
- [ ] Implement report caching - Future enhancement

**API Endpoint**: `POST /api/company-candidates/reports/generate`

**Implementation Notes**:
- AI analysis is currently mocked (generates report based on comments count/content)
- Report includes: Summary, Strengths, Areas for Improvement, Interview Insights, Recommendation
- Download currently exports as Markdown (PDF generation can be added later)

---

### 6. Legacy Module Cleanup ✅ COMPLETED

**Status**: Completed on 2025-12-05

**Modules Removed**:
```
src/candidate/      → removed (was empty, replaced by src/candidate_bc/)
src/company/        → removed (was empty, replaced by src/company_bc/)
src/notification/   → removed (was empty, replaced by src/notification_bc/)
```

**Completed Tasks**:
- [x] Audit all imports referencing legacy modules - No imports found
- [x] Update any remaining references - None needed
- [x] Remove legacy module directories - Removed empty directories
- [x] Update container.py registrations - None needed (no references existed)
- [x] Run mypy to verify - Passed with only pre-existing errors

**Notes**:
The legacy directories were already empty (no Python files), only containing empty subdirectory structures. Safe removal confirmed.

---

## P2 - Medium Priority Tasks

### 7. AI Interview Full Integration ✅ COMPLETED

**Status**: Implemented on 2025-12-06

**Files Created/Modified**:
- `client-vite/src/components/interview/AIInterviewChat.tsx` (NEW) - Conversational chat component
- `client-vite/src/components/admin/InterviewTemplateEditor.tsx` - Added `use_conversational_mode` toggle
- `client-vite/src/pages/public/InterviewAnswerPage.tsx` - Conditional AIInterviewChat rendering
- `client-vite/src/services/publicInterviewService.ts` - Added AI mode fields to interface
- `src/interview_bc/interview_template/domain/entities/interview_template.py` - Added field
- `src/interview_bc/interview_template/infrastructure/models/interview_template.py` - Added column
- `src/interview_bc/interview_template/infrastructure/repositories/interview_template_repository.py` - Updated mappings
- `src/interview_bc/interview_template/application/queries/dtos/*.py` - Added field to DTOs
- `src/interview_bc/interview_template/application/commands/*.py` - Added field to commands
- `alembic/versions/dba5b34b4c44_add_use_conversational_mode_to_.py` (NEW) - DB migration

**Completed Tasks**:
- [x] Enable AI interview mode in template configuration (`use_conversational_mode` toggle)
- [x] Complete `AIInterviewChat` component with mock AI responses
- [x] Implement conversation history (messages stored in state)
- [x] Add AI follow-up question display (mock contextual follow-ups)
- [x] Conditional rendering based on template settings
- [x] Add pause/resume functionality
- [x] Progress tracking across sections
- [ ] Test conversation flow end-to-end - Pending manual testing
- [ ] Connect real AI service (Anthropic/OpenAI) - Future enhancement

**Implementation Notes**:
- AI responses are currently mocked (simulated typing delays and contextual follow-ups)
- Real AI integration can be added later by connecting to Anthropic/OpenAI APIs
- Template must have both `allow_ai_questions` AND `use_conversational_mode` enabled

---

### 8. Bulk Email Sending ✅ COMPLETED

**Status**: Implemented on 2025-12-06

**Files Created/Modified**:
- `src/notification_bc/notification/application/commands/send_bulk_email_command.py` (NEW)
- `src/notification_bc/notification/application/handlers/send_bulk_email_handler.py` (NEW)
- `src/framework/domain/interfaces/email_service.py` - Added `send_template_email` method
- `src/notification_bc/notification/infrastructure/services/smtp_email_service.py` - Implemented template email
- `adapters/http/company_app/company/routers/email_template_router.py` - Added `/send-bulk` endpoint
- `core/containers.py` - Registered handler
- `client-vite/src/services/emailTemplateService.ts` - Added `sendBulkEmail` method
- `client-vite/src/components/company/email/BulkEmailModal.tsx` (NEW)
- `client-vite/src/pages/company/CandidatesListPage.tsx` - Added selection and bulk email integration
- `client-vite/src/locales/en/translation.json` - Added translations
- `client-vite/src/locales/es/translation.json` - Added translations

**Completed Tasks**:
- [x] Create `BulkEmailModal` component (multi-step: select template → preview → send → complete)
- [x] Add candidate selection in CandidatesListPage (checkboxes)
- [x] Implement merge tag preview with variable substitution
- [x] Add send progress indicator
- [x] Implement backend command/handler with async email sending
- [x] Add send confirmation dialog

**API Endpoint**: `POST /api/company/email-templates/send-bulk` (202 Accepted)

---

### 9. Advanced Filtering System ✅ COMPLETED

**Status**: Implemented on 2025-12-07

**Files Created/Modified**:
- `client-vite/src/hooks/useFilterState.ts` (NEW) - Reusable filter state hook with URL persistence
- `client-vite/src/components/filters/SavedFiltersDropdown.tsx` (NEW) - Dropdown for managing saved filters
- `client-vite/src/pages/company/CandidatesListPage.tsx` - Integrated new filter system
- `client-vite/src/locales/en/translation.json` - Added filter translations
- `client-vite/src/locales/es/translation.json` - Added filter translations

**Completed Tasks**:
- [x] Create `useFilterState` hook with URL persistence
- [x] Create `SavedFiltersDropdown` component
- [x] Add filter preset functionality (save, load, delete)
- [x] Add filter URL persistence via useSearchParams
- [x] Add default filter support (auto-loads on page visit)
- [x] Integrate into CandidatesListPage
- [x] Add translations (EN/ES)
- [ ] Implement filter sharing between team members - Future enhancement

**Features**:
- URL persistence for all filters (shareable links)
- localStorage-based saved filter presets
- Set default filter that loads automatically
- Active filter count badge
- Clear all filters button

---

### 10. Interview Calendar View ✅ COMPLETED

**Status**: Implemented on 2025-12-07

**Files Created/Modified**:
- `client-vite/src/components/interviews/InterviewFullCalendar.tsx` (NEW) - Full calendar component
- `client-vite/src/pages/company/CompanyInterviewsPage.tsx` - Added Lista/Calendario toggle

**Completed Tasks**:
- [x] Create `InterviewFullCalendar` component
- [x] Add week/month view toggle
- [x] Color code by interview type (6 types with distinct colors)
- [x] Add navigation (previous/next/today)
- [x] Add interview details on hover (tooltips)
- [x] Add legend for interview types
- [ ] Implement drag-to-reschedule - Future enhancement
- [ ] Add interviewer availability display - Future enhancement

**Implementation Notes**:
- Week view shows 7 days with interview cards
- Month view shows 42-day grid with compact entries
- Colors: Technical (blue), Behavioral (purple), Cultural Fit (green), Knowledge Check (yellow), Experience Check (orange), Custom (gray)

---

### 11. Notification System Enhancement ✅ COMPLETED

**Status**: Implemented on 2025-12-07

**Files Created/Modified**:
- `src/notification_bc/in_app_notification/` (NEW directory) - Complete domain, application, infrastructure layers
- `src/notification_bc/in_app_notification/domain/entities/in_app_notification.py` (NEW) - Core entity
- `src/notification_bc/in_app_notification/domain/enums/notification_enums.py` (NEW) - Types and priorities
- `src/notification_bc/in_app_notification/application/queries/*.py` (NEW) - ListUserNotificationsQuery, GetUnreadCountQuery
- `src/notification_bc/in_app_notification/application/commands/*.py` (NEW) - Create, MarkAsRead, MarkAllAsRead, Delete
- `src/notification_bc/in_app_notification/infrastructure/repositories/in_app_notification_repository.py` (NEW)
- `src/notification_bc/in_app_notification/infrastructure/models/in_app_notification_model.py` (NEW)
- `adapters/http/company_app/notification/` (NEW) - Complete HTTP layer (router, controller, schemas, mappers)
- `client-vite/src/services/notificationService.ts` (NEW) - Frontend API service
- `client-vite/src/components/notifications/NotificationBell.tsx` (NEW) - Bell icon with dropdown
- `client-vite/src/components/company/CompanyLayout.tsx` - Integrated NotificationBell
- `alembic/versions/bdc7f8f711e4_add_in_app_notifications_table.py` (NEW) - DB migration
- `core/containers/company_container.py` - Registered notification handlers and repository
- `core/containers/main_container.py` - Exposed notification controller
- `main.py` - Registered notification router

**Completed Tasks**:
- [x] Create notification center UI (NotificationBell with Popover dropdown)
- [x] Implement in-app notifications (full backend: entity, repository, queries, commands)
- [x] Create notification bell with badge (unread count badge, polling every 30s)
- [x] Implement mark as read functionality (individual and mark all)
- [x] Implement delete notification
- [x] Add priority levels and notification types
- [ ] Add notification preferences - Future enhancement
- [ ] Push notifications - Future enhancement

**API Endpoints**:
- `GET /api/company/notifications/` - List notifications (paginated)
- `GET /api/company/notifications/unread-count` - Get unread count
- `POST /api/company/notifications/{id}/read` - Mark as read
- `POST /api/company/notifications/read-all` - Mark all as read
- `DELETE /api/company/notifications/{id}` - Delete notification

**Implementation Notes**:
- Notification types: NEW_APPLICATION, INTERVIEW_SCHEDULED, NEW_COMMENT, MENTION, SYSTEM_ALERT, INFO, WARNING, ERROR
- Priority levels: LOW, NORMAL, HIGH, URGENT
- Polling for real-time updates (30 second intervals)
- Clickable notifications with optional link navigation

---

### 12. Application Questions (Screening Questions) - Backend Complete

**Current State**: Backend infrastructure implemented, frontend UI pending

**Design Decision**: Hybrid approach - Workflow-Defined, Position-Enabled

**Business Documentation**: See `docs/business/06-workflow-system.md` (FR-WF06)

**Tasks**:

#### Backend - COMPLETED
- [x] Create `ApplicationQuestion` entity in workflow domain
- [x] Create `PositionQuestionConfig` entity for position-level enablement
- [x] Create `ApplicationQuestionRepository` with SQLAlchemy implementation
- [x] Create `PositionQuestionConfigRepository` with SQLAlchemy implementation
- [x] Create CRUD commands for application questions (Create, Update, Delete)
- [x] Create `ListApplicationQuestionsQuery` query
- [x] Create HTTP layer (router, controller, schemas, mapper)
- [x] Create database migration for both tables
- [x] Register in dependency injection containers
- [x] Create position question toggle command (ConfigurePositionQuestionCommand)
- [x] Create `ListPositionQuestionConfigsQuery` query
- [x] Create position question config HTTP layer (router, controller, schemas, mapper)
- [x] Create `ApplicationQuestionAnswer` entity and repository
- [x] Create `SaveApplicationAnswersCommand` to save answers
- [x] Create `ListApplicationAnswersQuery` to retrieve answers
- [x] Create `GetEnabledQuestionsForPositionQuery` (combines workflow + position config)
- [x] Create application answers HTTP layer (router, controller, schemas, mapper)
- [x] Create database migration for `application_question_answers` table
- [x] Integrate with JsonLogic validation engine for automation rules

**Backend Files Created**:
- Domain: `src/shared_bc/customization/workflow/domain/entities/application_question.py`
- Domain: `src/shared_bc/customization/workflow/domain/interfaces/application_question_repository_interface.py`
- Domain: `src/shared_bc/customization/workflow/domain/enums/application_question_field_type.py`
- Domain: `src/company_bc/job_position/domain/entities/position_question_config.py`
- Domain: `src/company_bc/job_position/domain/repositories/position_question_config_repository_interface.py`
- Infrastructure: `src/shared_bc/customization/workflow/infrastructure/models/application_question_model.py`
- Infrastructure: `src/shared_bc/customization/workflow/infrastructure/repositories/application_question_repository.py`
- Infrastructure: `src/company_bc/job_position/infrastructure/models/position_question_config_model.py`
- Infrastructure: `src/company_bc/job_position/infrastructure/repositories/position_question_config_repository.py`
- Application: `src/shared_bc/customization/workflow/application/dtos/application_question_dto.py`
- Application: `src/shared_bc/customization/workflow/application/queries/application_question/list_application_questions_query.py`
- Application: `src/shared_bc/customization/workflow/application/commands/application_question/create_application_question_command.py`
- Application: `src/shared_bc/customization/workflow/application/commands/application_question/update_application_question_command.py`
- Application: `src/shared_bc/customization/workflow/application/commands/application_question/delete_application_question_command.py`
- HTTP: `adapters/http/company_app/application_question/` (complete layer)
- Migration: `alembic/versions/c3d4e5f6a7b8_add_application_questions_tables.py`

**API Endpoints - Application Questions (Workflow Level)**:
- `GET /api/company/workflows/{workflow_id}/questions/` - List questions
- `POST /api/company/workflows/{workflow_id}/questions/` - Create question
- `PUT /api/company/workflows/{workflow_id}/questions/{question_id}` - Update question
- `DELETE /api/company/workflows/{workflow_id}/questions/{question_id}` - Delete question

**API Endpoints - Position Question Config (Position Level)**:
- `GET /api/company/positions/{position_id}/questions/` - List question configs for position
- `POST /api/company/positions/{position_id}/questions/` - Configure question for position (enable/disable, set overrides)
- `DELETE /api/company/positions/{position_id}/questions/{question_id}` - Remove question config (revert to workflow defaults)

**Additional Files Created (Position Question Config)**:
- Application: `src/company_bc/job_position/application/dtos/position_question_config_dto.py`
- Application: `src/company_bc/job_position/application/queries/position_question_config/list_position_question_configs_query.py`
- Application: `src/company_bc/job_position/application/queries/position_question_config/get_enabled_questions_for_position_query.py`
- Application: `src/company_bc/job_position/application/commands/position_question_config/configure_position_question_command.py`
- Application: `src/company_bc/job_position/application/commands/position_question_config/remove_position_question_config_command.py`
- HTTP: `adapters/http/company_app/job_position/schemas/position_question_config_schemas.py`
- HTTP: `adapters/http/company_app/job_position/controllers/position_question_config_controller.py`
- HTTP: `adapters/http/company_app/job_position/routers/position_question_config_router.py`
- HTTP: `adapters/http/company_app/job_position/mappers/position_question_config_mapper.py`

**Additional Files Created (Application Answers)**:
- Domain: `src/company_bc/candidate_application/domain/entities/application_question_answer.py`
- Domain: `src/company_bc/candidate_application/domain/repositories/application_question_answer_repository_interface.py`
- Domain: `src/company_bc/candidate_application/domain/value_objects/application_question_answer_id.py`
- Infrastructure: `src/company_bc/candidate_application/infrastructure/models/application_question_answer_model.py`
- Infrastructure: `src/company_bc/candidate_application/infrastructure/repositories/application_question_answer_repository.py`
- Application: `src/company_bc/candidate_application/application/queries/question_answer/` (DTOs and ListApplicationAnswersQuery)
- Application: `src/company_bc/candidate_application/application/commands/question_answer/save_application_answers_command.py`
- HTTP: `adapters/http/candidate_app/application_answers/` (complete layer)
- Migration: `alembic/versions/d4e5f6a7b8c9_add_application_question_answers_table.py`

**API Endpoints - Application Answers**:
- `GET /api/applications/{application_id}/answers` - List answers for application
- `POST /api/applications/{application_id}/answers` - Save answers for application
- `GET /api/public/positions/{position_id}/questions` - Get enabled questions for position (public)

**Additional Files Created (JsonLogic Evaluation)**:
- Application Service: `src/company_bc/candidate_application/application/services/application_answer_evaluation_service.py`
- Application Command: `src/company_bc/candidate_application/application/commands/question_answer/evaluate_application_answers_command.py`

**JsonLogic Integration Notes**:
- `ApplicationAnswerEvaluationService` evaluates answers against automation rules defined on questions
- `EvaluateApplicationAnswersCommand` triggers auto-reject/auto-approve based on rule evaluation
- Rules format follows JsonLogic structure with `should_auto_reject` and `should_auto_approve` flags
- Type coercion handles NUMBER and BOOLEAN field types from string answers
- Rule messages support variable substitution from answer data

#### Frontend - COMPLETED
- [x] Create Application Questions management UI (workflow settings)
- [x] Add question toggle UI in job position editor
- [x] Update public application form to render enabled questions
- [x] Add question answer display in candidate detail view
- [ ] Create automation rule builder for question-based rules (optional - nice to have)

**Frontend Files Created**:
- Service: `client-vite/src/services/applicationQuestionService.ts`
- Service: `client-vite/src/services/positionQuestionConfigService.ts`
- Service: `client-vite/src/services/publicQuestionService.ts`
- Component: `client-vite/src/components/workflow/ApplicationQuestionsEditor.tsx`
- Component: `client-vite/src/components/jobPosition/PositionQuestionsEditor.tsx`
- Component: `client-vite/src/components/public/ApplicationQuestionsForm.tsx`
- Component: `client-vite/src/components/candidate/CandidateAnswersSection.tsx`
- Updated: `client-vite/src/pages/workflow/WorkflowAdvancedConfigPage.tsx`
- Updated: `client-vite/src/pages/company/EditPositionPage.tsx`
- Updated: `client-vite/src/pages/public/PublicPositionDetailPage.tsx`
- Updated: `client-vite/src/pages/company/CandidateDetailPage.tsx`

#### Data Model
```
ApplicationQuestion (workflow-level)
├── id, workflow_id, company_id, field_key, label, description
├── field_type (TEXT, TEXTAREA, NUMBER, DATE, SELECT, MULTISELECT, BOOLEAN)
├── options (JSON for SELECT/MULTISELECT)
├── is_required_default, validation_rules (JSON), sort_order
├── is_active, created_at, updated_at

PositionQuestionConfig (position-level)
├── id, position_id, question_id
├── enabled, is_required_override, sort_order_override
├── created_at, updated_at
```

**Priority**: P2
**Status**: COMPLETED (Backend and Frontend)

---

## P3 - Low Priority Tasks

### 14. Calendar Integration

**Tasks**:
- [ ] Google Calendar OAuth integration
- [ ] Microsoft Outlook integration
- [ ] Two-way sync for interviews
- [ ] Calendar availability check

**Estimated Effort**: High (1-2 weeks)

---

### 15. Mobile PWA Enhancement

**Tasks**:
- [ ] Improve offline support
- [ ] Add push notifications
- [ ] Optimize touch interactions
- [ ] Add install prompt
- [ ] Improve loading states

**Estimated Effort**: Medium (3-5 days)

---

### 16. Performance Optimization

**Tasks**:
- [ ] Implement list virtualization for large datasets
- [ ] Add React Query for caching
- [ ] Optimize bundle splitting
- [ ] Add image lazy loading
- [ ] Implement skeleton loaders

**Estimated Effort**: Medium (3-5 days)

---

### 17. Accessibility Improvements

**Tasks**:
- [ ] Complete ARIA labeling
- [ ] Fix keyboard navigation gaps
- [ ] Add screen reader announcements
- [ ] Implement focus management
- [ ] Test with accessibility tools

**Estimated Effort**: Medium (3-5 days)

---

### 18. Advanced Analytics Dashboard

**Tasks**:
- [ ] Implement time-to-hire metrics
- [ ] Add source effectiveness tracking
- [ ] Create diversity metrics dashboard
- [ ] Implement export functionality
- [ ] Add scheduled report delivery

**Estimated Effort**: High (1-2 weeks)

---

## Technical Debt

### Backend

| Item | Priority | Effort |
|------|----------|--------|
| ~~Remove legacy modules~~ | ~~P1~~ | ✅ Done |
| Add missing type hints | P3 | Low |
| Improve error messages | P2 | Low |
| Add API rate limiting | P2 | Medium |
| Implement request logging | P2 | Low |

### Frontend

| Item | Priority | Effort |
|------|----------|--------|
| Upgrade React to 19 | P3 | Medium |
| Migrate to TanStack Query | P3 | High |
| Add component unit tests | P2 | High |
| Improve TypeScript strictness | P2 | Medium |
| Document component props | P3 | Low |

### Infrastructure

| Item | Priority | Effort |
|------|----------|--------|
| Add CI/CD pipeline | P1 | Medium |
| Implement staging environment | P2 | Medium |
| Add automated backups | P1 | Low |
| Configure monitoring/alerting | P2 | Medium |
| Implement log aggregation | P3 | Medium |

---

## Recommended Sprint Planning

### Sprint 1: Critical Fixes ✅ COMPLETED
- ~~Permission system implementation (P0)~~ ✅
- ~~JsonLogic validation (P0)~~ ✅
- ~~Enable talent pool routes (P1)~~ ✅
- ~~Enable analytics routes (P1)~~ ✅

### Sprint 2: Feature Completion ✅ COMPLETED
- ~~Candidate report generation (P1)~~ ✅
- ~~Legacy module cleanup (P1)~~ ✅
- ~~AI interview integration (P2)~~ ✅
- ~~Bulk email sending (P2)~~ ✅

### Sprint 3: Enhancement ✅ COMPLETED
- ~~Advanced filtering (P2)~~ ✅
- ~~Interview calendar view (P2)~~ ✅
- ~~Notification system (P2)~~ ✅

### Sprint 4: Application Questions - COMPLETED
- Application Questions backend (P2) - ✅ COMPLETED
- JsonLogic evaluation integration (P2) - ✅ COMPLETED
- Position question toggle command (P2) - ✅ COMPLETED
- Application Questions frontend (P2) - ✅ COMPLETED
- Application submission with question answers - ✅ COMPLETED

### Sprint 5: Polish
- Performance optimization (P3)
- Accessibility improvements (P3)
- Calendar integration (P3)

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Backend completion | 98% | 100% |
| Frontend completion | 92% | 95% |
| Test coverage | 60% | 80% |
| Performance score | 75 | 90 |
| Accessibility score | 70 | 90 |

---

## Dependencies

### External Libraries Needed

| Library | Purpose | Status |
|---------|---------|--------|
| jsonlogic-python | Rule evaluation | Not installed |
| react-big-calendar | Calendar view | Not installed |
| workbox | PWA enhancement | Partial |

### API Integrations Needed

| Integration | Purpose | Status |
|-------------|---------|--------|
| Google Calendar API | Calendar sync | Not started |
| Microsoft Graph API | Outlook sync | Not started |
| SendGrid/SES | Email delivery | Configured |

---

**Document Status**: Living document
**Owner**: Development Team
**Update Frequency**: Sprint planning
