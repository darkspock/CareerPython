# Pending Tasks & Priorities

**Last Updated:** 2025-12-05
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

### 1. Permission System Implementation

**Current State**: Returns `False` for all permission checks

**Files to Fix**:
- `src/company_bc/company/domain/entities/company.py`
- `src/company_bc/company_user/domain/entities/company_user.py`

**Tasks**:
- [ ] Implement `can_receive_applications()` logic
- [ ] Implement `is_user_company_admin()` logic
- [ ] Add role-based permission checks
- [ ] Add feature flag support for billing tiers
- [ ] Write unit tests for permission logic

**Impact**: Without this, all permission-gated features are bypassed.

---

### 2. JsonLogic Validation Engine

**Current State**: Stage transition validation returns success without evaluation

**Files to Fix**:
- `src/company_bc/stage/domain/entities/stage.py`
- `src/company_bc/stage/domain/services/validation_service.py`

**Tasks**:
- [ ] Integrate jsonlogic-python library
- [ ] Implement rule evaluation in `validate_transition()`
- [ ] Add validation error messages
- [ ] Create validation rule builder UI component
- [ ] Write comprehensive test cases

**Impact**: Stage transitions work but don't enforce configured rules.

---

## P1 - High Priority Tasks

### 3. Enable Talent Pool Routes

**Current State**: Components implemented, routes not configured

**Tasks**:
- [ ] Add routes in `router/index.tsx`
  ```typescript
  { path: '/companies/:id/talent-pool', component: TalentPoolList }
  { path: '/talent-pool/:id', component: TalentPoolDetail }
  ```
- [ ] Add navigation link in sidebar
- [ ] Update breadcrumb configuration
- [ ] Test full flow end-to-end

**Estimated Effort**: Low (2-4 hours)

---

### 4. Enable Workflow Analytics Routes

**Current State**: Dashboard implemented, not accessible

**Tasks**:
- [ ] Add route in `router/index.tsx`
  ```typescript
  { path: '/companies/:id/analytics/workflow', component: WorkflowAnalytics }
  ```
- [ ] Add analytics section in sidebar
- [ ] Connect to real backend data
- [ ] Add date range filters

**Estimated Effort**: Low (2-4 hours)

---

### 5. Candidate Report Generation

**Current State**: Backend service ready, no frontend

**Backend Tasks**:
- [ ] Verify AI service integration
- [ ] Add PDF export endpoint
- [ ] Implement caching for generated reports

**Frontend Tasks**:
- [ ] Create `CandidateReportGenerator` component
- [ ] Create `CandidateReportViewer` component
- [ ] Add "Generate Report" button to candidate detail
- [ ] Implement PDF download functionality
- [ ] Add loading states for AI generation

**Estimated Effort**: Medium (1-2 days)

---

### 6. Legacy Module Cleanup

**Current State**: Duplicate modules exist

**Modules to Remove**:
```
src/candidate/      → replaced by src/candidate_bc/
src/company/        → replaced by src/company_bc/
src/notification/   → replaced by src/notification_bc/
```

**Tasks**:
- [ ] Audit all imports referencing legacy modules
- [ ] Update any remaining references
- [ ] Remove legacy module directories
- [ ] Update container.py registrations
- [ ] Run full test suite to verify

**Estimated Effort**: Medium (4-8 hours)

---

## P2 - Medium Priority Tasks

### 7. AI Interview Full Integration

**Current State**: Services ready, UI partial

**Tasks**:
- [ ] Enable AI interview mode in template configuration
- [ ] Complete `AIInterviewChat` component
- [ ] Implement conversation history
- [ ] Add AI follow-up question display
- [ ] Test conversation flow end-to-end
- [ ] Add error handling for AI service failures

**Estimated Effort**: Medium (2-3 days)

---

### 8. Bulk Email Sending

**Current State**: Templates ready, bulk UI missing

**Tasks**:
- [ ] Create `BulkEmailModal` component
- [ ] Add candidate selection in pipeline
- [ ] Implement merge tag preview
- [ ] Add send progress indicator
- [ ] Implement send rate limiting
- [ ] Add send confirmation dialog

**Estimated Effort**: Medium (1-2 days)

---

### 9. Advanced Filtering System

**Current State**: Basic filters only

**Tasks**:
- [ ] Create `SavedFilters` component
- [ ] Add filter preset functionality
- [ ] Implement filter sharing between team members
- [ ] Add filter URL persistence
- [ ] Create common filter presets

**Estimated Effort**: Medium (1-2 days)

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
| Remove legacy modules | P1 | Medium |
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

### Sprint 1: Critical Fixes
- Permission system implementation (P0)
- JsonLogic validation (P0)
- Enable talent pool routes (P1)
- Enable analytics routes (P1)

### Sprint 2: Feature Completion
- Candidate report generation (P1)
- Legacy module cleanup (P1)
- AI interview integration (P2)

### Sprint 3: Enhancement
- Bulk email sending (P2)
- Advanced filtering (P2)
- Interview calendar view (P2)

### Sprint 4: Polish
- Notification system (P2)
- Performance optimization (P3)
- Accessibility improvements (P3)

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
