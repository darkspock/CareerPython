# Global Flows - End-to-End User Journeys

**Document Type:** Business Requirements
**Version:** 1.0
**Last Updated:** 2025-12-05
**Module:** Cross-Platform Flows

---

## Overview

This document describes the complete user journeys in ATS Monkey, 
from initial job discovery through successful hiring. 
Quita It covers the interactions between candidates, companies, and the system across all platform modules.

---

## Flow 1: Candidate Application Journey

### 1.1 Job Discovery

```
┌─────────────────────────────────────────────────────────────────────┐
│                        JOB DISCOVERY                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ Global Job   │    │ Company      │    │ External     │          │
│  │ Board        │    │ Career Page  │    │ Sources      │          │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘          │
│         │                   │                   │                   │
│         └───────────────────┼───────────────────┘                   │
│                             ▼                                       │
│                    ┌────────────────┐                               │
│                    │ Job Detail     │                               │
│                    │ Page           │                               │
│                    └────────┬───────┘                               │
│                             │                                       │
│         ┌───────────────────┼───────────────────┐                   │
│         ▼                   ▼                   ▼                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ Save Job     │    │ Apply Now    │    │ Share Job    │          │
│  │ (Bookmark)   │    │              │    │ (Social)     │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Entry Points
| Source | Description |
|--------|-------------|
| **Global Job Board** | Browse all published positions across companies |
| **Company Career Page** | Direct access to specific company's jobs |
| **Search Engines** | SEO-optimized job listings (Google for Jobs) |
| **Social Media** | Shared job links |
| **Direct Link** | Referral or email campaign links |

#### Job Detail Page Content
- Job title, company, location, work modality
- Full job description
- Requirements (experience, skills, education)
- Benefits and compensation (if disclosed)
- Company culture information
- Application deadline (if set)
- "Apply Now" call-to-action

---

### 1.2 Application Process

```
┌─────────────────────────────────────────────────────────────────────┐
│                     APPLICATION PROCESS                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐                                                   │
│  │ Click Apply  │                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────┐               │
│  │              USER STATUS CHECK                    │               │
│  └──────────────────────┬───────────────────────────┘               │
│         │               │               │                           │
│         ▼               ▼               ▼                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │
│  │ Anonymous    │ │ Registered   │ │ Registered   │                │
│  │ User         │ │ Incomplete   │ │ Complete     │                │
│  │              │ │ Profile      │ │ Profile      │                │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘                │
│         │                │                │                         │
│         ▼                ▼                ▼                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │
│  │ Registration │ │ Complete     │ │ Quick Apply  │                │
│  │ Form         │ │ Profile      │ │ (1-click)    │                │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘                │
│         │                │                │                         │
│         └────────────────┼────────────────┘                         │
│                          ▼                                          │
│                 ┌────────────────┐                                  │
│                 │ Application    │                                  │
│                 │ Form           │                                  │
│                 │ (if required)  │                                  │
│                 └────────┬───────┘                                  │
│                          │                                          │
│                          ▼                                          │
│                 ┌────────────────┐                                  │
│                 │ Submit         │                                  │
│                 │ Application    │                                  │
│                 └────────┬───────┘                                  │
│                          │                                          │
│                          ▼                                          │
│                 ┌────────────────┐                                  │
│                 │ Thank You      │                                  │
│                 │ Page           │                                  │
│                 └────────────────┘                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Application Form Components
| Component | Required | Description |
|-----------|----------|-------------|
| Personal Info | Yes | Name, email, phone |
| Resume/CV | Configurable | Upload or use profile resume |
| Cover Letter | Configurable | Position-specific letter |
| Custom Questions | Configurable | Company-defined questions |
| Source | Yes | How did you hear about us? |
| Consent | Yes | Data processing agreement |

#### Post-Application Actions
1. **Confirmation Page**: Thank you message with next steps
2. **Email Confirmation**: Automatic acknowledgment email
3. **Account Creation Prompt**: For anonymous applicants
4. **Application Tracking**: Access to track status

---

### 1.3 Application Tracking (Candidate View)

