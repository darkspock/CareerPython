# Company Module - Roadmap de Implementación

**Fecha**: 2025-01-22
**Versión**: 2.0 (Updated with Resume Versioning)

## 📚 Documentación Relacionada

- **[RESUME_SHARING_STRATEGY.md](../old/RESUME_SHARING_STRATEGY.md)** - Estrategia híbrida de compartir resumes (structured data + PDF)
- **[WORKFLOW_SYSTEM_ARCHITECTURE.md](../WORKFLOW_SYSTEM_ARCHITECTURE.md)** - Sistema de workflows y permisos
- **[STORAGE_USAGE.md](../old/STORAGE_USAGE.md)** - Guía de uso del servicio de almacenamiento
- **[COMPANY_NEW_PARADIGM.md](COMPANY_NEW_PARADIGM.md)** - Paradigma de privacidad y modelo CRM

## 🎯 Estrategia de Implementación

### Decisión: ATS Primero, Head Hunting Después

**Razón**:
- El ATS (gestión de candidatos y candidaturas) es el core product
- Head Hunting es un add-on premium que puede esperar
- Queremos validar el producto base antes de agregar features avanzadas

### Decisión: Hybrid Resume Approach (Structured Data + PDF)

**Razón**:
- Companies can search/filter structured data (better ATS experience)
- PDF snapshots for legal/compliance requirements
- Version history when candidates update resumes
- Monetization opportunities for both B2C and B2B

---

## 📋 Fases de Desarrollo

### ✅ Fase 0: Documentación, Storage Abstraction & Resume Strategy (COMPLETADA)

- [x] Modelo de datos completo (3 niveles)
- [x] Flujos de negocio
- [x] Estrategia de productos
- [x] Especificación de Head Hunting (para futuro)
- [x] Storage abstraction implementation (Local + S3)
- [x] Storage configuration in environment
- [x] Storage service registered in DI container
- [x] Documentation: STORAGE_USAGE.md
- [x] **Resume Sharing Strategy - Hybrid Approach**
- [x] **Documentation: RESUME_SHARING_STRATEGY.md**
- [x] **Application flow with resume selection**
- [x] **Resume versioning design**

---

### 🎯 Fase 1: ATS Core - CompanyCandidate (PRIORIDAD ALTA)

**Objetivo**: Gestión básica de candidatos en el sistema

#### Backend

**1.1. CompanyCandidate Entity (actualizar existente)**
- [ ] Revisar entity existente en `src/company/domain/entities/company_candidate.py`
- [ ] Añadir campos faltantes:
  - `lead_id` (nullable, para futura integración con Head Hunting)
  - `source` enum con valores: `direct_application`, `referral`, `manual_entry`, `lead_conversion`
  - `resume_url` (S3 path)
  - `resume_uploaded_by` enum: `company`, `candidate`
  - `resume_uploaded_at`
- [ ] Factory methods: `create_manual()`, `create_from_application()`
- [ ] Métodos de negocio: `update_basic_info()`, `upload_resume()`, `archive()`

**1.2. CompanyCandidate Commands**
- [ ] `CreateCompanyCandidateCommand` (para crear manualmente)
- [ ] `UpdateCompanyCandidateCommand`
- [ ] `UploadCandidateResumeCommand` (con S3)
- [ ] `ArchiveCompanyCandidateCommand`
- [ ] Handlers para cada comando
- [ ] Registrar en container

**1.3. CompanyCandidate Queries**
- [ ] `GetCompanyCandidateByIdQuery`
- [ ] `ListCompanyCandidatesByCompanyQuery` (con filtros)
- [ ] `GetCompanyCandidateByEmailQuery` (para verificar duplicados)
- [ ] Handlers para cada query
- [ ] DTOs completos
- [ ] Registrar en container

**1.4. CompanyCandidate API**
- [ ] Controller con métodos CRUD
- [ ] Router con endpoints:
  - `POST /api/company/{company_id}/candidates`
  - `GET /api/company/{company_id}/candidates`
  - `GET /api/company/candidates/{candidate_id}`
  - `PUT /api/company/candidates/{candidate_id}`
  - `DELETE /api/company/candidates/{candidate_id}` (soft delete)
  - `POST /api/company/candidates/{candidate_id}/upload-resume`
- [ ] Schemas de request/response
- [ ] Mapper
- [ ] Registrar router en main.py

**1.5. Migration**
- [ ] Actualizar tabla `company_candidates` con nuevos campos
- [ ] Ejecutar migration

**Estimación Fase 1**: 3-4 días

---

### 🎯 Fase 1.5: Workflow Enhancements (PRIORIDAD ALTA)

**Objetivo**: Extender el sistema de workflows para soportar asignación de usuarios por stage y por position

