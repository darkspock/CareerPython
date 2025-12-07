# Workflow System - Business Requirements

**Document Type:** Business Requirements
**Version:** 1.0
**Last Updated:** 2025-12-07
**Module:** Unified Workflow Engine

---

## Overview

The Unified Workflow System is the core engine that powers all process management in ATS Monkey. It provides a flexible, configurable framework for defining and executing business processes across different entity types (candidates, job positions, etc.), enabling companies to customize their hiring processes while maintaining consistency and automation.

---

## Design Philosophy

### Core Principles

1. **Unification**: Single engine for all workflow types
2. **Flexibility**: Fully customizable per company
3. **Automation**: Rule-based transitions and actions
4. **Validation**: Business rules ensuring process integrity
5. **Scalability**: Supports simple to enterprise-grade processes

### Architecture Overview

```
Phase (Macro-level container)
  └── Workflows[] (Process definitions)
        └── Stages[] (Individual steps)
              └── Rules[] (Validation & Automation)
              └── Configurations[] (Interviews, Emails, etc.)
```

---

## Core Concepts

### Phases

A **Phase** is a high-level container representing a major segment of the hiring process. Phases group related workflows and enable automatic transitions between process segments.

#### Phase Examples (Candidate Application)
| Phase | Objective | Default View |
|-------|-----------|--------------|
| **Sourcing** | Screening and candidate qualification | Kanban |
| **Evaluation** | Interviews and assessments | Kanban |
| **Offer & Pre-Onboarding** | Offer negotiation and document verification | List |

#### Phase Properties
| Property | Description |
|----------|-------------|
| `id` | Unique identifier |
| `company_id` | Owner company |
| `workflow_type` | Type of workflow in this phase |
| `name` | Display name |
| `objective` | Description (used for AI context) |
| `default_view` | KANBAN or LIST |
| `sort_order` | Order in the process |

### Workflows

A **Workflow** defines a sequence of stages that an entity moves through within a phase. Multiple workflows can exist within a single phase, allowing for parallel or alternative paths.

#### Workflow Types
| Type | Code | Purpose |
|------|------|---------|
| **Candidate Application** | CA | Managing candidate selection process |
| **Job Position Opening** | PO | Managing job position lifecycle |
| **Candidate Onboarding** | CO | Managing new hire onboarding |

#### Workflow Properties
| Property | Description |
|----------|-------------|
| `id` | Unique identifier |
| `company_id` | Owner company |
| `workflow_type` | Type enum |
| `name` | Display name |
| `description` | Purpose description |
| `display` | KANBAN or LIST view |
| `phase_id` | Parent phase |
| `status` | DRAFT, ACTIVE, ARCHIVED |
| `is_default` | Default workflow for the phase |

### Stages

A **WorkflowStage** represents a single step in a workflow. Stages define where an entity currently is in the process and what can happen there.

#### Stage Types
| Type | Description | Constraints |
|------|-------------|-------------|
| **INITIAL** | Entry point | Only ONE per workflow |
| **PROGRESS** | Intermediate step | Multiple allowed |
| **SUCCESS** | Successful completion | Only ONE per workflow |
| **FAIL** | Rejection/failure | Multiple allowed |
| **HOLD** | Temporary pause | Multiple allowed |
| **ARCHIVED** | Closed/completed | Multiple allowed |

#### Stage Properties
| Property | Description |
|----------|-------------|
| `id` | Unique identifier |
| `workflow_id` | Parent workflow |
| `name` | Display name |
| `description` | Stage purpose |
| `stage_type` | Type enum |
| `order` | Visual order |
| `kanban_display` | COLUMN, ROW, or NONE |
| `next_phase_id` | Auto-transition target |
| `style` | Visual styling (icon, colors) |
| `validation_rules` | Blocking rules (JsonLogic) |
| `recommended_rules` | Warning rules (JsonLogic) |
| `default_role_ids` | Assigned roles |
| `default_assigned_users` | Assigned users |
| `email_template_id` | Email on entry |
| `deadline_days` | Completion deadline |
| `estimated_duration_days` | Expected time in stage |
| `estimated_cost` | Cost tracking |
| `interview_configurations` | Auto-interview setup |

---

## Functional Requirements

### FR-WF01: Workflow Configuration

