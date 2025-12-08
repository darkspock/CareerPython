# Company Folder Refactor Tasks

This document contains all tasks required to refactor the company folder frontend to use shadcn/ui components and fix React rules violations.

## Summary

- **Total Files to Refactor**: 50 files (22 components + 28 pages)
- **Available shadcn Components**: Dialog, Button, Input, Select, Card, Badge, Checkbox, Label, Textarea, Table, Tabs, Tooltip, Alert, Dropdown Menu, Popover
- **React Rules Violations**: 1 (useCompanyId hook)

---

## Phase 1: Fix React Rules Violations

### Task 1.1: Fix useCompanyId Hook

**File**: `src/hooks/useCompanyId.ts`

**Issue**: Uses `useMemo` with empty dependency array instead of `useState` with initializer function.

**Current Code**:
```tsx
export function useCompanyId(): string | null {
  return useMemo(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  }, []);
}
```

**Required Change**:
```tsx
import { useState } from 'react';

export function useCompanyId(): string | null {
  const [companyId] = useState<string | null>(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  });
  return companyId;
}
```

**Priority**: High

---

## Phase 2: Refactor Modal Components to Use Dialog

All modals currently use custom `<div>` overlays. They must be refactored to use the shadcn Dialog component.

### Task 2.1: Refactor InviteUserModal

**File**: `src/components/company/InviteUserModal.tsx`

**Changes Required**:
- Replace custom overlay div with `Dialog`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogDescription`, `DialogFooter`
- Replace native `<button>` with `Button` component
- Replace native `<input>` with `Input` component
- Replace native `<select>` with `Select`, `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectItem`
- Replace native `<label>` with `Label` component

**Imports to Add**:
```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"
```

**Priority**: High

---

### Task 2.2: Refactor AssignRoleModal

**File**: `src/components/company/AssignRoleModal.tsx`

**Changes Required**:
- Replace custom overlay with `Dialog` components
- Replace native `<button>` with `Button`
- Replace native `<select>` with `Select` components
- Replace native `<label>` with `Label`

**Priority**: High

---

### Task 2.3: Refactor RemoveUserConfirmModal

**File**: `src/components/company/RemoveUserConfirmModal.tsx`

**Changes Required**:
- Replace custom overlay with `Dialog` components
- Replace native `<button>` with `Button` (variant="destructive" for delete action)

**Priority**: High

---

### Task 2.4: Refactor BulkEmailModal

**File**: `src/components/company/email/BulkEmailModal.tsx`

**Changes Required**:
- Replace custom overlay with `Dialog` components
- Replace native form elements with shadcn components
- Replace native `<button>` with `Button`

**Priority**: Medium

---

## Phase 3: Refactor Form Pages

All form pages use native HTML form elements. They must be refactored to use shadcn form components.

### Task 3.1: Refactor AddCandidatePage

**File**: `src/pages/company/AddCandidatePage.tsx`

**Changes Required**:
- Replace native `<input>` with `Input`
- Replace native `<select>` with `Select` components
- Replace native `<textarea>` with `Textarea`
- Replace native `<label>` with `Label`
- Replace native `<button>` with `Button`
- Wrap form sections in `Card`, `CardHeader`, `CardContent`

**Priority**: High

---

### Task 3.2: Refactor EditCandidatePage

**File**: `src/pages/company/EditCandidatePage.tsx`

**Changes Required**:
- Same as AddCandidatePage

**Priority**: High

---

### Task 3.3: Refactor CreatePositionPage

**File**: `src/pages/company/CreatePositionPage.tsx`

**Changes Required**:
- Replace native form elements with shadcn components
- Use `Card` for form sections
- Use `Button` for actions

**Priority**: High

---

### Task 3.4: Refactor EditPositionPage

**File**: `src/pages/company/EditPositionPage.tsx`

**Changes Required**:
- Same as CreatePositionPage

**Priority**: High

---

### Task 3.5: Refactor CreateInterviewPage

**File**: `src/pages/company/CreateInterviewPage.tsx`

**Changes Required**:
- Replace native form elements with shadcn components
- Use `Card` for form sections
- Use `Button` for actions

**Priority**: Medium

---

### Task 3.6: Refactor EditInterviewPage

**File**: `src/pages/company/EditInterviewPage.tsx`

**Changes Required**:
- Same as CreateInterviewPage

**Priority**: Medium

---

### Task 3.7: Refactor CreateCompanyPagePage

**File**: `src/pages/company/CreateCompanyPagePage.tsx`

**Changes Required**:
- Replace native form elements with shadcn components

**Priority**: Medium

---

### Task 3.8: Refactor EditCompanyPagePage

**File**: `src/pages/company/EditCompanyPagePage.tsx`

**Changes Required**:
- Same as CreateCompanyPagePage

**Priority**: Medium

---

### Task 3.9: Refactor CreateJobPositionWorkflowPage

**File**: `src/pages/company/CreateJobPositionWorkflowPage.tsx`

**Changes Required**:
- Replace native form elements with shadcn components

**Priority**: Medium

---

### Task 3.10: Refactor EditJobPositionWorkflowCustomFieldsPage

**File**: `src/pages/company/EditJobPositionWorkflowCustomFieldsPage.tsx`

**Changes Required**:
- Replace native form elements with shadcn components

**Priority**: Medium

---

### Task 3.11: Refactor TemplateEditor

**File**: `src/components/company/email/TemplateEditor.tsx`

**Changes Required**:
- Replace native `<input>` with `Input`
- Replace native `<textarea>` with `Textarea`
- Replace native `<button>` with `Button`

**Priority**: Medium

---

### Task 3.12: Refactor EditCompanyPage

**File**: `src/pages/company/EditCompanyPage.tsx`

**Changes Required**:
- Replace native form elements with shadcn components

**Priority**: Medium

---

## Phase 4: Refactor List/Dashboard Pages

### Task 4.1: Refactor UsersManagementPage

**File**: `src/pages/company/UsersManagementPage.tsx`

**Changes Required**:
- Replace native `<button>` with `Button`
- Use `Table` components for user list if applicable
- Use `Card` for sections

**Priority**: High

---

### Task 4.2: Refactor CandidatesListPage

**File**: `src/pages/company/CandidatesListPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Table` for candidate list
- Use `Button` for actions
- Use `Input` for search/filters

**Priority**: High

---

### Task 4.3: Refactor PositionsListPage

**File**: `src/pages/company/PositionsListPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Card` or `Table` for position list
- Use `Button` for actions

**Priority**: High

---

### Task 4.4: Refactor CompanyInterviewsPage

**File**: `src/pages/company/CompanyInterviewsPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components

