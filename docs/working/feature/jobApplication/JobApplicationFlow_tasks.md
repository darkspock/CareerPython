# Job Application Flow - Implementation Tasks

## Current State Analysis

### Already Implemented

| Component | Status | Location |
|-----------|--------|----------|
| **Candidate Entity** | DONE | `src/candidate_bc/candidate/domain/entities/candidate.py` |
| **Candidate Education** | DONE | `src/candidate_bc/candidate/domain/entities/candidate_education.py` |
| **Candidate Experience** | DONE | `src/candidate_bc/candidate/domain/entities/candidate_experience.py` |
| **Candidate Projects** | DONE | `src/candidate_bc/candidate/domain/entities/candidate_project.py` |
| **User Entity** | DONE | `src/auth_bc/user/domain/entities/user.py` |
| **UserAsset (PDF storage)** | DONE | `src/auth_bc/user/domain/entities/user_asset.py` |
| **PDF Text Extraction** | DONE | `src/auth_bc/user/infrastructure/services/pdf_processing_service.py` |
| **AI Resume Analysis** | DONE | `src/framework/infrastructure/services/ai/` |
| **CandidateApplication Entity** | DONE | `src/company_bc/candidate_application/domain/entities/candidate_application.py` |
| **CreateCandidateApplication** | DONE | `src/company_bc/candidate_application/application/commands/create_candidate_application.py` |
| **CreateUserFromLanding** | DONE | `src/auth_bc/user/application/commands/create_user_from_landing.py` |
| **PopulateCandidateFromPDF** | DONE | `src/candidate_bc/candidate/application/commands/populate_candidate_from_pdf_analysis.py` |
| **OnboardingController** | DONE | `adapters/http/candidate_app/controllers/onboarding_controller.py` |
| **Password Reset Email** | DONE | Sent in CreateUserFromLandingCommandHandler |
| **Killer Questions (model)** | DONE | `job_positions.killer_questions` JSON field |
| **Application Question Answers** | DONE | `src/company_bc/candidate_application/application/commands/question_answer/` |

### Current Flow (What Exists)

```
Landing Page → email + PDF → CreateUserFromLanding
    ↓
Creates User immediately (no verification)
    ↓
Creates Candidate
    ↓
Processes PDF → AI extraction → Populates candidate
    ↓
Creates CandidateApplication (if job_position_id)
    ↓
Sends password reset email
    ↓
Returns JWT token + redirect to /candidate/onboarding/complete-profile
```

### Required Flow (JobApplicationFlow.md)

```
Landing Page → email + PDF + GDPR checkbox
    ↓
Creates user_registration (PENDING status)
    ↓
Sends verification email with link
    ↓
[Background] Processes PDF → AI extraction → stores in user_registration
    ↓
User clicks verification link
    ↓
Creates User + Candidate (or links to existing)
    ↓
Copies data to user_assets
    ↓
Creates CandidateApplication (if job_position_id)
    ↓
Redirects to Application Wizard
    ↓
Application Wizard (8 steps, all optional)
    ↓
Thank you page + confirmation email
```

---

## Implementation Tasks

### Phase 1: Database - user_registration Table ✅ COMPLETED

#### Task 1.1: Create user_registration Entity ✅
- [x] Create `src/auth_bc/user_registration/domain/entities/user_registration.py`
- [x] Fields:
  - id (PK)
  - email
  - verification_token
  - token_expires_at
  - status (PENDING, VERIFIED, EXPIRED)
  - company_id (nullable)
  - job_position_id (nullable)
  - file_name, file_size, content_type
  - text_content
  - extracted_data (JSON)
  - processing_status (PENDING, PROCESSING, COMPLETED, FAILED)
  - existing_user_id (nullable)
  - created_at, updated_at
- [x] Create factory method `create()`
- [x] Create status transition methods (`verify()`, `expire()`, `set_processing_status()`, `set_extracted_content()`)

#### Task 1.2: Create user_registration Model ✅
- [x] Create `src/auth_bc/user_registration/infrastructure/models/user_registration_model.py`
- [x] SQLAlchemy model with all fields
- [x] Indexes on email, verification_token, status, processing_status, company_id, job_position_id, existing_user_id

