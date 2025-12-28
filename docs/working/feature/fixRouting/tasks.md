# Fix Routing - Task List

**Reference:** `analysis.md`, `/docs/development/ROUTING.md`

## Phase 1: Backend Router Migration - COMPLETED

### 1.1 Migrate Company Enums Router - DONE
- [x] File: `adapters/http/company_app/company/routers/enum_router.py`
- [x] Change prefix from `/api/company/enums` to `/{company_slug}/admin/enums`
- [x] Add `AdminCompanyContext` dependency

### 1.2 Migrate Company Pages Router - DONE
- [x] File: `adapters/http/company_app/company_page/routers/company_page_router.py`
- [x] Change prefix from `/api/company` to `/{company_slug}/admin/pages`
- [x] Add company context dependencies
- [x] Update endpoint signatures

### 1.3 Migrate Notifications Router - DONE
- [x] File: `adapters/http/company_app/notification/routers/notification_router.py`
- [x] Change prefix from `/api/company/notifications` to `/{company_slug}/admin/notifications`
- [x] Add company context dependencies

### 1.4 Migrate Company Users Router - DONE
- [x] File: `adapters/http/company_app/company/routers/company_user_router.py`
- [x] Change prefix from `/company` to `/{company_slug}/admin/users`
- [x] Update dependencies

### 1.5 Migrate Phases Router - DONE
- [x] File: `adapters/http/shared/phase/routers/phase_router.py`
- [x] Change prefix from `/api/companies/{company_id}/phases` to `/{company_slug}/admin/phases`
- [x] Replace `company_id` path param with slug-based context

### 1.6 Migrate Company Roles Router - DONE
- [x] File: `adapters/http/company_app/company/routers/company_role_router.py`
- [x] Change prefix from `/companies/{company_id}/roles` to `/{company_slug}/admin/roles`
- [x] Update dependencies

## Phase 2: Frontend Services Migration - COMPLETED

### 2.1 Migrate Interview Templates Service - DONE
- [x] File: `src/services/companyInterviewTemplateService.ts`
- [x] Add `getCompanySlug()` helper
- [x] Replace `/api/company/interview-templates` with `/${slug}/admin/interview-templates`

### 2.2 Migrate Company Pages Service - DONE
- [x] File: `src/services/companyPageService.ts`
- [x] Add `getCompanySlug()` helper
- [x] Replace `/api/company/pages` with `/${slug}/admin/pages`
- [x] Update public page endpoints if needed

### 2.3 Migrate Notifications Service - DONE
- [x] File: `src/services/notificationService.ts`
- [x] Add `getCompanySlug()` helper
- [x] Replace `/api/company/notifications` with `/${slug}/admin/notifications`

### 2.4 Migrate Candidate Report Service - DONE
- [x] File: `src/services/candidateReportService.ts`
- [x] Add `getCompanySlug()` helper
- [x] Replace `/api/company/candidates/reports` with `/${slug}/admin/candidates/reports`

### 2.5 Migrate Email Templates Service - DONE
- [x] File: `src/services/emailTemplateService.ts`
- [x] Add `getCompanySlug()` helper
- [x] Replace `/api/company/email-templates` with `/${slug}/admin/email-templates`

### 2.6 Migrate Custom Field Value Service - DONE
- [x] File: `src/services/customFieldValueService.ts`
- [x] Add `getCompanySlug()` helper
- [x] Update base URL pattern

## Phase 3: Frontend Navigation Migration - PARTIALLY COMPLETED

### 3.1 Update CompanyLayout - DONE
- [x] File: `src/components/company/CompanyLayout.tsx`
- [x] Get `companySlug` from context/URL using `useParams`
- [x] Update all navigation links to use `/${slug}/admin/*`

### 3.2 Create Legacy Redirect Component - DONE
- [x] File: `src/components/company/LegacyCompanyRedirect.tsx`
- [x] Redirects `/company/*` routes to `/${slug}/admin/*`

### 3.3 Create useCompanyNavigation Hook - EXISTS
- [x] File: `src/hooks/useCompanyNavigation.ts`
- [x] Provides `basePath`, `getPath()`, `isActive()` helpers
- [x] Works with both legacy and new routes