**Priority**: Medium

---

### Task 4.5: Refactor CompanyInterviewTemplatesPage

**File**: `src/pages/company/CompanyInterviewTemplatesPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components

**Priority**: Medium

---

### Task 4.6: Refactor CompanyPagesListPage

**File**: `src/pages/company/CompanyPagesListPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components

**Priority**: Medium

---

### Task 4.7: Refactor EmailTemplatesPage

**File**: `src/components/company/email/EmailTemplatesPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Card` for template cards
- Use `Button` for actions

**Priority**: Medium

---

### Task 4.8: Refactor TalentPoolPage

**File**: `src/components/company/talentPool/TalentPoolPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Card` for talent pool entries
- Use `Button` for actions
- Use `Input` for search

**Priority**: Medium

---

### Task 4.9: Refactor TaskDashboard

**File**: `src/components/company/task/TaskDashboard.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Card` for task cards
- Use `Button` for actions

**Priority**: Medium

---

### Task 4.10: Refactor WorkflowAnalyticsPage

**File**: `src/components/company/workflowAnalytics/WorkflowAnalyticsPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Card` for analytics sections

**Priority**: Low

---

### Task 4.11: Refactor PhasesPage

**File**: `src/pages/company/PhasesPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components

**Priority**: Medium

---

### Task 4.12: Refactor CompanyRolesPage

**File**: `src/pages/company/CompanyRolesPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components

**Priority**: Medium

---

### Task 4.13: Refactor JobPositionWorkflowsSettingsPage

