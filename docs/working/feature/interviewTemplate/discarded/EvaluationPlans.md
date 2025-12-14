# Product Requirements Document: Evaluation Plans (Content Layer)

**Context:** The system already possesses a configurable **Workflow** engine (Stages/Phases). This module defines the **Content** (questions, scripts, scorecards) that populates those stages depending on the specific Job Position (e.g., Frontend vs. Backend).

## 1. Concept: The "Injection" Model
One Workflow can serve many Evaluation Plans.

* **Workflow:** "Engineering Pipeline" (Stage 1: Auto-Screening $\rightarrow$ Stage 2: Live Interview).
* **Evaluation Plan A (Frontend):**
    * *Maps to Stage 1:* React Quiz.
    * *Maps to Stage 2:* System Design (Client-side focus).
* **Evaluation Plan B (Backend):**
    * *Maps to Stage 1:* Python Quiz.
    * *Maps to Stage 2:* Database Architecture.

---

## 2. Entity: Evaluation Plan (The "Set of Interviews")
A grouped collection of assessment templates designed for a specific job profile.

### 2.1 Attributes
* **Name:** (e.g., "Senior Frontend Kit").
* **Department/Category:** (e.g., "Engineering").
* **Workflow Compatibility:** (Optional but recommended)
    * Links this Plan to a specific Workflow ID.
    * *Why?* To ensure you don't try to plug a "Retail Kit" (2 steps) into an "Executive Workflow" (10 steps).

### 2.2 The "Stage Mapping" (Crucial Logic)
This is the bridge between your existing Workflow and this new entity. Inside the Evaluation Plan, you do not just list templates; you **assign** them to Workflow Stages.

* **Mapping Table:**
    * `Workflow_Stage_ID` $\leftrightarrow$ `Interview_Template_Instance_ID`

* **Logic:**
    * When the candidate moves to **Stage X** in the Workflow...
    * The system looks at the **Evaluation Plan** assigned to this Job...
    * It finds the **Template** mapped to Stage X...
    * It triggers that specific interview/assessment.

---

## 3. Entity: Interview Template Instance (The Content)
* **Parent Plan:** ID of the Evaluation Plan.
* **Target Workflow Stage:** The stage in your workflow where this interview happens (e.g., "Screening").
* **Content:**
    * Questions (Killer Qs, Tech Qs).
    * Scorecard Criteria.
    * AI Normalization Schemas.

---

## 4. User Experience (UX)

### 4.1 Creating a New Evaluation Plan
1.  **Select Base Workflow:** User selects "Standard Technical Workflow".
    * *System displays the empty stages of that workflow.*
2.  **Define Content:**
    * The UI shows: **"Stage 1: Screening"**.
    * User action: **"Add Content"** $\rightarrow$ Create from scratch OR Import "Frontend Screening Template" from Library.
    * The UI shows: **"Stage 2: Technical Interview"**.
    * User action: **"Add Content"** $\rightarrow$ Import "React Live Coding Template".
3.  **Save Plan:** Saved as "Frontend Developer Plan".

### 4.2 Assigning to a Job Opening (The Setup)
When a recruiter creates a new Job Opening (e.g., "Senior React Dev"):
1.  **Select Workflow:** "Standard Technical Workflow".
2.  **Select Evaluation Plan:** "Frontend Developer Plan".
3.  **System Validation:** The system confirms that the Plan matches the Workflow structure.

### 4.3 Execution (The Recruiter View)
When a candidate is in the **"Technical Interview"** column:
1.  Recruiter clicks "Start Interview".
2.  System checks the Job Opening $\rightarrow$ Evaluation Plan.
3.  System loads the **"React Live Coding Template"**.
    * *Note:* If the candidate was for a Backend role (using the same Workflow but different Plan), the system would load the "Python Template".

---

## 5. Technical Data Model (simplified)

**Entity: Workflows** (You already have this)
* `id`: 100
* `name`: "Engineering Pipeline"
* `stages`: [Stage A (Screening), Stage B (Tech Interview)]

**Entity: EvaluationPlans** (The Set)
* `id`: 500
* `name`: "Frontend Kit"
* `workflow_id`: 100 (Linked to Engineering Pipeline)

**Entity: PlanStageConfigs** (The Mapping)
* `plan_id`: 500
* `workflow_stage_id`: Stage A
* `template_instance_id`: (The specific Questions for Frontend Screening)

---

## 6. Why this fits your need
* **Scalability:** You define the Workflow **once** (The Process).
* **Specificity:** You define the Evaluation Plans **per role** (The Content).
* **Flexibility:**
    * If you change the Workflow (add a "Security Check" stage), you update the Workflow definition.
    * The system prompts you to update your Evaluation Plans to add content for that new stage.

Does this differentiation between **Workflow (Structure)** and **Plan (Content Injection)** align better with your current architecture?