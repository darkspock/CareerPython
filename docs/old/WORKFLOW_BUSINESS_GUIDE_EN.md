# Workflow System - Business Guide

**Version**: 1.0
**Date**: 2025-10-26

---

## Introduction

The CareerPython Workflow System allows companies to manage the entire lifecycle of a candidate from initial contact with the company through hiring (or rejection). This system is fully customizable and adapts to the specific needs of each company and position type.

---

## Core Concepts

### What is a Workflow?

A workflow is a **template** that defines the stages a candidate goes through during the selection process. Each company can create multiple workflows according to their needs.

**Examples of workflows:**
- **Standard Hiring**: Screening → HR Interview → Technical Interview → Final Interview → Offer → Hired
- **Technical Hiring**: Resume Review → Technical Test → Technical Interview → Lead Interview → CTO Meeting → Offer → Hired
- **Fast Hiring**: Interview → Offer → Hired

### Workflow Types

There are two main types:

1. **Prospecting (Sourcing)**: To manage candidates who haven't yet applied to a specific position
   - Active talent search
   - Head hunting
   - Lead management
   - Talent pool

2. **Selection (Evaluation)**: To manage candidates who have already applied to a specific position
   - Interview process
   - Technical assessments
   - Offer negotiation
   - Pre-onboarding

---

## The Complete Flow: From Candidate to Employee

### 1. Sourcing - Recruitment and Screening

This is the first phase where potential candidates are identified and filtered.

**Typical stages:**
- **Pending**: Newly entered candidate
- **Screening**: Initial profile review
- **Discarded**: Doesn't meet minimum requirements
- **On Hold**: Good profile but no immediate vacancy
- **To Talent Pool**: Outstanding candidates saved for future opportunities

**Characteristics:**
- This flow is NOT customizable (for now)
- It's the entry point for all candidates
- Candidates can come from different sources:
  - Direct application on the website
  - Manual entry by HR team
  - Referrals
  - Head hunting

**Information captured:**
- Candidate basic data
- CV/Resume
- Recruitment source
- Initial notes
- Candidate priority

**Result:**
- **Accepted** candidates move to the next flow (Evaluation)
- Discarded candidates are recorded with reason
- Pool candidates remain available for future positions

### 2. Evaluation - Selection Process

Once a candidate is accepted in Sourcing (or applies directly to a position), they enter the evaluation flow.

**Customizable stages:**
Each company defines their own stages according to position type. Examples:

- **HR Interview**: First interview to validate cultural fit
- **Technical Test**: Assessment of specific skills
- **Technical Interview**: In-depth interview with technical team
- **Manager Interview**: Final validation with area manager
- **References**: Work reference validation
- **Negotiation**: Discussion of terms and expectations

**Characteristics:**
- Each stage can have:
  - Estimated duration (e.g., 3 days)
  - Mandatory deadline (e.g., maximum 5 days)
  - Estimated cost (to calculate total hiring cost)
  - Assigned responsible parties
  - Automatic email template
  - Custom fields to capture information

**Information captured:**
- Assessment results
- Interviewer notes
- Ratings
- Internal comments
- Attached documents
- Specific information according to custom fields

### 3. Offer and Pre-Onboarding - Offer and Preparation

The final phase of the process where hiring is formalized.

**Customizable stages:**
- **Offer Proposal**: Initial offer preparation
- **Negotiation**: Discussion of terms and conditions
- **Document Submission**: Candidate sends required documentation
- **Document Verification**: Documentation validation
- **Contract Signing**: Formalization of employment relationship

**Characteristics:**
- This flow is also customizable
- Deadlines can be defined for each stage
- Document sending can be automated

---

## Stage Management

### What can be configured in each stage?

Each workflow stage can be configured in great detail:

#### 1. Basic Information
- **Name**: What the stage will be called (e.g., "Technical Interview")
- **Description**: What happens in this stage
- **Type**: Initial, Intermediate, Final, or Custom
- **Order**: Position in the workflow

#### 2. Timing
- **Estimated Duration**: How long this stage typically takes (e.g., 5 days)
- **Deadline**: Maximum time to complete the stage (e.g., 7 days)
  - This helps prioritize tasks
  - Overdue alerts are automatically calculated

