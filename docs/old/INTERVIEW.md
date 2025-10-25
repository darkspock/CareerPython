# Interview Template System

## Overview

The Interview Template System is a comprehensive solution for managing structured interviews in the CareerPython platform. It follows Clean Architecture principles with Domain-Driven Design (DDD) and CQRS patterns, providing a flexible and scalable way to create, manage, and conduct interviews for candidates.

## Architecture

The system is divided into two main modules:

### 1. Interview Template Module (`src/interview/interview_template/`)
Handles the creation and management of reusable interview templates.

### 2. Interview Module (`src/interview/interview/`)
Handles the execution and management of actual interviews based on templates.

---

## Domain Model

### Interview Template

The root entity that represents a reusable interview template.

**Entity**: `InterviewTemplate`

**Attributes**:
- `id` - InterviewTemplateId (Value Object)
- `company_id` - Optional CompanyId (can be company-specific or global)
- `name` - Template name
- `intro` - Short introduction for the interview
- `prompt` - Instructions for the interviewer
- `goal` - What the template aims to achieve
- `status` - ENABLED, DRAFT, or DISABLED
- `template_type` - EXTENDED_PROFILE or POSITION_INTERVIEW
- `job_category` - Optional job category (TECHNOLOGY, OPERATIONS, SALES, etc.)
- `allow_ai_questions` - Boolean (default: False). If True, AI can generate additional questions beyond the defined ones
- `legal_notice` - Optional string. Legal text displayed to users for compliance (GDPR, labor laws, etc.)
- `tags` - Optional list of tags
- `metadata` - Optional metadata dictionary

**Status Lifecycle**:
```
DRAFT → ENABLED (publish) → DISABLED (disable)
  ↑        ↓
  └────────┘ (draft)
```

**Methods**:
- `create()` - Factory method to create new template
- `update_details()` - Update template information
- `enable()` - Enable the template
- `disable()` - Disable the template
- `publish()` - Publish template (sets to ENABLED)
- `draft()` - Set back to DRAFT status

---

### Interview Template Section

Represents a section within an interview template (e.g., Experience, Education, Soft Skills).

**Entity**: `InterviewTemplateSection`

**Attributes**:
- `id` - InterviewTemplateSectionId
- `interview_template_id` - Parent template ID
- `name` - Section name
- `intro` - Section introduction
- `prompt` - Section-specific instructions
- `goal` - Section objective
- `section` - Section type (EXPERIENCE, EDUCATION, PROJECT, SOFT_SKILL, GENERAL)
- `sort_order` - Position within the template (0 = first)
- `status` - ENABLED, DRAFT, or DISABLED
- `allow_ai_questions` - Boolean (default: False). If True, AI can generate additional questions for this section
- `allow_ai_override_questions` - Boolean (default: False). If True, AI can reformulate/override existing questions in this section
- `legal_notice` - Optional string. Legal text displayed to users for this section

**Methods**:
- `create()` - Factory method
- `update_details()` - Update section information
- `enable()`, `disable()`, `publish()`, `draft()` - Status management
- `update_sort_order()` - Change section position

---

### Interview Template Question

Represents individual questions within a section.

**Entity**: `InterviewTemplateQuestion`

**Attributes**:
- `id` - InterviewTemplateQuestionId
- `interview_template_section_id` - Parent section ID
- `sort_order` - Position within the section
- `name` - Question name/title
- `description` - Full question text
- `data_type` - INT, DATE, SHORT_STRING, or LARGE_STRING
- `scope` - GLOBAL (general question) or ITEM (specific to candidate items)
- `code` - Unique code for the question
- `status` - ENABLED, DRAFT, or DISABLED
- `allow_ai_followup` - Boolean (default: False). If True, AI can generate follow-up questions based on this question
- `legal_notice` - Optional string. Legal text displayed to users for this specific question

**Data Types**:
- `INT` - Integer values
- `DATE` - Date values
- `SHORT_STRING` - Short text (< 255 chars)
- `LARGE_STRING` - Long text (unlimited)

**Scope**:
- `GLOBAL` - General questions not tied to specific candidate data
- `ITEM` - Questions specific to candidate items (experience, education, projects)

**Methods**:
- `create()` - Factory method
- `update_details()` - Update question information
- `enable()`, `disable()`, `publish()`, `draft()` - Status management

---

## AI Question Generation

The Interview Template System supports AI-powered question generation at three hierarchical levels. This allows for flexible interview experiences where the AI can either strictly follow predefined questions or generate dynamic, context-aware questions.