#### Backend

**1.5.1. Add workflow_id to Position**
- [ ] Add `workflow_id: Optional[CompanyWorkflowId]` to Position entity
- [ ] Add `default_workflow_id` to Company entity (company-wide default)
- [ ] Update Position.create() factory to accept workflow_id
- [ ] Update Position.update_details() to allow changing workflow
- [ ] Migration to add workflow_id to positions table

**1.5.2. Create PositionStageAssignment Entity (NEW)**
- [ ] Create entity in `src/position_stage_assignment/domain/entities/position_stage_assignment.py`
- [ ] Fields:
  - `id: PositionStageAssignmentId`
  - `position_id: JobPositionId`
  - `stage_id: WorkflowStageId`
  - `assigned_user_ids: List[CompanyUserId]`
  - `created_at: datetime`
  - `updated_at: datetime`
- [ ] Factory: `create(position_id, stage_id, assigned_user_ids)`
- [ ] Methods: `add_user()`, `remove_user()`, `update_users()`
- [ ] Value objects: PositionStageAssignmentId

**1.5.3. PositionStageAssignment Module (estructura completa)**
```
src/position_stage_assignment/
  application/
    commands/
      assign_users_to_stage_command.py
      add_user_to_stage_command.py
      remove_user_from_stage_command.py
    queries/
      get_assignments_by_position_query.py
      get_assigned_users_for_stage_query.py
      check_user_can_process_stage_query.py
    dtos/
      position_stage_assignment_dto.py
  domain/
    entities/
      position_stage_assignment.py
    infrastructure/
      position_stage_assignment_repository_interface.py
  infrastructure/
    models/
      position_stage_assignment_model.py
    repositories/
      position_stage_assignment_repository.py
  presentation/
    controllers/
      position_stage_assignment_controller.py
    schemas/
      position_stage_assignment_request.py
      position_stage_assignment_response.py
    mappers/
      position_stage_assignment_mapper.py
```

**1.5.4. PositionStageAssignment API**
- [ ] Controller con métodos
- [ ] Router con endpoints:
  - `POST /api/positions/{position_id}/stage-assignments` - Assign users to stages (batch)
  - `GET /api/positions/{position_id}/stage-assignments` - Get all assignments
  - `PUT /api/positions/{position_id}/stages/{stage_id}/users` - Update assigned users
  - `POST /api/positions/{position_id}/stages/{stage_id}/users/{user_id}` - Add user
  - `DELETE /api/positions/{position_id}/stages/{stage_id}/users/{user_id}` - Remove user
  - `GET /api/positions/{position_id}/stages/{stage_id}/can-process` - Check if current user can process
- [ ] Schemas y mapper
- [ ] Registrar en container y main.py

**1.5.5. Update CompanyApplication Logic**
- [ ] Add validation: only assigned users can change stage
- [ ] Add method: `can_user_process_current_stage(user_id)` to entity
- [ ] Update ChangeStageCommand to check permissions
- [ ] Add proper error responses for unauthorized stage changes

**1.5.6. Migration**
- [ ] Add `workflow_id` to positions table
- [ ] Add `default_workflow_id` to companies table
- [ ] Create table `position_stage_assignments`
- [ ] Ejecutar migration

**1.5.7. Predefined Workflow Templates**
- [ ] Create seeder/migration with default workflows:
  - "Standard Hiring Process": Screening → HR Interview → Technical Interview → Final Interview → Offer → Hired
  - "Technical Hiring": HR Screen → Technical Test → Tech Interview → Team Lead Interview → CTO Meeting → Offer → Hired
  - "Quick Hiring": Interview → Offer → Hired
- [ ] Add command: `CreateDefaultWorkflowsCommand` (runs on company creation)

**Estimación Fase 1.5**: 3-4 días

---

### 🎯 Fase 2: Positions (Posiciones/Vacantes) (PRIORIDAD ALTA)

**Objetivo**: Gestión de posiciones abiertas

#### Backend

**2.1. Position Entity (UPDATE EXISTING)**
- [ ] Review existing entity in `src/job_position/domain/entities/job_position.py`
- [ ] Add workflow fields:
  - `workflow_id: Optional[CompanyWorkflowId]` - Workflow for applications to this position
- [ ] Add resume update policy fields:
  - `allow_resume_updates: bool` (default: False)
  - `resume_update_deadline_days: Optional[int]` (e.g., 7 days)
- [ ] Update factory method to accept new fields
- [ ] Update `update_details()` to allow changing workflow and resume policy

