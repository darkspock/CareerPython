# Routing Architecture

This document explains the URL routing patterns used in CareerPython for both frontend and backend.

## Overview

The application uses **company-scoped URLs** where the company slug is part of the URL path. This allows:
- Multi-tenant architecture with clear URL separation
- SEO-friendly URLs for public pages
- Easy identification of which company context you're in

## URL Patterns

### 1. Company-Scoped Admin Routes (NEW - Preferred)

**Pattern:** `/{company_slug}/admin/*`

These are the **current standard** for company administration pages.

| URL | Description |
|-----|-------------|
| `/{slug}/admin/dashboard` | Company dashboard |
| `/{slug}/admin/candidates` | Talent pool (company_candidates) |
| `/{slug}/admin/candidates/:id` | Candidate detail |
| `/{slug}/admin/positions` | Job positions list |
| `/{slug}/admin/positions/:id` | Position detail |
| `/{slug}/admin/interviews` | Interviews management |
| `/{slug}/admin/settings` | Company settings |
| `/{slug}/admin/users` | User management |

**Example:** `/acme-corp/admin/positions`

### 2. Company-Scoped Candidate Routes

**Pattern:** `/{company_slug}/candidate/*`

For candidates interacting with a specific company.

| URL | Description |
|-----|-------------|
| `/{slug}/candidate/apply/:positionId` | Apply to position |
| `/{slug}/candidate/portal` | Candidate portal |

### 3. Company-Scoped Public Routes

**Pattern:** `/{company_slug}/public/*` (without /admin or /candidate)

Public pages visible to anyone.

| URL                                      | Description |
|------------------------------------------|-------------|
| `/{slug}/public/careers`                 | Public careers page |
| `/{slug}/public/positions/:positionSlug` | Public position detail |
| `/{slug}/public/about`                   | Company about page |

### 4. Legacy Routes (DEPRECATED)

**Pattern:** `/company/*`

These routes are **deprecated** and should not be used in new code.

| Legacy URL | New URL |
|------------|---------|
| `/company/dashboard` | `/{slug}/admin/dashboard` |
| `/company/candidates` | `/{slug}/admin/candidates` |
| `/company/positions` | `/{slug}/admin/positions` |

**Why deprecated:**
- No company context in URL (company ID extracted from JWT token)
- Not SEO-friendly
- Harder to share links
- Confusing multi-company scenarios

### 5. Global Admin Routes

**Pattern:** `/admin/*` (do not allow a company called admin)

For platform-wide administration (superadmin only).

| URL | Description |
|-----|-------------|
| `/admin/dashboard` | Platform dashboard |
| `/admin/companies` | All companies management |
| `/admin/users` | All users management |

### 6. Candidate Personal Routes

**Pattern:** `/candidate/*` (do not allow a company called candidate)

For candidate's personal profile and settings (not company-specific).

| URL | Description |
|-----|-------------|
| `/candidate/profile` | Personal profile |
| `/candidate/applications` | My applications |
| `/candidate/settings` | Account settings |

## Backend API Routes

### Company-Scoped API (NEW - Preferred)

**Pattern:** `/{company_slug}/admin/*`

```
GET  /{slug}/admin/positions              # List positions
POST /{slug}/admin/positions              # Create position
GET  /{slug}/admin/positions/:id          # Get position
PUT  /{slug}/admin/positions/:id          # Update position

GET  /{slug}/admin/candidates             # List company candidates
GET  /{slug}/admin/interviews             # List interviews
```

### Legacy API Routes (DEPRECATED)

**Pattern:** `/api/company/*`

```
# DEPRECATED - Do not use in new code
GET  /api/company/positions
POST /api/company/positions
```

## Data Models

### Company Candidates vs Candidate Applications

There are **two different concepts** that are often confused:

#### 1. `company_candidates` (Talent Pool)
- Candidates added directly to the company's talent pool
- May or may not have applied to any position
- Managed manually by recruiters
- Displayed at: `/{slug}/admin/candidates`

#### 2. `candidate_applications` (Job Applications), should have also a company_candidate record
- Candidates who applied to a specific job position
- Created when someone applies through the careers page
- Linked to a specific `job_position`
- **NOT automatically added to talent pool**

```
┌─────────────────┐         ┌──────────────────────┐
│   candidates    │         │   company_candidates │
│  (global pool)  │◄────────│    (talent pool)     │
└────────┬────────┘         └──────────────────────┘
         │
         │
         ▼
┌─────────────────────┐
│ candidate_applications │
│   (job applications)   │
└─────────────────────┘
```

## Frontend Services

Each service should use company-scoped URLs:

```typescript
// CORRECT - Company-scoped
function getBasePath(): string {
  const slug = localStorage.getItem('company_slug');
  return `/${slug}/admin/positions`;
}

// DEPRECATED - Avoid
const BASE_PATH = '/api/company/positions';
```

## Authentication & Authorization

### Company Context Dependencies (Backend)

```python
# For admin routes requiring company staff membership
from adapters.http.shared.dependencies.company_context import (
    AdminCompanyContext,    # Validates user is staff
    CurrentCompanyUser,     # Returns CompanyUserDto
)

@router.get("/{company_slug}/admin/positions")
def list_positions(
    company: AdminCompanyContext,      # Company from URL slug
    current_user: CurrentCompanyUser,  # Authenticated company user
):
    ...
```

### Frontend Route Protection

```tsx
// Company-scoped admin routes
<Route path="/:companySlug/admin/*" element={
  <ProtectedCompanyScopedRoute>  {/* Validates slug + auth */}
    <CompanyLayout />
  </ProtectedCompanyScopedRoute>
}>
```

## Migration Guide

### Moving from Legacy to Company-Scoped

1. **Frontend Navigation:**
```typescript
// Before
navigate('/company/positions');

// After
const slug = localStorage.getItem('company_slug');
navigate(`/${slug}/admin/positions`);
```

2. **API Calls:**
```typescript
// Before
fetch('/api/company/positions');

// After
const slug = localStorage.getItem('company_slug');
fetch(`/${slug}/admin/positions`);
```

3. **Links in Components:**
```tsx
// Before
<Link to="/company/candidates">

// After
<Link to={`/${companySlug}/admin/candidates`}>
```

## Common Issues

### "Why doesn't my candidate appear?"

Check which table you're querying:
- `company_candidates` = Talent pool (manually added)
- `candidate_applications` = Applied to positions

### "Why is the URL missing the company slug?"

You're using legacy routes. Update to use `/{slug}/admin/*` pattern.

### "How do I get the company slug?"

```typescript
// Frontend
const slug = localStorage.getItem('company_slug');

// Backend (from URL)
def endpoint(company_slug: str = Path(...)):
    ...
```
