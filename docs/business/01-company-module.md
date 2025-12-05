# Company Module - Business Requirements

**Document Type:** Business Requirements
**Version:** 1.0
**Last Updated:** 2025-01-XX
**Module:** Company Area

---

## Overview

The Company module is the core operational area of ATS Monkey where organizations manage their entire recruitment lifecycle. 
It provides tools for job management, candidate tracking, interview coordination, team collaboration, and hiring analytics.

---

## User Personas

### 1. HR Manager
**Responsibilities:**
- Strategic oversight of hiring processes
- Communication standards and templates
- Final stage offer decisions
- Compliance and reporting

**Key Needs:**
- Dashboard with key metrics
- Process visibility across all positions
- Approval workflows for offers
- Compliance reporting tools

### 2. Recruiter
**Responsibilities:**
- Sourcing candidates
- Initial screening and qualification
- Pipeline management
- Candidate engagement

**Key Needs:**
- Efficient candidate search and filtering
- Bulk actions for high-volume processing
- Communication templates
- Activity tracking and reminders

### 3. Hiring Manager
**Responsibilities:**
- Position-specific hiring decisions
- Technical/functional evaluation
- Team fit assessment
- Final candidate selection

**Key Needs:**
- Focus on specific positions
- Evaluation forms and scorecards
- Interview feedback consolidation
- Comparison tools for final candidates

### 4. Interviewer
**Responsibilities:**
- Conduct assigned interviews
- Provide structured feedback
- Score candidates consistently

**Key Needs:**
- Interview schedule visibility
- Question guides and templates
- Easy feedback submission
- Candidate background information

### 5. Department Head / Executive
**Responsibilities:**
- High-level approvals
- Senior position decisions
- Headcount planning oversight

**Key Needs:**
- Summary views and reports
- Approval queues
- Minimal time investment
- Mobile access for quick decisions

---

## Functional Requirements

### FR-C01: Company Setup & Configuration

#### FR-C01.1: Company Profile
- **Description**: Companies can maintain their organizational profile
- **Fields**: Name, logo, industry, size, location, description
- **Public**: Information used on career pages and job listings

#### FR-C01.2: Company Type Selection
- **Description**: System adapts based on company type selection
- **Types**: Startup/Small, Mid-Size, Enterprise, Recruitment Agency
- **Impact**: Affects default workflows, roles, and configurations

#### FR-C01.3: Branding & Customization
- **Description**: Companies customize their candidate-facing appearance
- **Features**: Logo, colors, career page templates, email templates
- **Editor**: Visual Unlayer editor for page customization

### FR-C02: User & Role Management

#### FR-C02.1: User Roles
| Role | Description | Default Permissions |
|------|-------------|---------------------|
| **Owner** | Full system access | All permissions |
| **Admin** | Administrative access | All except billing |
| **HR Manager** | HR department lead | Manage all hiring processes |
| **Recruiter** | Talent acquisition | Manage candidates and positions |
| **Hiring Manager** | Position owner | Manage specific positions |
| **Interviewer** | Conduct interviews | View assigned interviews |
| **Guest** | External interviewer | Limited interview access |

#### FR-C02.2: Role Customization
- **Description**: Companies can create custom roles with specific permissions
- **Granularity**: Permission-level control for each feature
- **Inheritance**: Roles can inherit from base roles

#### FR-C02.3: Team Invitations
- **Description**: Invite users to join the company
- **Flow**: Email invitation with role pre-assignment
- **AI Feature**: System suggests appropriate roles based on company type

### FR-C03: Job Position Management

#### FR-C03.1: Position Creation
- **Fields**:
  - Basic: Title, department, location, work modality
  - Requirements: Experience, skills, languages, education
  - Compensation: Salary range (min/max), benefits
  - Process: Workflow assignment, deadline, headcount
  - Custom Attributes: Public / Private Custom Attributes (through the workflow configuration)

#### FR-C03.2: Position Workflow
- **Stages**: Draft → Under Review → Approved → Published → Closed → Cancelled
- **Customization**: Company-specific stages and approval flows
- **Visibility**: Stage determines public visibility

#### FR-C03.3: Position Publishing
- **Channels**: Company career page, global job board, external integrations
- **Control**: Per-position visibility settings
- **SEO**: Metadata optimization for search engines
- **Customization**: Custom Attributes through workflow configuration

#### FR-C03.4: Position Cloning
- **Description**: Duplicate existing positions for similar roles
- **Customization**: Select which elements to clone