```
┌─────────────────────────────────────────────────────────────────────┐
│                   CANDIDATE DASHBOARD                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    MY APPLICATIONS                            │  │
│  ├───────────────────────────────────────────────────────────────┤  │
│  │                                                               │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ Company A - Senior Developer                            │  │  │
│  │  │ Status: Under Review ●                                  │  │  │
│  │  │ Applied: 2025-01-15 │ Last Update: 2025-01-18          │  │  │
│  │  │ [View Details] [Withdraw]                               │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                               │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ Company B - Product Manager                             │  │  │
│  │  │ Status: Interview Scheduled ●                           │  │  │
│  │  │ Applied: 2025-01-10 │ Interview: 2025-01-22 10:00      │  │  │
│  │  │ [View Details] [Prepare Interview]                      │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Status Legend:                                                     │
│  ● Applied  ● Under Review  ● Interview  ● Offer  ● Hired         │
│  ● Rejected ● Withdrawn                                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Candidate Visibility
| Information | Visible to Candidate |
|-------------|---------------------|
| Application status | Yes (high-level) |
| Current stage name | Configurable |
| Interview schedules | Yes |
| Pending actions | Yes |
| Detailed feedback | Configurable |
| Rejection reason | Configurable |

---

## Flow 2: Company Recruitment Pipeline

### 2.1 Phase 1: Sourcing

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: SOURCING                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  WORKFLOW: Sourcing Workflow (Kanban View)                          │
│                                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │
│  │ PENDING   │  │ SCREENING │  │ QUALIFIED │  │           │        │
│  │ (INITIAL) │  │           │  │ (SUCCESS) │  │           │        │
│  ├───────────┤  ├───────────┤  ├───────────┤  │  NOT      │        │
│  │           │  │           │  │           │  │  SUITABLE │        │
│  │  ┌─────┐  │  │  ┌─────┐  │  │  ┌─────┐  │  │  (FAIL)   │        │
│  │  │John │──┼──┼─▶│John │──┼──┼─▶│John │──┼──┤           │        │
│  │  └─────┘  │  │  └─────┘  │  │  └─────┘  │  │  ┌─────┐  │        │
│  │  ┌─────┐  │  │  ┌─────┐  │  │           │  │  │Mary │  │        │
│  │  │Sarah│  │  │  │Mike │  │  │           │  │  └─────┘  │        │
│  │  └─────┘  │  │  └─────┘  │  │           │  │           │        │
│  │  ┌─────┐  │  │           │  │           │  │           │        │
│  │  │Lisa │  │  │           │  │           │  │           │        │
│  │  └─────┘  │  │           │  │           │  │           │        │
│  │           │  │           │  │           │  │           │        │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │
│                                                                     │
│  ─────────────────────────────────────────────────────              │
│  │ ON HOLD │ (Secondary row for paused candidates)                  │
│  └─────────┘                                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Sourcing Stage Actions

| Stage | Recruiter Actions | System Actions |
|-------|-------------------|----------------|
| **Pending** | Review application, assign tags, set priority | Auto-assign based on rules |
| **Screening** | Review CV, add comments, conduct initial call | Send screening interview link |
| **Qualified** | Approve for next phase | Auto-move to Evaluation phase |
| **Not Suitable** | Add rejection reason | Send rejection email |
| **On Hold** | Add note, set reminder | - |

#### Automatic Transitions (Sourcing → Evaluation)
```
Candidate reaches "Qualified" stage (SUCCESS)
        │
        ▼
System checks next_phase_id configuration
        │
        ▼
Move to Evaluation Phase → Initial Stage (HR Interview)
        │
        ▼
Update candidate's phase_id reference
        │
        ▼
Trigger stage entry actions (emails, interviews)
```

---

### 2.2 Phase 2: Evaluation

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 2: EVALUATION                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  WORKFLOW: Evaluation Workflow (Kanban View)                        │
│                                                                     │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │
│  │ HR         │ │ MANAGER    │ │ ASSESSMENT │ │ EXECUTIVE  │       │
│  │ INTERVIEW  │ │ INTERVIEW  │ │ TEST       │ │ INTERVIEW  │       │
│  │ (INITIAL)  │ │            │ │            │ │            │       │
│  ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤       │
│  │            │ │            │ │            │ │            │       │
│  │  ┌──────┐  │ │  ┌──────┐  │ │  ┌──────┐  │ │            │       │
│  │  │John  │──┼─┼─▶│John  │──┼─┼─▶│John  │──┼─┼─▶          │       │
│  │  │Score:│  │ │  │Score:│  │ │  │Score:│  │ │            │       │
│  │  │85/100│  │ │  │78/100│  │ │  │92/100│  │ │            │       │
│  │  └──────┘  │ │  └──────┘  │ │  └──────┘  │ │            │       │
│  │            │ │            │ │            │ │            │       │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │
│                                                                     │
│  ┌────────────┐                                                     │
│  │ SELECTED   │ ──────────────────────────────▶ To Phase 3         │
│  │ (SUCCESS)  │                                                     │
│  └────────────┘                                                     │
│                                                                     │
│  ─────────────────────────────────────────────────────              │
│  │ REJECTED │ (Secondary row)                                       │
│  └──────────┘                                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Evaluation Stage Details

| Stage | Purpose | Interview Type | Interviewers |
|-------|---------|----------------|--------------|
| **HR Interview** | Culture fit, expectations | BEHAVIORAL | HR Manager |
| **Manager Interview** | Technical/functional fit | TECHNICAL | Hiring Manager |
| **Assessment Test** | Skills validation | KNOWLEDGE_CHECK | Auto-graded |
| **Executive Interview** | Senior approval | CULTURAL_FIT | Department Head |
| **Selected** | Ready for offer | - | - |

#### Interview Flow Per Stage
```
Candidate enters stage
        │
        ▼
