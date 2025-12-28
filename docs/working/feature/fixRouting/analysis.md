# Routing Compliance Analysis

**Date:** 2025-12-27
**Reference:** `/docs/development/ROUTING.md`

## Summary

| Category | Compliant | Non-Compliant | Total |
|----------|-----------|---------------|-------|
| Backend Routers | 4 | 22 | 26 |
| Frontend Navigation | ~0 | ~92 | ~92 |
| Frontend API Services | ~6 | ~67 | ~73 |

## Backend Router Analysis

### Compliant Routers (Using `/{company_slug}/*`)

| File | Prefix | Status |
|------|--------|--------|
| `company_scoped_admin_router.py` | `/{company_slug}/admin` | OK |
| `company_scoped_public_router.py` | `/{company_slug}` | OK |
| `company_scoped_candidate_router.py` | `/{company_slug}/candidate` | OK |
| `job_position_comment_router.py` | `/{company_slug}/admin/positions` | OK |

### Non-Compliant Routers (Need Migration)

#### HIGH PRIORITY - Company Admin Routes (should be `/{slug}/admin/*`)

| File | Current Prefix | Should Be |
|------|----------------|-----------|
| `enum_router.py` (company) | `/api/company/enums` | `/{slug}/admin/enums` |
| `company_page_router.py` | `/api/company` | `/{slug}/admin/pages` |
| `notification_router.py` | `/api/company/notifications` | `/{slug}/admin/notifications` |
| `company_user_router.py` | `/company` | `/{slug}/admin/users` |
| `phase_router.py` | `/api/companies/{company_id}/phases` | `/{slug}/admin/phases` |
| `company_role_router.py` | `/companies/{company_id}/roles` | `/{slug}/admin/roles` |

#### MEDIUM PRIORITY - Public/Candidate Routes

| File | Current Prefix | Should Be |
|------|----------------|-----------|
| `public_company_page_router.py` | `/api/public/company` | `/{slug}/pages` (public) |
| `public_position_router.py` | `/public/positions` | `/{slug}/positions` (public) |

#### LOW PRIORITY - Global Routes (OK to keep)

| File | Prefix | Notes |
|------|--------|-------|
| `admin_router.py` | `/admin` | Global admin - OK |
| `enum_router.py` (admin) | `/admin/enums` | Global admin - OK |
| `company_router.py` | `/companies` | Company management - OK |
| `user_router.py` | `/user` | User profile - OK |
| `invitation_router.py` | `/invitations` | Auth - OK |
| `candidate_router.py` | `/candidate` | Candidate personal - OK |
| `job_router.py` | `/api/jobs` | Job search - OK |
| `file_router.py` | `/api/files` | File upload - OK |

## Frontend Navigation Analysis

### Files with Legacy `/company/*` Routes (~92 usages)

```
src/pages/company/CandidatesListPage.tsx
src/pages/company/PositionsListPage.tsx
src/pages/company/CompanyDashboardPage.tsx
src/components/company/CompanyLayout.tsx
src/components/company/CompanySidebar.tsx
src/pages/company/WorkflowBoardPage.tsx
src/pages/company/CreatePositionPage.tsx
src/pages/company/AddCandidatePage.tsx
... and more
```

### Examples of Non-Compliant Navigation

```tsx
// WRONG
navigate('/company/candidates');
<Link to="/company/positions">

// CORRECT
navigate(`/${companySlug}/admin/candidates`);
<Link to={`/${companySlug}/admin/positions`}>
```

## Frontend Services Analysis

### Services Using Legacy `/api/company/*` Routes

| Service | Legacy Routes Used |
|---------|-------------------|
| `companyInterviewTemplateService.ts` | `/api/company/interview-templates` |
| `companyPageService.ts` | `/api/company/pages`, `/api/company/{id}/pages` |
| `notificationService.ts` | `/api/company/notifications` |
| `candidateReportService.ts` | `/api/company/candidates/reports` |
| `emailTemplateService.ts` | `/api/company/email-templates` |
| `customFieldValueService.ts` | `/api/company-workflow/custom-field-values` |

### Services Already Migrated (Compliant)

| Service | Pattern Used |
|---------|--------------|
| `positionService.ts` | `/${slug}/admin/positions` |
| `companyInterviewService.ts` | `/${slug}/admin/interviews` |
| `candidateCommentService.ts` | `/${slug}/admin/candidates` |
| `candidateReviewService.ts` | `/${slug}/admin/candidates` |
| `JobPositionCommentService.ts` | `/${slug}/admin/positions` |

## App.tsx Route Analysis

### Duplicate Route Groups (Problem!)

The `App.tsx` has **two identical route groups**:

1. **Company-Scoped (NEW):** `/:companySlug/admin/*` (lines 238-281)
2. **Legacy (OLD):** `/company/*` (lines 302-346)

Both render the same components but:
- New routes require `companySlug` in URL
- Legacy routes get company from JWT token

### Recommendation

Remove the legacy `/company/*` routes and add redirects:

```tsx
// Add redirect from legacy to new
<Route path="/company/*" element={<RedirectToCompanyScoped />} />
```

## Migration Priority

### Phase 1 - Critical (Backend APIs used by frontend)
1. Interview templates service/router
2. Notifications service/router
3. Company pages service/router
4. Email templates service/router

### Phase 2 - High (Frontend navigation)
1. Update `CompanyLayout.tsx` sidebar links
2. Update all `navigate()` calls
3. Update all `<Link>` components
4. Update all `href` attributes

### Phase 3 - Cleanup
1. Remove legacy `/company/*` routes from App.tsx
2. Add redirect from old to new URLs
3. Update documentation

## Files Requiring Changes

### Backend (6 routers to migrate)
- `adapters/http/company_app/company/routers/enum_router.py`
- `adapters/http/company_app/company_page/routers/company_page_router.py`
- `adapters/http/company_app/notification/routers/notification_router.py`
- `adapters/http/company_app/company/routers/company_user_router.py`
- `adapters/http/shared/phase/routers/phase_router.py`
- `adapters/http/company_app/company/routers/company_role_router.py`

### Frontend Services (6 services to migrate)
- `src/services/companyInterviewTemplateService.ts`
- `src/services/companyPageService.ts`
- `src/services/notificationService.ts`
- `src/services/candidateReportService.ts`
- `src/services/emailTemplateService.ts`
- `src/services/customFieldValueService.ts`

### Frontend Components (~30 files with navigation)
- All files in `src/pages/company/`
- `src/components/company/CompanyLayout.tsx`
- Various other components

## Estimated Effort

| Task | Files | Complexity |
|------|-------|------------|
| Backend router migration | 6 | Medium |
| Frontend service migration | 6 | Low |
| Frontend navigation update | ~30 | Medium |
| Remove legacy routes | 1 | Low |
| Testing | - | High |

**Total estimated changes:** ~45 files
