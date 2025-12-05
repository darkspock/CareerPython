# Feature Catalog - Detailed Implementation Reference

**Document Type:** Feature Catalog
**Version:** 1.0
**Last Updated:** 2025-01-XX
**Purpose:** Comprehensive inventory of all implemented features

---

## Overview

This document provides a detailed catalog of all features implemented in ATS Monkey, organized by functional area. It serves as a reference for understanding the full capabilities of the platform.

---

## 1. Candidate Collaboration Features

### 1.1 Candidate Comments System

**Purpose:** Enable team collaboration through comments on candidates at different workflow stages.

#### Data Structure
| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `company_candidate_id` | UUID | Target candidate |
| `comment` | Text | Comment content |
| `workflow_id` | UUID | Associated workflow |
| `stage_id` | UUID | Stage context (null = global) |
| `created_by_user_id` | UUID | Comment author |
| `visibility` | Enum | Access level |
| `review_status` | Enum | Processing status |
| `created_at` | DateTime | Creation timestamp |

#### Visibility Levels
| Level | Description |
|-------|-------------|
| **PRIVATE** | Only visible to creator |
| **SHARED** | Visible to all team members |
| **SHARED_WITH_CANDIDATE** | Also visible to candidate |

#### Review Status
| Status | Description |
|--------|-------------|
| **PENDING** | Requires attention/review |
| **REVIEWED** | Has been processed |

#### Features
- Create, update, delete comments
- Filter by stage: Current Stage, Global, All
- Toggle review status
- Pending comments counter badge
- Author and timestamp display

#### API Endpoints
```
POST   /api/company/candidates/{id}/comments
GET    /api/company/candidates/{id}/comments
GET    /api/company/candidates/{id}/comments/stage/{stage_id}
GET    /api/company/candidates/{id}/comments/pending/count
PUT    /api/company/candidates/comments/{comment_id}
DELETE /api/company/candidates/comments/{comment_id}
POST   /api/company/candidates/comments/{comment_id}/mark-pending
POST   /api/company/candidates/comments/{comment_id}/mark-reviewed
```

---

### 1.2 Candidate Review/Evaluation System

**Purpose:** Structured scoring and evaluation of candidates by team members.

#### Scoring Scale
| Score | Value | Icon | Meaning |
|-------|-------|------|---------|
| **BAN** | 0 | 🚫 | Strongly not recommended, block |
| **NOT_RECOMMENDED** | 3 | 👎 | Does not meet criteria |
| **RECOMMENDED** | 6 | 👍 | Meets criteria, proceed |
| **FAVORITE** | 10 | ❤️ | Highly recommended, top candidate |

#### Data Structure
| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `company_candidate_id` | UUID | Target candidate |
| `score` | Integer | 0, 3, 6, or 10 |
| `comment` | Text | Optional explanation |
| `workflow_id` | UUID | Associated workflow |
| `stage_id` | UUID | Stage context (null = global) |
| `review_status` | Enum | PENDING or REVIEWED |
| `created_by_user_id` | UUID | Reviewer |

#### Features
- Submit reviews with score + optional comment
- Global reviews (visible across all stages)
- Stage-specific reviews
- Average score calculation and display
- Review count tracking
- Review status management
- Filter: Current Stage, Global, All

#### API Endpoints
```
POST   /api/company/candidates/{id}/reviews
GET    /api/company/candidates/{id}/reviews
GET    /api/company/candidates/{id}/reviews/stage/{stage_id}
PUT    /api/company/candidates/reviews/{review_id}
DELETE /api/company/candidates/reviews/{review_id}
```

---

### 1.3 Document/File Attachments

**Purpose:** Attach and manage files associated with candidates.

#### Supported File Types
- Documents: PDF, DOC, DOCX, TXT
- Images: JPG, JPEG, PNG

#### Data Structure
| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `candidate_id` | UUID | Owner candidate |
| `filename` | String | Original filename |
| `file_size` | Integer | Size in bytes |
| `content_type` | String | MIME type |
| `storage_path` | String | Storage location |
| `uploaded_at` | DateTime | Upload timestamp |

#### Features
- Upload files with type validation
- Display file list with metadata
- Download files
- Delete files
- Upload progress indicator
- File size display (KB format)

---

## 2. Candidate Management Features

### 2.1 Tags System

**Purpose:** Categorize and filter candidates using custom tags.

#### Features
- Add tags to candidates
- Remove tags
- Tag input with autocomplete
- Filter candidates by tags
- Tag display on candidate cards and lists

