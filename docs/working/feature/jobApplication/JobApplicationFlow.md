# Job Application Flow

## Application Form
Application form focused only on this:
* email
* attach pdf
* GDPR+privacy checkbox
* submit

Must display Company name, logo, and job position name.

## user_registration Table

Stores registration data before email verification. Supports multiple registration scenarios.

| Field | Type | Description |
|-------|------|-------------|
| id | PK | Unique identifier |
| email | String | User email |
| verification_token | String | Token for email verification |
| token_expires_at | DateTime | Token expiration |
| status | Enum | PENDING, VERIFIED, EXPIRED |
| company_id | FK (nullable) | Company reference |
| job_position_id | FK (nullable) | Job position reference |
| file_name | String | PDF filename |
| file_size | Integer | PDF size |
| content_type | String | MIME type |
| text_content | Text | Extracted PDF text |
| extracted_data | JSON | AI-processed structured data |
| processing_status | Enum | PENDING, PROCESSING, COMPLETED, FAILED |
| existing_user_id | FK (nullable) | Link to existing user if email matches |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

**Registration Scenarios:**
| Scenario | company_id | job_position_id |
|----------|------------|-----------------|
| Apply to specific job position | ✓ (inferred) | ✓ |
| Register with company (no specific job) | ✓ | null |
| General registration (future) | null | null |

## New User Flow
1. Creates a `user_registration` entry with status `PENDING`
2. Send email with verification link
3. While user opens email, process PDF asynchronously:
   - Extract text from PDF
   - Use AI to extract structured content
   - Store in `user_registration.text_content` and `user_registration.extracted_data`
4. User clicks link → Creates user account with status `active`
5. Creates Candidate linked to user
6. Copies PDF data to `user_assets` table
7. If `job_position_id` exists → Creates `candidate_application`

## Existing User Flow
The user may be legitimately applying again. We cannot override the PDF or information until the user clicks the email.

1. Creates `user_registration` entry, linked to existing user via `existing_user_id`
2. Send email with verification link
3. While user opens email, process PDF asynchronously (same as new user)
4. User clicks link
5. **Data conflict resolution**: If candidate profile already has data, keep existing data (don't override with PDF)
6. Only add new information to empty fields
7. If `job_position_id` exists → Creates `candidate_application`

## Application Wizard
All steps are optional (except Submit). Users can save progress and continue later.
Pre-filled data from PDF is editable.

1. General Data
2. Experience
3. Education
4. Projects
5. Skills
6. Questions (includes all position-specific questions)
7. Submit

## Thank You Page
1. Display thank you message
2. Send email confirmation with details
3. If the user is new, send email with link to set password
4. If the user is existing, send email with link to application info

