# Resume Sharing Strategy - Hybrid Approach

**Date**: 2025-01-22
**Version**: 1.0

## Overview

CareerPython uses a **hybrid approach** for sharing candidate resumes with companies:
- **Structured Data**: Primary view for in-app browsing (searchable, filterable)
- **Generated PDF**: Secondary option for download (portable, immutable snapshot)

This strategy maximizes both user experience and monetization potential.

---

## Core Principles

### 1. **Structured Data First**
Companies see candidate information as **structured data** (education, experience, skills) through the platform UI. This enables:
- Searching and filtering candidates
- Auto-matching to position requirements
- Timeline views and skill tags
- Responsive design across devices

### 2. **PDF as Backup**
A **generated PDF resume** is created at application time and stored as a snapshot. This provides:
- Downloadable format for offline review
- Immutable record for compliance/audit
- Shareable format outside platform
- Professional presentation

### 3. **Company Controls Updates**
Each position has an **update policy** that determines if candidates can modify their resume after applying:
- `allow_resume_updates: boolean` (per position)
- `resume_update_deadline: datetime` (optional time limit)
- Version history maintained if updates allowed

---

## Data Model

### CompanyApplication Entity

```python
@dataclass
class CompanyApplication:
    """Formal application to a specific position"""

    # Identity
    id: CompanyApplicationId
    company_candidate_id: CompanyCandidateId
    candidate_id: CandidateId  # Required - must be registered
    company_id: CompanyId
    position_id: PositionId

    # Structured Data (for in-app viewing)
    shared_data: SharedDataPermissions  # What candidate authorized to share

    # PDF Resume (for download/snapshot)
    resume_pdf_url: str  # S3 path: company/{id}/applications/{id}/resume_v{version}.pdf
    resume_pdf_version: int  # Current version (starts at 1)
    resume_snapshot_at: datetime  # When current PDF was generated

    # Update Policy
    allow_resume_updates: bool  # Copied from Position at application time
    resume_update_deadline: Optional[datetime]  # Deadline for updates
    resume_last_updated_at: Optional[datetime]  # Last update timestamp

    # Workflow
    workflow_id: CompanyWorkflowId
    current_stage_id: WorkflowStageId

    # Metadata
    status: ApplicationStatus
    applied_at: datetime
    tags: List[str]
    internal_notes: str
    priority: Priority

    # Version History (if updates allowed)
    resume_versions: List[ResumeVersion]

    created_at: datetime
    updated_at: datetime
    archived_at: Optional[datetime]


@dataclass
class ResumeVersion:
    """Historical version of resume for an application"""
    version: int
    pdf_url: str
    created_at: datetime
    changelog: Optional[str]  # "Updated work experience at Google"
    created_by: str  # "candidate" or "system"


@dataclass
class SharedDataPermissions:
    """What candidate data is shared with company"""
    include_education: bool = True
    include_experience: bool = True
    include_projects: bool = True
    include_skills: bool = True
    include_languages: bool = True
    include_certifications: bool = True
    custom_message: Optional[str] = None  # Cover letter
```

### Position Entity (Update)

```python
@dataclass
class Position:
    ...existing fields...

    # Resume Update Policy
    allow_resume_updates: bool = False  # Default: no updates after applying
    resume_update_deadline_days: Optional[int] = None  # e.g., 7 days

    # If both are set:
    # - Candidate can update resume within X days of application
    # - After deadline, resume is locked
```

---

## Application Flow

### 1. Candidate Registration & Onboarding

```
User creates account
    ↓
Candidate profile created
    ↓
Complete onboarding:
- Education history
- Work experience
- Projects
- Skills & languages
    ↓
Generate initial resume (PDF)
    ↓
Profile complete ✓
```

**If referred from company subdomain**:
```
Lead created during registration:
- Lead.candidate_id = NULL (initially)
- Basic info captured

After profile complete:
- Lead.candidate_id = candidate.id (linked)
- Lead can now be converted to CompanyCandidate when applying
```

