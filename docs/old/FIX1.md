## Backend
Tenemos 2 grupos de endpoint
* candidate
* admin
no existen mas grupos de endpoint, no deben exister mas.

Dentro de candidate tenemos todo lo relacionado con el candidato.
* auth
* Profile (datos basicos) del candidate
* Experience
* Education
* Projects
* Resume
* Application

Dentro de admin:
* candidates
* interview
* interview template
* companies
* open positions
* auth

## Frontend
Todos los endpoints usan jwt
Las pantallas se agrupan en:
* Candidate
  * onboarding
  * profile
  * experience
  * education
  * projects
  * resume
  * application
  * interview
  * open positions
  * login
* Admin
  * login
  * candidates
     * resumes
     * interview
  * interview template
  * companies
    * applications
    * open positions


Las pantallas de candidate y onboarding deben compartir los mismo endpoints.