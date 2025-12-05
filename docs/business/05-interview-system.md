# Interview System - Business Requirements

**Document Type:** Business Requirements
**Version:** 1.0
**Last Updated:** 2025-01-XX
**Module:** Interview Management

---

## Overview

The Interview System is a comprehensive solution for managing all aspects of candidate evaluation, from initial screening questionnaires to complex multi-interviewer assessment processes. It supports various interview formats, scoring methods, and AI-assisted capabilities.

---

## Strategic Goals

1. **Structured Evaluation**: Ensure consistent, fair candidate assessment
2. **Flexibility**: Support diverse interview formats and company needs
3. **AI Enhancement**: Augment human evaluation with AI capabilities
4. **Collaboration**: Enable multi-stakeholder involvement
5. **Data-Driven Decisions**: Provide actionable insights from interviews

---

## Core Concepts

### Interview Templates

Interview Templates are reusable blueprints that define the structure, questions, and scoring criteria for interviews.

#### Template Types

| Type | Purpose | Use Case |
|------|---------|----------|
| **EXTENDED_PROFILE** | Gather additional candidate information | Pre-screening, extended applications |
| **POSITION_INTERVIEW** | Position-specific evaluation | Technical, cultural fit interviews |
| **SCREENING** | Initial candidate filtering | Quick qualification checks |
| **CUSTOM** | Flexible format for any need | Specialized evaluations |

#### Template Structure
```
InterviewTemplate
├── Metadata (name, type, status, scoring_mode)
├── Sections[]
│   ├── Section Metadata (name, order, AI settings)
│   └── Questions[]
│       ├── Question text
│       ├── Question type (text, choice, scale)
│       ├── Required/optional
│       └── AI follow-up settings
└── Scoring Configuration (mode, weights)
```

### Interview Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **AUTOMATIC** | Created automatically by workflow stage | Standard process |
| **AI** | AI-assisted interview execution | Screening, preliminary |
| **MANUAL** | Fully human-conducted | Final rounds, complex evaluation |

### Interview Types

| Type | Description |
|------|-------------|
| **CUSTOM** | General purpose interview |
| **TECHNICAL** | Technical skill assessment |
| **BEHAVIORAL** | Behavioral/situational questions |
| **CULTURAL_FIT** | Culture and values alignment |
| **KNOWLEDGE_CHECK** | Domain knowledge verification |
| **EXPERIENCE_CHECK** | Experience validation |

### Process Phase Types

| Phase | When Used |
|-------|-----------|
| **CANDIDATE_SIGN_UP** | During platform registration |
| **CANDIDATE_APPLICATION** | During job application |
| **SCREENING** | Initial filtering stage |
| **INTERVIEW** | Main evaluation process |
| **FEEDBACK** | Final candidate feedback |

---

## Functional Requirements

### FR-IV01: Interview Templates

#### FR-IV01.1: Template Management
- **Create**: Build new templates from scratch or clone existing
- **Edit**: Modify template structure and content
- **Version**: Track template changes over time
- **Status**: DRAFT, ENABLED, DISABLED lifecycle

#### FR-IV01.2: Template Sections
- **Purpose**: Organize questions into logical groups
- **Order**: Configurable section sequence
- **AI Settings**:
  - `allow_ai_questions`: AI can add questions to section
  - `allow_ai_override_questions`: AI can reformulate existing questions

#### FR-IV01.3: Template Questions
- **Types**: Text, single choice, multiple choice, scale, file upload
- **Validation**: Required/optional, character limits
- **Scoring**: Weight for scored templates
- **AI Settings**:
  - `allow_ai_followup`: AI can ask follow-up questions

### FR-IV02: Scoring System

#### FR-IV02.1: Scoring Modes

| Mode | Description | Scale | Calculation |
|------|-------------|-------|-------------|
| **ABSOLUTE** | Higher score is better | 1-10 | Weighted average scaled to 0-100 |
| **LEGACY** | Simple average | 0-100 | Direct average (backward compatibility) |

#### FR-IV02.2: Score Components
- **Question Scores**: Individual question ratings (1-10)
- **Section Scores**: Aggregate of questions in section
- **Interview Score**: Overall interview rating (0-100)
- **Summary Score**: Aggregate across all interviews for candidate

#### FR-IV02.3: Score Summary
| Metric | Description |
|--------|-------------|
| **Overall Score** | Weighted average of all scores |
| **By Section** | Breakdown by template section |
| **By Evaluator** | Scores from each interviewer |
| **Trend** | Progress across interviews |

### FR-IV03: Interview Execution

#### FR-IV03.1: Interview Lifecycle

```
PENDING → IN_PROGRESS → FINISHED
            ↓
          PAUSED ↔ (resume)
            ↓
        DISCARDED
```

| Status | Description |
|--------|-------------|
| **PENDING** | Created, not started |
| **IN_PROGRESS** | Currently being conducted |
| **PAUSED** | Temporarily stopped |
| **FINISHED** | Completed successfully |
| **DISCARDED** | Cancelled/abandoned |