**2.2. Position Module (estructura completa)**
```
src/position/
  application/
    commands/
      create_position_command.py
      update_position_command.py
      publish_position_command.py
      pause_position_command.py
      close_position_command.py
      delete_position_command.py
    queries/
      get_position_by_id_query.py
      list_positions_by_company_query.py
      list_public_positions_query.py (para job board)
    dtos/
      position_dto.py
  domain/
    entities/
      position.py
    infrastructure/
      position_repository_interface.py
  infrastructure/
    models/
      position_model.py
    repositories/
      position_repository.py
  presentation/
    controllers/
      position_controller.py
    schemas/
      position_request.py
      position_response.py
    mappers/
      position_mapper.py
```

**2.3. Position API**
- [ ] Controller completo
- [ ] Router con endpoints:
  - `POST /api/company/{company_id}/positions`
  - `GET /api/company/{company_id}/positions`
  - `GET /api/positions/{position_id}`
  - `PUT /api/positions/{position_id}`
  - `DELETE /api/positions/{position_id}`
  - `POST /api/positions/{position_id}/publish`
  - `POST /api/positions/{position_id}/pause`
  - `POST /api/positions/{position_id}/close`
  - `GET /api/public/positions` (para job board público)
- [ ] Schemas y mapper
- [ ] Registrar en container y main.py

**2.4. Migration**
- [ ] Crear tabla `positions`
- [ ] Ejecutar migration

**Estimación Fase 2**: 2-3 días

---

### 🎯 Fase 3: CompanyApplication (Candidaturas Formales) (PRIORIDAD ALTA)

**Objetivo**: Gestión de candidaturas a posiciones específicas

#### Backend

**3.1. CompanyApplication Entity (NUEVA) - HYBRID RESUME APPROACH**
- [ ] Crear entity en `src/company_application/domain/entities/company_application.py`
- [ ] Campos según modelo:
  - `shared_data: SharedDataPermissions` (JSON) - What candidate authorized to share
  - **`resume_pdf_url: str`** - S3 path to generated PDF snapshot
  - **`resume_pdf_version: int`** - Current version (starts at 1)
  - **`resume_snapshot_at: datetime`** - When current PDF was generated
  - **`allow_resume_updates: bool`** - Copied from Position at application time
  - **`resume_update_deadline: Optional[datetime]`** - Deadline for resume updates
  - **`resume_last_updated_at: Optional[datetime]`** - Last update timestamp
  - **`resume_versions: List[ResumeVersion]`** - Version history
  - `status`, `workflow_id`, `current_stage_id`, etc.
- [ ] Value Object: `SharedDataPermissions` (include_education, include_experience, etc.)
- [ ] Value Object: `ResumeVersion` (version, pdf_url, created_at, changelog)
- [ ] Factory: `create_from_candidate_application()` - Generate PDF at creation
- [ ] Métodos:
  - `change_stage()`, `make_offer()`, `accept()`, `reject()`, `withdraw()`
  - **`update_resume(new_pdf_url, changelog)`** - Create new version
  - **`can_update_resume()`** - Check if updates allowed and within deadline
  - **`get_resume_version(version_number)`** - Get specific version

**3.2. CompanyApplication Module (estructura completa)**
```
src/company_application/
  application/
    commands/
      create_application_command.py  (includes PDF generation)
      change_application_stage_command.py
      update_application_resume_command.py  (NEW - candidate updates resume)
      make_offer_command.py
      accept_application_command.py
      reject_application_command.py
      withdraw_application_command.py
      archive_application_command.py
    queries/
      get_application_by_id_query.py  (includes resume versions)
      list_applications_by_position_query.py
      list_applications_by_candidate_query.py
      list_applications_by_company_query.py
      get_candidate_shared_data_query.py (para ver datos autorizados)
      get_resume_versions_query.py  (NEW - get version history)
      download_resume_version_query.py  (NEW - get specific version URL)
    dtos/
      application_dto.py  (includes resume_versions)
      shared_data_dto.py
      resume_version_dto.py  (NEW)
  domain/
    entities/
      company_application.py
    value_objects/
      shared_data_permissions.py  (what candidate authorized to share)
      resume_version.py  (version, pdf_url, created_at, changelog)
    infrastructure/
      application_repository_interface.py
  infrastructure/
    models/
      company_application_model.py
    repositories/
      application_repository.py
  presentation/
    controllers/
      application_controller.py
    schemas/
      application_request.py
      application_response.py
    mappers/
      application_mapper.py
```