**File**: `src/pages/company/JobPositionWorkflowsSettingsPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components

**Priority**: Medium

---

### Task 4.14: Refactor CompanySettingsPage

**File**: `src/pages/company/CompanySettingsPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Card` for settings sections
- Use `Button` for actions

**Priority**: Medium

---

## Phase 5: Refactor Detail Pages

### Task 5.1: Refactor CandidateDetailPage

**File**: `src/pages/company/CandidateDetailPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Card` for detail sections
- Use `Badge` for status/tags
- Use `Button` for actions
- Use `Tabs` if applicable

**Priority**: High

---

### Task 5.2: Refactor PositionDetailPage

**File**: `src/pages/company/PositionDetailPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components
- Use `Card` for detail sections
- Use `Badge` for status
- Use `Button` for actions

**Priority**: High

---

### Task 5.3: Refactor CompanyInterviewDetailPage

**File**: `src/pages/company/CompanyInterviewDetailPage.tsx`

**Changes Required**:
- Replace native elements with shadcn components

**Priority**: Medium

---

### Task 5.4: Refactor ViewCompanyPagePage

**File**: `src/pages/company/ViewCompanyPagePage.tsx`

**Changes Required**:
- Replace native elements with shadcn components

**Priority**: Low

---

## Phase 6: Refactor Card Components

### Task 6.1: Refactor ApplicationCard

**File**: `src/components/company/application/ApplicationCard.tsx`

**Changes Required**:
- Replace custom card div with `Card`, `CardHeader`, `CardContent`, `CardFooter`
- Use `Badge` for status
- Use `Button` for actions

**Priority**: Medium

---

### Task 6.2: Refactor TalentPoolCard

**File**: `src/components/company/talentPool/TalentPoolCard.tsx`

**Changes Required**:
- Replace custom card div with `Card` components
- Use `Badge` for tags/status
- Use `Button` for actions

**Priority**: Medium

---

### Task 6.3: Refactor EmailTemplateCard

**File**: `src/components/company/email/EmailTemplateCard.tsx`

**Changes Required**:
- Replace custom card div with `Card` components
- Use `Button` for actions

**Priority**: Medium

---

### Task 6.4: Refactor TaskCard

**File**: `src/components/company/task/TaskCard.tsx`

**Changes Required**:
- Replace custom card div with `Card` components
- Use `Badge` for priority/status
- Use `Button` for actions

**Priority**: Medium

---

### Task 6.5: Refactor CompanyPageCard

**File**: `src/components/company/CompanyPageCard.tsx`

**Changes Required**:
- Replace custom card div with `Card` components
- Use `Button` for actions

**Priority**: Low

---

## Phase 7: Refactor Badge Components

### Task 7.1: Refactor UserRoleBadge

**File**: `src/components/company/UserRoleBadge.tsx`

**Changes Required**:
- Replace custom badge span with `Badge` component
- Map role types to Badge variants

**Priority**: Low

---

### Task 7.2: Refactor UserStatusBadge

**File**: `src/components/company/UserStatusBadge.tsx`

**Changes Required**:
- Replace custom badge span with `Badge` component
- Map status types to Badge variants

**Priority**: Low

---

## Phase 8: Refactor Layout and Navigation

### Task 8.1: Refactor CompanyLayout

**File**: `src/components/company/CompanyLayout.tsx`

**Changes Required**:
- Replace native `<button>` elements with `Button`
- Use `Tooltip` for icon buttons
- Consider `DropdownMenu` for user menu

**Priority**: Medium

---

### Task 8.2: Refactor UserSettingsMenu

**File**: `src/components/company/UserSettingsMenu.tsx`

**Changes Required**:
- Replace native elements with `DropdownMenu` components
- Use `Button` for trigger

**Priority**: Medium

---

## Phase 9: Refactor Misc Components

### Task 9.1: Refactor ApplicationHistory

**File**: `src/components/company/application/ApplicationHistory.tsx`

**Changes Required**:
- Use `Card` for history entries if applicable
- Use `Badge` for status changes

**Priority**: Low

---

### Task 9.2: Refactor StageTransitionButton

**File**: `src/components/company/application/StageTransitionButton.tsx`

**Changes Required**:
- Replace native `<button>` with `Button`
- Consider using `Popover` or `DropdownMenu` for stage selection

**Priority**: Medium

---

### Task 9.3: Refactor UserPermissionsList

**File**: `src/components/company/UserPermissionsList.tsx`