System creates interview (AUTOMATIC mode)
        │
        ▼
Interview assigned to stage roles
        │
        ▼
Candidate receives interview link
        │
        ▼
Candidate completes interview
        │
        ▼
Interviewer scores answers
        │
        ▼
System calculates interview score
        │
        ▼
Recruiter reviews and moves to next stage
```

---

### 2.3 Phase 3: Offer & Pre-Onboarding

```
┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 3: OFFER & PRE-ONBOARDING                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  WORKFLOW: Offer Workflow (List View)                               │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Stage          │ Candidate │ Status    │ Deadline │ Actions│    │
│  ├─────────────────────────────────────────────────────────────┤    │
│  │ Offer Proposal │ John D.   │ Pending   │ Jan 25   │ [Edit] │    │
│  │ Negotiation    │ Sarah M.  │ Active    │ Jan 28   │ [View] │    │
│  │ Doc Submission │ Mike R.   │ Waiting   │ Feb 01   │ [View] │    │
│  │ Doc Verify     │ Lisa K.   │ Complete  │ Feb 05   │ [Hire] │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  Stage Flow:                                                        │
│                                                                     │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐               │
│  │ OFFER       │   │ NEGOTIATION │   │ DOCUMENT    │               │
│  │ PROPOSAL    │──▶│             │──▶│ SUBMISSION  │               │
│  │ (INITIAL)   │   │             │   │             │               │
│  └─────────────┘   └─────────────┘   └─────────────┘               │
│                           │                 │                       │
│                           ▼                 ▼                       │
│                    ┌─────────────┐   ┌─────────────┐               │
│                    │ LOST        │   │ DOCUMENT    │               │
│                    │ (FAIL)      │   │ VERIFICATION│               │
│                    └─────────────┘   │ (SUCCESS)   │               │
│                                      └──────┬──────┘               │
│                                             │                       │
│                                             ▼                       │
│                                      ┌─────────────┐               │
│                                      │   HIRED!    │               │
│                                      └─────────────┘               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Offer Stage Details

| Stage | Actions | Documents |
|-------|---------|-----------|
| **Offer Proposal** | Generate offer letter, set compensation | Offer letter template |
| **Negotiation** | Adjust terms, counter-offers | Revised offer |
| **Document Submission** | Request required documents | ID, certificates, references |
| **Document Verification** | Verify authenticity, background check | Verification reports |

---

## Flow 3: Complete Candidate Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     COMPLETE CANDIDATE LIFECYCLE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────┐                                                                │
│  │ DISCOVER│ ──▶ See job on board/career page/search                        │
│  └────┬────┘                                                                │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────┐                                                                │
│  │ APPLY   │ ──▶ Submit application (register if needed)                    │
│  └────┬────┘                                                                │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         SOURCING PHASE                              │    │
│  │  Pending ──▶ Screening ──▶ Qualified                                │    │
│  │                    │            │                                   │    │
│  │                    ▼            │                                   │    │
│  │              Not Suitable       │                                   │    │
│  └─────────────────────────────────┼───────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        EVALUATION PHASE                             │    │
│  │  HR Interview ──▶ Manager Interview ──▶ Assessment ──▶ Selected     │    │
│  │       │                  │                  │              │        │    │
│  │       ▼                  ▼                  ▼              │        │    │
│  │   Rejected           Rejected           Rejected          │        │    │
│  └───────────────────────────────────────────────────────────┼────────┘    │
│                                                              │              │
│                                                              ▼              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    OFFER & PRE-ONBOARDING PHASE                     │    │
│  │  Offer Proposal ──▶ Negotiation ──▶ Doc Submit ──▶ Doc Verify       │    │
│  │       │                  │                              │           │    │
│  │       ▼                  ▼                              ▼           │    │
│  │     Lost               Lost                          HIRED!         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  Timeline: Application ──────────────────────────────────────▶ Hired        │
│            Day 0        ~7 days      ~14 days     ~21 days    ~30 days     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Flow 4: Interview Execution Flow