### 2. Candidate Views Position (Company Subdomain)

```
URL: jobs.techcorp.com/positions/senior-python-dev

Position details shown:
- Title, description, requirements
- Location, salary range
- Company info

Metadata visible to candidate:
✓ "This company allows resume updates for 7 days after applying"
or
✓ "Resume will be locked after submitting application"

[Apply Now] button
```

### 3. Application Submission Flow

```
Step 1: Login/Register Check
    ↓
Step 2: Select Data to Share
┌───────────────────────────────────────┐
│ Apply to: Senior Python Developer    │
├───────────────────────────────────────┤
│ What information do you want to share?│
│                                       │
│ ☑ Education (2 degrees)              │
│ ☑ Work Experience (3 positions)      │
│ ☑ Projects (5 projects)              │
│ ☑ Skills (Python, Django, etc.)      │
│ ☑ Languages (English, Spanish)       │
│ ☑ Certifications (AWS, etc.)         │
│                                       │
│ Optional Cover Letter:                │
│ ┌─────────────────────────────────┐  │
│ │ [Text area]                     │  │
│ └─────────────────────────────────┘  │
└───────────────────────────────────────┘
    ↓
Step 3: Select/Generate Resume
┌───────────────────────────────────────┐
│ Select Resume Version:                │
│                                       │
│ ○ General Resume                     │
│   Created: Jan 15, 2025              │
│   [Preview]                          │
│                                       │
│ ● Position-Specific Resume (New)     │
│   Generate optimized for this role   │
│   [Preview]                          │
│                                       │
│ Note: ⚠️ Resume updates allowed for  │
│ 7 days after applying                │
└───────────────────────────────────────┘
    ↓
Step 4: Review & Submit
┌───────────────────────────────────────┐
│ Application Summary:                  │
│                                       │
│ Position: Senior Python Developer    │
│ Company: TechCorp                     │
│                                       │
│ Shared Data:                          │
│ ✓ Education, Experience, Projects    │
│ ✓ Skills, Languages                  │
│                                       │
│ Resume: Position-Specific (new)      │
│                                       │
│ [< Back]  [Submit Application]        │
└───────────────────────────────────────┘
```

### 4. Backend Processing

```python
# When candidate clicks "Submit Application"

async def submit_application(
    candidate_id: str,
    position_id: str,
    shared_data: SharedDataPermissions,
    resume_choice: ResumeChoice,  # existing or generate new
) -> CompanyApplication:

    # 1. Get position details
    position = await get_position(position_id)

    # 2. Create or get CompanyCandidate
    company_candidate = await get_or_create_company_candidate(
        company_id=position.company_id,
        candidate_id=candidate_id,
        source="direct_application"
    )

    # 3. Generate PDF resume
    if resume_choice == "new":
        # Generate position-specific resume
        resume_pdf = await generate_resume_for_position(
            candidate_id=candidate_id,
            position_id=position_id,
            template="professional"
        )
    else:
        # Use existing resume
        resume_pdf = await get_existing_resume(resume_choice.resume_id)

    # 4. Upload PDF to S3
    pdf_path = f"company/{position.company_id}/applications/{new_id}/resume_v1.pdf"
    pdf_url = await storage_service.upload_file(
        file_content=resume_pdf,
        filename="resume.pdf",
        content_type="application/pdf",
        storage_type=StorageType.APPLICATION_RESUME,
        entity_id=str(new_id),
        company_id=str(position.company_id)
    )

    # 5. Calculate update deadline
    deadline = None
    if position.allow_resume_updates and position.resume_update_deadline_days:
        deadline = datetime.utcnow() + timedelta(days=position.resume_update_deadline_days)

    # 6. Create CompanyApplication
    application = CompanyApplication.create(
        id=new_id,
        company_candidate_id=company_candidate.id,
        candidate_id=candidate_id,
        company_id=position.company_id,
        position_id=position_id,
        shared_data=shared_data,
        resume_pdf_url=pdf_url,
        resume_pdf_version=1,
        resume_snapshot_at=datetime.utcnow(),
        allow_resume_updates=position.allow_resume_updates,
        resume_update_deadline=deadline,
        workflow_id=position.workflow_id,
        current_stage_id=position.initial_stage_id
    )

    # 7. Save to database
    await repository.save(application)

    # 8. Send notifications (future)
    # await notify_assigned_recruiters(application)

    return application
```