**Changes Required**:
- Use `Badge` for permission tags
- Use `Checkbox` if permissions are toggleable

**Priority**: Low

---

### Task 9.4: Refactor ProtectedCompanyRoute

**File**: `src/components/company/ProtectedCompanyRoute.tsx`

**Changes Required**:
- Review and update any UI elements to use shadcn components

**Priority**: Low

---

## Component Mapping Reference

| Native HTML | shadcn Component | Import Path |
|-------------|------------------|-------------|
| `<button>` | `Button` | `@/components/ui/button` |
| `<input type="text">` | `Input` | `@/components/ui/input` |
| `<input type="checkbox">` | `Checkbox` | `@/components/ui/checkbox` |
| `<select>` | `Select`, `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectItem` | `@/components/ui/select` |
| `<textarea>` | `Textarea` | `@/components/ui/textarea` |
| `<label>` | `Label` | `@/components/ui/label` |
| Custom modal div | `Dialog`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogFooter` | `@/components/ui/dialog` |
| Custom card div | `Card`, `CardHeader`, `CardContent`, `CardFooter`, `CardTitle`, `CardDescription` | `@/components/ui/card` |
| Custom badge span | `Badge` | `@/components/ui/badge` |
| `<table>` | `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell` | `@/components/ui/table` |
| Custom tabs | `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent` | `@/components/ui/tabs` |
| Custom dropdown | `DropdownMenu`, `DropdownMenuTrigger`, `DropdownMenuContent`, `DropdownMenuItem` | `@/components/ui/dropdown-menu` |
| Custom tooltip | `Tooltip`, `TooltipTrigger`, `TooltipContent`, `TooltipProvider` | `@/components/ui/tooltip` |

---

## Button Variant Mapping

| Use Case | Variant | Example |
|----------|---------|---------|
| Primary action | `default` | Save, Create, Submit |
| Secondary action | `secondary` | Cancel, Back |
| Destructive action | `destructive` | Delete, Remove |
| Tertiary action | `outline` | Edit, View |
| Icon-only button | `ghost` + `size="icon"` | Close, Menu |
| Link-style button | `link` | Learn more |

---

## Priority Summary

### High Priority (Do First)
1. Task 1.1: Fix useCompanyId Hook
2. Task 2.1-2.3: Modal components (InviteUserModal, AssignRoleModal, RemoveUserConfirmModal)
3. Task 3.1-3.4: Main form pages (AddCandidatePage, EditCandidatePage, CreatePositionPage, EditPositionPage)
4. Task 4.1-4.3: Main list pages (UsersManagementPage, CandidatesListPage, PositionsListPage)
5. Task 5.1-5.2: Main detail pages (CandidateDetailPage, PositionDetailPage)

### Medium Priority (Do Second)
- Remaining form pages
- Remaining list/dashboard pages
- Card components
- Layout components
- StageTransitionButton

### Low Priority (Do Last)
- Badge components (UserRoleBadge, UserStatusBadge)
- View-only pages
- ApplicationHistory
- UserPermissionsList
- ProtectedCompanyRoute

---

## Estimated Task Count

| Phase | Tasks | Priority |
|-------|-------|----------|
| Phase 1: React Rules | 1 | High |
| Phase 2: Modals | 4 | High/Medium |
| Phase 3: Form Pages | 12 | High/Medium |
| Phase 4: List/Dashboard Pages | 14 | High/Medium/Low |
| Phase 5: Detail Pages | 4 | High/Medium/Low |
| Phase 6: Card Components | 5 | Medium/Low |
| Phase 7: Badge Components | 2 | Low |
| Phase 8: Layout/Navigation | 2 | Medium |
| Phase 9: Misc Components | 4 | Medium/Low |
| **Total** | **48** | |

---

## Notes

1. **Testing**: After each refactor, verify that the component still functions correctly
2. **Styling**: shadcn components use CSS variables defined in `globals.css` - ensure theme colors are configured
3. **Accessibility**: shadcn components have built-in accessibility - preserve all aria attributes
4. **Form State**: When refactoring forms, ensure form state management (React Hook Form or useState) remains intact
5. **i18n**: Preserve all `useTranslation` hooks and `t()` function calls