### 4.1 Self-Administered Interview

```
┌─────────────────────────────────────────────────────────────────────┐
│                 SELF-ADMINISTERED INTERVIEW FLOW                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CANDIDATE SIDE                    SYSTEM SIDE                      │
│                                                                     │
│  ┌──────────────┐                 ┌──────────────┐                  │
│  │ Receive      │                 │ Generate     │                  │
│  │ Interview    │◀────────────────│ Unique Link  │                  │
│  │ Link (email) │                 │ + Token      │                  │
│  └──────┬───────┘                 └──────────────┘                  │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐                 ┌──────────────┐                  │
│  │ Click Link   │────────────────▶│ Validate     │                  │
│  │              │                 │ Token        │                  │
│  └──────────────┘                 └──────┬───────┘                  │
│                                          │                          │
│                                          ▼                          │
│  ┌──────────────┐                 ┌──────────────┐                  │
│  │ View         │◀────────────────│ Load         │                  │
│  │ Interview    │                 │ Questions    │                  │
│  │ Instructions │                 │ (Template)   │                  │
│  └──────┬───────┘                 └──────────────┘                  │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐                 ┌──────────────┐                  │
│  │ Start        │────────────────▶│ Set Status   │                  │
│  │ Interview    │                 │ IN_PROGRESS  │                  │
│  └──────┬───────┘                 └──────────────┘                  │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐                                                   │
│  │ Answer       │                                                   │
│  │ Questions    │◀────────┐                                         │
│  │ (Section 1)  │         │                                         │
│  └──────┬───────┘         │                                         │
│         │                 │ Save Progress                           │
│         ▼                 │                                         │
│  ┌──────────────┐         │       ┌──────────────┐                  │
│  │ Save &       │─────────┴──────▶│ Store        │                  │
│  │ Continue     │                 │ Answers      │                  │
│  └──────┬───────┘                 └──────────────┘                  │
│         │                                                           │
│         ▼ (Repeat for all sections)                                 │
│         │                                                           │
│  ┌──────────────┐                 ┌──────────────┐                  │
│  │ Submit       │────────────────▶│ Set Status   │                  │
│  │ Interview    │                 │ FINISHED     │                  │
│  └──────┬───────┘                 └──────┬───────┘                  │
│         │                                │                          │
│         ▼                                ▼                          │
│  ┌──────────────┐                 ┌──────────────┐                  │
│  │ Confirmation │                 │ Notify       │                  │
│  │ Page         │                 │ Interviewers │                  │
│  └──────────────┘                 └──────────────┘                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 AI-Assisted Interview

```
┌─────────────────────────────────────────────────────────────────────┐
│                   AI-ASSISTED INTERVIEW FLOW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CANDIDATE                    AI SYSTEM                COMPANY      │
│                                                                     │
│  ┌──────────┐                                                       │
│  │ Start    │                                                       │
│  │ Interview│                                                       │
│  └────┬─────┘                                                       │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────┐          ┌──────────────┐                             │
│  │ Read     │◀─────────│ Present      │                             │
│  │ Question │          │ Question     │                             │
│  └────┬─────┘          └──────────────┘                             │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────┐          ┌──────────────┐                             │
│  │ Provide  │─────────▶│ Analyze      │                             │
│  │ Answer   │          │ Response     │                             │
│  └──────────┘          └──────┬───────┘                             │
│                               │                                     │
│                               ▼                                     │
│                        ┌──────────────┐                             │
│                        │ Generate     │                             │
│                        │ Follow-up?   │                             │
│                        └──────┬───────┘                             │
│                               │                                     │
│              ┌────────────────┼────────────────┐                    │
│              │ Yes            │                │ No                 │
│              ▼                │                ▼                    │
│  ┌──────────┐          │           │    ┌──────────────┐           │
│  │ Answer   │◀─────────┘           │    │ Next         │           │
│  │ Follow-up│                      │    │ Question     │           │
│  └────┬─────┘                      │    └──────────────┘           │
│       │                            │                                │
│       └────────────────────────────┘                                │
│                                                                     │
│  (Repeat until all questions answered)                              │
│                                                                     │
│       ▼                                                             │
│  ┌──────────┐          ┌──────────────┐    ┌──────────────┐        │
│  │ Complete │─────────▶│ Generate     │───▶│ Review       │        │
│  │          │          │ Summary &    │    │ AI Report    │        │
│  └──────────┘          │ Scores       │    │              │        │
│                        └──────────────┘    └──────────────┘        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Flow 5: Stage Transition with Validation