### Hierarchy and Inheritance

The AI question generation settings follow a hierarchical structure:

```
InterviewTemplate (allow_ai_questions)
    ↓
InterviewTemplateSection (allow_ai_questions, allow_ai_override_questions)
    ↓
InterviewTemplateQuestion (allow_ai_followup)
```

**Note**: The section level has two distinct AI controls:
- `allow_ai_questions` - Controls whether AI can **add** new questions
- `allow_ai_override_questions` - Controls whether AI can **reformulate** existing questions

### Configuration Levels

#### 1. Template Level (`allow_ai_questions`)

When enabled at the template level, the AI can:
- Generate entirely new questions not defined in the template
- Create custom interview flows based on candidate responses
- Adapt the interview depth based on candidate expertise

**Use Cases**:
- Exploratory interviews where flexibility is key
- Initial screening interviews
- Research-focused candidate assessments

**Example**:
```python
template = InterviewTemplate.create(
    name="Adaptive Technical Interview",
    allow_ai_questions=True,  # AI can create new questions
    ...
)
```

#### 2. Section Level (`allow_ai_questions`)

When enabled at the section level, the AI can:
- Generate additional questions within this specific section
- Explore topics in more depth based on candidate answers
- Fill gaps in candidate experience within the section context

**Use Cases**:
- Deep-dive into specific areas (e.g., technical experience)
- Adaptive questioning for soft skills assessment
- Exploring candidate projects in detail

**Example**:
```python
section = InterviewTemplateSection.create(
    name="Technical Deep Dive",
    allow_ai_questions=True,  # AI can create NEW questions for this section
    section=InterviewTemplateSectionEnum.EXPERIENCE,
    ...
)
```

#### 3. Section Level (`allow_ai_override_questions`)

When enabled at the section level, the AI can:
- Reformulate existing predefined questions to match candidate level
- Override question phrasing for better clarity
- Adapt question complexity based on candidate responses

**Important**: This is different from `allow_ai_questions`:
- `allow_ai_questions=True` → AI **adds** new questions beyond what's defined
- `allow_ai_override_questions=True` → AI **reformulates** existing questions

**Use Cases**:
- Adapting question difficulty for junior vs senior candidates
- Rephrasing technical questions for non-technical candidates
- Localizing or simplifying complex questions

**Example**:
```python
section = InterviewTemplateSection.create(
    name="Technical Experience",
    allow_ai_questions=False,  # Don't add new questions
    allow_ai_override_questions=True,  # But reformulate existing ones
    section=InterviewTemplateSectionEnum.EXPERIENCE,
    ...
)
```

#### 4. Question Level (`allow_ai_followup`)

When enabled at the question level, the AI can:
- Generate follow-up questions based on the candidate's answer
- Probe deeper into specific responses
- Clarify ambiguous or interesting points

**Use Cases**:
- Behavioral interview questions requiring examples
- Technical questions that need elaboration
- Experience-based questions requiring context

**Example**:
```python
question = InterviewTemplateQuestion.create(
    name="Most Complex Project",
    description="Describe your most technically complex project",
    allow_ai_followup=True,  # AI can ask follow-ups
    scope=InterviewTemplateQuestionScopeEnum.ITEM,
    ...
)
```

### Best Practices

**Structured Interviews**:
- Set all flags to `False` for completely standardized interviews
- Use when consistency and fairness are critical
- Best for compliance and regulated industries

**Hybrid Approach**:
- Enable `allow_ai_followup` on key questions
- Keep template and section flags disabled
- Maintains structure while allowing depth

**Adaptive Interviews**:
- Enable at template or section level for flexibility
- Best for senior roles or specialized positions
- Allows AI to explore unique candidate experiences

**Configuration Strategy**:
```python
# Structured (No AI)
template.allow_ai_questions = False
section.allow_ai_questions = False
section.allow_ai_override_questions = False
question.allow_ai_followup = False

# Hybrid (AI follow-ups only)
template.allow_ai_questions = False
section.allow_ai_questions = False
section.allow_ai_override_questions = False
question.allow_ai_followup = True  # Only on specific questions

# Adaptive with Override (reformulate existing questions)
template.allow_ai_questions = False
section.allow_ai_questions = False
section.allow_ai_override_questions = True  # AI reformulates questions
question.allow_ai_followup = True

# Adaptive (Full AI - new questions + reformulation)
template.allow_ai_questions = True
section.allow_ai_questions = True
section.allow_ai_override_questions = True
question.allow_ai_followup = True
```

