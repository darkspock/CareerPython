# Stage Assignments Integration Guide

**Version**: 1.0
**Date**: 2025-10-26
**Status**: Phase 4 Complete - Integration Ready

---

## Overview

Phase 4: Stage Assignments is 100% complete. This guide explains how to integrate the `StageAssignmentEditor` component into Position pages.

## Backend APIs Available

### Position Stage Assignment Endpoints

All endpoints are under `/position-stage-assignments`:

```typescript
POST   /assign                                    - Assign users to stage (bulk)
POST   /add-user                                  - Add single user
POST   /remove-user                               - Remove single user
POST   /copy-workflow                             - Copy from workflow defaults
GET    /position/{position_id}                    - List all assignments for position
GET    /position/{position_id}/stage/{stage_id}/users  - Get users for specific stage
```

### Supporting Endpoints

```typescript
GET    /api/company-workflows/stages/{workflow_id}  - List stages by workflow
GET    /company/{company_id}/users?active_only=true - List company users
```

---

## Frontend Integration Steps

### 1. Import Required Services and Component

```typescript
import { companyWorkflowService } from '../../services/companyWorkflowService';
import { StageAssignmentEditor } from '../../components/workflow';
import type { WorkflowStage } from '../../types/workflow';
```

### 2. Add State Management

Add these state variables to your component:

```typescript
const [workflowStages, setWorkflowStages] = useState<WorkflowStage[]>([]);
const [companyUsers, setCompanyUsers] = useState<Array<{ id: string; name: string; email: string }>>([]);
const [loadingStages, setLoadingStages] = useState(false);
const [loadingUsers, setLoadingUsers] = useState(false);
```

### 3. Load Workflow Stages

Add effect to load stages when workflow_id changes:

```typescript
useEffect(() => {
  const loadWorkflowStages = async () => {
    if (!formData.workflow_id) {
      setWorkflowStages([]);
      return;
    }

    setLoadingStages(true);
    try {
      const stages = await companyWorkflowService.listStagesByWorkflow(formData.workflow_id);
      setWorkflowStages(stages);
    } catch (err) {
      console.error('Error loading workflow stages:', err);
      setWorkflowStages([]);
    } finally {
      setLoadingStages(false);
    }
  };

  loadWorkflowStages();
}, [formData.workflow_id]);
```

### 4. Load Company Users

Add effect to load users when component mounts:

```typescript
useEffect(() => {
  const loadCompanyUsers = async () => {
    if (!companyId) return;

    setLoadingUsers(true);
    try {
      // Note: You'll need to create this service method
      const response = await api.authenticatedRequest(`/company/${companyId}/users?active_only=true`);

      // Map to the format expected by StageAssignmentEditor
      const users = response.map((user: any) => ({
        id: user.user_id,
        name: user.name || user.email,
        email: user.email
      }));

      setCompanyUsers(users);
    } catch (err) {
      console.error('Error loading company users:', err);
      setCompanyUsers([]);
    } finally {
      setLoadingUsers(false);
    }
  };

  loadCompanyUsers();
}, [companyId]);
```

### 5. Add Component to JSX

Add the component in your form, typically after the WorkflowSelector:

```tsx
{/* Workflow Selector */}
<div className="md:col-span-2">
  <WorkflowSelector
    companyId={companyId}
    selectedWorkflowId={formData.workflow_id}
    onWorkflowChange={(workflowId) => setFormData({ ...formData, workflow_id: workflowId })}
    label="Application Workflow (Optional)"
  />
  <p className="mt-1 text-sm text-gray-500">
    Select a workflow to automate candidate processing with custom fields and validation rules
  </p>
</div>

{/* Stage Assignments Editor */}
{formData.workflow_id && !loadingStages && workflowStages.length > 0 && (
  <div className="md:col-span-2">
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <StageAssignmentEditor
        positionId={id!}
        stages={workflowStages}
        companyUsers={companyUsers}
        disabled={saving || loadingUsers}
      />
      <p className="mt-3 text-sm text-gray-500">
        Assign team members to each workflow stage. They will be responsible for processing candidates at that stage.
      </p>
    </div>
  </div>
)}
```

---

## Integration Points

### CreatePositionPage

**Path**: `client-vite/src/pages/company/CreatePositionPage.tsx`

**When to show**: Only after position is created and has an ID

**Implementation options**:
1. **Post-creation step**: After creating position, navigate to edit page
2. **Wizard step**: Add as final step in creation wizard
3. **Optional initial setup**: Modal or section after creation