**3.3. CompanyApplication API - WITH RESUME VERSIONING**
- [ ] Controller completo
- [ ] Router con endpoints:
  - `POST /api/positions/{position_id}/apply` (público - candidato aplica)
    - Accepts: shared_data, resume_choice (generate new or use existing)
    - Generates PDF and stores in S3
    - Returns: application_id, resume_version, pdf_url, update_deadline
  - `GET /api/company/{company_id}/applications`
  - `GET /api/positions/{position_id}/applications`
  - `GET /api/applications/{application_id}`
    - Returns: structured data + resume versions history
  - `PUT /api/applications/{application_id}`
  - `POST /api/applications/{application_id}/change-stage`
  - **`PUT /api/applications/{application_id}/resume`** (NEW - candidate updates resume)
    - Validates: deadline, permissions
    - Generates new PDF version
    - Returns: new version number, pdf_url, versions_history
  - **`GET /api/applications/{application_id}/resume/versions`** (NEW - get version history)
  - **`GET /api/applications/{application_id}/resume/versions/{version}`** (NEW - download specific version)
  - `POST /api/applications/{application_id}/make-offer`
  - `POST /api/applications/{application_id}/accept` (candidato)
  - `POST /api/applications/{application_id}/reject` (empresa)
  - `POST /api/applications/{application_id}/withdraw` (candidato)
  - `POST /api/applications/{application_id}/archive`
  - `GET /api/applications/{application_id}/candidate-data` (ver datos autorizados)
- [ ] Schemas:
  - ApplyToPositionRequest (includes shared_data, resume_choice)
  - UpdateResumeRequest (includes changelog)
  - ResumeVersionResponse
- [ ] Mapper
- [ ] Registrar en container y main.py

**3.4. Resume Generation Integration**
- [ ] Integrate with existing resume generation service
- [ ] Add method: `generate_resume_for_position(candidate_id, position_id, template)`
- [ ] Position-specific resume optimization (match keywords from job description)
- [ ] Store generated PDF using StorageService
- [ ] Support for multiple resume templates (basic, professional, modern)

**3.5. Migration**
- [ ] Crear tabla `company_applications` con campos:
  - `resume_pdf_url` (varchar)
  - `resume_pdf_version` (integer, default 1)
  - `resume_snapshot_at` (timestamp)
  - `allow_resume_updates` (boolean, default false)
  - `resume_update_deadline` (timestamp, nullable)
  - `resume_last_updated_at` (timestamp, nullable)
  - `resume_versions` (jsonb array - store version history)
- [ ] Add indexes: application_id, candidate_id, position_id, status
- [ ] Ejecutar migration

**Estimación Fase 3**: 5-6 días (increased for resume versioning)

---

### 🎯 Fase 4: Comments & Notes (PRIORIDAD MEDIA)

**Objetivo**: Sistema de comentarios sobre candidatos y aplicaciones

#### Backend

**4.1. CandidateComment Module**
- [ ] Revisar si ya existe (según COMPANY.md sí existe)
- [ ] Actualizar para soportar:
  - `company_candidate_id` (nullable)
  - `company_application_id` (nullable)
  - Solo uno de los dos debe estar presente
- [ ] Commands: Create, Update, Delete
- [ ] Queries: List by Candidate, List by Application
- [ ] API endpoints
- [ ] Migration (actualizar tabla si es necesario)

**Estimación Fase 4**: 1-2 días

---

### 🎯 Fase 4.5: Candidate Communication (Pseudo-Chat) (PRIORIDAD MEDIA)

**Objetivo**: Sistema de mensajería entre empresa y candidato con notificaciones por email (pseudo-chat)

**Flujo**:
1. Company user sends message → Saved in DB → Email sent to candidate with notification
2. Candidate receives email → Clicks link → Logs into platform → Sees conversation → Replies in-app
3. Candidate reply → Saved in DB → Company user sees in dashboard (NO email to company)
4. **NO replies via email** - All communication happens in-app, emails are just notifications

#### Backend

**4.5.1. CandidateMessage Entity (NEW)**
- [ ] Create entity in `src/candidate_message/domain/entities/candidate_message.py`
- [ ] Fields:
  - `id: MessageId`
  - `company_id: CompanyId`
  - `candidate_id: CandidateId`
  - `application_id: Optional[CompanyApplicationId]` (contexto de la conversación)
  - `sender_type: MessageSenderType` (enum: COMPANY, CANDIDATE)
  - `sender_user_id: Optional[UserId]` (el CompanyUser que envía, si sender_type=COMPANY)
  - `message: str`
  - `is_read: bool`
  - `read_at: Optional[datetime]`
  - `created_at: datetime`
- [ ] Factory: `create_from_company()`, `create_from_candidate()`
- [ ] Methods: `mark_as_read()`
- [ ] Enums: MessageSenderType
- [ ] Value objects: MessageId