### AI Behavior

When AI generation is enabled, the system:

1. **Analyzes Context**: Reviews candidate profile, previous answers, and template goals
2. **Generates Questions**: Creates relevant, context-aware questions
3. **Maintains Flow**: Ensures questions align with section objectives
4. **Respects Boundaries**: Stays within the defined scope and data types
5. **Tracks Provenance**: Marks AI-generated questions for audit purposes

---

## Legal Compliance (Legal Notices)

The Interview Template System includes `legal_notice` fields at three levels to ensure compliance with labor laws, GDPR, and other regulations. These fields allow displaying legal disclaimers to users during the interview process.

### Legal Notice Levels

#### 1. Template Level (`legal_notice`)

Displays legal text that applies to the entire interview template.

**Use Cases**:
- GDPR compliance notices
- General data processing disclaimers
- Company-wide legal requirements
- Recording consent notices

**Example**:
```python
template = InterviewTemplate.create(
    name="Software Engineer Interview",
    legal_notice="By participating in this interview, you consent to the processing of your personal data in accordance with GDPR. Your responses will be stored securely and used only for recruitment purposes.",
    ...
)
```

#### 2. Section Level (`legal_notice`)

Displays legal text specific to a section of the interview.

**Use Cases**:
- Background check consent for experience verification
- Reference check authorization
- Specific data processing for sensitive topics
- Section-specific disclaimers

**Example**:
```python
section = InterviewTemplateSection.create(
    name="Background Verification",
    legal_notice="By providing the following information, you authorize us to verify your employment history with previous employers.",
    section=InterviewTemplateSectionEnum.EXPERIENCE,
    ...
)
```

#### 3. Question Level (`legal_notice`)

Displays legal text for specific questions that require special compliance considerations.

**Use Cases**:
- Sensitive data collection (health, religion, etc.)
- Criminal background questions
- Financial information requests
- Questions requiring explicit consent

**Example**:
```python
question = InterviewTemplateQuestion.create(
    name="Disability Accommodation",
    description="Do you require any workplace accommodations?",
    legal_notice="This question is asked to ensure we can provide necessary accommodations. Answering is voluntary and will not affect your application.",
    scope=InterviewTemplateQuestionScopeEnum.GLOBAL,
    ...
)
```

### Hierarchy and Display

The legal notices follow a hierarchical structure:

```
Template Legal Notice (shown at interview start)
    ↓
Section Legal Notice (shown before each section)
    ↓
Question Legal Notice (shown with specific question)
```

### Best Practices for Legal Notices

1. **Template Level**: Use for general GDPR/data protection notices
2. **Section Level**: Use when a group of questions requires specific consent
3. **Question Level**: Use sparingly for questions requiring explicit individual consent
4. **Language**: Keep legal text clear and concise for user understanding
5. **Updates**: Review and update legal notices when regulations change
6. **Localization**: Consider translating legal notices for international candidates
7. **Documentation**: Keep records of legal notice versions for compliance audits

### Example Configuration

```python
# General template notice
template.legal_notice = "Your interview data is processed according to GDPR."

# Specific section notice for sensitive topics
experience_section.legal_notice = "We may contact your previous employers to verify employment."

# Individual question notice for optional questions
diversity_question.legal_notice = "Answering this question is voluntary and does not affect your application."
```

---

## Interview Execution

### Interview Entity

Represents an actual interview session with a candidate.

**Entity**: `Interview`

**Attributes**:
- `id` - InterviewId
- `candidate_id` - CandidateId
- `job_position_id` - Optional JobPositionId
- `application_id` - Optional CandidateApplicationId
- `interview_template_id` - Optional template used
- `interview_type` - JOB_POSITION or EXTENDED_PROFILE
- `status` - ENABLED, IN_PROGRESS, FINISHED, PAUSED, DISCARDED
- `title` - Interview title
- `description` - Interview description
- `scheduled_at` - When interview is scheduled
- `started_at` - When interview was started
- `finished_at` - When interview was finished
- `duration_minutes` - Interview duration
- `interviewers` - List of interviewer names
- `interviewer_notes` - Notes from interviewers
- `candidate_notes` - Notes from candidate
- `score` - Overall score (0-100)
- `feedback` - Interview feedback
- `free_answers` - Free text answers from candidate

