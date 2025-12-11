# Killer Questions Tab for Job Position Edit

## Overview

Add a new tab "Killer Questions" to the Job Position edit form that allows managing screening interview templates with knockout questions.

## Current State

### What Exists
1. **SCREENING template type** - Already implemented in `InterviewTemplateTypeEnum`
2. **Job Position has `screening_template_id`** - Direct reference to interview template
3. **Interview Template Structure**: Template → Sections → Questions with scoring
4. **Inline Template Creation**: `CreateInlineScreeningTemplateCommand` creates templates linked to positions
5. **Workflow can define default screening template** - Can be inherited

### What's Missing
- No "Killer Questions" tab in job position edit form
- No UI to view/edit screening questions inline
- No clone mechanism for position-specific modifications
- No visual distinction between inherited vs position-specific templates

## Proposed Solution

### Tab Structure: "Killer Questions"

```
┌─────────────────────────────────────────────────────────────────┐
│ Killer Questions                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─ Template Source ─────────────────────────────────────────┐   │
│ │ ○ Use workflow default (Technical Screening v2)          │   │
│ │ ○ Select existing template: [Dropdown ▼]                 │   │
│ │ ○ Create new template for this position                  │   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│ ┌─ Questions Preview ───────────────────────────────────────┐   │
│ │                                                            │   │
│ │ Section: Technical Skills                                  │   │
│ │ ┌──────────────────────────────────────────────────────┐  │   │
│ │ │ 1. What is your experience with Python?              │  │   │
│ │ │    Type: Scoring | Options: None/Basic/Advanced      │  │   │
│ │ └──────────────────────────────────────────────────────┘  │   │
│ │ ┌──────────────────────────────────────────────────────┐  │   │
│ │ │ 2. Do you have legal authorization to work here?     │  │   │
│ │ │    Type: Boolean | Killer: Yes (fails if No)         │  │   │
│ │ └──────────────────────────────────────────────────────┘  │   │
│ │                                                            │   │
│ │ Section: Availability                                      │   │
│ │ ┌──────────────────────────────────────────────────────┐  │   │
│ │ │ 3. When can you start?                               │  │   │
│ │ │    Type: Date                                        │  │   │
│ │ └──────────────────────────────────────────────────────┘  │   │
│ │                                                            │   │
│ └────────────────────────────────────────────────────────────┘   │
│                                                                  │
│ [Edit Questions]                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Edit Flow - Smart Clone Decision

**Simple Rule:**
- If template is used **only by this position** (or not used at all) → Edit directly, no questions asked
- If template is used **by other positions too** → Show clone decision modal

**Logic Flow:**
```
User clicks "Edit Questions"
    ↓
Count positions using this template (excluding current position)
    ↓
If count == 0:
    → Open editor directly (no modal)
    ↓
If count > 0:
    → Show clone decision modal
```

**Clone Decision Modal (only shown when template is shared):**

```
┌─────────────────────────────────────────────────────────────────┐
│ Edit Killer Questions                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ⚠️ This template is used by 12 other positions.                 │
│                                                                  │
│ How would you like to proceed?                                   │
│                                                                  │
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ ○ Edit the original template                              │   │
│ │   Changes will affect ALL 12 positions using this template│   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ ○ Create a copy for this position only (Recommended)      │   │
│ │   The original template will remain unchanged             │   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│                              [Cancel]  [Continue]                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**After cloning:** The position now has its own template. Next time user clicks Edit, it opens directly (no modal) because no other position uses it.

### Inline Question Editor

After choosing to edit (either original or clone):

