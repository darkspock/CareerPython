# Frontend Workflow Pages Consolidation Analysis

## Current Situation

### Duplicated Routes
1. **`/company/workflows/{id}/edit`** → `EditWorkflowPage.tsx` (Generic system - **WORKING BETTER**)
2. **`/company/settings/job-position-workflows/{id}/edit`** → `EditJobPositionWorkflowPage.tsx` (Old system - **DEPRECATED**)

### Duplicated Functionality
Both `EditWorkflowPage.tsx` and `WorkflowAdvancedConfigPage.tsx` contain:
- **Custom Fields Editor** (`EntityCustomFieldEditor`)
- **Field Visibility Matrix** (`FieldVisibilityMatrix`)
- **Validation Rules Editor** (`ValidationRuleEditor`)

## Problem

1. **Two different edit pages** for the same workflow entity (backend has only one workflow identity)
2. **Duplicated functionality** between `EditWorkflowPage` and `WorkflowAdvancedConfigPage`
3. **Confusion** about which page to use
4. **Maintenance burden** - changes need to be made in multiple places

## Proposed Solution

### Phase 1: Consolidate Routes
1. **Update `JobPositionWorkflowsSettingsPage.tsx`** to use generic route:
   ```typescript
   editRoute={(id) => `/company/workflows/${id}/edit`}
   ```

2. **Remove route** `/company/settings/job-position-workflows/{id}/edit` from `App.tsx`

3. **Delete** `EditJobPositionWorkflowPage.tsx` (old system, no longer needed)

### Phase 2: Remove Duplication
1. **Keep** `EditWorkflowPage.tsx` as the single source of truth
2. **Remove** `WorkflowAdvancedConfigPage.tsx` (functionality already in EditWorkflowPage)
3. **Update** `WorkflowsSettingsPage.tsx` to remove `advancedConfigRoute` prop
4. **Remove route** `/company/workflows/{id}/advanced-config` from `App.tsx`

### Result
- **Single edit page**: `/company/workflows/{id}/edit` (works for all workflow types)
- **No duplication**: Custom Fields, Validation Rules, and Field Visibility all in one place
- **Cleaner navigation**: One clear path to edit workflows

## Implementation Steps

1. Update `JobPositionWorkflowsSettingsPage.tsx` to redirect to generic route
2. Remove old routes from `App.tsx`
3. Delete `EditJobPositionWorkflowPage.tsx`
4. Delete `WorkflowAdvancedConfigPage.tsx`
5. Update any navigation links that point to old routes
6. Test that all workflow types (CA, PO, CO) work with the generic page