**Status Flow**:
```
ENABLED → IN_PROGRESS → FINISHED
            ↓     ↑
            PAUSED

DISCARDED (can be set from any status)
```

**Methods**:
- `create()` - Factory method
- `start()` - Start the interview
- `finish()` - Finish the interview
- `pause()` - Pause the interview
- `resume()` - Resume paused interview
- `discard()` - Discard the interview
- `schedule()` - Schedule the interview
- `set_score()` - Set overall score
- `add_interviewer_notes()` - Add interviewer notes
- `add_feedback()` - Add feedback
- `update_details()` - Update interview details

---

### Interview Answer

Represents answers to specific questions during an interview.

**Entity**: `InterviewAnswer`

**Attributes**:
- `id` - InterviewAnswerId
- `interview_id` - Parent interview ID
- `interview_template_question_id` - Question being answered
- `answer_text` - The actual answer
- `score` - Score for this answer (0-100)
- `notes` - Additional notes
- `answered_at` - When answer was provided
- `scored_at` - When answer was scored

---

## Commands (Write Operations)

### Interview Template Commands

**Template Management**:
- `CreateInterviewTemplateCommand` - Create new template
- `UpdateInterviewTemplateCommand` - Update template details
- `DeleteInterviewTemplateCommand` - Delete template
- `EnableInterviewTemplateCommand` - Enable template
- `DisableInterviewTemplateCommand` - Disable template
- `PublishInterviewTemplateCommand` - Publish template
- `DraftInterviewTemplateCommand` - Set template to draft

**Section Management**:
- `CreateInterviewTemplateSectionCommand` - Create new section
- `UpdateInterviewTemplateSectionCommand` - Update section
- `DeleteInterviewTemplateSectionCommand` - Delete section
- `EnableInterviewTemplateSectionCommand` - Enable section
- `DisableInterviewTemplateSectionCommand` - Disable section
- `PublishInterviewTemplateSectionCommand` - Publish section
- `DraftInterviewTemplateSectionCommand` - Set section to draft
- `MoveSectionUpCommand` - Move section up in order
- `MoveSectionDownCommand` - Move section down in order

**Question Management**:
- `CreateInterviewTemplateQuestionCommand` - Create new question
- `UpdateInterviewTemplateQuestionCommand` - Update question
- `DeleteInterviewTemplateQuestionCommand` - Delete question
- `EnableInterviewTemplateQuestionCommand` - Enable question
- `DisableInterviewTemplateQuestionCommand` - Disable question
- `PublishInterviewTemplateQuestionCommand` - Publish question
- `DraftInterviewTemplateQuestionCommand` - Set question to draft

### Interview Commands

**Interview Management**:
- `CreateInterviewCommand` - Create new interview
- `StartInterviewCommand` - Start an interview
- `FinishInterviewCommand` - Finish an interview

**Answer Management**:
- `CreateInterviewAnswerCommand` - Create/submit an answer
- `UpdateInterviewAnswerCommand` - Update an answer
- `ScoreInterviewAnswerCommand` - Score an answer

---

## Queries (Read Operations)

### Interview Template Queries

- `ListInterviewTemplatesQuery` - List all templates with filtering
- `GetInterviewTemplateByIdQuery` - Get template by ID
- `GetInterviewTemplateFullByIdQuery` - Get template with all sections and questions
- `GetInterviewTemplateByJobCategoryQuery` - Get templates by job category
- `GetQuestionsBySectionQuery` - Get questions for a specific section
- `ListInterviewTemplateQuestionsQuery` - List all questions with filtering
- `GetInterviewTemplateQuestionByIdQuery` - Get question by ID

### Interview Queries

- `ListInterviewsQuery` - List all interviews with filtering
- `GetInterviewByIdQuery` - Get interview by ID
- `GetInterviewsByCandidateQuery` - Get interviews for a candidate
- `GetScheduledInterviewsQuery` - Get scheduled interviews
- `GetInterviewScoreSummaryQuery` - Get score summary for interview
- `GetAnswersByInterviewQuery` - Get all answers for an interview
- `GetInterviewAnswerByIdQuery` - Get specific answer by ID

---

## DTOs (Data Transfer Objects)

### Template DTOs

- `InterviewTemplateDto` - Template summary
- `InterviewTemplateFullDto` - Template with sections and questions
- `InterviewTemplateSectionDto` - Section data
- `InterviewTemplateQuestionDto` - Question data

### Interview DTOs