### 5. Company Views Application

**Default View (Structured Data)**:
```
┌─────────────────────────────────────────────┐
│ John Doe - Senior Python Developer         │
│ Applied: Jan 22, 2025 at 10:30 AM          │
├─────────────────────────────────────────────┤
│ 📧 john.doe@email.com                       │
│ 📱 +1 555-0123                              │
│ 🌍 San Francisco, CA                        │
│ 💼 LinkedIn: linkedin.com/in/johndoe        │
├─────────────────────────────────────────────┤
│ Work Experience                             │
│ ────────────────────────────────────────    │
│ ● Software Engineer at Google               │
│   Jan 2020 - Present (5 years)             │
│   • Led team of 5 engineers                │
│   • Built microservices architecture       │
│                                             │
│ ● Backend Developer at Startup Inc          │
│   Mar 2018 - Dec 2019 (2 years)            │
│   • Developed REST APIs                    │
│   • Migrated to PostgreSQL                 │
├─────────────────────────────────────────────┤
│ Education                                   │
│ ────────────────────────────────────────    │
│ 🎓 BS Computer Science                      │
│    MIT, 2014 - 2018                         │
├─────────────────────────────────────────────┤
│ Skills                                      │
│ ────────────────────────────────────────    │
│ Python  Django  PostgreSQL  Docker          │
│ AWS  Kubernetes  Redis  Git                 │
├─────────────────────────────────────────────┤
│ Resume PDF                                  │
│ ────────────────────────────────────────    │
│ Version 1 (Original)                        │
│ Generated: Jan 22, 2025 at 10:30 AM        │
│ [📄 Download PDF]  [👁 Preview]             │
│                                             │
│ ⚠️ Updates allowed until Jan 29, 2025      │
├─────────────────────────────────────────────┤
│ Actions                                     │
│ ────────────────────────────────────────    │
│ [Move to Next Stage]  [Add Comment]         │
│ [Send Message]  [Reject]                    │
└─────────────────────────────────────────────┘
```

### 6. Candidate Updates Resume (If Allowed)

```
Candidate dashboard shows:
┌─────────────────────────────────────────┐
│ Your Applications                       │
├─────────────────────────────────────────┤
│ Senior Python Developer - TechCorp      │
│ Status: Under Review                    │
│ Applied: Jan 22, 2025                   │
│                                         │
│ ⏰ Resume updates allowed until:        │
│    Jan 29, 2025 (7 days remaining)     │
│                                         │
│ [Update Resume]                         │
└─────────────────────────────────────────┘

When clicking "Update Resume":
┌─────────────────────────────────────────┐
│ Update Resume for This Application      │
├─────────────────────────────────────────┤
│ Current Version: v1                     │
│ Last Updated: Jan 22, 2025              │
│                                         │
│ What changed?                           │
│ ┌─────────────────────────────────┐    │
│ │ Added recent project at Google  │    │
│ │ Fixed typo in education section │    │
│ └─────────────────────────────────┘    │
│                                         │
│ [Preview Updated Resume]                │
│                                         │
│ ⚠️ Company will be notified of update  │
│                                         │
│ [Cancel]  [Update Resume]               │
└─────────────────────────────────────────┘
```