#### FR-C03.5: Position Comments
- **Purpose**: Team collaboration on job positions
- **Structure**: Same as candidate comments (visibility, review status)
- **Scope**: Stage-specific or global comments

#### FR-C03.6: Position Activity Log
- **Purpose**: Audit trail for all position changes
- **Activity Types**:
  | Type | Tracked Data |
  |------|--------------|
  | CREATED | Initial creation details |
  | EDITED | Changed fields, old/new values |
  | STAGE_MOVED | Previous and new stage |
  | STATUS_CHANGED | Previous and new status |
  | COMMENT_ADDED | Comment reference |
- **Features**: Immutable log, rich metadata, timeline view

#### FR-C03.7: Position Stage Assignments
- **Purpose**: Assign team members to specific workflow stages
- **Features**:
  - Assign/remove users from stages
  - Bulk assignment
  - Copy assignments from another position
  - View assigned users per stage

#### FR-C03.8: Position Visibility
- **Levels**:
  | Level | Description |
  |-------|-------------|
  | HIDDEN | Internal draft only |
  | INTERNAL | Company-wide visibility |
  | PUBLIC | External candidates can see |

### FR-C04: Candidate Pipeline Management

#### FR-C04.1: Kanban Board View
- **Description**: Visual pipeline management with drag-and-drop
- **Columns**: Configurable based on workflow stages
- **Rows**: Optional horizontal grouping for secondary stages
- **Actions**: Quick actions from card context menu

#### FR-C04.2: List View
- **Description**: Tabular view for detailed candidate information
- **Features**: Sorting, filtering, bulk actions, custom columns
- **Export**: CSV/Excel export capability

#### FR-C04.3: Candidate Cards
- **Information**: Photo, name, current stage, key indicators
- **Quick Actions**: Move stage, schedule interview, add note
- **Visual Cues**: Icons for pending interviews, warnings, deadlines
- **Priority Indicator**: Color-coded priority (HIGH=red, MEDIUM=yellow, LOW=green)
- **Ownership Badge**: COMPANY_OWNED (blue) or USER_OWNED (purple)
- **Comment Count**: Badge showing number of comments
- **Tags Display**: Candidate tags visible on card

#### FR-C04.4: Candidate Detail View
- **Header**: Name, email, edit button, move to stage dropdown
- **Sidebar**: Status card, priority, workflow info, stage transition buttons, dates
- **Tabs**:
  - **Information**: Contact details, tags, status, job position
  - **Comments**: Team notes with visibility and review status (see FR-C04.6)
  - **Reviews**: Structured evaluations with scoring (see FR-C05.4)
  - **Documents**: File attachments (see FR-C04.5)
  - **Interviews**: Scheduled and completed interviews
  - **History**: Stage timeline with full activity log
  - **Custom Fields**: Workflow-specific custom data fields

#### FR-C04.5: Document Attachments
- **Supported Types**: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG
- **Features**:
  - Upload with progress indicator
  - File list with name, size, upload date
  - Download and delete capabilities
  - File size display in KB

#### FR-C04.6: Candidate Comments
- **Purpose**: Team collaboration through stage-specific or global notes
- **Visibility Levels**:
  - PRIVATE: Only visible to creator
  - SHARED: Visible to all team members
  - SHARED_WITH_CANDIDATE: Also visible to candidate
- **Review Status**: PENDING or REVIEWED for processing tracking
- **Features**:
  - Filter by: Current Stage, Global, All
  - Toggle review status
  - Pending comments counter badge
  - Author and timestamp display

#### FR-C04.7: Tags & Priority
- **Tags**: Add/remove custom tags for categorization and filtering
- **Priority Levels**: HIGH, MEDIUM, LOW with visual indicators
- **Ownership**: COMPANY_OWNED or USER_OWNED with transfer capability

#### FR-C04.8: Task Assignment
- **Purpose**: Assign candidate processing to team members
- **Task Status**: PENDING, IN_PROGRESS, COMPLETED, BLOCKED
- **Actions**: Claim task, unclaim task, view "My assigned tasks"

### FR-C05: Candidate Evaluation

#### FR-C05.1: Scoring System
- **Scale**: 0-100 overall score
- **Components**: Interview scores, assessment results, evaluator ratings
- **Modes**: Absolute (higher score is better)

#### FR-C05.2: Feedback Collection
- **Structured**: Form-based with predefined criteria
- **Freeform**: Open text feedback
- **Recommendation**: Yes/No/Maybe with confidence level