#### FR-WF01.1: Workflow Management
- **Create**: Build new workflows within phases
- **Edit**: Modify workflow structure and properties
- **Clone**: Duplicate existing workflows
- **Archive**: Disable without deletion
- **Delete**: Remove unused workflows

#### FR-WF01.2: Stage Management
- **Add/Remove**: Manage stages within workflow
- **Reorder**: Change stage sequence
- **Configure**: Set all stage properties
- **Validate**: Enforce stage type constraints

#### FR-WF01.3: Validation Rules
| Rule | Enforcement |
|------|-------------|
| Only one INITIAL | Creation/update blocked |
| Only one SUCCESS | Creation/update blocked |
| Must have SUCCESS | Save blocked |
| PROGRESS requires INITIAL | Save blocked |

### FR-WF02: Stage Transitions

#### FR-WF02.1: Manual Transitions
- **Drag-Drop**: Kanban board movement
- **Select**: Dropdown stage selection
- **Batch**: Move multiple entities

#### FR-WF02.2: Automatic Transitions
| Trigger | Action |
|---------|--------|
| **SUCCESS Stage** | Move to next phase's initial stage |
| **Rule Match** | Move to target stage |
| **Time Elapsed** | Auto-move after deadline |

#### FR-WF02.3: Transition Validation
- **Blocking Rules**: Prevent invalid transitions
- **Warning Rules**: Alert but allow override
- **Override Tracking**: Log when rules bypassed

### FR-WF03: Automation Rules

#### FR-WF03.1: Rule Types
| Type | Description | Action |
|------|-------------|--------|
| **BLOCK** | Prevent transition | Block with error |
| **WARNING** | Alert user | Show warning, allow proceed |
| **AUTO_MOVE** | Automatic transition | Move to target stage |

#### FR-WF03.2: Rule Components
```yaml
StageRule:
  name: "Rule Name"
  rule_type: BLOCK | WARNING | AUTO_MOVE
  blocked_stage_types: [SUCCESS, FAIL]  # Types to block
  blocked_stage_ids: ["specific-id"]     # Specific stages
  target_stage_id: "dest-id"             # For AUTO_MOVE
  evaluation_logic: AND | OR             # How to combine validations
  validations: [...]                     # Conditions to check
  allow_override: true                   # Can user bypass
  override_reason_required: true         # Needs justification
```

#### FR-WF03.3: Validation Types
| Type | Description | Example |
|------|-------------|---------|
| **CANDIDATE_FIELD** | Candidate attribute | expected_salary |
| **APPLICATION_FIELD** | Application attribute | source, date |
| **CUSTOM_FIELD** | Custom field value | Any configured field |
| **POSITION_COMPARISON** | Compare to position | salary vs. max_salary |
| **INTERVIEW_STATUS** | Interview state | All completed? |
| **EVALUATION_SCORE** | Score thresholds | Average >= 7 |

#### FR-WF03.4: Comparison Operators
| Category | Operators |
|----------|-----------|
| **Equality** | EQUALS, NOT_EQUALS |
| **Numeric** | GREATER_THAN, LESS_THAN, etc. |
| **Content** | CONTAINS, CONTAINS_ALL, CONTAINS_ANY |
| **List** | IN_LIST, NOT_IN_LIST |
| **Empty** | IS_EMPTY, IS_NOT_EMPTY |
| **Temporal** | DAYS_AGO_LESS_THAN, HOURS_AGO_GREATER_THAN, etc. |

#### FR-WF03.5: Aggregators (for collections)
| Aggregator | Description |
|------------|-------------|
| **ALL** | All items must match |
| **ANY** | At least one must match |
| **NONE** | No items should match |
| **COUNT** | Count matching items |
| **AVG** | Average of numeric values |
| **MIN/MAX** | Minimum/maximum value |
| **SUM** | Sum of values |

### FR-WF04: Stage Actions

#### FR-WF04.1: Interview Creation
- **Trigger**: Candidate enters stage
- **Mode**: AUTOMATIC (from configuration)
- **Template**: From stage interview_configurations
- **Roles**: From stage default_role_ids

#### FR-WF04.2: Email Notifications
- **Trigger**: Stage entry
- **Template**: From stage email_template_id
- **Recipients**: Candidate, assigned users
- **Variables**: Dynamic merge fields

#### FR-WF04.3: Role Assignments
- **Automatic**: From default_role_ids
- **Notification**: Alert assigned users
- **Tasks**: Create tasks for assigned roles