---

### 2.2 Priority Management

**Purpose:** Prioritize candidate processing.

#### Priority Levels
| Level | Color | Description |
|-------|-------|-------------|
| **HIGH** | Red | Urgent, process first |
| **MEDIUM** | Yellow | Standard priority |
| **LOW** | Green | Can wait |

#### Features
- Set priority on candidate creation
- Update priority
- Visual indicators in lists (colored icons)
- Sort by priority

---

### 2.3 Ownership Model

**Purpose:** Control candidate data ownership and access.

#### Ownership Types
| Type | Description |
|------|-------------|
| **COMPANY_OWNED** | Shared across all company users |
| **USER_OWNED** | Restricted to specific user |

#### Features
- Transfer ownership between users
- Visual indicators (blue = company, purple = user)
- Filter by ownership type

#### API Endpoint
```
POST /api/company-candidates/{id}/transfer-ownership
```

---

### 2.4 Task Assignment System

**Purpose:** Assign candidate processing work to team members.

#### Task Status
| Status | Description |
|--------|-------------|
| **PENDING** | Not started |
| **IN_PROGRESS** | Being worked on |
| **COMPLETED** | Finished |
| **BLOCKED** | Cannot proceed |

#### Features
- Claim task (self-assign)
- Unclaim task (release)
- View "My assigned tasks"
- Task status tracking
- Team workload visibility

#### API Endpoints
```
POST /api/company-candidates/{id}/claim-task
POST /api/company-candidates/{id}/unclaim-task
GET  /api/company-candidates/my-tasks
```

---

## 3. Talent Pool

**Purpose:** Maintain a database of candidates for future opportunities.

#### Features
- Add candidates to talent pool
- Remove from talent pool
- Update talent pool entry status
- Search talent pool
- Status management

#### API Endpoints
```
POST   /api/talent-pool/add
DELETE /api/talent-pool/{entry_id}
PUT    /api/talent-pool/{entry_id}/status
GET    /api/talent-pool/search
GET    /api/talent-pool
```

---

## 4. Job Position Features

### 4.1 Job Position Comments

**Purpose:** Team collaboration on job positions.

#### Structure
Same as Candidate Comments:
- Visibility levels (PRIVATE, SHARED)
- Review status (PENDING, REVIEWED)
- Stage-specific or global

#### API Endpoints
```
POST   /api/company/job-positions/{id}/comments
GET    /api/company/job-positions/{id}/comments
PUT    /api/company/job-positions/comments/{comment_id}
DELETE /api/company/job-positions/comments/{comment_id}
```

---

### 4.2 Job Position Activity Log

**Purpose:** Audit trail of all changes to job positions.

#### Activity Types
| Type | Tracked Data |
|------|--------------|
| **CREATED** | Initial creation details |
| **EDITED** | Changed fields, old/new values |
| **STAGE_MOVED** | Previous stage, new stage |
| **STATUS_CHANGED** | Previous status, new status |
| **COMMENT_ADDED** | Comment reference |

#### Data Structure
| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `job_position_id` | UUID | Target position |
| `activity_type` | Enum | Type of activity |
| `description` | String | Human-readable description |
| `performed_by_user_id` | UUID | Actor |
| `metadata` | JSON | Activity-specific data |
| `created_at` | DateTime | Timestamp |

#### Features
- Immutable audit trail
- Rich metadata per activity type
- Timeline view
- Filter by activity type

---

### 4.3 Position Stage Assignments

**Purpose:** Assign team members to specific workflow stages for a job position.

#### Features
- Assign users to stages
- Remove users from stages
- Bulk assignment
- Copy assignments from another position
- View assigned users per stage

#### API Endpoints
```
POST   /api/company/job-positions/{id}/stage-assignments
DELETE /api/company/job-positions/{id}/stage-assignments/{assignment_id}
POST   /api/company/job-positions/{id}/stage-assignments/bulk
POST   /api/company/job-positions/{id}/stage-assignments/copy
GET    /api/company/job-positions/{id}/stage-assignments
```

---

### 4.4 Job Position Visibility

**Purpose:** Control who can see job positions.

#### Visibility Levels
| Level | Description |
|-------|-------------|
| **HIDDEN** | Internal draft only |
| **INTERNAL** | Company-wide visibility |
| **PUBLIC** | External candidates can see |

---

## 5. Workflow Analytics

**Purpose:** Performance insights and optimization recommendations.

### 5.1 Stage Analytics