```
┌─────────────────────────────────────────────────────────────────┐
│ Edit Questions                                    [Save] [Cancel]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Template: Technical Screening (Position-specific)               │
│                                                                  │
│ ┌─ Section: Technical Skills ─────────────── [+ Add Question] ─┐│
│ │                                                               ││
│ │ ┌─ Question 1 ─────────────────────────────────────────────┐ ││
│ │ │ Question: [What is your experience with Python?       ]  │ ││
│ │ │ Type: [Scoring ▼]                                        │ ││
│ │ │ Options:                                                 │ ││
│ │ │   [None    ] Score: [0 ]                                 │ ││
│ │ │   [Basic   ] Score: [50]                                 │ ││
│ │ │   [Advanced] Score: [100]                                │ ││
│ │ │ □ Killer Question (auto-reject if score < [___])         │ ││
│ │ │                                        [↑] [↓] [🗑️]      │ ││
│ │ └──────────────────────────────────────────────────────────┘ ││
│ │                                                               ││
│ │ ┌─ Question 2 ─────────────────────────────────────────────┐ ││
│ │ │ Question: [Do you have legal authorization to work?   ]  │ ││
│ │ │ Type: [Boolean ▼]                                        │ ││
│ │ │ ☑ Killer Question (auto-reject if answer is No)          │ ││
│ │ │                                        [↑] [↓] [🗑️]      │ ││
│ │ └──────────────────────────────────────────────────────────┘ ││
│ └───────────────────────────────────────────────────────────────┘│
│                                                                  │
│ [+ Add Section]                                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Model Changes

### Option A: Metadata-based Killer Flag (Recommended - No Schema Changes)

Use existing `metadata` field in InterviewTemplateQuestion:

```python
# In question metadata
{
    "is_killer": true,
    "killer_threshold": 50,  # Score below this = auto-reject
    "killer_fail_value": "No"  # For boolean questions
}
```

### Option B: Explicit Field (Requires Migration)

Add to `InterviewTemplateQuestion`:

```python
is_killer: bool = False
killer_threshold: Optional[int] = None  # For scoring questions
```

### Template Cloning

Add to `InterviewTemplate` entity:

```python
@dataclass
class InterviewTemplate:
    # ... existing fields ...
    source_template_id: Optional[str] = None  # Points to original if cloned
    is_position_specific: bool = False  # True if cloned for a specific position

    @classmethod
    def clone_for_position(cls, original: "InterviewTemplate", position_id: str) -> "InterviewTemplate":
        """Creates a position-specific copy of a template"""
        return cls(
            id=InterviewTemplateId.generate(),
            company_id=original.company_id,
            name=f"{original.name} (Position Copy)",
            # ... copy all other fields ...
            source_template_id=original.id.value,
            is_position_specific=True,
            metadata={
                **(original.metadata or {}),
                "cloned_for_position_id": position_id,
                "cloned_from_template_id": original.id.value,
                "cloned_at": datetime.utcnow().isoformat()
            }
        )
```

## Backend Implementation

### New Commands

1. **CloneScreeningTemplateForPositionCommand**
```python
@dataclass
class CloneScreeningTemplateForPositionCommand(Command):
    source_template_id: InterviewTemplateId
    position_id: JobPositionId
    company_id: CompanyId
```

2. **UpdateScreeningTemplateQuestionsCommand**
```python
@dataclass
class UpdateScreeningTemplateQuestionsCommand(Command):
    template_id: InterviewTemplateId
    sections: List[SectionData]  # Includes questions with killer flags
```

### New Queries

1. **GetScreeningTemplateWithQuestionsQuery**
```python
@dataclass
class GetScreeningTemplateWithQuestionsQuery(Query):
    template_id: InterviewTemplateId
    # Returns full template with sections and questions
```

2. **CountPositionsUsingTemplateQuery**
```python
@dataclass
class CountPositionsUsingTemplateQuery(Query):
    template_id: InterviewTemplateId
    # Returns count for warning message
```

### API Endpoints

```
GET    /api/company/positions/{id}/screening-template
       Returns current screening template with questions

POST   /api/company/positions/{id}/screening-template/clone
       Clones the template for this position

PUT    /api/company/positions/{id}/screening-template
       Updates the screening template (creates inline if none exists)

GET    /api/company/interview-templates?type=SCREENING&scope=APPLICATION
       Lists available screening templates for selection