```
┌─────────────────────────────────────────────────────────────────────┐
│                    STAGE TRANSITION FLOW                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐                                                   │
│  │ Recruiter    │                                                   │
│  │ Drags Card   │                                                   │
│  │ to New Stage │                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                  VALIDATION ENGINE                            │   │
│  │                                                               │   │
│  │  1. Check BLOCKING rules                                      │   │
│  │     - All interviews completed?                               │   │
│  │     - Required fields filled?                                 │   │
│  │     - Minimum score met?                                      │   │
│  │                                                               │   │
│  │  2. Check WARNING rules                                       │   │
│  │     - Salary expectation vs budget?                           │   │
│  │     - Time in previous stage?                                 │   │
│  │                                                               │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                             │                                       │
│         ┌───────────────────┼───────────────────┐                   │
│         ▼                   ▼                   ▼                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ BLOCKED      │    │ WARNING      │    │ ALLOWED      │          │
│  │              │    │              │    │              │          │
│  │ Show error   │    │ Show warning │    │ Proceed      │          │
│  │ Cannot move  │    │ Allow        │    │              │          │
│  │              │    │ override     │    │              │          │
│  └──────────────┘    └──────┬───────┘    └──────┬───────┘          │
│                             │                   │                   │
│                             ▼                   │                   │
│                      ┌──────────────┐           │                   │
│                      │ User         │           │                   │
│                      │ Confirms?    │           │                   │
│                      └──────┬───────┘           │                   │
│                             │                   │                   │
│              ┌──────────────┼───────────────────┘                   │
│              │ Yes          │ No                                    │
│              ▼              ▼                                       │
│       ┌──────────────┐   ┌──────────────┐                          │
│       │ EXECUTE      │   │ CANCEL       │                          │
│       │ TRANSITION   │   │              │                          │
│       └──────┬───────┘   └──────────────┘                          │
│              │                                                      │
│              ▼                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                   POST-TRANSITION ACTIONS                     │   │
│  │                                                               │   │
│  │  1. Update candidate stage_id and phase_id                    │   │
│  │  2. Create stage history entry                                │   │
│  │  3. Execute stage entry actions:                              │   │
│  │     - Send email template (if configured)                     │   │
│  │     - Create interviews (if configured)                       │   │
│  │     - Notify assigned users                                   │   │
│  │  4. Check for AUTO_MOVE rules                                 │   │
│  │  5. If SUCCESS stage: trigger phase transition                │   │
│  │                                                               │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Flow 6: Review & Comment Collaboration

```
┌─────────────────────────────────────────────────────────────────────┐
│                 TEAM COLLABORATION FLOW                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CANDIDATE DETAIL PAGE                                              │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  COMMENTS TAB                                               │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │ Filter: [Current Stage] [Global] [All]              │    │    │
│  │  ├─────────────────────────────────────────────────────┤    │    │
│  │  │                                                     │    │    │
│  │  │  ┌─────────────────────────────────────────────┐    │    │    │
│  │  │  │ John (HR Manager) - Jan 15, 2025            │    │    │    │
│  │  │  │ "Great communication skills, very engaged"  │    │    │    │
│  │  │  │ [SHARED] [REVIEWED] ✓                       │    │    │    │
│  │  │  └─────────────────────────────────────────────┘    │    │    │
│  │  │                                                     │    │    │
│  │  │  ┌─────────────────────────────────────────────┐    │    │    │
│  │  │  │ Sarah (Recruiter) - Jan 14, 2025            │    │    │    │
│  │  │  │ "Salary expectation slightly above budget"  │    │    │    │
│  │  │  │ [PRIVATE] [PENDING] ○                       │    │    │    │
│  │  │  └─────────────────────────────────────────────┘    │    │    │
│  │  │                                                     │    │    │
│  │  │  [+ Add Comment]                                    │    │    │
│  │  │                                                     │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  REVIEWS TAB                     Average Score: 👍 6.5       │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │                                                     │    │    │
│  │  │  Your Review:                                       │    │    │
│  │  │  [🚫 Ban] [👎 Not Rec] [👍 Rec] [❤️ Favorite]       │    │    │
│  │  │                                                     │    │    │
│  │  │  Comment: [________________________]                │    │    │
│  │  │  ☐ Global (visible at all stages)                  │    │    │
│  │  │  [Submit Review]                                    │    │    │
│  │  │                                                     │    │    │
│  │  ├─────────────────────────────────────────────────────┤    │    │
│  │  │  Team Reviews:                                      │    │    │
│  │  │                                                     │    │    │
│  │  │  👍 John (HR) - "Good culture fit"                  │    │    │
│  │  │  👍 Mike (Tech Lead) - "Strong technical skills"    │    │    │
│  │  │  👎 Lisa (Manager) - "Concerns about experience"    │    │    │
│  │  │                                                     │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Flow 7: Offer Generation & Negotiation

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OFFER FLOW                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  COMPANY                                  CANDIDATE                 │
│                                                                     │
│  ┌──────────────┐                                                   │
│  │ Generate     │                                                   │
│  │ Offer        │                                                   │
│  │ (Template)   │                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐                                                   │
│  │ Set Terms:   │                                                   │
│  │ - Salary     │                                                   │
│  │ - Start Date │                                                   │
│  │ - Benefits   │                                                   │
│  │ - Conditions │                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐         ┌──────────────┐                         │
│  │ Send Offer   │────────▶│ Receive      │                         │
│  │              │         │ Offer Email  │                         │
│  └──────────────┘         └──────┬───────┘                         │
│                                  │                                  │
│                                  ▼                                  │
│                           ┌──────────────┐                         │
│                           │ Review       │                         │
│                           │ Offer        │                         │
│                           └──────┬───────┘                         │
│                                  │                                  │
│              ┌───────────────────┼───────────────────┐              │
│              ▼                   ▼                   ▼              │
│       ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│       │ ACCEPT       │   │ NEGOTIATE    │   │ DECLINE      │       │
│       └──────┬───────┘   └──────┬───────┘   └──────┬───────┘       │
│              │                  │                  │                │
│              │                  ▼                  │                │
│              │           ┌──────────────┐          │                │
│              │           │ Counter      │          │                │
│              │           │ Offer        │          │                │
│              │           └──────┬───────┘          │                │
│              │                  │                  │                │
│              │    ┌─────────────┴─────────────┐    │                │
│              │    ▼                           ▼    │                │
│              │  Accept                    Decline  │                │
│              │    │                           │    │                │
│              ▼    ▼                           ▼    ▼                │
│       ┌──────────────┐                 ┌──────────────┐             │
│       │ Document     │                 │ Mark as      │             │
│       │ Submission   │                 │ LOST         │             │
│       │ Stage        │                 │              │             │
│       └──────┬───────┘                 └──────────────┘             │
│              │                                                      │
│              ▼                                                      │
│       ┌──────────────┐                                             │
│       │ Collect      │                                             │
│       │ Documents    │                                             │
│       └──────┬───────┘                                             │
│              │                                                      │
│              ▼                                                      │
│       ┌──────────────┐                                             │
│       │ Verify &     │                                             │
│       │ HIRE!        │                                             │
│       └──────────────┘                                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Metrics by Flow Stage

| Stage | Key Metrics |
|-------|-------------|
| **Discovery** | Job views, apply rate, source attribution |
| **Application** | Completion rate, drop-off points, time to apply |
| **Sourcing** | Time in stage, qualification rate, screening pass rate |
| **Evaluation** | Interview completion rate, average scores, interviewer load |
| **Offer** | Offer acceptance rate, negotiation time, reasons for decline |
| **Overall** | Time-to-hire, cost-per-hire, quality of hire |

---

## System Events Throughout Flow

| Event | Trigger | Actions |
|-------|---------|---------|
| `ApplicationSubmitted` | Candidate submits | Create CompanyCandidate, send confirmation |
| `CandidateStageChanged` | Stage transition | Update history, trigger automations |
| `InterviewCreated` | Enter interview stage | Generate link, notify candidate |
| `InterviewCompleted` | Submit answers | Calculate score, notify interviewers |
| `PhaseTransitioned` | SUCCESS stage reached | Move to next phase, update references |
| `OfferSent` | Enter offer stage | Send offer email |
| `CandidateHired` | Complete verification | Close position (if filled), archive candidate |

---

**Document Status**: Living document
**Owner**: Product Team
**Last Review**: 2025-12-05
