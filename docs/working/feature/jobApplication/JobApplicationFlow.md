# Job Application Flow

## Full or short application
In the job application creating, the company may require that the user fills normalized application 
(experience, education, etc.. ) So, should display the sections that are required for applying.
Add something awesome in UX, require CV in pdf, require candidate to fill info with a drown down or what ever.



## Application Form
Application form focused will be different depending on the job application configuration.

The system can help the candidate to build a CV.

* email
* Attach PDF or "Help me on creating a CV"
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
2. Experience,EducationProjects,Skills (displayed when user click on help me creating a cv or when activated in job position)
3. Questions (includes all position-specific questions)
4. Submit

## Sending the info to the company
If the user clicked on "help me with the cv". Will go to the CV generation section.
The application will stay on pending and visible a top in a badged or whateever, so the candidate can remember is still pending.
When the CV is generated, the candidate can click on send application (on the pending one).

## Info passed to the company
All the info is passed in a markdown (EVERYTHING), and also writen in the job application column or custom column 
if exists.
That way, the company see a snapshot of the user information at that time.
In the user changes contact information, this information will be updated for the company. Live data, no historical.
The CV is attached, the generated or the orginal one.


## Thank You Page
1. Display thank you message
2. Send email confirmation with details
3. If the user is new, send email with link to set password
4. If the user is existing, send email with link to application info