```

## Frontend Implementation

### New Components

1. **KillerQuestionsTab.tsx**
   - Main tab component for job position form
   - Shows template source selector
   - Shows questions preview
   - Edit button with clone decision modal

2. **ScreeningTemplateSelector.tsx**
   - Radio options: workflow default, select existing, create new
   - Dropdown for existing templates

3. **QuestionsPreview.tsx**
   - Read-only view of sections and questions
   - Shows killer question indicators
   - Shows scoring options

4. **CloneDecisionModal.tsx**
   - Modal asking user whether to edit original or create copy
   - Shows count of affected positions

5. **InlineQuestionEditor.tsx**
   - Full CRUD for sections and questions
   - Killer question toggle with threshold
   - Reorder functionality
   - Scoring options editor

### State Management

```typescript
interface KillerQuestionsTabState {
  templateSource: 'workflow' | 'existing' | 'new' | 'position-specific';
  selectedTemplateId: string | null;
  template: ScreeningTemplate | null;
  isEditing: boolean;
  isCloneModalOpen: boolean;
  isDirty: boolean;
}
```

## Implementation Phases

### Phase 1: Read-Only Preview
- Add Killer Questions tab
- Template source selector (workflow default, existing, none)
- Questions preview component
- No editing capability yet

### Phase 2: Inline Creation
- "Create new" option
- Inline question editor for new templates
- Save creates template and links to position

### Phase 3: Edit with Clone
- Edit button with clone decision modal
- Clone command implementation
- Position-specific template tracking

### Phase 4: Killer Question Logic
- Killer question flag in metadata
- Interview scoring considers killer questions
- Auto-reject logic in interview completion handler

## Files to Create/Modify

### New Files
```
client-vite/src/components/jobPosition/form/KillerQuestionsTab.tsx
client-vite/src/components/interview/ScreeningTemplateSelector.tsx
client-vite/src/components/interview/QuestionsPreview.tsx
client-vite/src/components/interview/CloneDecisionModal.tsx
client-vite/src/components/interview/InlineQuestionEditor.tsx

src/interview_bc/interview_template/application/commands/clone_template_for_position.py
src/interview_bc/interview_template/application/queries/get_template_with_questions.py
src/interview_bc/interview_template/application/queries/count_positions_using_template.py

adapters/http/company_app/interview/routers/position_screening_router.py
```

### Files to Modify
```
client-vite/src/components/jobPosition/form/PositionFormTabs.tsx
  - Add new tab for Killer Questions

src/interview_bc/interview_template/domain/entities/interview_template.py
  - Add clone_for_position method
  - Add source_template_id and is_position_specific fields (optional)

adapters/http/company_app/job_position/routers/company_position_router.py
  - Add screening template endpoints
```

## Open Questions

1. **Should killer question logic be in interview scoring or separate service?**
   - Recommendation: Add to interview completion handler

2. **How to handle when workflow default changes after position has been using it?**
   - Option A: Position always inherits latest workflow default
   - Option B: Position snapshots template ID when created (current behavior)
   - Recommendation: Option B with notification when workflow default changes

3. **Should position-specific templates be visible in template library?**
   - Recommendation: No, filter them out in template listing, show only in position context

4. **Max questions/sections limit?**
   - Recommendation: No hard limit, but UI shows warning if > 20 questions

## Estimated Effort

| Phase | Description | Effort |
|-------|-------------|--------|
| Phase 1 | Read-Only Preview | 2-3 days |
| Phase 2 | Inline Creation | 3-4 days |
| Phase 3 | Edit with Clone | 2-3 days |
| Phase 4 | Killer Logic | 2-3 days |
| **Total** | | **9-13 days** |

## Decision Points for User

1. **Metadata vs Schema change for killer flag?**
   - Metadata = faster, no migration
   - Schema = cleaner, requires migration

2. **Phase order priority?**
   - Start with Phase 1 for immediate visibility
   - Or jump to Phase 2 if creation is more urgent

3. **Clone naming convention?**
   - `{original_name} (Position Copy)`
   - `{original_name} - {position_title}`
   - Let user rename during clone
