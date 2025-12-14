# Job Application Flow - Analysis

## Document Summary

This document describes the user flow for job applications in CareerPython. It covers the application form, user registration process (for both new and existing users), the multi-step application wizard, and the thank you page.

---

## Strengths

### 1. Simple Initial Form
- Minimal friction for first contact (email + PDF only)
- Good UX decision to defer data collection until after email verification

### 2. Asynchronous PDF Processing
- Smart approach: process PDF while user waits for email
- Uses AI extraction to pre-populate candidate data
- Reduces manual data entry for candidates

### 3. Handles Both User Types
- Clear distinction between new and existing users
- Existing users don't lose their current data until they confirm

### 4. Complete Application Wizard
- Covers all relevant candidate information
- Logical progression from general to specific

---

## Areas Requiring Clarification

### 1. Application Section (Line 3-8)
- **Typo**: "Conpany" should be "Company"
- **Missing**: GDPR/privacy consent checkbox requirement

### 2. New User Flow (Lines 10-16)
- **Line 11**: What is `user_registration` table? Need entity definition
- **Line 12**: What's the email subject/content? Link expiration time?
- **Line 13**:
  - "separata table" appears to be a typo for "separate table"
  - What happens if PDF processing fails?
  - What's the timeout for AI extraction?
- **Line 14-15**: What fields are required for user account creation?

### 3. Existing User Flow (Lines 18-24)
- **Line 19**: "user_registration" linked to existing user - need to clarify relationship
- **Line 22**: "If candidate profile is outdated" - what defines "outdated"?

**Resolved**: For conflicts between existing data and PDF extracted data → if profile already has info, we won't override it (keep existing data).

### 4. Application Wizard (Lines 26-33)
**Resolved**:
- All steps are optional (except Submit)
- Users can save progress and continue later
- Pre-filled data from PDF is editable

**Killer Questions** (already implemented in `JobPosition` entity):

Stored in `job_positions.killer_questions` as JSON array. Each question has:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Question text |
| `description` | string | No | Additional context |
| `data_type` | string | Yes | Type of answer expected |
| `scoring_values` | array | No | List of `{label, scoring}` for scoring options |
| `is_killer` | boolean | No | If true, wrong answer can disqualify candidate |

Source: `src/company_bc/job_position/domain/entities/job_position.py:98-100`

**Resolved**: No validation rules for wizard sections.

### 5. Thank You Page (Lines 35-40)
- **Line 38**: "send email with link to set password" - is this separate from the verification email?
- **Line 39**: "link to application info" - where does this link lead?

**Resolved**: After password is set, user can log in with password. Nothing more.

---

## Technical Considerations

### Database Entities

| Entity | Status | Purpose |
|--------|--------|---------|
| `candidate_applications` | **EXISTS** | Links candidate to job position with workflow stage tracking |
| `application_question_answers` | **EXISTS** | Stores answers to specific questions |
| `user_assets` | **EXISTS** | Stores PDFs and extracted data (requires `user_id`) |
| `user_registration` | **NEEDED** | Temporary storage before email verification |

### The `user_assets` Problem

The existing `user_assets` table handles PDF storage and AI extraction perfectly:
- `asset_type`: Supports `PDF_RESUME`
- `processing_status`: `PENDING` → `COMPLETED` / `FAILED`
- `text_content`: Raw extracted text
- `content`: JSON with structured data
- Built-in extraction for: name, phone, LinkedIn

**However**, `user_assets` requires a `user_id`, but in the application flow the user doesn't exist yet (only email is provided).

### Proposed Solution: `user_registration` Table

This table handles user registration independently from job applications. This allows future scenarios where users register without applying to a specific position.

```
user_registration
├── id (PK)
├── email
├── verification_token
├── token_expires_at
├── status: PENDING | VERIFIED | EXPIRED
├── company_id (FK, nullable)
├── job_position_id (FK, nullable)
├── file_name, file_size, content_type
├── text_content (extracted PDF text)
├── extracted_data (JSON - AI processed)
├── processing_status: PENDING | PROCESSING | COMPLETED | FAILED
├── existing_user_id (nullable - if email matches existing user)
├── created_at, updated_at
```

**Registration Scenarios:**

| Scenario | company_id | job_position_id |
|----------|------------|-----------------|
| Apply to specific job position | ✓ (inferred) | ✓ |
| Register with company (no specific job) | ✓ | null |
| General registration (future) | null | null |

**Flow:**
```
                    user_registration
                    (email + PDF + token)
                           ↓
                  [async PDF processing]
                           ↓
                    email verification
                           ↓
                    User + Candidate
                           ↓
            ┌──────────────┴──────────────┐
            ↓                             ↓
    Has job_position_id            No job_position_id
            ↓                             ↓
    candidate_application              (done)
    (link to job)
```

1. User submits email + PDF → Create `user_registration`
2. Background job extracts PDF → Updates `text_content` and `extracted_data`
3. User clicks verification link →
   - If new user: Create User, Candidate, copy data to `user_assets`
   - If existing user: Link to existing, optionally update profile
4. If `job_position_id` exists → Create `candidate_application` linking candidate to job position

### API Endpoints Required

1. `POST /api/applications` - Submit initial application (email + PDF)
2. `GET /api/applications/verify/{token}` - Verify email and create/update user
3. `GET /api/applications/{id}` - Get application details
4. `PUT /api/applications/{id}` - Update application data (wizard steps)
5. `POST /api/applications/{id}/submit` - Final submission

### Background Jobs

1. **PDF Processing Job**: Extract text from PDF
2. **AI Extraction Job**: Parse extracted text to structured data
3. **Email Sending Jobs**: Multiple email types (verification, confirmation, password reset)

### Security Considerations

- Rate limiting on application submission (prevent spam)
- Token expiration for verification links
- Secure PDF handling (malware scanning?)
- GDPR compliance: consent tracking, data retention policy

---

## Missing Information

1. **Business Rules**
   - How long is the verification link valid?
   - What happens if user never verifies?
   - Can a user apply to the same position twice?
   - What triggers "outdated profile" detection?

2. **UI/UX Details**
   - Progress indicator in wizard?
   - Mobile responsiveness requirements?
   - Accessibility requirements?

3. **Integration Points**
   - Which AI service for PDF extraction?
   - Email service provider?
   - How does this integrate with existing candidate workflow?

4. **Error Handling**
   - PDF upload fails
   - AI extraction fails
   - Email delivery fails
   - User abandons mid-wizard

---

## Recommendations

### Priority 1 - Clarify Before Implementation

1. Define `user_registration` entity with all fields
2. Specify email link expiration policy
3. Define "outdated profile" criteria
4. Document Killer Questions feature (or link to existing docs)
5. Add GDPR consent requirement to initial form

### Priority 2 - Add to Specification

1. Error handling for each step
2. Validation rules for wizard steps
3. Save/resume functionality for wizard
4. Data conflict resolution strategy

### Priority 3 - Technical Design

1. Design background job architecture for PDF processing
2. Define AI extraction output schema
3. Plan email templates
4. Design token generation and validation

---

## Suggested Next Steps

1. **Fix typos** in the document
2. **Create entity diagram** for `user_registration` and related tables
3. **Define API contracts** with request/response schemas
4. **Create wireframes** for each screen
5. **Write acceptance criteria** for each user story