| Metric | Description |
|--------|-------------|
| **Applications Count** | Candidates in stage |
| **Average Time in Stage** | Duration analysis |
| **Conversion Rate** | % moving to next stage |
| **Dropout Rate** | % exiting process |

### 5.2 Bottleneck Detection

- Identifies slowest stages
- Calculates bottleneck score
- Provides recommendations

### 5.3 Workflow KPIs

| KPI | Description |
|-----|-------------|
| **Time to Hire** | Average days to complete |
| **Cost per Hire** | Average cost calculation |
| **Overall Conversion** | Application to hire rate |
| **Fastest Stage** | Quickest processing stage |
| **Slowest Stage** | Longest processing stage |

#### API Endpoints
```
GET /api/company/workflows/{id}/analytics
GET /api/company/workflows/{id}/bottlenecks
GET /api/company/workflows/{id}/kpis
```

---

## 6. Company Pages (CMS)

**Purpose:** Manage public-facing company content.

### 6.1 Page Types

| Type | Purpose |
|------|---------|
| **PUBLIC_COMPANY_DESCRIPTION** | Company profile page |
| **JOB_POSITION_DESCRIPTION** | Benefits/culture for job posts |
| **DATA_PROTECTION** | Privacy policy (GDPR/CCPA) |
| **TERMS_OF_USE** | Legal terms |
| **THANK_YOU_APPLICATION** | Post-application message |

### 6.2 Page Status

| Status | Description |
|--------|-------------|
| **DRAFT** | Not published |
| **PUBLISHED** | Live and visible |
| **ARCHIVED** | Removed from view |

### 6.3 Features

- Visual HTML editor (Unlayer)
- Version history
- Multi-language support
- SEO metadata
- Preview before publish
- Set default page per type

#### API Endpoints
```
POST   /api/company/pages
GET    /api/company/pages
GET    /api/company/pages/{page_id}
PUT    /api/company/pages/{page_id}
DELETE /api/company/pages/{page_id}
POST   /api/company/pages/{page_id}/publish
POST   /api/company/pages/{page_id}/archive
GET    /public/company/{company_id}/pages/{page_type}
```

---

## 7. Custom Fields System

**Purpose:** Company-specific data capture on various entities.

### 7.1 Supported Entities

- Job Position
- Candidate Application
- Candidate
- Workflow Stage

### 7.2 Field Types

| Type | Description |
|------|-------------|
| **TEXT** | Single line text |
| **TEXTAREA** | Multi-line text |
| **NUMBER** | Numeric value |
| **CURRENCY** | Money value |
| **EMAIL** | Email address |
| **PHONE** | Phone number |
| **URL** | Web link |
| **DATE** | Date picker |
| **BOOLEAN** | Yes/No toggle |
| **DROPDOWN** | Select from options |

### 7.3 Features

- Add custom fields to entities
- Field visibility (candidate/recruiter)
- Inline editing
- Field type icons
- Validation rules

#### API Endpoints
```
POST   /api/company/custom-fields
GET    /api/company/custom-fields/entity/{entity_type}
PUT    /api/company/custom-fields/{field_id}
DELETE /api/company/custom-fields/{field_id}
GET    /api/company/entities/{entity_id}/custom-field-values
PUT    /api/company/entities/{entity_id}/custom-field-values
```

---

## 8. Field Validation Rules

**Purpose:** Enforce data quality rules on fields.

### 8.1 Rule Types

| Type | Description |
|------|-------------|
| **REQUIRED** | Field must have value |
| **CONDITIONAL** | Required based on condition |
| **FORMAT** | Must match pattern |
| **RANGE** | Numeric range limits |

### 8.2 Comparison Operators

- EQUALS, NOT_EQUALS
- GREATER_THAN, LESS_THAN
- CONTAINS, NOT_CONTAINS
- IN_LIST, NOT_IN_LIST
- IS_EMPTY, IS_NOT_EMPTY
- MATCHES_REGEX

### 8.3 Severity Levels

| Level | Behavior |
|-------|----------|
| **ERROR** | Blocks action |
| **WARNING** | Allows with confirmation |
| **INFO** | Informational only |

---

## 9. Resume AI Analysis

**Purpose:** Extract candidate data from uploaded resumes.

### 9.1 Process Flow

1. Upload PDF resume
2. AI analyzes document
3. Extract: Name, contact, experience, education, skills
4. Populate candidate profile
5. Track processing status

### 9.2 AI Providers

- Groq AI
- X-AI (xAI)

### 9.3 Processing Status