#### Task 1.3: Create user_registration Repository ✅
- [x] Create `src/auth_bc/user_registration/domain/repositories/user_registration_repository_interface.py`
- [x] Create `src/auth_bc/user_registration/infrastructure/repositories/user_registration_repository.py`
- [x] Methods:
  - save()
  - get_by_id()
  - get_by_email()
  - get_by_verification_token()
  - get_by_email_and_job_position()
  - update()
  - delete() (replaces delete_expired)
  - find_expired_registrations()

#### Task 1.4: Create Alembic Migration ✅
- [x] Migration created: `alembic/versions/8c6c3906e50c_add_user_registrations_table.py`
- [x] Table `user_registrations` created
- [x] All indexes created

#### Task 1.5: Register in DI Container ✅
- [x] Added `UserRegistrationRepository` to `core/containers/auth_container.py`

**Files created:**
- `src/auth_bc/user_registration/domain/value_objects/user_registration_id.py`
- `src/auth_bc/user_registration/domain/enums/registration_status.py`
- `src/auth_bc/user_registration/domain/entities/user_registration.py`
- `src/auth_bc/user_registration/domain/repositories/user_registration_repository_interface.py`
- `src/auth_bc/user_registration/infrastructure/models/user_registration_model.py`
- `src/auth_bc/user_registration/infrastructure/repositories/user_registration_repository.py`
- `alembic/versions/8c6c3906e50c_add_user_registrations_table.py`

---

### Phase 2: Registration Flow Commands ✅ COMPLETED

#### Task 2.1: Create InitiateRegistrationCommand ✅
- [x] Create `src/auth_bc/user_registration/application/commands/initiate_registration_command.py`
- [x] Input: email, pdf_file, pdf_filename, job_position_id, company_id
- [x] Logic:
  1. Check if existing user_registration for same email+job_position
  2. Create user_registration with PENDING status
  3. Generate verification_token (secure random)
  4. Set token_expires_at (24 hours)
  5. Check if email belongs to existing user → set existing_user_id
  6. Save user_registration
  7. Dispatch SendVerificationEmailCommand
  8. Dispatch ProcessRegistrationPdfCommand (async)

#### Task 2.2: Create ProcessRegistrationPdfCommand ✅
- [x] Create `src/auth_bc/user_registration/application/commands/process_registration_pdf_command.py`
- [x] Input: registration_id, pdf_bytes
- [x] Logic:
  1. Get user_registration
  2. Update status to PROCESSING
  3. Extract text from PDF using PDFProcessingService
  4. Run AI analysis using AIServiceInterface
  5. Update user_registration with text_content and extracted_data
  6. Update processing_status to COMPLETED

#### Task 2.3: Create VerifyRegistrationCommand ✅
- [x] Create `src/auth_bc/user_registration/application/commands/verify_registration_command.py`
- [x] Input: verification_token
- [x] Output: user_id, candidate_id, is_new_user, has_job_application
- [x] Logic:
  1. Get user_registration by token
  2. Check if expired
  3. If existing_user_id → link to existing user
  4. If new user → create User + Candidate
  5. Copy extracted_data to candidate profile
  6. Copy PDF to user_assets
  7. If job_position_id → create CandidateApplication
  8. Update user_registration status to VERIFIED
  9. Send password setup email for new users

**Files created:**
- `src/auth_bc/user_registration/application/commands/initiate_registration_command.py`
- `src/auth_bc/user_registration/application/commands/process_registration_pdf_command.py`
- `src/auth_bc/user_registration/application/commands/send_verification_email_command.py`
- `src/auth_bc/user_registration/application/commands/verify_registration_command.py`

**Handlers registered in:**
- `core/containers/auth_container.py`
- `core/containers/main_container.py`

---

### Phase 3: Email Verification ✅ COMPLETED

