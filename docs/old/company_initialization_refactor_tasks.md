# Company Initialization Refactor Tasks

## Overview

Currently, company initialization is mixed in `CreateCompanyCommand` which automatically calls `InitializeCompanyPhasesCommand`. We need to separate this into 3 distinct commands following DDD & CQRS principles:

1. **ONBOARDING** - Basic configuration (roles, pages)
2. **WORKFLOWS** - Default workflow configuration  
3. **SAMPLE DATA** - Optional sample data for evaluation

## Current State Analysis

### What Exists:
- ✅ `CreateCompanyCommand` - Creates company entity
- ✅ `InitializeCompanyPhasesCommand` - Creates phases and workflows (WORKFLOWS)
- ✅ `InitializeSampleDataCommand` - Creates sample users, candidates, and relationships (SAMPLE DATA)
- ✅ `CreateRoleCommand` - Creates individual company roles
- ✅ `CreateCompanyPageCommand` - Creates individual company pages
- ✅ `create_sample_roles()` function in `scripts/seed_dev_data.py` (not a command)

### What's Missing:
- ❌ `InitializeOnboardingCommand` - Command to create default roles and pages
- ❌ Automatic page creation during onboarding
- ❌ Page creation with content during sample data initialization
- ❌ Proper separation of concerns in `CreateCompanyCommand`

## Task Breakdown

### Phase 1: Create InitializeOnboardingCommand

#### Task 1.1: Create Command and Handler
**File**: `src/company/application/commands/initialize_onboarding_command.py`

**Command Structure**:
```python
@dataclass(frozen=True)
class InitializeOnboardingCommand(Command):
    """Command to initialize onboarding for a new company
    
    Creates:
    - 7 default company roles (HR Manager, Recruiter, Tech Lead, etc.)
    - 5 default company pages in DRAFT status (empty)
    """
    company_id: CompanyId
    create_pages: bool = True  # Whether to create default pages
    create_roles: bool = True  # Whether to create default roles
```

**Handler Dependencies**:
- `CompanyRoleRepositoryInterface` - To save roles
- `CompanyPageRepositoryInterface` - To save pages
- `CommandBus` - To dispatch `CreateRoleCommand` and `CreateCompanyPageCommand`

**Handler Logic**:
1. If `create_roles=True`:
   - Create 7 default roles using `CreateRoleCommand` via CommandBus
   - Roles: HR Manager, Recruiter, Tech Lead, Hiring Manager, Interviewer, Department Head, CTO
2. If `create_pages=True`:
   - Create 5 default pages in DRAFT status with empty content using `CreateCompanyPageCommand` via CommandBus
   - Pages: public_company_description, job_position_description, data_protection, terms_of_use, thank_you_application
   - Each page should have a default title and empty HTML content

#### Task 1.2: Register Command in Container
**File**: `core/container.py`

- Import `InitializeOnboardingCommand` and `InitializeOnboardingCommandHandler`
- Create provider `initialize_onboarding_command_handler`
- Dependencies: `company_role_repository`, `company_page_repository`, `command_bus`

#### Task 1.3: Export Command
**File**: `src/company/application/commands/__init__.py`

- Add `InitializeOnboardingCommand` and `InitializeOnboardingCommandHandler` to exports

---

### Phase 2: Refactor InitializeCompanyPhasesCommand (WORKFLOWS)

#### Task 2.1: Review and Document Current Implementation
**File**: `src/phase/application/commands/initialize_company_phases_command.py`

**Current State**: ✅ Already exists and works correctly

**Action**: 
- Verify the command is properly structured
- Ensure it follows DDD principles
- Document that this is the WORKFLOWS initialization command

**Note**: The command name `InitializeCompanyPhasesCommand` is acceptable, but we could consider renaming to `InitializeWorkflowsCommand` for clarity. However, since it's already in use, we'll keep the name but document it clearly.

#### Task 2.2: Ensure Command is Independent
- Verify that `InitializeCompanyPhasesCommand` can be called independently
- Ensure it doesn't have hidden dependencies on other initialization steps
- Document that this command can be called separately or as part of a sequence