### 3.4 Update Individual Pages - PENDING
The following files still have hardcoded `/company/` navigation calls:

**High Priority (frequently used):**
- [ ] `src/pages/company/PositionsListPage.tsx`
- [ ] `src/pages/company/CandidatesListPage.tsx`
- [ ] `src/pages/company/CandidateDetailPage.tsx`
- [ ] `src/pages/company/PositionDetailPage.tsx`
- [ ] `src/pages/company/CompanySettingsPage.tsx`
- [ ] `src/pages/workflow/WorkflowBoardPage.tsx`

**Medium Priority:**
- [ ] `src/pages/company/CreatePositionPage.tsx`
- [ ] `src/pages/company/EditPositionPage.tsx`
- [ ] `src/pages/company/AddCandidatePage.tsx`
- [ ] `src/pages/company/EditCandidatePage.tsx`
- [ ] `src/pages/company/WorkflowSelectionPage.tsx`
- [ ] `src/pages/company/CompanyInterviewsPage.tsx`
- [ ] `src/pages/company/CompanyInterviewDetailPage.tsx`
- [ ] `src/pages/company/CreateInterviewPage.tsx`
- [ ] `src/pages/company/EditInterviewPage.tsx`
- [ ] `src/pages/company/TalentPoolPageWrapper.tsx`

**Lower Priority:**
- [ ] `src/pages/company/CompanyPagesListPage.tsx`
- [ ] `src/pages/company/CreateCompanyPagePage.tsx`
- [ ] `src/pages/company/EditCompanyPagePage.tsx`
- [ ] `src/pages/company/ViewCompanyPagePage.tsx`
- [ ] `src/pages/company/EditCompanyPage.tsx`
- [ ] `src/pages/company/CompanyInterviewTemplatesPage.tsx`
- [ ] `src/pages/company/WorkflowAnalyticsPageWrapper.tsx`
- [ ] `src/pages/company/PendingApprovalsPage.tsx`
- [ ] `src/pages/workflow/WorkflowsSettingsPage.tsx`
- [ ] `src/pages/workflow/CreateWorkflowPage.tsx`
- [ ] `src/pages/workflow/EditWorkflowPage.tsx`
- [ ] `src/pages/workflow/WorkflowAdvancedConfigPage.tsx`
- [ ] `src/components/candidate/CandidateHeader.tsx`
- [ ] `src/components/notifications/NotificationBell.tsx`
- [ ] `src/components/interviews/InterviewTableRow.tsx`

## Phase 4: Cleanup - PARTIALLY COMPLETED

### 4.1 Remove Legacy Routes from App.tsx - DONE
- [x] File: `src/App.tsx`
- [x] Replaced duplicate `/company/*` route group with redirect
- [x] Added `LegacyCompanyRedirect` component

### 4.2 Update Main.py (if needed) - NOT NEEDED
- [x] All company-scoped routers are already registered via existing wiring

### 4.3 Testing - PENDING
- [ ] Test all company admin pages
- [ ] Test all API endpoints
- [ ] Test navigation between pages
- [ ] Test authentication/authorization

## Summary

### Completed Work:
1. **Backend Routers (6/6)**: All company-scoped backend routers migrated to `/{slug}/admin/*` pattern
2. **Frontend Services (6/6)**: All API service files updated with `getCompanySlug()` helper
3. **CompanyLayout**: Main navigation component updated with slug-based navigation
4. **Legacy Routes**: Replaced with redirect component that sends `/company/*` to `/${slug}/admin/*`
5. **Navigation Hook**: `useCompanyNavigation` hook exists and works with both patterns

### Remaining Work:
1. **Individual Pages (~35 files)**: Need to update `navigate()` calls to use `useCompanyNavigation` hook
   - These pages will work via the redirect, but should be updated for clean navigation
   - Can be done incrementally as pages are touched

### How the Redirect Works:
When a user visits `/company/dashboard`:
1. `ProtectedCompanyRoute` validates authentication
2. `LegacyCompanyRedirect` reads `company_slug` from localStorage
3. Redirects to `/${company_slug}/admin/dashboard`
4. `ProtectedCompanyScopedRoute` validates company access
5. `CompanyLayout` renders with correct navigation

This means **all existing navigation will continue to work** via redirects while pages are migrated incrementally.