#### Task 3.1: Create SendVerificationEmailCommand ✅
- [x] Create `src/auth_bc/user_registration/application/commands/send_verification_email_command.py`
- [x] Input: registration_id
- [x] Logic:
  1. Get user_registration
  2. Build verification URL with token
  3. Dispatch SendEmailCommand with verification template

#### Task 3.2: Create Verification Email Template
- [ ] Create verification email template in notification_bc (pending - using existing template)
- [ ] Include: company name, job position name (if applicable), verification link
- [ ] Expiration notice

**Note**: SendVerificationEmailCommand uses the existing email infrastructure. A custom email template can be added later.

---

### Phase 4: API Endpoints ✅ COMPLETED

#### Task 4.1: Create Registration Controller ✅
- [x] Created `adapters/http/candidate_app/controllers/registration_controller.py`
- [x] `initiate_registration()` - handles new registration flow with GDPR validation
- [x] `verify_registration()` - verifies token and creates user/candidate
- [x] `get_registration_status()` - returns registration status and preview data

#### Task 4.2: Create Registration Router ✅
- [x] Created `adapters/http/candidate_app/routers/registration_router.py`
- [x] `POST /candidate/registration` - Initiate registration with email verification
- [x] `GET /candidate/registration/verify/{token}` - Verify registration
- [x] `GET /candidate/registration/{registration_id}/status` - Get registration status

#### Task 4.3: Register in DI Container ✅
- [x] Added `RegistrationController` to `core/containers/auth_container.py`
- [x] Exposed `registration_controller` in `core/containers/main_container.py`
- [x] Added router to `main.py` and wiring configuration

**Files created:**
- `adapters/http/candidate_app/controllers/registration_controller.py`
- `adapters/http/candidate_app/routers/registration_router.py`

**Note**: The old landing endpoint (`/candidate/onboarding/landing`) still exists for backward compatibility. The new registration flow uses `/candidate/registration`.

---

### Phase 5: Application Wizard Backend ✅ COMPLETED

#### Task 5.1: Review Existing Candidate Endpoints ✅
- [x] Verified endpoints exist in `adapters/http/candidate_app/routers/candidate_router.py`:
  - `PUT /candidate/profile` - Update candidate basic info
  - `POST/PUT/DELETE /candidate/education/{id}` - Education CRUD
  - `POST/PUT/DELETE /candidate/experience/{id}` - Experience CRUD
  - `POST/PUT/DELETE /candidate/projects/{id}` - Projects CRUD
  - Bulk operations also available: `/candidate/experience/bulk`

#### Task 5.2: Application Questions Endpoints ✅
- [x] Verified `application_question_answers` endpoints exist:
  - `GET /api/applications/{application_id}/answers` - List answers
  - `POST /api/applications/{application_id}/answers` - Save answers
  - `GET /api/public/positions/{position_id}/questions` - Get enabled questions (public)
- [x] Located in `adapters/http/candidate_app/application_answers/routers/application_answer_router.py`

#### Task 5.3: Killer Questions Integration ✅
- [x] Killer questions already exist in `JobPosition.killer_questions` JSON field
- [x] Added `killer_questions` to `JobPositionPublicResponse` schema
- [x] Added `killer_questions` to `PublicPositionResponse` schema
- [x] Updated `JobPositionMapper.dto_to_public_response()` to include killer_questions
- [x] Killer questions are now returned in `GET /public/positions/{slug_or_id}` endpoint
- [ ] TODO: Add killer question evaluation logic (disqualify if wrong answer) - can be done in Phase 7

**Note**: Killer questions are returned as part of the public position response. The evaluation logic for disqualifying candidates can be added later as an enhancement.

---

### Phase 6: Frontend (Candidate App) ✅ COMPLETED

#### Task 6.1: Update Landing Page Form ✅
- [x] Add GDPR checkbox using shadcn Checkbox component
- [x] Update submit to call new `api.initiateRegistration()` endpoint
- [x] Show "check your email" message on success (inline success state)
- [x] Different flow for job applications vs general CV landing
- [x] Form validation requires GDPR consent for job applications

**Files modified:**
- `client-vite/src/pages/LandingPage.tsx` - Added GDPR checkbox, new registration flow
- `client-vite/src/lib/api.ts` - Added `initiateRegistration`, `verifyRegistration`, `getRegistrationStatus` methods