**Recommended approach**: Post-creation
```typescript
// After successful position creation:
const createdPosition = await PositionService.createPosition(formData);
navigate(`/company/positions/${createdPosition.id}/edit#assignments`);
```

### EditPositionPage ⭐ PRIMARY

**Path**: `client-vite/src/pages/company/EditPositionPage.tsx`

**When to show**: When workflow_id is set and stages are loaded

**Full integration**: See steps 1-5 above

**Key points**:
- Component appears automatically when workflow is selected
- Updates are saved in real-time
- No additional save button needed (component handles its own saves)

### PositionDetailPage

**Path**: `client-vite/src/pages/company/PositionDetailPage.tsx`

**Implementation**: Add "Edit Assignments" button

```tsx
{position.workflow_id && (
  <button
    onClick={() => navigate(`/company/positions/${position.id}/edit#assignments`)}
    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
  >
    <Users className="w-4 h-4 inline mr-2" />
    Edit Stage Assignments
  </button>
)}
```

---

## Component Props Reference

### StageAssignmentEditor

```typescript
interface StageAssignmentEditorProps {
  positionId: string;                      // Required: Position ID
  stages: WorkflowStage[];                 // Required: Array of workflow stages
  companyUsers: Array<{                    // Required: Available users
    id: string;
    name: string;
    email: string;
  }>;
  onAssignmentsChange?: (                  // Optional: Callback for updates
    assignments: PositionStageAssignment[]
  ) => void;
  disabled?: boolean;                      // Optional: Disable all interactions
}
```

### WorkflowStage Type

```typescript
interface WorkflowStage {
  id: string;
  workflow_id: string;
  name: string;
  description?: string;
  stage_order: number;
  is_initial: boolean;
  is_final: boolean;
  stage_type: 'review' | 'interview' | 'offer' | 'other';
  auto_advance: boolean;
  time_limit_hours?: number;
  required_approval: boolean;
  is_active: boolean;
}
```

---

## Service Method to Create

You'll need to add this method to a company user service:

```typescript
// client-vite/src/services/companyUserService.ts (create if doesn't exist)

import { api } from '../lib/api';

export class CompanyUserService {
  static async listCompanyUsers(companyId: string, activeOnly: boolean = true) {
    try {
      const response = await api.authenticatedRequest(
        `/company/${companyId}/users?active_only=${activeOnly}`
      );
      return response;
    } catch (error) {
      console.error('Error loading company users:', error);
      throw error;
    }
  }
}

export default CompanyUserService;
```

---

## Testing Checklist

### Backend (API Testing)

- [ ] POST /position-stage-assignments/assign - works with valid data
- [ ] POST /position-stage-assignments/add-user - adds user successfully
- [ ] POST /position-stage-assignments/remove-user - removes user successfully
- [ ] GET /position-stage-assignments/position/{id} - returns all assignments
- [ ] Verify unique constraint on (position_id, stage_id)
- [ ] Verify foreign key cascades work

### Frontend (Component Testing)

- [ ] Component loads stages correctly
- [ ] Component loads company users correctly
- [ ] Can add user to stage via dropdown
- [ ] Can remove user from stage
- [ ] Shows loading states appropriately
- [ ] Shows error messages when operations fail
- [ ] Shows success notifications
- [ ] Disabled state works correctly
- [ ] Component doesn't crash with empty stages array
- [ ] Component doesn't crash with empty users array

### Integration Testing

- [ ] Workflow selector changes trigger stage load
- [ ] Stage assignments persist after page refresh
- [ ] Multiple stages can have different users
- [ ] Same user can be assigned to multiple stages
- [ ] Component updates in real-time without page refresh
- [ ] Works in both Create and Edit position flows

---

## Known Limitations

1. **No role-based suggestions**: Users are shown as flat list (Phase 6 feature)
2. **No default assignments copy**: Must manually copy or implement "Copy from Workflow" button
3. **No permission checks**: Any user can edit assignments (Phase 5 feature)
4. **No task assignment**: This only assigns stage ownership, not individual tasks (Phase 6 feature)

---

## Future Enhancements (Later Phases)

### Phase 5: Application Processing
- Add permission checks before allowing edits
- Validate user has necessary role for stage

### Phase 6: Task Management
- Show user roles in the component
- Filter users by role compatibility with stage
- Add "Suggested Users" section based on roles

### Phase 7: Notifications
- Notify users when assigned to new stage
- Send digest of assignments

---

## Troubleshooting

### Stages don't load
- Verify workflow_id is set correctly
- Check browser console for API errors
- Verify workflow has stages created

### Users don't load
- Verify companyId is available
- Check GET /company/{id}/users endpoint
- Ensure user has permission to view company users

### Assignments don't save
- Check browser console for API errors
- Verify position_id and stage_id are valid
- Check backend logs for validation errors

### Component shows "No workflow stages"
- This is expected when no workflow is selected
- Select a workflow first using WorkflowSelector

---

## Example: Complete EditPositionPage Integration

See `client-vite/src/pages/company/EditPositionPage.tsx` for reference implementation pattern.

Key sections to add:
1. Import statements (lines ~6-8)
2. State variables (lines ~42-45)
3. Load stages effect (lines ~100-120)
4. Load users effect (lines ~122-145)
5. Component in JSX (lines ~280-300)

---

## Support

For questions or issues:
1. Check backend logs: `make logs`
2. Check frontend console for errors
3. Verify API endpoints with Postman/curl
4. Review Phase 4 implementation in `docs/WORKFLOW_IMPLEMENTATION_STATUS.md`

---

**Document Status**: ✅ Complete and Ready for Integration