### FR-WF05: Visual Configuration

#### FR-WF05.1: Kanban Display
| Display | Description |
|---------|-------------|
| **COLUMN** | Full vertical column |
| **ROW** | Horizontal row (secondary stages) |
| **NONE** | Hidden from kanban view |

#### FR-WF05.2: Stage Styling
- **Icon**: Emoji or icon identifier
- **Colors**: Text color, background color
- **Order**: Visual sequence

### FR-WF06: Application Questions (Screening Questions)

Application Questions enable companies to collect additional information from candidates during the application process. These questions support automation rules for auto-qualification or disqualification.

#### FR-WF06.1: Design Philosophy (Hybrid Approach)

The system uses a **Workflow-Defined, Position-Enabled** model:

```
Workflow defines AVAILABLE questions (templates)
├── "expected_salary" (number)
├── "relocation_willing" (boolean)
├── "start_date_available" (date)
├── "drivers_license" (boolean)
└── "work_authorization" (select)

Job Position ENABLES specific questions
├── ✅ expected_salary (enabled for this role)
├── ✅ relocation_willing (enabled)
├── ❌ drivers_license (not relevant for remote role)
└── ❌ start_date_available (disabled)
```

**Rationale**: This hybrid approach balances:
- **UX**: Recruiters feel they're customizing the position
- **Automation**: Questions are workflow-defined, enabling predictable rules
- **Consistency**: Same question definitions across positions
- **Flexibility**: Each position shows only relevant questions

#### FR-WF06.2: Application Question Properties

| Property | Description |
|----------|-------------|
| `id` | Unique identifier |
| `workflow_id` | Parent workflow |
| `field_key` | Unique key for automation rules (e.g., `expected_salary`) |
| `label` | Display label for candidates |
| `description` | Help text for candidates |
| `field_type` | TEXT, NUMBER, DATE, SELECT, MULTISELECT, BOOLEAN |
| `options` | For SELECT/MULTISELECT types |
| `is_required_default` | Default required state |
| `validation_rules` | Field-level validation (min/max, pattern, etc.) |
| `order` | Display order |

#### FR-WF06.3: Position Question Configuration

| Property | Description |
|----------|-------------|
| `position_id` | Job position |
| `question_id` | Application question from workflow |
| `enabled` | Whether to show this question |
| `is_required` | Override required state (optional) |
| `order_override` | Override display order (optional) |

#### FR-WF06.4: Automation Integration

Application questions can be used in:

1. **Validation Rules** (blocking/warning):
```json
{
  "rule": {">=": [{"var": "expected_salary"}, {"*": [{"var": "position.max_salary"}, 1.2]}]},
  "field": "expected_salary",
  "message": "Expected salary exceeds budget by more than 20%"
}
```

2. **Auto-Move Rules**:
```json
{
  "rule_type": "AUTO_MOVE",
  "target_stage_id": "rejected-stage-id",
  "validations": [{
    "type": "APPLICATION_FIELD",
    "field": "work_authorization",
    "operator": "EQUALS",
    "value": "NO"
  }]
}
```

3. **Scoring/Qualification**:
- Questions contribute to candidate qualification scores
- Can trigger automatic stage transitions

#### FR-WF06.5: Common Application Questions

| Question | Type | Use Case |
|----------|------|----------|
| **Expected Salary** | NUMBER | Budget validation |
| **Available Start Date** | DATE | Timeline alignment |
| **Relocation Willing** | BOOLEAN | Location requirements |
| **Work Authorization** | SELECT | Legal compliance |
| **Driver's License** | BOOLEAN | Role requirements |
| **Notice Period** | SELECT | Hiring timeline |
| **How Did You Hear About Us** | SELECT | Source tracking |
| **Why This Role** | TEXT | Motivation screening |

#### FR-WF06.6: UX Guidelines

**For Recruiters (Position Editor)**:
- Show inherited questions from workflow
- Toggle to enable/disable each question
- Visual indicator for questions with automation rules
- Cannot create new questions (only at workflow level)

**For Candidates (Application Form)**:
- Clear, concise question labels
- Help text for complex questions
- Progress indicator for multi-step forms
- Mobile-optimized input controls

---

### FR-WF07: Phase Transitions