**4.5.2. CandidateMessage Module (estructura completa)**
```
src/candidate_message/
  application/
    commands/
      send_message_to_candidate_command.py
      send_message_to_company_command.py
      mark_message_as_read_command.py
    queries/
      list_messages_by_application_query.py
      list_unread_messages_query.py
      get_conversation_query.py
    dtos/
      candidate_message_dto.py
  domain/
    entities/
      candidate_message.py
    enums/
      message_sender_type.py
    infrastructure/
      candidate_message_repository_interface.py
  infrastructure/
    models/
      candidate_message_model.py
    repositories/
      candidate_message_repository.py
  presentation/
    controllers/
      candidate_message_controller.py
    schemas/
      message_request.py
      message_response.py
    mappers/
      message_mapper.py
```

**4.5.3. Email Notification Integration**
- [ ] Create email template: `message_notification.html`
  - Subject: "New message from {company_name} regarding {position_title}"
  - Body: Preview of message + CTA button "View Conversation"
  - Link: `{FRONTEND_URL}/candidate/applications/{application_id}/messages`
- [ ] Update SendMessageToCandidate command handler:
  - After saving message to DB
  - Dispatch email notification (only if sender is COMPANY)
  - Include deep link to conversation
- [ ] NO email sent when candidate replies (company checks dashboard)

**4.5.4. CandidateMessage API**
- [ ] Controller con métodos
- [ ] Router con endpoints:
  - `POST /api/applications/{application_id}/messages` - Send message (company or candidate)
  - `GET /api/applications/{application_id}/messages` - Get conversation
  - `GET /api/company/{company_id}/messages/unread` - Get unread messages for company
  - `GET /api/candidate/messages/unread` - Get unread messages for candidate
  - `POST /api/messages/{message_id}/read` - Mark as read
  - `GET /api/applications/{application_id}/messages/stats` - Message stats (count, unread)
- [ ] Schemas y mapper
- [ ] Permissions: only company users assigned to current stage + candidate can send
- [ ] Registrar en container y main.py

**4.5.5. Migration**
- [ ] Create table `candidate_messages`
- [ ] Indexes: application_id, candidate_id, company_id, is_read, created_at
- [ ] Ejecutar migration

**Estimación Fase 4.5**: 2-3 días

---

### ✅ Fase 5: File Storage (S3) (COMPLETADA)

**Objetivo**: Subida y gestión de CVs en S3

#### Backend

**5.1. Storage Service**
- [x] Created `StorageServiceInterface` (domain layer)
- [x] Created `LocalStorageService` implementation
- [x] Created `S3StorageService` implementation
- [x] Created `StorageFactory` for automatic selection
- [x] Métodos implementados:
  - `upload_file()` - Upload with validation
  - `delete_file()` - Delete file
  - `get_file_url()` - Get public URL
  - `file_exists()` - Check existence
  - `get_file_size()` - Get size
- [x] Built-in validations: file type, size limits
- [x] Support for presigned URLs (S3 only)

**5.2. Configuration**
- [x] Added storage settings to `core/config.py`
- [x] Updated `.env.example` with storage variables
- [x] Added boto3 dependency to `pyproject.toml`
- [x] Registered in DI container

**5.3. Documentation**
- [x] Complete usage guide: `docs/STORAGE_USAGE.md`
- [x] Examples for all operations
- [x] Migration guide from direct file access

**5.4. Integration Points**
- [ ] Integrate in CompanyCandidate: `POST /candidates/{id}/upload-resume`
- [ ] Integrate in CompanyApplication for candidate applications
- [ ] Serve static files in FastAPI (for local storage)

**Estimación Fase 5**: COMPLETED (2 días)

---

### 🎯 Fase 6: Frontend - ATS Dashboard (PRIORIDAD ALTA)

**Objetivo**: Interfaz para gestionar candidatos y aplicaciones

#### 6.1. Layout y Navegación
- [ ] Company Login Page (`/company/auth/login`)
- [ ] CompanyLayout con sidebar
- [ ] Rutas protegidas (ProtectedCompanyRoute)
- [ ] Navegación:
  - Dashboard
  - Candidatos
  - Posiciones
  - Ajustes

**6.2. Servicios API**
- [ ] `companyCandidateService.ts` (CRUD + upload resume)
- [ ] `positionService.ts` (CRUD + publish/pause/close)
- [ ] `companyApplicationService.ts` (CRUD + change stage + **resume versioning**)
  - `applyToPosition(positionId, sharedData, resumeChoice)` - Submit application
  - `updateResume(applicationId, changelog)` - Update resume (candidate)
  - `getResumeVersions(applicationId)` - Get version history
  - `downloadResumeVersion(applicationId, version)` - Download specific version
- [ ] `fileUploadService.ts` (upload resume con progress)
- [ ] `resumeGenerationService.ts` (generate position-specific resume)