| Status | Description |
|--------|-------------|
| **PENDING** | Queued for processing |
| **PROCESSING** | Currently analyzing |
| **COMPLETED** | Successfully extracted |
| **FAILED** | Error during processing |

#### API Endpoints
```
POST /candidate/upload-resume
GET  /candidate/resume/analysis-status/{job_id}
GET  /candidate/resume/analysis-results/{job_id}
```

---

## 10. Notification System

**Purpose:** Automated communication via email.

### 10.1 Email Templates

#### Template Variables
Templates support Jinja2-style variables: `{{ variable_name }}`

#### Available Variables
| Variable | Description |
|----------|-------------|
| `candidate_name` | Candidate full name |
| `candidate_email` | Candidate email |
| `job_position_title` | Position name |
| `company_name` | Company name |
| `stage_name` | Current stage |
| `interview_date` | Scheduled date |

### 10.2 Trigger Events

| Event | Description |
|-------|-------------|
| **STAGE_ENTERED** | Candidate enters stage |
| **INTERVIEW_SCHEDULED** | Interview created |
| **APPLICATION_RECEIVED** | New application |
| **OFFER_SENT** | Offer extended |

### 10.3 Email Providers

- SMTP (generic)
- Mailgun

#### API Endpoints
```
POST   /api/company/email-templates
GET    /api/company/email-templates
PUT    /api/company/email-templates/{template_id}
DELETE /api/company/email-templates/{template_id}
POST   /api/company/email-templates/{template_id}/activate
POST   /api/company/email-templates/{template_id}/deactivate
```

---

## 11. Interview Advanced Features

### 11.1 Interview Score Calculator

#### Scoring Modes
| Mode | Description |
|------|-------------|
| **ABSOLUTE** | Higher score = better (1-10 scaled to 0-100) |
| **DISTANCE** | Closer to target = better |
| **LEGACY** | Simple average (0-100 direct) |

### 11.2 Interview Analytics

| Metric | Description |
|--------|-------------|
| **Completion Rate** | % of scheduled interviews completed |
| **Average Score** | Mean interview score |
| **Response Quality** | Answer quality analysis |
| **Engagement Score** | Candidate engagement level |

### 11.3 AI Features

- AI-generated follow-up questions
- Response sentiment analysis
- Keyword extraction
- Confidence scoring

---

## 12. Storage Services

**Purpose:** File storage abstraction.

### 12.1 Supported Backends

| Backend | Description |
|---------|-------------|
| **S3** | Amazon S3 compatible storage |
| **Local** | Local filesystem storage |

### 12.2 Features

- Configurable storage backend
- Secure file URLs
- File type validation
- Size limits

---

## 13. Stage Timeline/History

**Purpose:** Visual representation of candidate journey.

### 13.1 Timeline Events

| Event | Description |
|-------|-------------|
| **CANDIDATE_ADDED** | Initial creation |
| **INVITATION_SENT** | Invite to apply |
| **CANDIDATE_CONFIRMED** | Accepted invitation |
| **STAGE_CHANGED** | Moved to new stage |
| **PHASE_CHANGED** | Moved to new phase |
| **REJECTED** | Process ended negatively |
| **ARCHIVED** | Process completed |

### 13.2 Display Features

- Chronological timeline view
- Status icons (completed, current, pending)
- Timestamps
- Duration in each stage
- Actor information

---

## Quick Reference: API Endpoint Summary

### Candidate Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/company-candidates/` | Create candidate |
| GET | `/api/company-candidates/{id}` | Get candidate |
| PUT | `/api/company-candidates/{id}` | Update candidate |
| POST | `/api/company-candidates/{id}/change-stage` | Move stage |
| POST | `/api/company-candidates/{id}/archive` | Archive |
| POST | `/api/company-candidates/{id}/transfer-ownership` | Transfer |

### Comment Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/company/candidates/{id}/comments` | Add comment |
| GET | `/api/company/candidates/{id}/comments` | List comments |
| PUT | `/api/company/candidates/comments/{id}` | Update |
| DELETE | `/api/company/candidates/comments/{id}` | Delete |

### Review Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/company/candidates/{id}/reviews` | Add review |
| GET | `/api/company/candidates/{id}/reviews` | List reviews |
| PUT | `/api/company/candidates/reviews/{id}` | Update |
| DELETE | `/api/company/candidates/reviews/{id}` | Delete |

---

**Document Status**: Living document - updated as features are added
**Owner**: Development Team
**Last Code Audit**: 2025-01
