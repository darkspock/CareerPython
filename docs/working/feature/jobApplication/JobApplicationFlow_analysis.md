# Job Application Flow - Analysis

## Document Summary

This document describes the user flow for job applications in CareerPython. It covers configurable application forms (short vs full), CV assistance, user registration process, application wizard, and how data is passed to companies.

---

## Key Design Decisions

### 1. Configurable Application Depth
The company decides per job position whether the candidate must fill normalized data or just submit CV:

| Mode | Required | Optional |
|------|----------|----------|
| **Short** | Email + CV + GDPR | - |
| **Full** | Email + CV + GDPR | Experience, Education, Projects, Skills |

**Implementation**: `job_position.requires_normalized_data` boolean field

### 2. CV Assistance Option
Candidates without a CV can use "Help me creating a CV":
- System guides them through structured data entry
- Generates a PDF CV from the data
- Application stays "pending" until CV is generated and submitted

### 3. Data Snapshot for Companies
When application is submitted:
- **Markdown summary**: All candidate info rendered as markdown, stored in `candidate_application.profile_snapshot_markdown`
- **Contact info**: Live data (always current email/phone)
- **Profile data**: Historical snapshot (what they had when they applied)
- **CV attached**: Generated or original PDF

---

## Strengths

### 1. Flexible Application Process
- Companies control complexity per position
- Reduces friction for simple roles
- Full data when needed for complex roles

### 2. CV Assistance
- Helps candidates without professional CV
- Captures structured data as byproduct
- Platform adds value beyond just application

### 3. Clear Data Separation
- Live contact data = company can always reach candidate
- Historical profile = fair evaluation based on what was submitted
- Markdown snapshot = recruiter sees everything in one view

### 4. Existing Infrastructure
All phases (1-7) already implemented:
- user_registration table ✅
- Registration commands ✅
- Email verification ✅
- API endpoints ✅
- Application wizard ✅
- Frontend pages ✅
- Cleanup jobs ✅

---

## New Requirements Identified

### 1. Job Position Configuration
Need to add field to control application type:

```python
class JobPosition:
    # ... existing fields ...
    application_mode: ApplicationModeEnum  # SHORT, FULL, CV_BUILDER
    required_sections: List[str]  # ['experience', 'education', 'skills']
```

### 2. CV Builder Flow
New flow for "Help me creating a CV":

```
Click "Help me creating a CV"
    ↓
Wizard: General Data → Experience → Education → Projects → Skills
    ↓
Generate PDF CV (ResumeGenerationService)
    ↓
Return to pending application
    ↓
Submit application with generated CV
```

### 3. Profile Snapshot Storage
New fields in `candidate_application`:

```python
class CandidateApplication:
    # ... existing fields ...
    profile_snapshot_markdown: str  # Full profile as markdown
    profile_snapshot_json: dict     # Structured data at time of application
    cv_file_id: str                 # Reference to attached CV
```

### 4. Pending Application Badge
UI component showing pending applications that need CV completion.

---

## Data Flow Comparison

### Current Flow
```
Apply → Create CandidateApplication → Company sees live candidate data
```

### New Flow
```
Apply → Create CandidateApplication with snapshot → Company sees:
├── Contact info (live) - always current
├── Profile markdown (historical) - what they submitted
├── Profile JSON (historical) - structured for filtering
└── CV PDF (attached) - generated or uploaded
```

---

## Technical Considerations

### 1. Markdown Generation
Create service to render candidate profile as markdown:

```python
class ProfileMarkdownService:
    def render(self, candidate: Candidate) -> str:
        """
        Returns:
        # Juan García
        📧 juan@email.com | 📱 +34 612 345 678 | 📍 Madrid

        ## Experiencia Profesional

        ### Senior Developer @ TechCorp (2020-2024)
        - Desarrollo de APIs REST
        - Liderazgo de equipo de 5 personas

        ## Educación
        ...
        """
```

### 2. Application Pending State
Add state to track incomplete applications:

```python
class ApplicationStatusEnum(Enum):
    DRAFT = "draft"           # Started but not submitted
    PENDING_CV = "pending_cv" # Waiting for CV generation
    SUBMITTED = "submitted"   # Complete and sent
    # ... existing statuses ...
```

### 3. CV Generation Integration
Reuse existing `ResumeGenerationService` for CV builder flow.

---

## Questions Resolved

| Question | Answer |
|----------|--------|
| Does candidate fill normalized data? | Depends on job position config |
| What if no CV? | "Help me creating a CV" option |
| Live or historical data for company? | Historical snapshot + live contact |
| Format for company? | Markdown + JSON + PDF |

---

## Recommendations

### Priority 1 - Schema Updates
1. Add `application_mode` to JobPosition entity
2. Add `profile_snapshot_markdown` and `profile_snapshot_json` to CandidateApplication
3. Add `cv_file_id` to CandidateApplication

### Priority 2 - New Services
1. Create `ProfileMarkdownService` for rendering
2. Update `CreateCandidateApplicationCommand` to generate snapshots
3. Create `CompleteApplicationWithCVCommand` for CV builder flow

### Priority 3 - UI Updates
1. Add "Help me creating a CV" button to application form
2. Add pending applications badge to candidate dashboard
3. Show snapshot vs live data indicator in company view

---

## Next Steps

See `JobApplicationFlow_tasks.md` for implementation tasks.