#### 3. Responsibilities
- **Default Roles**: Which roles should handle this stage
  - Examples: "Recruiter", "Tech Lead", "HR Manager"
- **Assigned People**: Specific users always assigned
  - Useful when a person must always be involved

#### 4. Communication
- **Email Template**: Automatic email sent to candidate
  - Can be customized with variables (name, position, etc.)
- **Additional Text**: Specific additional message to include in email
- **Available Variables**:
  - Candidate name
  - Position title
  - Company name
  - Stage name
  - Custom text

#### 5. Costs
- **Estimated Cost**: Cost to complete this stage
  - Useful for calculating total hiring cost
  - Example: cost of technical tests, interviews, verifications

#### 6. Custom Fields

Each workflow can have custom fields to capture specific information:

**Field types:**
- **Text**:
  - Short text
  - Long text (text area)
- **Fixed Answers**:
  - Dropdown list
  - Checkboxes
  - Radio buttons
- **Date and Time**:
  - Full date and time
  - Time only
- **File**: For attaching documents
- **Numbers**:
  - Currency (e.g., salary expectation)
  - Integer
  - Decimal
  - Percentage

**Field configuration per stage:**
Each field can have different behaviors depending on the stage:
- **Hidden**: Not shown in this stage
- **Mandatory**: Must be filled to advance
- **Recommended**: Suggested but not required
- **Optional**: Can be filled if desired

**Practical example:**
Field: "Salary Expectation"
- In Screening: Hidden
- In First Interview: Recommended
- In Negotiation: Mandatory
- In Final Offer: Optional (already negotiated)

#### 7. Field Validations

Each custom field can have **validation rules** that are automatically checked when moving to the next stage. These validations help ensure candidates meet requirements and can even automatically discard candidates who don't fit the position.

**Validation Types:**

1. **Warning**: Shows an alert but allows proceeding to the next stage
   - Used for non-critical mismatches
   - User sees a warning message but can choose to continue
   - Example: "Candidate lives far from office location"

2. **Error**: Blocks progression to the next stage
   - Used for critical deal-breakers
   - User cannot advance the candidate
   - Example: "Candidate salary expectation exceeds position budget"

**Comparison with Position Fields:**

Validations can compare custom field values against position requirements:

- **Salary Comparison**: Compare candidate's salary expectation with position's salary range
- **Location Comparison**: Verify if candidate's location matches position requirements
- **Experience Level**: Check if candidate's years of experience meet minimum requirements
- **Skills Match**: Validate required skills against candidate's skills
- **Availability**: Check if candidate's start date aligns with position needs

**Validation Rules Configuration:**

Each field can have multiple validation rules:
- **Condition**: The comparison to perform (e.g., "greater than", "not equal to", "outside range")
- **Compare To**: Position field to compare against (e.g., "max_salary", "required_experience")
- **Severity**: Warning or Error
- **Message**: Custom message to show the user

**Practical Examples:**

**Example 1: Salary Validation (Error)**
```
Field: "Salary Expectation"
Validation Rule:
- Condition: Greater than
- Compare To: Position.max_salary
- Severity: Error
- Message: "Candidate expects ${candidate_salary}, but position max is ${position_max_salary}. Cannot proceed."

Result: If candidate expects $150,000 but position max is $120,000, user sees error and cannot advance to next stage.
```

**Example 2: Location Validation (Warning)**
```
Field: "Current Location"
Validation Rule:
- Condition: Different from
- Compare To: Position.location
- Severity: Warning
- Message: "Candidate is in ${candidate_location}, position is in ${position_location}. Consider relocation needs."

Result: User sees warning but can still proceed if they decide candidate is worth relocating.
```

**Example 3: Experience Validation (Error)**
```
Field: "Years of Experience"
Validation Rule:
- Condition: Less than
- Compare To: Position.minimum_experience
- Severity: Error
- Message: "Candidate has ${candidate_experience} years, position requires minimum ${position_minimum_experience} years."

Result: Blocks advancement if candidate doesn't meet minimum experience requirement.
```