**6.3. Tipos TypeScript**
- [ ] `types/companyCandidate.ts`
- [ ] `types/position.ts` (includes allow_resume_updates, resume_update_deadline_days)
- [ ] `types/companyApplication.ts` (includes resume_versions, resume_pdf_url, etc.)
- [ ] `types/resumeVersion.ts` (version, pdf_url, created_at, changelog)
- [ ] `types/sharedDataPermissions.ts`
- [ ] Enums compartidos

**6.4. Páginas - Candidatos**
- [ ] `/company/candidates` - Lista de candidatos
  - Tabla con columnas: Nombre, Email, Source, Status, Fecha
  - Filtros: Status, Source, Búsqueda
  - Paginación
  - Botón "Añadir Candidato"
- [ ] `/company/candidates/add` - Formulario añadir candidato
  - Campos: Nombre, Email, Teléfono, País, LinkedIn
  - Upload CV (drag & drop)
  - Tags, Notas internas, Prioridad
  - Validaciones
- [ ] `/company/candidates/:id` - Detalle de candidato
  - Tabs: Overview, Applications, Comments, History
  - Editar info básica
  - Ver/descargar CV
  - Lista de aplicaciones del candidato
  - Comentarios

**6.5. Páginas - Posiciones (WITH RESUME POLICY)**
- [ ] `/company/positions` - Lista de posiciones
  - Cards o tabla
  - Filtros: Status, Departamento
  - Botón "Crear Posición"
- [ ] `/company/positions/create` - Formulario crear posición
  - Título, Descripción, Departamento, Ubicación
  - Tipo de empleo, Tipo remoto
  - Salario (rango)
  - Requisitos, Responsabilidades, Beneficios
  - **Workflow selector** (dropdown de workflows de la empresa)
  - **Resume Update Policy section**:
    - Checkbox: "Allow candidates to update resume after applying"
    - If checked: Number input "Update deadline (days after application)" (default: 7)
  - Status: Draft/Active
  - is_public (mostrar en job board)