**Backend Processing**:
```python
async def update_application_resume(
    application_id: str,
    candidate_id: str,
    changelog: str
) -> None:
    # 1. Verify candidate owns application
    application = await get_application(application_id)
    if application.candidate_id != candidate_id:
        raise Forbidden()

    # 2. Check if updates are allowed
    if not application.allow_resume_updates:
        raise ResumeUpdatesNotAllowed()

    # 3. Check deadline
    if application.resume_update_deadline:
        if datetime.utcnow() > application.resume_update_deadline:
            raise ResumeUpdateDeadlineExpired()

    # 4. Generate new PDF
    new_version = application.resume_pdf_version + 1
    resume_pdf = await generate_resume_for_position(
        candidate_id=candidate_id,
        position_id=application.position_id,
        template="professional"
    )

    # 5. Upload new version to S3
    pdf_path = f"company/{application.company_id}/applications/{application_id}/resume_v{new_version}.pdf"
    pdf_url = await storage_service.upload_file(
        file_content=resume_pdf,
        filename=f"resume_v{new_version}.pdf",
        content_type="application/pdf",
        storage_type=StorageType.APPLICATION_RESUME,
        entity_id=str(application_id),
        company_id=str(application.company_id)
    )

    # 6. Store version history
    old_version = ResumeVersion(
        version=application.resume_pdf_version,
        pdf_url=application.resume_pdf_url,
        created_at=application.resume_snapshot_at,
        changelog=None,
        created_by="candidate"
    )

    # 7. Update application
    application.resume_versions.append(old_version)
    application.resume_pdf_url = pdf_url
    application.resume_pdf_version = new_version
    application.resume_snapshot_at = datetime.utcnow()
    application.resume_last_updated_at = datetime.utcnow()

    # Add new version to history
    application.resume_versions.append(ResumeVersion(
        version=new_version,
        pdf_url=pdf_url,
        created_at=datetime.utcnow(),
        changelog=changelog,
        created_by="candidate"
    ))

    # 8. Save
    await repository.save(application)

    # 9. Notify company (optional)
    # await notify_recruiters_of_resume_update(application)
```

**Company sees update**:
```
┌─────────────────────────────────────────┐
│ 🔔 Resume Updated                       │
│ John Doe updated their resume           │
│ Jan 25, 2025 at 3:45 PM                │
│ Reason: "Added recent project"          │
│                                         │
│ View updated resume? [Yes]  [Later]     │
└─────────────────────────────────────────┘

Resume section now shows:
┌─────────────────────────────────────────┐
│ Resume PDF                              │
│ ────────────────────────────────────    │
│ Version: 2 (Current) ⚠️ UPDATED         │
│ Updated: Jan 25, 2025 at 3:45 PM       │
│ Changelog: "Added recent project"       │
│ [📄 Download PDF v2]                    │
│                                         │
│ Previous Versions:                      │
│ • Version 1 (Original)                  │
│   Jan 22, 2025 at 10:30 AM             │
│   [📄 Download]                         │
└─────────────────────────────────────────┘
```

---

## Storage Structure

### S3 Bucket Organization

```
s3://careerpython-resumes/
├── company/
│   └── {company_id}/
│       ├── candidates/
│       │   └── {candidate_id}/
│       │       └── resume.pdf  (from CompanyCandidate)
│       │
│       └── applications/
│           └── {application_id}/
│               ├── resume_v1.pdf  (original)
│               ├── resume_v2.pdf  (after update 1)
│               └── resume_v3.pdf  (after update 2)
│
└── candidate/
    └── {candidate_id}/
        └── resumes/
            ├── general_resume.pdf
            ├── resume_techcorp.pdf
            └── resume_startup.pdf
```

---

## API Endpoints

### Application Submission