**Example 4: Availability Validation (Warning)**
```
Field: "Available Start Date"
Validation Rule:
- Condition: After
- Compare To: Position.desired_start_date
- Severity: Warning
- Message: "Candidate available from ${candidate_start_date}, position needs someone by ${position_start_date}."

Result: Shows warning but allows proceeding if hiring manager accepts the delay.
```

**How Validations Work:**

1. **During Stage Transition**: When a user tries to move a candidate to the next stage, all field validations for the current stage are checked.

2. **Validation Results**:
   - ✅ **All pass**: Candidate moves to next stage smoothly
   - ⚠️ **Warnings only**: User sees warning message(s) with option to proceed or cancel
   - ❌ **Any errors**: User sees error message(s) and cannot proceed until issues are resolved

3. **User Actions**:
   - If validations fail, user can:
     - Edit field values to fix the issue
     - Contact candidate to negotiate (e.g., lower salary expectation)
     - Mark candidate as rejected with reason
     - Override validation (only for warnings, and only if they have special permission)

4. **Automatic Rejection**: Optionally, companies can configure certain error validations to automatically reject candidates, saving time on clearly unsuitable candidates.

**Benefits:**
- **Efficiency**: Automatically catch mismatches early in the process
- **Consistency**: Ensure all candidates meet the same criteria
- **Transparency**: Clear reasons for rejections or concerns
- **Data Quality**: Catch data entry errors before they become issues
- **Time Savings**: Avoid interviewing candidates who clearly don't fit

---

## Assigning Responsible Parties

### How are people assigned to stages?

When creating a **job position**, you must:

1. **Select a workflow** from available templates
2. **Assign users to each stage** of the flow

**Example:**
```
Position: "Senior Python Developer"
Flow: "Technical Hiring" (6 stages)

Assignments:
- Stage 1 (HR Screening)        → Maria (Recruiter)
- Stage 2 (Technical Test)      → Juan (Tech Lead), Ana (Senior Developer)
- Stage 3 (Technical Interview)  → Juan (Tech Lead), Ana (Senior Developer)
- Stage 4 (CTO Interview)        → Carlos (CTO)
- Stage 5 (Verification)         → Maria (Recruiter)
- Stage 6 (Offer)                → Maria (Recruiter), Carlos (CTO)
```

**Characteristics:**
- **Multiple people** can be assigned to the same stage (collaborative work)
- People can be **changed at any time**
- Only assigned people can **move candidates** to the next stage
- Administrators can always see everything (but cannot move candidates unless assigned)

---

## Task System

### How do users know what they need to do?

Each user has a **personalized task dashboard** that shows:

### 1. Directly Assigned Tasks
Candidates in stages where the user is specifically assigned.

### 2. Available Tasks by Role
Candidates in stages that match the user's roles but don't have an assigned person yet.

**Example:**
- Maria has the "Recruiter" role
- There are 5 candidates in the "HR Screening" stage (which requires "Recruiter" role)
- Maria sees those 5 tasks as "available"
- Maria can "claim" a task to work on it
- Once claimed, only Maria can process it

### Task Prioritization

Tasks are automatically prioritized based on:

1. **Stage deadline**:
   - Overdue (past deadline): +50 priority points
   - Due today: +30 points
   - Due in 1-2 days: +20 points
   - Due in 3-5 days: +10 points
   - Due in 6+ days: 0 points

2. **Position priority**: 0-5 stars
   - Multiplied by 10 (0-50 points)
   - Useful for critical or urgent positions

3. **Candidate priority**: 0-5 stars
   - Multiplied by 5 (0-25 points)
   - Useful for exceptional candidates

**Total Priority = 100 (base) + deadline + position + candidate**

**Maximum possible score: 225**

### Task Visualization

In the dashboard, each task shows:
- **Candidate name and photo**
- **Position applied for**
- **Current stage**
- **Priority indicator** (color):
  - Red: High priority (175+)
  - Orange: Medium-High (150-174)
  - Yellow: Medium (125-149)
  - Gray: Normal (<125)
- **Deadline** with urgency indicator
- **Time in stage**
- **Quick actions**: View, Claim, Move to next stage

---

## Communication with Candidates

### Pseudo-Chat Message System

