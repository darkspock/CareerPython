# Pending Tasks & Priorities

**Last Updated:** 2025-12-07
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

### 10. Interview Calendar View

**Current State**: List view only

**Tasks**:
- [ ] Create `InterviewCalendar` component
- [ ] Add week/month view toggle
- [ ] Implement drag-to-reschedule
- [ ] Add interviewer availability display
- [ ] Color code by interview type

**Estimated Effort**: Medium (2-3 days)

---

### 11. Notification System Enhancement

**Current State**: Toast notifications only

**Tasks**:
- [ ] Create notification center UI
- [ ] Implement in-app notifications
- [ ] Add notification preferences
- [ ] Create notification bell with badge
- [ ] Implement mark as read functionality

**Estimated Effort**: Medium (2-3 days)

---

## P3 - Low Priority Tasks

### 12. Calendar Integration

**Tasks**:
- [ ] Google Calendar OAuth integration
- [ ] Microsoft Outlook integration
- [ ] Two-way sync for interviews
- [ ] Calendar availability check

**Estimated Effort**: High (1-2 weeks)

---

### 13. Mobile PWA Enhancement

**Tasks**:
- [ ] Improve offline support
- [ ] Add push notifications
- [ ] Optimize touch interactions
- [ ] Add install prompt
- [ ] Improve loading states

**Estimated Effort**: Medium (3-5 days)

---

### 14. Performance Optimization

**Tasks**:
- [ ] Implement list virtualization for large datasets
- [ ] Add React Query for caching
- [ ] Optimize bundle splitting
- [ ] Add image lazy loading
- [ ] Implement skeleton loaders

**Estimated Effort**: Medium (3-5 days)

---

### 15. Accessibility Improvements

**Tasks**:
- [ ] Complete ARIA labeling
- [ ] Fix keyboard navigation gaps
- [ ] Add screen reader announcements
- [ ] Implement focus management
- [ ] Test with accessibility tools

**Estimated Effort**: Medium (3-5 days)

---

### 16. Advanced Analytics Dashboard

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

### Sprint 3: Enhancement (In Progress)
- ~~Advanced filtering (P2)~~ ✅
- Interview calendar view (P2)
- Notification system (P2)

### Sprint 4: Polish
- Performance optimization (P3)
- Accessibility improvements (P3)
- Calendar integration (P3)

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Backend completion | 95% | 100% |
| Frontend completion | 85% | 95% |
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