#### FR-WF07.1: Automatic Phase Advancement
```
Candidate in Stage A (SUCCESS, next_phase_id = Phase B)
    ↓ [Automatic Transition]
Move to Phase B → Default Workflow → INITIAL Stage
```

#### FR-WF07.2: Cross-Phase Display
- SUCCESS stages can show candidates from next phase's INITIAL
- Enables drag back within original phase kanban
- Updates phase_id when moved

---

## Rule Templates

Pre-configured rules companies can activate:

### Qualification Templates
| Template | Description |
|----------|-------------|
| TPL_REQUIRED_CV | Block if no resume |
| TPL_MIN_EXPERIENCE | Require years experience |
| TPL_REQUIRED_LANGUAGES | Check required languages |
| TPL_LOCATION_MATCH | Verify location compatibility |

### Compensation Templates
| Template | Description |
|----------|-------------|
| TPL_SALARY_IN_BUDGET | Block if over max salary |
| TPL_SALARY_WARNING | Warn if near max salary |

### Interview Templates
| Template | Description |
|----------|-------------|
| TPL_ALL_INTERVIEWS_COMPLETED | Block if pending interviews |
| TPL_MIN_INTERVIEW_SCORE | Require minimum score |
| TPL_NO_LOW_SCORES | Block if any score too low |
| TPL_MIN_POSITIVE_RECOMMENDATIONS | Require X positive recommendations |

### Timeline Templates
| Template | Description |
|----------|-------------|
| TPL_APPLICATION_NOT_STALE | Block old applications |
| TPL_AUTO_ARCHIVE_INACTIVE | Auto-move inactive candidates |
| TPL_INTERVIEW_PENDING_WARNING | Warn about pending interviews |

### Automation Templates
| Template | Description |
|----------|-------------|
| TPL_AUTO_ADVANCE_ON_INTERVIEWS_DONE | Move when interviews complete |
| TPL_AUTO_REJECT_NO_CV | Auto-reject without CV |

---

## Company Type Differentiation

### Startup / Small Business
- Simplified workflows (fewer stages)
- Fast process (minimal approvals)
- Multi-role users

### Mid-Size Company
- Standard workflows
- Balanced structure
- Additional stages (Team Fit Interview)

### Enterprise / Large Corporation
- Complex workflows
- Compliance stages (Background Check, Compliance Review)
- Multiple approval layers

### Recruitment Agency
- Client-focused workflows
- Client Matching stages
- Multi-client management

---

## Default Workflow Configuration

### Job Position Workflow (JOB_POSITION_OPENING)

| Stage | Type | Emoji |
|-------|------|-------|
| Draft | INITIAL | 📝 |
| Under Review | PROGRESS | 🔍 |
| Approved | PROGRESS | ✅ |
| Published | SUCCESS | 🌐 |
| Closed | ARCHIVED | 🔒 |
| Cancelled | FAIL | ❌ |

### Candidate Application Workflows

#### Phase 1: Sourcing
| Stage | Type | Display | Next Phase |
|-------|------|---------|------------|
| Pending | INITIAL | COLUMN | - |
| Screening | PROGRESS | COLUMN | - |
| Qualified | SUCCESS | COLUMN | Phase 2 |
| Not Suitable | FAIL | ROW | - |
| On Hold | PROGRESS | ROW | - |

#### Phase 2: Evaluation
| Stage | Type | Display | Next Phase |
|-------|------|---------|------------|
| HR Interview | INITIAL | COLUMN | - |
| Manager Interview | PROGRESS | COLUMN | - |
| Assessment Test | PROGRESS | COLUMN | - |
| Executive Interview | PROGRESS | COLUMN | - |
| Selected | SUCCESS | COLUMN | Phase 3 |
| Rejected | FAIL | ROW | - |

#### Phase 3: Offer & Pre-Onboarding
| Stage | Type | Display |
|-------|------|---------|
| Offer Proposal | INITIAL | LIST |
| Negotiation | PROGRESS | LIST |
| Document Submission | PROGRESS | LIST |
| Document Verification | SUCCESS | LIST |
| Lost | FAIL | LIST |

---

## HR Expert Recommendations

### Process Design Best Practices

#### 1. Keep It Simple
- **Recommendation**: Minimize stages; each should add clear value
- **Rationale**: Too many stages slow the process and frustrate candidates
- **Guideline**: 5-7 stages per workflow maximum