The system allows bidirectional communication between company and candidate:

**How does it work?**

1. **Company sends message to candidate**:
   - Message is saved in the system
   - An **email notification** is sent to the candidate
   - Email includes a "View Conversation" button

2. **Candidate receives email**:
   - Sees a message summary
   - Clicks "View Conversation"
   - Is redirected to the platform (must log in)

3. **Candidate responds in platform**:
   - Sees entire conversation history
   - Writes their response
   - Response is saved in the system
   - **NO email is sent to company** (avoids saturation)

4. **Company sees response**:
   - On next login, sees a notification
   - Accesses the conversation
   - Can respond (this does send email to candidate)

**Important:**
- All responses must be made **within the platform**
- Cannot respond directly to email
- This keeps all communication organized and traceable

### Automatic Emails per Stage

When a candidate advances to a new stage, an email can be automatically sent if:
- The stage has a configured **email template**
- The template is personalized with candidate and position data
- **Additional text** specific to that stage can be added

---

## Permissions and Visibility

### Who can see what?

#### Company Users:
- ✅ Can see **all applications** from their company
- ✅ Can see **all stages** of the workflow
- ✅ Can see **details** of any candidate
- ❌ Can only **move candidates** in stages where they're assigned

#### Company Administrators:
- ✅ Can see everything
- ✅ Can move candidates in any stage (have special permission)
- ✅ Can change user assignments

#### Candidates:
- ✅ Can see **their own applications**
- ✅ Can see **current stage name**
- ✅ Can see **stage history**
- ❌ Cannot see **internal notes** or **private comments**
- ❌ Cannot see **who is assigned** to stages

### Candidate Movement Rules

1. **Only assigned users can move**: A user can only advance/move back a candidate if assigned to the current stage

2. **Only adjacent movements**: Cannot skip stages
   - If in stage 2, can only go to stage 1 (back) or stage 3 (forward)

3. **Final stages are terminal**: Stages marked as "final" don't allow advancing
   - Examples: "Hired", "Rejected", "Withdrawn"

---

## Analysis and Reports

### Available Metrics

The system allows analyzing workflow performance:

#### Metrics per Workflow:
- **Average time per stage**: How long candidates spend in each stage
- **Conversion rate per stage**: What percentage advances from one stage to another
- **Total applications**: How many candidates have used this flow
- **Active candidates**: How many are currently in process
- **Hired candidates**: How many successfully completed
- **Rejected candidates**: How many were discarded

#### Bottleneck Detection:
- Identifies stages where candidates stay longer than expected
- Useful for optimizing the process

#### Cost Analysis:
- **Cost per hire**: Sum of costs from all stages
- **Average cost per flow**: Helps with budgeting
- **Hiring ROI**: Compare cost vs. employee value

#### Visualizations:
- Conversion funnel
- Time per stage charts
- Cost timeline
- Bottleneck tables

---

## Practical Use Cases

### Case 1: Developer Hiring

**Context:**
- Technology company looking for a Senior Python Developer
- Rigorous technical process
- Multiple interviewers

**Workflow used:** "Technical Hiring"

**Stages and Responsible Parties:**
1. **HR Screening** (3 days) → Maria (Recruiter)
2. **Technical Test** (7 days) → Juan and Ana (Dev Team)
3. **Technical Interview** (5 days) → Juan and Ana
4. **Lead Interview** (5 days) → Juan
5. **CTO Interview** (5 days) → Carlos
6. **Offer** (3 days) → Maria and Carlos

**Candidate experience:**
- Applies to position on website
- Receives automatic confirmation email
- Maria reviews CV (2 days)
- Receives technical test invitation email
- Completes test (5 days)
- Juan reviews test and sends feedback
- Receives technical interview invitation
- Conducts interview with Juan and Ana
- Receives CTO interview invitation
- Conducts final interview
- Receives job offer
- Negotiates terms via platform messages
- Accepts offer

**Total: 28 estimated days**

### Case 2: Urgent Hiring

**Context:**
- Urgent replacement due to resignation
- Simplified process
- Quick decision

**Workflow used:** "Fast Hiring"

**Stages:**
1. **Initial Interview** (1 day) → Maria (HR) + Area Manager
2. **Offer** (1 day) → Maria

