# Company-Scoped URL Architecture

## Problem Statement

Current architecture has endpoints like `/candidate/me` that have **no company context**. This causes:

1. **Impossible validation**: Cannot check if user is admin of "which company?" - there's no company in the request
2. **Blind candidate creation**: System auto-creates candidate profile without knowing the context
3. **Session mixing**: Admin accessing any candidate endpoint creates a candidate record

### Root Cause
The `/candidate/*` routes are company-agnostic, but the business logic requires company context to:
- Prevent admins from applying to their own company
- Scope candidate actions to a specific company context

## Proposed Solution: Company-Scoped URLs

**All URLs (except auth) must include company identifier.**

### URL Structure

```
# Public - No company context
/login
/register
/forgot-password

# Company-scoped - Everything else
/{company_slug}/positions                    → Public job board for company
/{company_slug}/positions/{id}               → Position detail
/{company_slug}/apply/{position_id}          → Application flow
/{company_slug}/candidate/me                 → My profile as candidate FOR THIS company
/{company_slug}/candidate/applications       → My applications TO THIS company
/{company_slug}/admin/dashboard              → Admin panel (requires admin role)
/{company_slug}/admin/candidates             → Manage candidates (requires admin role)
/{company_slug}/admin/positions              → Manage positions (requires admin role)
```

### Validation Logic

```python
@router.get("/{company_slug}/candidate/me")
def get_my_profile(company_slug: str, current_user: User):
    company = get_company_by_slug(company_slug)

    # VALIDATION: Admin cannot access candidate routes for their own company
    if is_user_admin_of_company(current_user.id, company.id):
        raise HTTPException(403, "Admins cannot access candidate portal for their own company")

    # Now we have company context - can proceed safely
    return get_or_create_candidate_profile(current_user.id, company.id)
```

## Requirements

### REQ-1: Company Slug in All Non-Auth URLs
**Priority**: Critical

Every endpoint except authentication must include `{company_slug}` as first path parameter.

**Examples**:
- `/acme-corp/positions` - View Acme Corp's job positions
- `/acme-corp/candidate/me` - My candidate profile for Acme Corp
- `/techstart/apply/pos_123` - Apply to TechStart position

### REQ-2: Company Slug Validation
**Priority**: Critical

Every request must validate that `{company_slug}` exists and is active.

```python
def get_company_from_slug(company_slug: str) -> Company:
    company = company_repository.get_by_slug(company_slug)
    if not company:
        raise HTTPException(404, "Company not found")
    if not company.is_active:
        raise HTTPException(404, "Company not found")
    return company
```

### REQ-3: Admin Self-Access Prevention
**Priority**: Critical

If user is admin/recruiter of company X, they CANNOT access `/{company_x_slug}/candidate/*` routes.

```python
def validate_not_own_company_candidate_access(user_id: str, company_id: str):
    if is_user_staff_of_company(user_id, company_id):
        raise HTTPException(
            403,
            "Staff members cannot access candidate portal for their own company"
        )
```

### REQ-4: Cross-Company Application Allowed
**Priority**: High

Admin of Company A CAN access `/company-b/candidate/*` routes - this is valid (job seeking at other companies).

### REQ-5: Company Slug in Database
**Priority**: High

Companies must have a unique, URL-safe slug.

```sql
ALTER TABLE companies ADD COLUMN slug VARCHAR(100) UNIQUE NOT NULL;
CREATE INDEX ix_companies_slug ON companies(slug);
```

**Slug rules**:
- Lowercase alphanumeric + hyphens only
- 3-100 characters
- Unique across all companies
- Examples: `acme-corp`, `tech-startup-inc`, `my-company`

### REQ-6: Redirect Logic
**Priority**: Medium

When user logs in, redirect based on their roles:
- If admin of any company → `/{primary_company_slug}/admin/dashboard`
- If candidate only → `/{last_applied_company_slug}/candidate/applications` or landing page

## Database Changes

### Companies Table
```sql
-- Add slug column
ALTER TABLE companies
ADD COLUMN slug VARCHAR(100);

-- Generate slugs from company names (one-time migration)
UPDATE companies
SET slug = LOWER(REGEXP_REPLACE(name, '[^a-zA-Z0-9]+', '-', 'g'));

-- Make slug required and unique
ALTER TABLE companies
ALTER COLUMN slug SET NOT NULL,
ADD CONSTRAINT uk_companies_slug UNIQUE (slug);

-- Add index
CREATE INDEX ix_companies_slug ON companies(slug);
```