---

### Phase 3: Enhance InitializeSampleDataCommand (SAMPLE DATA)

#### Task 3.1: Add Page Creation with Content
**File**: `src/company/application/commands/initialize_sample_data_command.py`

**Current State**: Creates users, candidates, and relationships

**Enhancement Needed**:
- Add method `_create_sample_pages()` that creates the 5 company pages with sample content
- Pages should be created with actual HTML content (not empty)
- Pages can be in DRAFT or PUBLISHED status depending on type
- Use `CreateCompanyPageCommand` via CommandBus

**Sample Content Structure**:
- Each page type should have predefined sample HTML content
- Content should be realistic and useful for evaluation
- Consider creating a helper method or constants file for sample content

#### Task 3.2: Update Execute Method
- Call `_create_sample_pages()` in the `execute` method
- Ensure pages are created after roles (if roles are created in onboarding)
- Order: Roles → Pages → Users → Candidates → Relationships

---

### Phase 4: Refactor CreateCompanyCommand

#### Task 4.1: Remove Automatic Workflow Initialization
**File**: `src/company/application/commands/create_company_command.py`

**Current Issue**: 
- `CreateCompanyCommand` automatically calls `InitializeCompanyPhasesCommand`
- This couples company creation with workflow initialization

**Action**:
- Remove the automatic dispatch of `InitializeCompanyPhasesCommand` from `CreateCompanyCommandHandler`
- `CreateCompanyCommand` should ONLY create the company entity
- Workflow initialization should be called explicitly by the caller

#### Task 4.2: Update Callers
**Files to Update**:
- `src/company/application/commands/register_company_with_user_command.py`
- `src/company/application/commands/link_user_to_company_command.py`
- `scripts/seed_dev_data.py`
- Any other places that call `CreateCompanyCommand`

**Action**:
- After calling `CreateCompanyCommand`, explicitly call:
  1. `InitializeOnboardingCommand` (for roles and pages)
  2. `InitializeCompanyPhasesCommand` (for workflows)
  3. Optionally: `InitializeSampleDataCommand` (for sample data)

---

### Phase 5: Update Container Registration

#### Task 5.1: Register InitializeOnboardingCommandHandler
**File**: `core/container.py`

- Add provider for `initialize_onboarding_command_handler`
- Ensure all dependencies are correctly wired

#### Task 5.2: Verify Existing Handlers
- Verify `initialize_company_phases_command_handler` is correctly registered
- Verify `initialize_sample_data_command_handler` is correctly registered

---

### Phase 6: Update Scripts and Endpoints

#### Task 6.1: Update Seed Script
**File**: `scripts/seed_dev_data.py`

**Current State**: 
- Has `create_sample_roles()` function (not a command)
- Calls `InitializeSampleDataCommand`

**Action**:
- Remove `create_sample_roles()` function
- Replace with `InitializeOnboardingCommand` call
- Update `main()` to call commands in correct order:
  1. `CreateCompanyCommand`
  2. `InitializeOnboardingCommand` (roles + empty pages)
  3. `InitializeCompanyPhasesCommand` (workflows)
  4. `InitializeSampleDataCommand` (sample data + pages with content)

#### Task 6.2: Update Registration Endpoints
**Files**:
- `src/company/application/commands/register_company_with_user_command.py`
- `src/company/application/commands/link_user_to_company_command.py`

**Registration Flow Logic**:

The registration process should call commands based on user selections during registration. The `RegisterCompanyWithUserCommand` receives an `include_example_data` boolean flag.

**Command Execution Logic**:

```python
# After CreateCompanyCommand succeeds:

# ALWAYS execute (regardless of options):
1. InitializeOnboardingCommand(
    company_id=company_id,
    create_roles=True,   # Always create default roles
    create_pages=True    # Always create empty pages in DRAFT
)

# CONDITIONALLY execute based on user options:
if initialize_workflows:
    2. InitializeCompanyPhasesCommand(
        company_id=company_id
    )

if include_example_data:
    3. InitializeSampleDataCommand(
        company_id=company_id,
        company_user_id=company_user_id,  # The admin user who registered
        num_candidates=50,
        num_recruiters=3,
        num_viewers=2
    )
    # Note: InitializeSampleDataCommand will update pages with content
    # So pages created in onboarding will be updated/replaced with sample content
```