```http
POST /api/positions/{position_id}/apply
Authorization: Bearer {candidate_token}
Content-Type: application/json

{
  "shared_data": {
    "include_education": true,
    "include_experience": true,
    "include_projects": true,
    "include_skills": true,
    "include_languages": true,
    "custom_message": "I'm very interested in this role..."
  },
  "resume_choice": {
    "type": "generate_new",  // or "use_existing"
    "resume_id": null,  // if use_existing, provide ID
    "template": "professional"
  }
}

Response 201:
{
  "application_id": "app_123",
  "status": "submitted",
  "applied_at": "2025-01-22T10:30:00Z",
  "resume_version": 1,
  "resume_pdf_url": "https://s3.../resume_v1.pdf",
  "allow_updates": true,
  "update_deadline": "2025-01-29T10:30:00Z"
}
```

### Resume Update

```http
PUT /api/applications/{application_id}/resume
Authorization: Bearer {candidate_token}
Content-Type: application/json

{
  "changelog": "Added recent project at Google"
}

Response 200:
{
  "application_id": "app_123",
  "resume_version": 2,
  "resume_pdf_url": "https://s3.../resume_v2.pdf",
  "updated_at": "2025-01-25T15:45:00Z",
  "versions_history": [
    {
      "version": 1,
      "created_at": "2025-01-22T10:30:00Z",
      "pdf_url": "https://s3.../resume_v1.pdf"
    },
    {
      "version": 2,
      "created_at": "2025-01-25T15:45:00Z",
      "pdf_url": "https://s3.../resume_v2.pdf",
      "changelog": "Added recent project at Google"
    }
  ]
}
```

### Get Application (Company View)

```http
GET /api/applications/{application_id}
Authorization: Bearer {company_user_token}

Response 200:
{
  "id": "app_123",
  "candidate": {
    "id": "cand_456",
    "name": "John Doe",
    "email": "john@email.com",
    "phone": "+1 555-0123",
    "location": "San Francisco, CA"
  },
  "position": {
    "id": "pos_789",
    "title": "Senior Python Developer"
  },
  "shared_data": {
    "education": [...],  // Structured data
    "experience": [...],
    "projects": [...],
    "skills": [...],
    "languages": [...]
  },
  "resume": {
    "current_version": 2,
    "pdf_url": "https://s3.../resume_v2.pdf",
    "last_updated": "2025-01-25T15:45:00Z",
    "changelog": "Added recent project at Google",
    "versions": [
      { "version": 1, "pdf_url": "...", "created_at": "..." },
      { "version": 2, "pdf_url": "...", "created_at": "...", "changelog": "..." }
    ]
  },
  "applied_at": "2025-01-22T10:30:00Z",
  "status": "under_review",
  "current_stage": "Technical Interview"
}
```

---

## Monetization Opportunities

### B2C (Candidates)

**Free Tier**:
- ✅ Create account and profile
- ✅ Generate 1 resume version
- ✅ Apply to unlimited positions
- ❌ No resume updates after applying
- ❌ Basic resume template only

**Premium Tier ($9.99/month)**:
- ✅ All Free features
- ✅ Update resumes after applying (if company allows)
- ✅ Unlimited resume versions
- ✅ Position-specific resume optimization
- ✅ Premium resume templates
- ✅ Resume analytics ("Viewed 15 times")
- ✅ Priority support

**Pro Tier ($19.99/month)**:
- ✅ All Premium features
- ✅ AI resume optimization
- ✅ Cover letter generator
- ✅ Application tracking analytics
- ✅ Interview preparation resources

### B2B (Companies)

**Basic Tier (Free)**:
- ✅ Post unlimited positions
- ✅ Receive applications
- ✅ View structured data + PDF
- ✅ Download PDFs
- ✅ Basic Kanban board
- ❌ Max 3 active positions
- ❌ Limited filtering

**Professional Tier ($99/month)**:
- ✅ All Basic features
- ✅ Unlimited active positions
- ✅ Advanced filtering (skills, experience, education)
- ✅ Bulk PDF downloads
- ✅ Resume comparison tool
- ✅ Candidate scoring vs requirements
- ✅ Custom workflows
- ✅ Team collaboration (5 users)