**Candidate experience:**
- Applies on website
- Receives call same day
- Interview next day
- Receives offer 2 hours later
- Accepts offer

**Total: 2 days**

### Case 3: Head Hunting

**Context:**
- Active talent search
- Candidate didn't apply, was contacted
- "Courting" process

**Workflow used:** "Prospecting" → "Technical Hiring"

**Prospecting stages:**
1. **Identification**: Recruiter finds interesting profile on LinkedIn
2. **First Contact**: Sends initial message
3. **Screening**: Informal call to gauge interest
4. **To Talent Pool**: Interested candidate but no vacancy yet

**6 months later, position opens:**
- Candidate moves from "Talent Pool" to "Evaluation"
- Begins formal selection process
- Follows standard "Technical Hiring" flow

---

## System Benefits

### For the Company:

1. **Standardization**: All candidates follow the same process
2. **Traceability**: Every action and decision is recorded
3. **Collaboration**: Multiple people can work on the process
4. **Automation**: Automatic emails save time
5. **Metrics**: Data to continuously improve the process
6. **Flexibility**: Each position can have its own flow
7. **Compliance**: Complete history for audits

### For Recruiters:

1. **Clarity**: Know exactly what they need to do
2. **Prioritization**: Urgent tasks automatically highlighted
3. **Organization**: All information in one place
4. **Efficiency**: Less time searching for information
5. **Follow-up**: Automatic deadline alerts

### For Candidates:

1. **Transparency**: Know what stage they're in
2. **Communication**: Direct channel with company
3. **Professionalism**: Organized and clear process
4. **Speed**: Faster responses
5. **Experience**: Better impression of company

---

## Frequently Asked Questions

### Can I change a position's workflow after creating it?
Yes, but it will only affect new applications. Existing applications will continue with the original flow.

### What happens if I delete a stage from a workflow?
You cannot delete a stage if there are candidates currently in it. First you must move candidates to another stage.

### Can I have different workflows for different position types?
Yes, that's precisely the goal. For example: "Junior Hiring", "Senior Hiring", "Executive Hiring", etc.

### Can candidates see who is evaluating them?
No, candidates only see the stage name but not who is assigned or internal comments.

### What happens if a user goes on vacation?
An administrator can temporarily reassign their tasks to another person. When they return, tasks can be reassigned back.

### Can group interviews be conducted?
Yes, you can assign multiple people to the same stage. Everyone will see the candidate and can leave comments.

### Are custom fields mandatory?
It depends on how they're configured. They can be mandatory, recommended, or optional depending on the stage.

### What happens with candidates in the talent pool?
They remain saved in the database and can be contacted in the future for new positions. It's like a "reserve" of good candidates.

### Does the system send deadline reminders?
Yes, when a task is close to deadline or already overdue, it's highlighted in red/orange on the task dashboard.

### Can I export reports?
Yes, the system allows exporting reports in CSV and PDF with workflow metrics.

---

## Glossary of Terms

- **Workflow**: Template that defines selection process stages
- **Stage**: Specific step within a flow (e.g., "Technical Interview")
- **Candidate**: Person who applies or is proposed for a position
- **Application**: Link between a candidate and a specific position
- **Talent Pool**: Reserve of outstanding candidates for future opportunities
- **Sourcing**: Process of searching and recruiting candidates
- **Screening**: Initial review to filter candidates
- **Evaluation**: Formal evaluation process (interviews, tests)
- **Task**: Pending action on a user's dashboard
- **Assignment**: Link between a user and a stage
- **Priority**: Score that determines task urgency
- **Deadline**: Maximum time to complete a stage
- **Custom Field**: Additional field to capture specific information
- **Email Template**: Predefined format for automatic emails

---

## Conclusion

The CareerPython Workflow System is a powerful and flexible tool that allows companies to manage their hiring process efficiently, organized, and transparently.

Its modular design allows adapting to any type of company and process, from fast hiring to complex processes with multiple stages and evaluators.

Automation of repetitive tasks, intelligent prioritization, and performance metrics help HR teams be more productive and effective, while candidates enjoy a more professional and transparent process.