### Candidates Table (Optional Enhancement)
Consider adding company context to candidates:

```sql
-- Candidate profile is now per-company
ALTER TABLE candidates
ADD COLUMN company_id VARCHAR(26) REFERENCES companies(id);

-- A user can have multiple candidate profiles (one per company they apply to)
ALTER TABLE candidates
DROP CONSTRAINT IF EXISTS candidates_user_id_key;

ALTER TABLE candidates
ADD CONSTRAINT uk_candidates_user_company UNIQUE (user_id, company_id);
```

**Note**: This is optional. Alternative is to keep candidates global but scope applications.

## Implementation Phases

### Phase 1: Add Company Slug to Companies
1. Add `slug` column to companies table
2. Create migration to generate slugs from names
3. Add slug validation in Company entity

### Phase 2: Create Company-Scoped Router Structure
1. Create base router with `/{company_slug}` prefix
2. Add middleware to extract and validate company
3. Add company context to request state

```python
# New router structure
company_scoped_router = APIRouter(prefix="/{company_slug}")

@company_scoped_router.middleware("http")
async def add_company_context(request: Request, call_next):
    company_slug = request.path_params.get("company_slug")
    company = get_company_by_slug(company_slug)
    request.state.company = company
    return await call_next(request)
```

### Phase 3: Migrate Existing Routes
1. Move `/candidate/*` → `/{company_slug}/candidate/*`
2. Move `/api/company/*` → `/{company_slug}/admin/*`
3. Keep `/public/positions` → `/{company_slug}/positions`
4. Update all controllers to use company from request state

### Phase 4: Update Frontend
1. Update all API calls to include company slug
2. Store current company context in app state
3. Update routing to include company slug
4. Handle company switching UI

### Phase 5: Add Validation Middleware
1. Implement admin self-access prevention
2. Add comprehensive logging
3. Add rate limiting per company

## API Changes Summary

### Before (Current)
```
GET  /candidate/profile              → Global candidate profile
GET  /candidate/experience           → Global experiences
GET  /candidate/education            → Global education
GET  /candidate/projects             → Global projects
GET  /candidate/application          → All applications (no company filter)
POST /candidate/application          → Apply without company context
```

### After (Implemented)
```
# Global routes (candidate profile is the same for all companies)
GET  /candidate/profile              → Global candidate profile
GET  /candidate/experience           → Global experiences
GET  /candidate/education            → Global education
GET  /candidate/projects             → Global projects

# Company-scoped routes (applications are per-company)
GET  /{company_slug}/candidate/company-info   → Company info (public)
GET  /{company_slug}/candidate/positions      → Open positions (public)
GET  /{company_slug}/candidate/me             → Profile in company context (blocked for staff)
GET  /{company_slug}/candidate/applications   → My applications TO THIS company
POST /{company_slug}/candidate/apply/{pos_id} → Apply to position (blocked for own company staff)
```

### Key Design Decision
**Profile is global, applications are company-scoped.**

- A candidate's CV (experiences, education, projects) is the same regardless of which company they apply to
- Applications are specific to each company
- Staff members are blocked from accessing candidate routes for their OWN company only

## Security Considerations

1. **Slug enumeration**: Company slugs are public (needed for job boards), so no security issue
2. **Authorization**: Every route must still check user permissions for that company
3. **Rate limiting**: Consider per-company rate limits to prevent abuse

## Migration Strategy

1. **Backward compatibility**: Keep old routes working temporarily with deprecation warnings
2. **Frontend coordination**: Coordinate frontend changes with backend deployment
3. **Redirect old URLs**: Add redirects from old URLs to new company-scoped URLs

## Open Questions

1. **Default company**: What if user accesses `/` without company slug? → Redirect to company selector or last used company
2. **Multiple companies**: User is admin of multiple companies - how to handle? → Company switcher in UI
3. **Candidate without company**: Can a user create a candidate profile without applying? → No, profile created on first application

## Files to Modify

### Backend
- `main.py` - Router structure
- `adapters/http/candidate_app/routers/*.py` - All candidate routes
- `adapters/http/company_app/**/*.py` - All company routes
- `src/company_bc/company/infrastructure/models/company_model.py` - Add slug
- `src/company_bc/company/domain/entities/company.py` - Add slug
- New: `adapters/http/middleware/company_context.py` - Company extraction middleware

### Frontend
- All API service files
- Router configuration
- App state management
- Navigation components

### Database
- New migration for slug column
- Data migration to generate slugs