- [ ] `/company/positions/:id` - Detalle de posición
  - Ver info completa
  - Botones: Editar, Publicar, Pausar, Cerrar
  - Show resume update policy settings
  - Lista de aplicaciones a esta posición
  - Estadísticas (# aplicaciones, # en cada stage)

**6.6. Páginas - Aplicaciones (WITH RESUME VERSIONING)**
- [ ] `/company/positions/:id/applications` - Lista de aplicaciones de posición
  - Kanban por stages
  - Drag & drop para cambiar stage
  - Filtros: Status, Prioridad
  - **Badge indicator**: "Resume Updated" if version > 1
- [ ] `/company/applications/:id` - Detalle de aplicación (Company View)
  - Datos autorizados del candidato (según shared_data) - Structured view (default)
  - **Resume Section**:
    - Current version badge (e.g., "v2 - Updated Jan 25")
    - "Download PDF" button for current version
    - Dropdown: "View Version History" showing all versions
    - Each version shows: version number, date, changelog, download button
    - If updated: Show changelog and "What changed" summary
  - Cambiar stage (dropdown)
  - Hacer oferta (modal)
  - Rechazar (modal con razón)
  - Comments sobre la aplicación

**6.7. Páginas - Job Board Público (WITH RESUME SELECTION)**
- [ ] `/jobs` - Lista de posiciones públicas (sin auth)
- [ ] `/jobs/:id` - Detalle de posición pública
  - Show if resume updates are allowed
  - Example: "✓ You can update your resume for 7 days after applying"
- [ ] `/jobs/:id/apply` - Formulario de aplicación (Multi-step)
  - **Step 1**: Login/register si no está autenticado
  - **Step 2**: Seleccionar datos a compartir (checkboxes)
    - ☑ Education
    - ☑ Work Experience
    - ☑ Projects
    - ☑ Skills & Languages
    - Optional: Cover Letter textarea
  - **Step 3**: Resume Selection
    - Radio buttons:
      - ○ Use existing resume (if has any): "General Resume (created Jan 15)"
      - ● Generate position-specific resume (recommended)
    - [Preview Resume] button (opens modal with PDF preview)
    - Template selector (if generating new): Professional, Modern, Minimal
  - **Step 4**: Review & Submit
    - Summary of shared data
    - Resume preview thumbnail
    - Update policy reminder if applicable
    - [Submit Application] button

**6.8. Páginas - Candidate Dashboard (Resume Management)**
- [ ] `/candidate/applications` - My Applications
  - List of all applications
  - For each application show:
    - Position title, company name
    - Status, current stage
    - Applied date
    - **Resume version badge** (if > 1)
    - **"Update Resume" button** (if allowed and before deadline)
    - **Countdown timer**: "Updates allowed for 5 more days"
- [ ] `/candidate/applications/:id` - Application Detail (Candidate View)
  - Position details
  - Current status & stage
  - Shared data summary
  - **Resume section**:
    - Current version
    - Last updated timestamp
    - [Download My Resume] button
    - **[Update Resume] button** (if within deadline)
    - Version history (read-only for candidate)
  - Messages with company
- [ ] **Modal: Update Resume**
  - Triggered when clicking "Update Resume"
  - Shows:
    - Current resume preview
    - "What changed?" textarea (required)
    - [Regenerate from Profile] button (uses latest profile data)
    - Warning: "Company will be notified of this update"
    - Update deadline countdown
    - [Cancel] [Update Resume]

**6.9. Páginas - Mensajería (Pseudo-Chat)**
- [ ] `/company/applications/:id/messages` - Conversación con candidato
  - Vista de chat (company side)
  - Enviar mensaje (trigger email to candidate)
  - Ver historial completo
- [ ] `/candidate/applications/:id/messages` - Conversación con empresa
  - Vista de chat (candidate side)
  - Responder mensaje (NO email to company)
  - Ver historial completo
- [ ] Unread message indicators en dashboard
- [ ] Deep linking desde email a conversación

**6.10. Components Compartidos**
- [ ] CandidateCard
- [ ] PositionCard
- [ ] ApplicationCard
- [ ] StatusBadge
- [ ] PriorityIndicator
- [ ] FileUpload (drag & drop con progress)
- [ ] KanbanBoard (para applications)
- [ ] ConfirmDialog
- [ ] ChatWindow (pseudo-chat UI)
- [ ] MessageList
- [ ] MessageInput
- [ ] **ResumeVersionBadge** (shows version number with updated indicator)
- [ ] **ResumeVersionDropdown** (version history selector)
- [ ] **ResumePreviewModal** (PDF preview in modal)
- [ ] **UpdateDeadlineCountdown** (shows remaining time for updates)
- [ ] **SharedDataChecklist** (checkboxes for data sharing in apply form)
- [ ] **ResumeTemplateSelector** (radio buttons for templates)

**6.11. Email Templates (Backend)**
- [ ] `message_notification.html` - Notification when company sends message
  - Subject: "New message from {company_name} regarding {position_title}"
  - Preview of message (first 100 chars)
  - CTA button: "View Conversation"
  - Deep link to conversation in app
  - Footer: "Please log in to reply. Do not reply to this email."
- [ ] **`resume_updated_notification.html`** (Optional) - Notification when candidate updates resume
  - Subject: "Resume updated for {position_title}"
  - Changelog preview
  - CTA button: "View Updated Resume"
  - Deep link to application detail

**Estimación Fase 6**: 12-14 días (increased for resume versioning UI)

---

### 🎯 Fase 7: Workflows (PRIORIDAD MEDIA)

**Objetivo**: Configurar flujos de trabajo personalizados

**Nota**: CompanyWorkflow y WorkflowStage ya están implementados según COMPANY.md

#### Backend
- [ ] Verificar que endpoints funcionan correctamente
- [ ] Asegurar que CompanyApplication usa workflows

#### Frontend
- [ ] `/company/settings/workflows` - Lista de workflows
- [ ] `/company/settings/workflows/:id/edit` - Editor de workflow
  - Drag & drop de stages
  - Añadir/editar/eliminar stages
  - Configurar transiciones
- [ ] Integrar workflows en Kanban de aplicaciones

**Estimación Fase 7**: 3-4 días

---

### 🎯 Fase 8: Testing & Polish (PRIORIDAD MEDIA)

- [ ] Unit tests backend (entities, repositories, handlers)
- [ ] Integration tests backend (endpoints)
- [ ] Unit tests frontend (components, services)
- [ ] E2E tests (flujos principales)
- [ ] Fixes de bugs encontrados
- [ ] Optimizaciones de performance
- [ ] Mejoras de UX

**Estimación Fase 8**: 5 días

---

## 📅 Cronograma Estimado (ATS Core) - UPDATED WITH RESUME VERSIONING

| Fase | Descripción | Días | Acumulado |
|------|-------------|------|-----------|
| 0 | ✅ Documentación + Storage Abstraction + Resume Strategy | 2 | 2 |
| 1 | CompanyCandidate Backend | 3-4 | 6 |
| 1.5 | Workflow Enhancements (Stage Assignments) | 3-4 | 10 |
| 2 | Position Backend (+ Resume Policy) | 2-3 | 13 |
| 3 | CompanyApplication Backend (+ Resume Versioning) | 5-6 | 19 |
| 4 | Comments Backend | 1-2 | 21 |
| 4.5 | Candidate Communication (Pseudo-Chat) | 2-3 | 24 |
| 5 | ✅ File Storage (Completed) | 0 | 24 |
| 6 | Frontend ATS (+ Resume Versioning UI) | 12-14 | 38 |
| 7 | Workflows Frontend | 3-4 | 42 |
| 8 | Testing & Polish | 5 | 47 |

**Total**: ~47 días de desarrollo para ATS completo (MVP)

**Progreso actual**: Fase 0 completada ✅
- Storage Abstraction (Local + S3)
- Resume Sharing Strategy documented
- Hybrid approach (structured data + PDF) defined

---

## 🚫 Fuera de Scope (V1)

Las siguientes features están documentadas pero NO se implementarán en V1:

### Head Hunting Product (Futuro)
- ❌ Lead entity
- ❌ Lead sourcing
- ❌ Lead notifications
- ❌ GDPR compliance checks
- ❌ Lead conversion to Candidate

**Razón**: Es un producto premium separado. Primero validamos el ATS core.

### Features Avanzadas (V2+)
- ❌ Lead scoring automático
- ❌ Email campaigns para leads
- ❌ Integración con LinkedIn API
- ❌ Analytics avanzados
- ❌ AI-powered candidate matching
- ❌ Entrevistas por video integradas
- ❌ Background checks integrados
- ❌ Offer letter templates
- ❌ E-signature para contratos

---

## 🎯 MVP Definition (V1)

**El MVP incluye**:

✅ **Para Empresa**:
- Gestionar candidatos manualmente
- Crear y publicar posiciones
- Asignar workflows a posiciones
- **Asignar usuarios a cada etapa del workflow por posición**
- Recibir aplicaciones de candidatos
- Ver datos autorizados por candidato
- **Control de permisos: solo usuarios asignados pueden mover candidatos en su etapa**
- Comentarios internos sobre candidatos y aplicaciones
- **Mensajería in-app con candidatos (sin email)**
- Workflows personalizables con predefined templates
- Dashboard básico

✅ **Para Candidato**:
- Ver posiciones públicas
- Aplicar a posiciones
- Autorizar qué datos compartir
- Ver estado de sus aplicaciones
- **Comunicarse con la empresa (mensajes in-app)**
- Retirar aplicación

✅ **Core Features**:
- CRUD completo de Candidatos, Posiciones, Aplicaciones
- Upload de CVs (S3 o local) con storage abstraction
- Sistema de permisos (compartir datos)
- **Asignación de usuarios por stage por position**
- **Permisos granulares para cambio de etapa**
- Workflows con Kanban
- **Predefined workflow templates**
- **Sistema de mensajería interno**
- Job board público

---

## 📝 Notas Importantes

### Simplificaciones para V1

1. **Sin Lead/Head Hunting**: Candidatos se crean manualmente o por aplicación directa
2. **Workflows con permisos básicos**: Stage assignments por position, sin reglas complejas
3. **Comments simples**: Solo texto, sin attachments ni menciones
4. **Pseudo-chat con email notifications**:
   - Company → Candidate: Message saved in DB + email notification sent
   - Candidate → Company: Reply in-app, NO email to company
   - All communication happens in-app, emails are just notifications
5. **Sin analytics avanzados**: Dashboard básico con contadores simples
6. **Predefined templates**: 3 workflows predefinidos, customizable por empresa

### Dependencias Externas

- **S3**: Para producción (local filesystem para desarrollo)
- **PostgreSQL**: Base de datos
- **Alembic**: Migraciones

### Variables de Entorno Nuevas

```env
# Storage
STORAGE_TYPE=s3  # o 'local' para desarrollo
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_BUCKET=company-resumes
AWS_REGION=us-east-1

# File Upload Limits
MAX_RESUME_SIZE_MB=10
ALLOWED_RESUME_TYPES=application/pdf
```

---

## ✅ Siguiente Paso

**Comenzar con Fase 1**: CompanyCandidate Backend

### Progreso Actual:
- ✅ **Fase 0 COMPLETADA**: Storage Abstraction (Local + S3)
  - StorageServiceInterface con implementaciones
  - Configuración en environment
  - Documentación completa
  - Registered en DI container

### Tareas Inmediatas (Fase 1):
1. Revisar CompanyCandidate entity existente
2. Añadir campos: `lead_id`, `source`, `resume_url`, `resume_uploaded_by`, `resume_uploaded_at`
3. Crear migration para nuevos campos
4. Implementar Commands (Create, Update, UploadResume, Archive)
5. Implementar Queries (GetById, ListByCompany, GetByEmail)
6. Crear API endpoints con storage service integration
7. Testing básico

### Después de Fase 1:
- **Fase 1.5**: Workflow enhancements (stage assignments, user permissions)
- **Fase 2**: Position backend (with workflow_id)
- **Fase 3**: CompanyApplication (with stage permission checks)

**¿Comenzamos con Fase 1?**