**Detailed Flow**:

1. **User Registration Options** (from frontend):
   - `initialize_workflows: bool` - Whether to initialize default workflows (default: `true`)
   - `include_example_data: bool` - Whether to load sample data for evaluation (default: `false`)

2. **Command Execution Sequence**:

   **Scenario A: Minimal Registration** (`initialize_workflows=False`, `include_example_data=False`)
   ```
   CreateCompanyCommand
       ↓
   InitializeOnboardingCommand
       ├─→ Create 7 default roles
       └─→ Create 5 empty pages (DRAFT, empty content)
   ```
   **Result**: Company ready with roles and empty pages (no workflows, no sample data)

   **Scenario B: With Workflows** (`initialize_workflows=True`, `include_example_data=False`)
   ```
   CreateCompanyCommand
       ↓
   InitializeOnboardingCommand
       ├─→ Create 7 default roles
       └─→ Create 5 empty pages (DRAFT, empty content)
       ↓
   InitializeCompanyPhasesCommand
       ├─→ Create 3 phases (CANDIDATE_APPLICATION)
       └─→ Create 1 phase (JOB_POSITION_OPENING)
   ```
   **Result**: Company ready with roles, empty pages, and workflows

   **Scenario C: With Sample Data Only** (`initialize_workflows=False`, `include_example_data=True`)
   ```
   CreateCompanyCommand
       ↓
   InitializeOnboardingCommand
       ├─→ Create 7 default roles
       └─→ Create 5 empty pages (DRAFT, empty content)
       ↓
   InitializeSampleDataCommand
       ├─→ Create sample users (3 recruiters, 2 viewers)
       ├─→ Create 50 sample candidates
       ├─→ Create company-candidate relationships
       └─→ Update 5 pages with sample content (PUBLISHED/DRAFT)
   ```
   **Result**: Company ready with roles, sample content pages, and sample data (no workflows)

   **Scenario D: Full Registration** (`initialize_workflows=True`, `include_example_data=True`)
   ```
   CreateCompanyCommand
       ↓
   InitializeOnboardingCommand
       ├─→ Create 7 default roles
       └─→ Create 5 empty pages (DRAFT, empty content)
       ↓
   InitializeCompanyPhasesCommand
       ├─→ Create 3 phases (CANDIDATE_APPLICATION)
       └─→ Create 1 phase (JOB_POSITION_OPENING)
       ↓
   InitializeSampleDataCommand
       ├─→ Create sample users (3 recruiters, 2 viewers)
       ├─→ Create 50 sample candidates
       ├─→ Create company-candidate relationships
       └─→ Update 5 pages with sample content (PUBLISHED/DRAFT)
   ```
   **Result**: Company ready with roles, sample content pages, workflows, and sample data