#### FR-IV03.2: Candidate Self-Interviews
- **Access**: Via unique link with secure token
- **Authentication**: Token validation + optional login
- **Progress**: Save and continue capability
- **Submission**: Clear completion confirmation

#### FR-IV03.3: AI-Assisted Interviews
- **Conversation Flow**: AI guides candidate through questions
- **Follow-ups**: Dynamic questions based on responses
- **Adaptation**: Adjust difficulty based on answers
- **Transcription**: Record all interactions

#### FR-IV03.4: Human-Conducted Interviews
- **Scheduling**: Integrated calendar management
- **Multiple Interviewers**: Support for panel interviews
- **Real-time Scoring**: Score during or after interview
- **Notes**: Free-form note taking

### FR-IV04: Interview Scheduling

#### FR-IV04.1: Calendar Management
- **Dashboard Header Metrics**:
  - Pending scheduling (no date or interviewer)
  - Scheduled (date + interviewer assigned)
  - In progress (today's interviews)
  - Recently completed (last 30 days)
  - Overdue (past deadline)
  - Pending feedback/scoring

- **Calendar View**: Visual calendar with interview counts per day
- **Click-to-Filter**: Click date to filter to that day's interviews

#### FR-IV04.2: Scheduling Interface
- **Quick Schedule**: Click on N/A date to open calendar picker
- **Time Selection**: Date + time picker
- **Interviewer Assignment**: Assign from available team members
- **Self-Assign**: "Assign to me" quick action

#### FR-IV04.3: Deadline Management
- **Deadline Date**: Optional completion deadline
- **Overdue Tracking**: Visual indicators for overdue interviews
- **Reminders**: Notifications for upcoming deadlines

### FR-IV05: Interviewer Management

#### FR-IV05.1: Interviewer Roles
- **Required Roles**: Roles that must have an interviewer assigned
- **Role Display**: Show role if no specific user assigned
- **Multi-Assignment**: Multiple interviewers per interview

#### FR-IV05.2: External Interviewers
- **Guest Role**: GUEST role for external interviewers
- **Invitation Flow**: Invite → Accept → Access
- **Limited Access**: Only assigned interview access
- **Email Integration**: Future email notifications

#### FR-IV05.3: Interviewer Assignment
| Action | Description |
|--------|-------------|
| **Browse** | View all company employees |
| **Search** | Filter while typing |
| **Self-Assign** | Quick "Assign to me" button |
| **Multi-Select** | Assign multiple (at least one per role) |

### FR-IV06: Interview Access & Links

#### FR-IV06.1: Link Generation
- **Token**: Unique secure token per interview
- **Expiration**: Configurable expiry (default 30 days)
- **Validation**: Token + interview ID validation
- **Regeneration**: Generate new link if needed

#### FR-IV06.2: Access Methods
| Method | Description |
|--------|-------------|
| **Direct Link** | Token-based access for candidates |
| **Authenticated** | Logged-in access for company users |
| **External Interviewer** | Token for guest interviewers |

#### FR-IV06.3: Link Management
- **Copy Link**: One-click copy to clipboard
- **Share**: Future email integration
- **Track**: View link usage/access

### FR-IV07: Interview Answers

#### FR-IV07.1: Answer Management
- **Capture**: Store all candidate responses
- **Types**: Text, selected choices, scales, file references
- **Timestamps**: Record submission times
- **Edit History**: Track answer modifications

#### FR-IV07.2: AI-Generated Content
- **AI Answers**: Responses generated during AI interviews
- **AI Questions**: Dynamic follow-up questions
- **Context**: Conversation context preservation

### FR-IV08: Interview List View

#### FR-IV08.1: List Display
| Column | Description |
|--------|-------------|
| **Interview/Type** | Name + type (type in smaller font below) |
| **Candidate** | Candidate name |
| **Position** | Job position title |
| **Scheduled** | Date/time (click to edit) |
| **Deadline** | Deadline date |
| **Status** | Current status |
| **Interviewer** | Assigned person or role |
| **Score** | Score if completed |
| **Actions** | Quick actions menu |

#### FR-IV08.2: Filtering
| Filter | Options |
|--------|---------|
| **Search** | Candidate name |
| **Phase Type** | Process phase selection |
| **Interview Type** | Type multi-select |
| **Status** | Status multi-select |
| **Date Range** | Date picker |
| **Position** | Active + recently closed (30 days) |
| **Interviewer** | Team member selection |

---

## Workflow Integration

### Stage-Interview Configuration
- **Automatic Creation**: Interviews created when candidate enters stage
- **Template Assignment**: Configure which template for each stage
- **Role Assignment**: Inherit roles from stage configuration

### Validation Rules
- **Pending Interview Block**: Cannot leave stage with pending interviews
- **Score Requirements**: Minimum score to advance (future)

---

## AI Capabilities

### Template Enhancement
- **AI Questions**: Generate additional questions during interview
- **Question Reformulation**: Adapt question phrasing to context
- **Follow-up Generation**: Create follow-ups based on answers

### Interview Execution
- **Conversational AI**: Natural dialogue interview experience
- **Answer Analysis**: Real-time response quality assessment
- **Adaptive Questioning**: Adjust based on candidate responses

### Post-Interview Analysis
- **Answer Summarization**: Condense lengthy responses
- **Sentiment Analysis**: Assess response tone and confidence
- **Recommendation Generation**: AI-suggested evaluation

---

## HR Expert Recommendations

### Structured Interview Best Practices

#### 1. Consistency is Key
- **Recommendation**: Use templates for all interviews
- **Rationale**: Reduces bias, improves defensibility
- **Implementation**: Required template selection for each interview

#### 2. Scoring Calibration
- **Recommendation**: Regular interviewer calibration sessions
- **Rationale**: Ensures consistent scoring across team
- **Implementation**: Scorecard comparison tools, training resources

#### 3. Legal Defensibility
- **Recommendation**: Document all interview decisions
- **Rationale**: Required for EEO compliance
- **Implementation**: Mandatory notes, structured rejection reasons

### Interview Experience Optimization

#### 1. Candidate Preparation
- **Recommendation**: Provide interview context to candidates
- **Information to Share**:
  - Who they'll meet
  - Duration expectations
  - Topics to be covered
  - How to prepare
- **Implementation**: Automated prep emails with interview details

#### 2. Timely Feedback
- **Recommendation**: Set SLAs for post-interview feedback
- **Targets**:
  - Interviewer feedback: Within 24 hours
  - Candidate notification: Within 3 business days
- **Implementation**: Reminder system, completion tracking

#### 3. Multi-Round Efficiency
- **Recommendation**: Avoid redundant questioning across rounds
- **Implementation**:
  - Visible previous interview summaries
  - Role-specific question guides
  - Clear stage-by-stage focus areas

### Bias Reduction

#### 1. Structured Questions
- **Recommendation**: Same questions for all candidates
- **Implementation**: Template-driven interviews, question locking

#### 2. Blind Review Option
- **Recommendation**: Option to hide candidate identifying information
- **Implementation**: Anonymized mode for initial screening

#### 3. Panel Interviews
- **Recommendation**: Multiple perspectives reduce individual bias
- **Implementation**: Multi-interviewer support, independent scoring

---

## Reporting & Analytics

### Interview Metrics
| Metric | Description |
|--------|-------------|
| **Completion Rate** | Interviews completed vs scheduled |
| **Time to Complete** | Average interview duration |
| **Score Distribution** | Distribution of scores across interviews |
| **Interviewer Load** | Interviews per team member |
| **Candidate Progression** | Pass rates by interview stage |

### Quality Metrics
| Metric | Description |
|--------|-------------|
| **Score Correlation** | How scores predict hiring success |
| **Interviewer Consistency** | Score variance across interviewers |
| **Template Effectiveness** | Which templates predict success |

### Advanced Interview Analytics (AI-Powered)

#### Response Quality Analysis
| Metric | Description |
|--------|-------------|
| **Response Quality Score** | AI-assessed answer quality |
| **Engagement Score** | Candidate engagement level |
| **Sentiment Score** | Response tone analysis |
| **Confidence Score** | AI confidence in assessment |

#### Behavioral Insights
- **Communication Style**: Analysis of response patterns
- **Stress Indicators**: Detected stress markers
- **Confidence Patterns**: Consistency in responses
- **Follow-up Needs**: Questions requiring clarification

#### Candidate Performance History
- Track improvement trends (improving/stable/declining)
- Overall quality, sentiment, and confidence scores
- Common strengths and improvement areas
- Performance recommendations

#### Interview Feedback Summary
| Field | Description |
|-------|-------------|
| `total_responses` | Total answers submitted |
| `completed_responses` | Fully answered questions |
| `average_quality_score` | Mean quality rating |
| `responses_needing_followup` | Count requiring follow-up |
| `feedback_highlights` | Key positive points |
| `improvement_areas` | Areas to address |

---

## Answer Scoring & Feedback

### FR-IV09: Answer Evaluation

#### FR-IV09.1: Answer Scoring
- **Score Range**: 1-10 per answer (optional)
- **Feedback Field**: Free-text feedback per answer
- **Scorer Tracking**: Who scored and when
- **Bulk Scoring**: Score multiple answers in sequence

#### FR-IV09.2: Score Calculator Service
- **Automatic Calculation**: Computes interview score from answer scores
- **Weighted Scoring**: Section weights affect final score
- **Mode-Specific**: Different calculation per scoring mode

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Interview scheduling time | < 2 minutes |
| Score submission rate | > 95% within 24 hours |
| Candidate interview completion | > 90% |
| AI interview satisfaction | > 4/5 rating |
| Link generation success | 100% first-click |

---

## Future Roadmap

### Phase 1 (Current)
- Template management
- Basic scheduling
- Scoring system
- External interviewers

### Phase 2
- AI-assisted interviews
- Video interview recording
- Advanced scheduling
- Calendar integration

### Phase 3
- Interview analytics
- Predictive insights
- Automated scheduling
- Mobile interviewer app

---

**Document Status**: Living document
**Owner**: Product Team
**Next Review**: Quarterly