#### Task 6.2: Create Verification Page ✅
- [x] Page at `/candidate/registration/verify/:token`
- [x] Call verification endpoint on mount
- [x] Show loading, success, error, and expired states
- [x] Auto-redirect to wizard or profile after 3 seconds
- [x] Store access_token and candidate_id on success

**Files created:**
- `client-vite/src/pages/VerifyRegistrationPage.tsx`
- Route added in `client-vite/src/App.tsx`

#### Task 6.3: Create Application Wizard ✅
- [x] Create wizard component with 8 steps
- [x] Step 1: General Data (uses ProfileBasicInfoForm)
- [x] Step 2: Experience (uses ProfileExperienceForm)
- [x] Step 3: Education (uses ProfileEducationForm)
- [x] Step 4: Projects (uses ProfileProjectsForm)
- [x] Step 5: Skills (placeholder - can edit from full profile)
- [x] Step 6: Specific Application Questions (placeholder)
- [x] Step 7: Killer Questions (placeholder)
- [x] Step 8: Submit (review and send)
- [x] All steps optional with skip functionality
- [x] Step indicator with navigation

**Files created:**
- `client-vite/src/pages/ApplicationWizardPage.tsx`
- Route `/candidate/application/wizard` added in `client-vite/src/App.tsx`

#### Task 6.4: Create Thank You Page ✅
- [x] Display thank you message with success icon
- [x] Show "what's next" steps
- [x] For new users: prompt to set password (yellow notice)
- [x] Links to profile and home

**Files created:**
- `client-vite/src/pages/ApplicationThankYouPage.tsx`
- Route `/candidate/application/thank-you` added in `client-vite/src/App.tsx`

---

### Phase 7: Cleanup & Migration ✅ COMPLETED

#### Task 7.1: Deprecate Old Flow ✅
- [x] Mark CreateUserFromLandingCommand as deprecated (docstrings + runtime warnings)
- [x] Update OnboardingController.process_landing() with deprecation warnings
- [x] Mark `/candidate/onboarding/landing` endpoint as deprecated in OpenAPI
- [x] Keep old endpoints functional for backward compatibility during transition

**Files modified:**
- `src/auth_bc/user/application/commands/create_user_from_landing.py` - Added deprecation docstrings and warnings
- `adapters/http/candidate_app/controllers/onboarding_controller.py` - Added deprecation warnings
- `adapters/http/candidate_app/routers/landing_router.py` - Added `deprecated=True` to endpoint

#### Task 7.2: Background Job for Expired Registrations ✅
- [x] Create `CleanupExpiredRegistrationsCommand` to delete old registrations
- [x] Register handler in DI container
- [x] Create admin endpoint `POST /admin/maintenance/cleanup-expired-registrations`
- [x] Supports `max_age_days` and `dry_run` parameters

**Files created:**
- `src/auth_bc/user_registration/application/commands/cleanup_expired_registrations_command.py`

**Files modified:**
- `core/containers/auth_container.py` - Registered cleanup handler
- `core/containers/main_container.py` - Exposed cleanup handler
- `adapters/http/admin_app/routes/admin_router.py` - Added maintenance endpoint

**Note:** The cleanup can be triggered via:
1. Manual API call: `POST /admin/maintenance/cleanup-expired-registrations`
2. External cron/scheduler calling the endpoint daily

---

## Implementation Order

1. **Phase 1** (Database) - Required first
2. **Phase 2** (Commands) - Core logic
3. **Phase 3** (Email) - Verification flow
4. **Phase 4** (API) - Backend endpoints
5. **Phase 5** (Wizard Backend) - Mostly done, verify/enhance
6. **Phase 6** (Frontend) - UI implementation
7. **Phase 7** (Cleanup) - After testing

---

## Notes

- Current OnboardingController has a working PDF analysis flow that can be reused
- Most candidate CRUD operations already exist
- Killer questions model exists but needs answer collection endpoint
- The main change is introducing email verification before user creation