#### 2. Clear Stage Definitions
- **Recommendation**: Each stage should have explicit entry/exit criteria
- **Implementation**: Document purpose and requirements for each stage
- **Benefit**: Consistent usage across team members

#### 3. Time Tracking
- **Recommendation**: Set realistic stage duration expectations
- **Metrics to Track**:
  - Average time in stage
  - Bottleneck identification
  - SLA compliance
- **Implementation**: estimated_duration_days + reporting

### Automation Guidelines

#### 1. Start Manual, Then Automate
- **Recommendation**: Understand process before automating
- **Approach**: Run manual process first, identify patterns, then automate
- **Risk**: Premature automation codifies bad processes

#### 2. Override Capability
- **Recommendation**: Always allow human override of automation
- **Rationale**: Edge cases require human judgment
- **Implementation**: allow_override = true with reason tracking

#### 3. Notification Balance
- **Recommendation**: Avoid notification fatigue
- **Guidelines**:
  - Critical only: Stage changes, deadlines
  - Digest mode: Daily summary vs. real-time
  - Role-based: Only notify relevant people

### Compliance Considerations

#### 1. Audit Trail
- **Requirement**: Track all stage changes with reason
- **Data**: Who, when, from stage, to stage, reason
- **Retention**: Per jurisdiction requirements

#### 2. Consistent Treatment
- **Recommendation**: Same process for all candidates in same workflow
- **Implementation**: Locked workflows, template enforcement
- **Exception Process**: Documented deviation approval

#### 3. Rejection Documentation
- **Recommendation**: Always document rejection reasons
- **Implementation**: Required fields on FAIL stage transitions
- **Benefit**: Legal defensibility, process improvement

---

## Analytics & Reporting

### Pipeline Metrics
| Metric | Description |
|--------|-------------|
| **Stage Distribution** | Candidates per stage |
| **Conversion Rates** | % advancing between stages |
| **Drop-off Points** | Where candidates exit |
| **Time in Stage** | Average duration per stage |

### Process Metrics
| Metric | Description |
|--------|-------------|
| **Time to Hire** | Application to hire duration |
| **Bottleneck Analysis** | Slowest stages |
| **Rule Trigger Rates** | How often rules fire |
| **Override Frequency** | How often rules bypassed |

### Advanced Workflow Analytics

#### Stage-Level Analytics
| Metric | Description |
|--------|-------------|
| **Applications Count** | Total candidates in stage |
| **Average Time Spent** | Mean duration in stage |
| **Conversion Rate** | % advancing to next stage |
| **Dropout Rate** | % exiting at this stage |
| **Estimated vs Actual Duration** | Comparison for planning |
| **Estimated vs Actual Cost** | Cost variance analysis |

#### Bottleneck Detection Service
- **Bottleneck Scoring**: Algorithm to identify problem stages
- **Slowest Stage Identification**: Automatic detection
- **Highest Dropout Stage**: Where candidates leave most
- **Optimization Recommendations**: AI-suggested improvements

#### Workflow KPIs Dashboard
| KPI | Description |
|-----|-------------|
| **Overall Time to Hire** | Average days from application to hire |
| **Cost per Hire** | Total cost divided by successful hires |
| **Overall Conversion Rate** | Application to offer acceptance |
| **Fastest Stage** | Best performing stage |
| **Slowest Stage** | Stage needing attention |
| **Highest Conversion Stage** | Most effective stage |
| **Lowest Conversion Stage** | Needs optimization |

#### Stage Recommendations
- Auto-generated suggestions based on:
  - Time in stage vs estimated
  - Conversion rate trends
  - Bottleneck scores
  - Historical patterns

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Workflow configuration time | < 30 minutes for new company |
| Stage transition response | < 1 second |
| Rule evaluation time | < 500ms |
| Automation accuracy | > 99% correct triggers |
| User satisfaction with process | > 4/5 |

---

## Future Roadmap

### Phase 1 (Current)
- Basic workflow configuration
- Manual stage transitions
- Phase-based organization
- Interview integration

### Phase 2
- Advanced automation rules
- JsonLogic evaluator
- Auto-move functionality
- Time-based triggers

### Phase 3
- AI-powered optimization
- Process mining
- Predictive analytics
- Custom integrations

---

**Document Status**: Living document
**Owner**: Product Team
**Next Review**: Quarterly