#### FR-C05.3: Candidate Reviews (4-Point Scale)
- **Purpose**: Quick structured evaluation by team members
- **Scoring Scale**:
  | Score | Value | Icon | Meaning |
  |-------|-------|------|---------|
  | BAN | 0 | 🚫 | Strongly not recommended |
  | NOT_RECOMMENDED | 3 | 👎 | Does not meet criteria |
  | RECOMMENDED | 6 | 👍 | Meets criteria |
  | FAVORITE | 10 | ❤️ | Top candidate |
- **Features**:
  - Optional comment with score
  - Stage-specific or global reviews
  - Review status tracking (PENDING/REVIEWED)
  - Average score display with icon
  - Review count badge

#### FR-C05.4: Comparison Tools
- **Side-by-Side**: Compare multiple candidates
- **Scorecard Summary**: Aggregate scores across evaluators
- **Qualification Matrix**: Requirements vs. candidate attributes

### FR-C06: Interview Management

See detailed requirements in [05-interview-system.md](./05-interview-system.md)

**Key Features:**
- Interview scheduling with calendar integration
- Template-based interview structures
- Scoring and feedback collection
- External interviewer support
- AI-assisted interview capabilities

### FR-C07: Workflow Management

See detailed requirements in [06-workflow-system.md](./06-workflow-system.md)

**Key Features:**
- Multi-phase pipeline configuration
- Custom stage creation
- Validation rules and automation
- Automatic transitions

### FR-C08: Communication

#### FR-C08.1: Email Templates
- **Types**: Application received, Interview invitation, Offer, Rejection
- **Personalization**: Merge tags for candidate/position data
- **Editor**: Visual template builder with preview

#### FR-C08.2: Bulk Communication
- **Description**: Send messages to multiple candidates
- **Filters**: By stage, position, date range
- **Tracking**: Open rates, response rates

#### FR-C08.3: Notes & Comments
- **Types**: Internal (team only), External (candidate visible)
- **Mentions**: @mention team members
- **Threading**: Reply capability on notes

### FR-C09: Analytics & Reporting

#### FR-C09.1: Dashboard Metrics
| Metric | Description |
|--------|-------------|
| **Time-to-Hire** | Average days from application to hire |
| **Pipeline Velocity** | Average time in each stage |
| **Source Effectiveness** | Application/hire rates by source |
| **Recruiter Workload** | Candidates per recruiter |
| **Offer Acceptance Rate** | Offers accepted vs. extended |
| **Diversity Metrics** | Demographics at each stage |

#### FR-C09.2: Custom Reports
- **Builder**: Drag-and-drop report creation
- **Filters**: Date range, position, source, stage
- **Export**: PDF, Excel, CSV formats
- **Scheduling**: Automated report delivery

#### FR-C09.3: Activity Logs
- **Tracking**: All user actions with timestamps
- **Audit Trail**: Who did what, when
- **Compliance**: Data retention and access logs

### FR-C10: AI-Powered Candidate Reports

#### FR-C10.1: Report Generation
- **Input**: All candidate data, comments, interview answers
- **Output**: Comprehensive markdown report
- **Format**: Executive summary, strengths, concerns, recommendation
- **Export**: PDF download capability

### FR-C11: Talent Pool

#### FR-C11.1: Talent Pool Management
- **Purpose**: Maintain database of candidates for future opportunities
- **Features**:
  - Add candidates to talent pool
  - Remove from talent pool
  - Update entry status
  - Search talent pool
  - "Silver medalist" tracking

#### FR-C11.2: Re-engagement
- **Purpose**: Enable returning to previously evaluated candidates
- **Features**:
  - Status tracking per candidate
  - Quick re-application to new positions
  - Historical evaluation access

### FR-C12: Workflow Analytics

#### FR-C12.1: Stage Analytics
| Metric | Description |
|--------|-------------|
| **Applications Count** | Candidates currently in stage |
| **Average Time** | Duration in stage |
| **Conversion Rate** | % moving to next stage |
| **Dropout Rate** | % exiting process |

#### FR-C12.2: Bottleneck Detection
- **Purpose**: Identify process inefficiencies
- **Features**:
  - Bottleneck scoring per stage
  - Slowest stage identification
  - Optimization recommendations

#### FR-C12.3: Workflow KPIs
| KPI | Description |
|-----|-------------|
| **Time to Hire** | Average days to complete |
| **Cost per Hire** | Average hiring cost |
| **Overall Conversion** | Application to hire rate |
| **Fastest/Slowest Stage** | Stage performance |