3. **Page Handling Strategy**:
   - **Onboarding**: Creates pages empty in DRAFT status
   - **Sample Data**: Updates existing pages with sample content (or creates if they don't exist)
   - Pages can be in DRAFT or PUBLISHED status depending on the page type and sample data configuration

**Implementation in RegisterCompanyWithUserCommandHandler**:

```python
def execute(self, command: RegisterCompanyWithUserCommand) -> None:
    # Step 1: Create user
    # ... existing user creation code ...
    
    # Step 2: Create company
    create_company_command = CreateCompanyCommand(...)
    self.command_bus.dispatch(create_company_command)
    
    # Step 3: Link user to company
    # ... existing company_user creation code ...
    
    # Step 4: Initialize onboarding (ALWAYS)
    onboarding_command = InitializeOnboardingCommand(
        company_id=command.company_id,
        create_roles=True,
        create_pages=True
    )
    self.command_bus.dispatch(onboarding_command)
    
    # Step 5: Initialize workflows (CONDITIONAL)
    if command.initialize_workflows:
        workflows_command = InitializeCompanyPhasesCommand(
            company_id=command.company_id
        )
        self.command_bus.dispatch(workflows_command)
    
    # Step 6: Initialize sample data (CONDITIONAL)
    if command.include_example_data:
        sample_data_command = InitializeSampleDataCommand(
            company_id=command.company_id,
            company_user_id=company_user_id,  # The admin user
            num_candidates=50,
            num_recruiters=3,
            num_viewers=2
        )
        self.command_bus.dispatch(sample_data_command)
```

**Error Handling**:
- If any command fails, the previous commands should have already succeeded
- Consider transaction management if needed (rollback on failure)
- Log each step for debugging
- Return appropriate error messages to the user

**Note**: The same logic applies to `LinkUserToCompanyCommand` if it's used for registration scenarios.

---

### Phase 7: Frontend Changes for Registration Options

#### Task 7.1: Update Registration Types
**File**: `client-vite/src/types/companyRegistration.ts`

**Current State**: 
- Only has `include_example_data: boolean`

**Changes Needed**:
```typescript
export interface CompanyRegistrationRequest {
  // ... existing fields ...
  
  // Initialization Options
  initialize_workflows: boolean;      // NEW: Whether to initialize default workflows (default: true)
  include_example_data: boolean;       // EXISTING: Whether to include sample data (default: false)
  
  // ... existing fields ...
}
```

**Note**: 
- `initialize_workflows` should default to `true` (most users want default workflows)
- `include_example_data` should default to `false` (optional feature)

#### Task 7.2: Update AdditionalOptionsForm Component
**File**: `client-vite/src/components/registration/AdditionalOptionsForm.tsx`

**Current State**: 
- Only shows checkbox for `include_example_data`
- Description mentions workflows but doesn't separate them

**Changes Needed**:

1. **Add new checkbox for workflows** (checked by default):
```tsx
<div className="space-y-4">
  {/* Workflows Option */}
  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
    <div className="flex items-start space-x-3">
      <Info className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
      <div className="flex-1">
        <label className="flex items-start space-x-3 cursor-pointer group">
          <input
            type="checkbox"
            checked={formData.initialize_workflows}
            onChange={(e) => onChange('initialize_workflows', e.target.checked)}
            className="mt-1 w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500"
          />
          <div>
            <span className="text-gray-900 font-medium group-hover:text-green-600 transition">
              Inicializar workflows por defecto (Recomendado)
            </span>
            <p className="text-sm text-gray-600 mt-1">
              Esto creará workflows predefinidos para candidatos y posiciones de trabajo que puedes personalizar después.
            </p>
          </div>
        </label>
      </div>
    </div>
  </div>

  {/* Sample Data Option */}
  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
    <div className="flex items-start space-x-3">
      <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
      <div className="flex-1">
        <label className="flex items-start space-x-3 cursor-pointer group">
          <input
            type="checkbox"
            checked={formData.include_example_data}
            onChange={(e) => onChange('include_example_data', e.target.checked)}
            className="mt-1 w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <div>
            <span className="text-gray-900 font-medium group-hover:text-blue-600 transition">
              Incluir datos de ejemplo (Opcional)
            </span>
            <p className="text-sm text-gray-600 mt-1">
              Esto incluirá usuarios de ejemplo, candidatos, roles y páginas con contenido para ayudarte a evaluar la plataforma.
            </p>
          </div>
        </label>
      </div>
    </div>
  </div>
</div>
```

2. **Update component props**:
```tsx
interface AdditionalOptionsFormProps {
  formData: {
    initialize_workflows: boolean;  // NEW
    include_example_data: boolean;
    accept_terms: boolean;
    accept_privacy: boolean;
  };
  onChange: (field: string, value: boolean) => void;
  errors: Record<string, string>;
}
```

#### Task 7.3: Update CompanyRegisterPage Component
**File**: `client-vite/src/pages/public/CompanyRegisterPage.tsx`

**Changes Needed**:

1. **Update formData state**:
```tsx
const [formData, setFormData] = useState({
  // ... existing fields ...
  
  // Options
  initialize_workflows: true,        // NEW: Default to true
  include_example_data: false,       // Keep default false
  accept_terms: false,
  accept_privacy: false
});
```

2. **Update registrationData object**:
```tsx
const registrationData = {
  // ... existing fields ...
  initialize_workflows: formData.initialize_workflows,  // NEW
  include_example_data: formData.include_example_data,
  accept_terms: formData.accept_terms,
  accept_privacy: formData.accept_privacy
};
```

#### Task 7.4: Update Backend Request Schema
**File**: `adapters/http/company/schemas/company_registration_request.py`

**Changes Needed**:

```python
class CompanyRegistrationRequest(BaseModel):
    # ... existing fields ...
    
    # Initialization Options
    initialize_workflows: bool = True   # NEW: Default to True
    include_example_data: bool = False  # EXISTING: Default to False
    
    # ... existing fields ...
```

#### Task 7.5: Update RegisterCompanyWithUserCommand
**File**: `src/company/application/commands/register_company_with_user_command.py`

**Changes Needed**:

1. **Add new field to command**:
```python
@dataclass(frozen=True)
class RegisterCompanyWithUserCommand(Command):
    # ... existing fields ...
    
    # Options
    initialize_workflows: bool = True   # NEW
    include_example_data: bool = False
```

2. **Update handler logic**:
```python
def execute(self, command: RegisterCompanyWithUserCommand) -> None:
    # ... existing user and company creation ...
    
    # Step 4: Initialize onboarding (ALWAYS)
    onboarding_command = InitializeOnboardingCommand(
        company_id=command.company_id,
        create_roles=True,
        create_pages=True
    )
    self.command_bus.dispatch(onboarding_command)
    
    # Step 5: Initialize workflows (CONDITIONAL)
    if command.initialize_workflows:
        workflows_command = InitializeCompanyPhasesCommand(
            company_id=command.company_id
        )
        self.command_bus.dispatch(workflows_command)
    
    # Step 6: Initialize sample data (CONDITIONAL)
    if command.include_example_data:
        sample_data_command = InitializeSampleDataCommand(
            company_id=command.company_id,
            company_user_id=company_user_id,
            num_candidates=50,
            num_recruiters=3,
            num_viewers=2
        )
        self.command_bus.dispatch(sample_data_command)
```

#### Task 7.6: Update LinkUserToCompanyCommand
**File**: `src/company/application/commands/link_user_to_company_command.py`

**Changes Needed**:
- Apply the same changes as `RegisterCompanyWithUserCommand`:
  - Add `initialize_workflows: bool = True` field
  - Update handler to conditionally call `InitializeCompanyPhasesCommand`

#### Task 7.7: Update Service Layer (if needed)
**File**: `client-vite/src/services/companyRegistrationService.ts`

**Changes Needed**:
- Verify that the service correctly passes both `initialize_workflows` and `include_example_data` to the API
- Update TypeScript types if needed

---

### Phase 8: Create Sample Page Content

#### Task 8.1: Create Sample Content Constants
**File**: `src/company/application/constants/sample_page_content.py` (new file)

**Purpose**: Store sample HTML content for each page type

**Structure**:
```python
SAMPLE_PAGE_CONTENT = {
    PageType.PUBLIC_COMPANY_DESCRIPTION: {
        "title": "About Our Company",
        "html_content": "<h1>About Our Company</h1><p>...</p>",
        "meta_description": "...",
        "status": "PUBLISHED"  # or "DRAFT"
    },
    # ... for each page type
}
```

#### Task 8.2: Use Constants in InitializeSampleDataCommand
- Import sample content constants
- Use them when creating pages in `_create_sample_pages()`

---

### Phase 9: Testing and Validation

#### Task 9.1: Unit Tests
**Files to Create/Update**:
- `tests/unit/company/application/commands/test_initialize_onboarding_command.py`
- `tests/unit/company/application/commands/test_initialize_sample_data_command.py` (update existing)

**Test Cases**:
- Test that all 7 roles are created
- Test that all 5 pages are created in DRAFT status (onboarding)
- Test that pages are created with content (sample data)
- Test idempotency (can be called multiple times safely)
- Test partial creation (if one fails, others still succeed)

#### Task 9.2: Integration Tests
- Test full initialization flow
- Test that commands can be called independently
- Test that commands can be called in sequence

#### Task 9.3: Manual Testing
- Test company creation via API
- Test seed script execution
- Verify all roles and pages are created correctly

---

## Implementation Order

1. **Phase 1**: Create `InitializeOnboardingCommand` (roles + empty pages)
2. **Phase 8**: Create sample page content constants
3. **Phase 3**: Enhance `InitializeSampleDataCommand` (add pages with content)
4. **Phase 4**: Refactor `CreateCompanyCommand` (remove automatic workflow init)
5. **Phase 5**: Update container registrations
6. **Phase 6**: Update scripts and endpoints
7. **Phase 7**: Update frontend registration form (workflows + sample data options)
8. **Phase 9**: Testing

## Command Flow Diagram

### Minimal Registration Flow (`initialize_workflows=False`, `include_example_data=False`)

```
CreateCompanyCommand
    ↓
InitializeOnboardingCommand (ALWAYS)
    ├─→ Create 7 default roles
    └─→ Create 5 empty pages (DRAFT, empty content)
```

### Registration with Workflows Flow (`initialize_workflows=True`, `include_example_data=False`)

```
CreateCompanyCommand
    ↓
InitializeOnboardingCommand (ALWAYS)
    ├─→ Create 7 default roles
    └─→ Create 5 empty pages (DRAFT, empty content)
    ↓
InitializeCompanyPhasesCommand (CONDITIONAL - WORKFLOWS)
    ├─→ Create 3 phases (CANDIDATE_APPLICATION)
    └─→ Create 1 phase (JOB_POSITION_OPENING)
```

### Registration with Sample Data Flow (`initialize_workflows=True`, `include_example_data=True`)

```
CreateCompanyCommand
    ↓
InitializeOnboardingCommand (ALWAYS)
    ├─→ Create 7 default roles
    └─→ Create 5 empty pages (DRAFT, empty content)
    ↓
InitializeCompanyPhasesCommand (ALWAYS - WORKFLOWS)
    ├─→ Create 3 phases (CANDIDATE_APPLICATION)
    └─→ Create 1 phase (JOB_POSITION_OPENING)
    ↓
InitializeSampleDataCommand (CONDITIONAL - SAMPLE DATA)
    ├─→ Create sample users (3 recruiters, 2 viewers)
    ├─→ Create 50 sample candidates
    ├─→ Create company-candidate relationships
    └─→ Update 5 pages with sample content (PUBLISHED/DRAFT)
```

### Registration Decision Tree

```
User Registration
    │
    ├─→ initialize_workflows = False, include_example_data = False
    │   │
    │   └─→ Execute: ONBOARDING ONLY
    │       Result: Company with roles, empty pages (no workflows, no sample data)
    │
    ├─→ initialize_workflows = True, include_example_data = False
    │   │
    │   └─→ Execute: ONBOARDING + WORKFLOWS
    │       Result: Company with roles, empty pages, workflows
    │
    ├─→ initialize_workflows = False, include_example_data = True
    │   │
    │   └─→ Execute: ONBOARDING + SAMPLE DATA
    │       Result: Company with roles, sample content pages, sample data (no workflows)
    │
    └─→ initialize_workflows = True, include_example_data = True
        │
        └─→ Execute: ONBOARDING + WORKFLOWS + SAMPLE DATA
            Result: Company with roles, sample content pages, workflows, sample data
```

**Default Behavior**:
- `initialize_workflows = true` (recommended, most users want default workflows)
- `include_example_data = false` (optional, for evaluation purposes)

## Notes

- All commands should be idempotent (safe to call multiple times)
- Commands should handle partial failures gracefully
- Each command should be independently testable
- Commands should follow the existing DDD & CQRS patterns in the codebase
- Value Objects should be used for IDs (CompanyId, CompanyRoleId, PageId, etc.)
- Commands are void (return None)
- Use CommandBus to dispatch sub-commands when needed