**Enterprise Tier ($499/month)**:
- ✅ All Professional features
- ✅ API access to structured data
- ✅ Custom resume templates
- ✅ White-label career page
- ✅ Analytics dashboard
- ✅ ATS integrations
- ✅ Unlimited users
- ✅ Dedicated support

---

## Implementation Checklist

### Phase 1: Core Functionality

- [ ] Update CompanyApplication entity with resume fields
- [ ] Update Position entity with update policy fields
- [ ] Create ResumeVersion value object
- [ ] Update apply endpoint to generate and store PDF
- [ ] Add resume versioning to storage service
- [ ] Create update resume endpoint
- [ ] Add version history to application detail view
- [ ] Add update deadline validation
- [ ] Create "Download PDF" button in company view

### Phase 2: UX Enhancements

- [ ] Build resume selection UI in application form
- [ ] Add resume preview modal
- [ ] Show update notification to companies
- [ ] Build version history dropdown
- [ ] Add changelog input for updates
- [ ] Show update deadline countdown to candidates
- [ ] Add "Update Resume" button in candidate dashboard

### Phase 3: Monetization

- [ ] Create subscription tiers
- [ ] Add "Premium" badge for update feature
- [ ] Implement update limits based on tier
- [ ] Add paywall for premium templates
- [ ] Build analytics dashboard for candidates
- [ ] Implement company tier restrictions

---

## Technical Considerations

### Performance

- ✅ **Lazy load PDFs**: Only generate when requested, not automatically
- ✅ **Cache generated PDFs**: Store in S3, don't regenerate on each view
- ✅ **Async generation**: Generate PDFs in background job
- ✅ **CDN delivery**: Use CloudFront for PDF downloads

### Storage Costs

- **Estimated cost**: $0.023 per GB/month (S3 Standard)
- **Average resume PDF**: ~500KB
- **1000 applications**: ~500MB = $0.01/month
- **10,000 applications**: ~5GB = $0.12/month
- **Negligible cost at scale**

### Data Consistency

- ✅ **Structured data is source of truth**: PDF is generated from DB records
- ✅ **PDF is snapshot**: Reflects data at generation time
- ✅ **Version history**: Track all changes with timestamps
- ✅ **Atomic updates**: Update DB + S3 in single transaction

### Privacy & Compliance

- ✅ **Candidate controls sharing**: Explicit opt-in for each data type
- ✅ **Immutable audit trail**: All versions stored, never deleted
- ✅ **GDPR compliance**: Candidate can request data deletion (archives application)
- ✅ **Access control**: Only assigned company users can view

---

## Future Enhancements

### V2 Features

- **AI Resume Scoring**: Auto-score against position requirements
- **Resume A/B Testing**: Test different versions with different companies
- **Smart Suggestions**: AI-powered resume improvement tips
- **Video Resumes**: Upload video introduction
- **Portfolio Integration**: Link to GitHub, Behance, etc.
- **Skills Verification**: Badge system for verified skills

### V3 Features

- **Blockchain Verification**: Tamper-proof resume history
- **Resume Analytics**: Heat maps showing which sections get most attention
- **Multi-language Resumes**: Auto-translate for international positions
- **ATS Integration**: Export to Greenhouse, Lever, etc.
- **Resume Templates Marketplace**: Community-created templates

---

## Summary

The **hybrid approach** (structured data + PDF) provides:

✅ **Best UX**: Companies can search/filter structured data
✅ **Portability**: PDFs for offline review and legal compliance
✅ **Flexibility**: Companies control update policy per position
✅ **Monetization**: Multiple tier opportunities on both sides
✅ **Platform Lock-in**: Structured data only accessible through platform
✅ **Data Moat**: Rich structured data enables future AI features

This strategy balances user needs, business goals, and technical feasibility.