---

## Workflow Integration Points

### Stage Change Triggers
1. **Validation Rules**: Block or warn based on conditions
2. **Automatic Interviews**: Create interviews when entering configured stages
3. **Email Notifications**: Send templates when entering stages
4. **Role Assignments**: Notify assigned roles of new candidates

### Cross-Phase Transitions
1. **Automatic Advancement**: Move to next phase on SUCCESS stage
2. **Phase Assignment**: Update candidate's phase reference
3. **Workflow Reset**: Enter initial stage of new phase's default workflow

---

## HR Expert Recommendations

### Recruitment Process Optimization

#### 1. Structured Hiring Process
- **Recommendation**: Implement consistent evaluation criteria across all positions
- **Rationale**: Reduces bias, improves quality, ensures legal compliance
- **Implementation**: Template-based interviews, standardized scorecards

#### 2. Candidate Communication Standards
- **Recommendation**: Set SLA targets for candidate response times
- **Suggested SLAs**:
  - Application acknowledgment: Within 24 hours
  - Stage update: Within 3 business days
  - Rejection notification: Within 5 business days of decision
- **Implementation**: Automated triggers, reminder system for overdue actions

#### 3. Collaborative Hiring
- **Recommendation**: Involve multiple stakeholders in hiring decisions
- **Rationale**: Reduces single-point bias, improves team buy-in
- **Implementation**: Required minimum evaluators per stage, scorecard aggregation

#### 4. Talent Pool Management
- **Recommendation**: Maintain relationships with qualified candidates not hired
- **Features Needed**:
  - "Silver medalist" tagging
  - Periodic re-engagement campaigns
  - Quick application for new positions
- **Rationale**: Reduces future sourcing costs, improves time-to-hire

### Compliance & Legal Considerations

#### 1. Data Protection
- **GDPR Compliance**: Right to access, right to deletion, data portability
- **CCPA Compliance**: California consumer privacy requirements
- **Implementation**: Consent tracking, data export tools, deletion workflows

#### 2. Equal Opportunity
- **EEO Tracking**: Voluntary demographic data collection
- **OFCCP Compliance**: Federal contractor requirements
- **Adverse Impact Analysis**: Stage-by-stage demographic tracking

#### 3. Documentation
- **Requirement**: Document reasons for all hiring decisions
- **Implementation**: Mandatory notes on stage changes, rejection reasons
- **Retention**: Configurable retention policies per jurisdiction

### Process Improvements

#### 1. Interview Load Balancing
- **Problem**: Uneven interview distribution among team members
- **Solution**: Automatic assignment based on availability and workload
- **Benefit**: Faster scheduling, reduced interviewer burnout

#### 2. Feedback Loop
- **Problem**: Recruiters don't know if quality of candidates meets hiring manager needs
- **Solution**: Post-hire feedback surveys, source quality tracking
- **Benefit**: Continuous improvement in sourcing strategy

#### 3. Candidate Experience Surveys
- **Recommendation**: Collect feedback at key touchpoints
- **Touchpoints**: Post-application, post-interview, post-decision
- **Metrics**: NPS score, process satisfaction, communication quality

---

## Non-Functional Requirements

### Performance
- Dashboard load time: < 2 seconds
- Candidate search results: < 1 second
- Kanban drag-and-drop: Real-time response
- Bulk actions: Progress indicator for > 10 items

### Usability
- Mobile-responsive design
- Keyboard navigation support
- Accessibility compliance (WCAG 2.1 AA)
- Multi-language support (i18n)

### Security
- Role-based access control (RBAC)
- Audit logging for all actions
- Data encryption at rest and in transit
- SSO integration capability

---

## Integration Requirements

### Calendar Systems
- Google Calendar
- Microsoft Outlook
- Apple Calendar
- iCal export

### Communication
- Email (SMTP/API)
- Future: SMS notifications
- Future: Slack/Teams integration

### Job Boards
- Future: LinkedIn integration
- Future: Indeed integration
- API for custom integrations

---

## Success Criteria

| Metric | Target |
|--------|--------|
| User adoption rate | > 80% of invited users active |
| Average session duration | > 15 minutes |
| Feature utilization | > 60% of features used monthly |
| User satisfaction (NPS) | > 50 |
| Time-to-hire reduction | > 20% vs. baseline |

---

**Document Status**: Living document
**Owner**: Product Team
**Next Review**: Quarterly