- `InterviewDto` - Interview data
- `InterviewAnswerDto` - Answer data
- `InterviewScoreSummaryDto` - Score summary

---

## Use Cases

### 1. Creating an Interview Template

```python
# 1. Create template
create_template_cmd = CreateInterviewTemplateCommand(
    company_id=company_id,
    name="Software Engineer Interview",
    intro="Technical assessment for SE role",
    prompt="Focus on technical skills and problem solving",
    goal="Assess technical competency",
    template_type=InterviewTemplateTypeEnum.POSITION_INTERVIEW,
    job_category=JobCategoryEnum.TECHNOLOGY
)
command_bus.execute(create_template_cmd)

# 2. Add sections
create_section_cmd = CreateInterviewTemplateSectionCommand(
    interview_template_id=template_id,
    name="Technical Experience",
    intro="Let's discuss your technical background",
    prompt="Ask about specific technologies",
    goal="Evaluate technical depth",
    section=InterviewTemplateSectionEnum.EXPERIENCE,
    sort_order=0
)
command_bus.execute(create_section_cmd)

# 3. Add questions
create_question_cmd = CreateInterviewTemplateQuestionCommand(
    interview_template_section_id=section_id,
    sort_order=0,
    name="Primary Language",
    description="What is your primary programming language?",
    data_type=InterviewTemplateQuestionDataTypeEnum.SHORT_STRING,
    scope=InterviewTemplateQuestionScopeEnum.ITEM,
    code="tech_exp_primary_lang"
)
command_bus.execute(create_question_cmd)

# 4. Publish template
publish_cmd = PublishInterviewTemplateCommand(template_id=template_id)
command_bus.execute(publish_cmd)
```

### 2. Conducting an Interview

```python
# 1. Create interview
create_interview_cmd = CreateInterviewCommand(
    candidate_id=candidate_id,
    job_position_id=job_position_id,
    interview_template_id=template_id,
    interview_type=InterviewTypeEnum.JOB_POSITION,
    title="Software Engineer Position - Round 1",
    scheduled_at=datetime(2025, 1, 15, 10, 0)
)
command_bus.execute(create_interview_cmd)

# 2. Start interview
start_cmd = StartInterviewCommand(interview_id=interview_id)
command_bus.execute(start_cmd)

# 3. Submit answers
answer_cmd = CreateInterviewAnswerCommand(
    interview_id=interview_id,
    interview_template_question_id=question_id,
    answer_text="Python is my primary language with 5 years experience"
)
command_bus.execute(answer_cmd)

# 4. Score answers
score_cmd = ScoreInterviewAnswerCommand(
    interview_answer_id=answer_id,
    score=85.0,
    notes="Strong technical background in Python"
)
command_bus.execute(score_cmd)

# 5. Finish interview
finish_cmd = FinishInterviewCommand(interview_id=interview_id)
command_bus.execute(finish_cmd)
```

### 3. Querying Templates and Interviews

```python
# Get template with all details
template = query_bus.query(
    GetInterviewTemplateFullByIdQuery(template_id=template_id)
)

# List interviews for a candidate
interviews = query_bus.query(
    GetInterviewsByCandidateQuery(candidate_id=candidate_id)
)

# Get score summary
summary = query_bus.query(
    GetInterviewScoreSummaryQuery(interview_id=interview_id)
)
```

---

## Repository Interfaces

### Template Repositories

- `InterviewTemplateRepositoryInterface` - Template persistence
- `InterviewTemplateSectionRepositoryInterface` - Section persistence
- `InterviewTemplateQuestionRepositoryInterface` - Question persistence

### Interview Repositories

- `InterviewRepositoryInterface` - Interview persistence
- `InterviewAnswerRepositoryInterface` - Answer persistence

---

## Events

### Interview Events

- `InterviewCreatedEvent` - When interview is created
- `InterviewStartedEvent` - When interview starts
- `InterviewFinishedEvent` - When interview finishes

### Answer Events

- `InterviewAnswerCreatedEvent` - When answer is submitted
- `InterviewAnswerScoredEvent` - When answer is scored

---

## API Endpoints

### Template Endpoints

```
GET    /admin/interview-templates              # List templates
GET    /admin/interview-templates/{id}         # Get template
GET    /admin/interview-templates/{id}/full    # Get template with details
POST   /admin/interview-templates              # Create template
PUT    /admin/interview-templates/{id}         # Update template
DELETE /admin/interview-templates/{id}         # Delete template
POST   /admin/interview-templates/{id}/enable  # Enable template
POST   /admin/interview-templates/{id}/disable # Disable template

POST   /admin/interview-templates/{id}/sections     # Create section
PUT    /admin/interview-templates/sections/{id}     # Update section
DELETE /admin/interview-templates/sections/{id}     # Delete section

POST   /admin/interview-templates/sections/{id}/questions  # Create question
PUT    /admin/interview-templates/questions/{id}            # Update question
DELETE /admin/interview-templates/questions/{id}            # Delete question
```

### Interview Endpoints

```
GET    /admin/interviews                   # List interviews
GET    /admin/interviews/{id}              # Get interview
POST   /admin/interviews                   # Create interview
POST   /admin/interviews/{id}/start        # Start interview
POST   /admin/interviews/{id}/finish       # Finish interview

GET    /admin/interviews/{id}/answers      # Get answers
POST   /admin/interviews/{id}/answers      # Submit answer
PUT    /admin/interviews/answers/{id}      # Update answer
POST   /admin/interviews/answers/{id}/score # Score answer
```

---

## Database Schema

### interview_templates
- id, company_id, name, intro, prompt, goal, status, template_type, job_category, allow_ai_questions, legal_notice, tags, metadata
- Indexes: company_id, status, job_category, template_type

### interview_template_sections
- id, interview_template_id, name, intro, prompt, goal, section, sort_order, status, allow_ai_questions, allow_ai_override_questions, legal_notice
- Indexes: interview_template_id, sort_order

### interview_template_questions
- id, interview_template_section_id, sort_order, name, description, data_type, scope, code, status, allow_ai_followup, legal_notice
- Indexes: interview_template_section_id, sort_order, code

### interviews
- id, candidate_id, job_position_id, application_id, interview_template_id, interview_type, status, title, description, scheduled_at, started_at, finished_at, duration_minutes, score, feedback, etc.
- Indexes: candidate_id, job_position_id, status, scheduled_at

### interview_answers
- id, interview_id, interview_template_question_id, answer_text, score, notes, answered_at, scored_at
- Indexes: interview_id, interview_template_question_id

---

## Best Practices

### Template Design

1. **Modular Sections**: Break templates into logical sections (Experience, Education, Skills)
2. **Reusable Questions**: Create questions that can be used across multiple templates
3. **Clear Instructions**: Provide clear `prompt` and `goal` for each section
4. **Proper Scoping**: Use `GLOBAL` for general questions, `ITEM` for specific candidate data
5. **AI Configuration**:
   - Use `allow_ai_questions=True` at template level for exploratory interviews
   - Use `allow_ai_questions=True` at section level to add new questions for specific topics
   - Use `allow_ai_override_questions=True` at section level to reformulate existing questions based on candidate level
   - Use `allow_ai_followup=True` on questions that benefit from elaboration
   - Keep all AI flags `False` for standardized, compliance-driven interviews
   - Consider using only `allow_ai_override_questions=True` for maintaining structure while adapting difficulty
6. **Legal Compliance**:
   - Always include `legal_notice` at template level for GDPR/data protection compliance
   - Add section-level `legal_notice` for background checks or sensitive data collection
   - Use question-level `legal_notice` for questions requiring explicit consent
   - Review and update legal notices regularly to match current regulations
   - Keep legal text clear and user-friendly

### Interview Execution

1. **Status Management**: Always follow the proper status flow (ENABLED → IN_PROGRESS → FINISHED)
2. **Scoring**: Score answers consistently (0-100 scale)
3. **Notes**: Use notes fields for context and feedback
4. **Scheduling**: Schedule interviews in advance when possible

### Data Consistency

1. **Cascading Deletes**: Deleting a template deletes all sections and questions
2. **Status Propagation**: Disabling a template doesn't auto-disable existing interviews
3. **Immutability**: Once an interview is FINISHED, avoid modifying answers

---

## Future Enhancements

1. **AI-Assisted Scoring**: Automatic scoring based on answer analysis
2. **Video Integration**: Support for video interview recordings
3. **Collaborative Scoring**: Multiple interviewers can score independently
4. **Template Versioning**: Track changes to templates over time
5. **Question Banks**: Shared question libraries across companies
6. **Analytics**: Interview performance metrics and insights

---

## Related Documentation

- [Clean Architecture Guide](./CLAUDE.md)
- [API Documentation](./API.md)
- [Database Schema](./DATABASE.md)
- [Domain Events](./EVENTS.md)
