# Company Dashboard - Análisis y Tareas Frontend/Backend

## Estado Actual

### Frontend Existente

**Servicios disponibles:**
- `client-vite/src/services/companyService.ts` - **ADMIN-FOCUSED** (usa `/admin/companies`)
  - Gestión administrativa de empresas (aprobar, rechazar, activar, desactivar)
  - NO sirve para el dashboard de company users
  - Base path: `/admin/companies`

- `client-vite/src/services/positionService.ts` - Servicio de posiciones (pendiente verificar)

**Tipos definidos:**
- `client-vite/src/types/company.ts` - Tipos básicos de Company

**Componentes:**
- `client-vite/src/components/common/CompanySelector.tsx` - Selector de empresa

**Páginas existentes:**
- ❌ NO existe CompanyLoginPage
- ❌ NO existe CompanyDashboardPage
- ❌ NO existen páginas de gestión de candidatos para company
- ✅ Existe AdminLoginPage (línea 11 en App.tsx:11)
- ✅ Existe CandidateLoginPage (línea 10 en App.tsx:10)

**Rutas configuradas en App.tsx:**
- `/candidate/auth/login` - Login de candidatos
- `/admin/auth/login` - Login de admin
- ❌ NO existe `/company/auth/login` - **FALTA IMPLEMENTAR**
- ❌ NO existen rutas para dashboard de company

### Backend Implementado

**Endpoints disponibles (según COMPANY.md y revisión de routers):**

#### 1. Company (adapters/http/company/routers/company_router.py)
- ✅ POST `/api/company` - Crear empresa (201)
- ✅ GET `/api/company/{company_id}` - Obtener empresa por ID
- ✅ GET `/api/company/domain/{domain}` - Obtener empresa por dominio
- ✅ GET `/api/company` - Listar empresas (query: active_only)
- ✅ PUT `/api/company/{company_id}` - Actualizar empresa
- ✅ POST `/api/company/{company_id}/suspend` - Suspender empresa
- ✅ POST `/api/company/{company_id}/activate` - Activar empresa
- ✅ DELETE `/api/company/{company_id}` - Eliminar empresa (soft delete, 204)
- ✅ POST `/api/company/auth/login` - Login de company user (OAuth2, Token)

#### 2. CompanyUser (adapters/http/company/routers/company_user_router.py)
- ✅ POST `/api/company/{company_id}/users` - Añadir usuario a empresa (201)
- ✅ GET `/api/company/{company_id}/users` - Listar usuarios de empresa (query: active_only)
- ✅ GET `/api/company/{company_id}/users/user/{user_id}` - Obtener usuario por company_id + user_id
- ✅ GET `/api/company/users/{company_user_id}` - Obtener usuario por ID
- ✅ PUT `/api/company/users/{company_user_id}` - Actualizar usuario
- ✅ POST `/api/company/users/{company_user_id}/activate` - Activar usuario
- ✅ POST `/api/company/users/{company_user_id}/deactivate` - Desactivar usuario
- ✅ DELETE `/api/company/users/{company_user_id}` - Eliminar usuario (204)

#### 3. CompanyWorkflow (adapters/http/company_workflow/routers/company_workflow_router.py)
- ✅ POST `/api/company-workflows` - Crear workflow (201)
- ✅ GET `/api/company-workflows/{workflow_id}` - Obtener workflow por ID
- ✅ GET `/api/company-workflows/company/{company_id}` - Listar workflows de empresa
- ✅ PUT `/api/company-workflows/{workflow_id}` - Actualizar workflow
- ✅ POST `/api/company-workflows/{workflow_id}/deactivate` - Desactivar workflow
- ✅ POST `/api/company-workflows/{workflow_id}/archive` - Archivar workflow
- ✅ POST `/api/company-workflows/{workflow_id}/set-default` - Establecer como default
- ✅ POST `/api/company-workflows/{workflow_id}/unset-default` - Quitar default
- ✅ POST `/api/company-workflows/{workflow_id}/delete` - Eliminar workflow

#### 4. WorkflowStage (adapters/http/company_workflow/routers/workflow_stage_router.py)
- ✅ POST `/api/workflow-stages` - Crear etapa (201)
- ✅ GET `/api/workflow-stages/{stage_id}` - Obtener etapa por ID
- ✅ GET `/api/workflow-stages/workflow/{workflow_id}` - Listar etapas de workflow
- ✅ GET `/api/workflow-stages/workflow/{workflow_id}/initial` - Obtener etapa inicial
- ✅ GET `/api/workflow-stages/workflow/{workflow_id}/final` - Obtener etapas finales
- ✅ PUT `/api/workflow-stages/{stage_id}` - Actualizar etapa
- ✅ DELETE `/api/workflow-stages/{stage_id}` - Eliminar etapa (204)
- ✅ POST `/api/workflow-stages/workflow/{workflow_id}/reorder` - Reordenar etapas
- ✅ POST `/api/workflow-stages/{stage_id}/activate` - Activar etapa
- ✅ POST `/api/workflow-stages/{stage_id}/deactivate` - Desactivar etapa

#### 5. CompanyCandidate (Parcialmente implementado según COMPANY.md)
Según la documentación, se implementaron comandos/queries pero pendiente verificar endpoints en router.

**Módulos backend FALTANTES (según COMPANY.md):**
- ❌ CandidateComment (comentarios sobre candidatos)
- ❌ CandidateInvitation (gestión de invitaciones)
- ❌ CandidateAccessLog (log de accesos)

---

## Requisitos del Usuario

El dashboard de company debe incluir:

1. **Lista de candidatos**: Añadir, eliminar, modificar, comentarios, incluir en candidatura
2. **Formulario de añadir candidato**: Datos básicos + subida de PDF
3. **Gestión de posiciones**: Con sus opciones
4. **Ajustes**: Configurar flujos de trabajo (workflows)
5. **Dashboard Kanban**: Ver flujos activos en la empresa (estilo CRM)

---

## TAREAS FRONTEND

### 1. Autenticación y Routing (PRIORIDAD: ALTA)

#### 1.1 Página de Login
**Archivo:** `client-vite/src/pages/CompanyLoginPage.tsx`
- [ ] Crear página de login para company users
- [ ] Reutilizar componente de login existente (CandidateLoginPage como referencia)
- [ ] Integrar con endpoint `POST /api/company/auth/login`
- [ ] Usar OAuth2PasswordRequestForm (username=email, password)
- [ ] Guardar token en localStorage/sessionStorage
- [ ] Redireccionar a `/company/dashboard` después del login exitoso

#### 1.2 Rutas y Layout
**Archivo:** `client-vite/src/App.tsx`
- [ ] Añadir ruta `/company/auth/login` → CompanyLoginPage
- [ ] Añadir redirect `/company/login` → `/company/auth/login` (conveniencia)
- [ ] Crear ProtectedCompanyRoute component (similar a ProtectedAdminRoute)
- [ ] Crear CompanyLayout component con sidebar/navigation
- [ ] Añadir rutas protegidas bajo `/company/*`:
  - `/company/dashboard` - Dashboard principal
  - `/company/candidates` - Lista de candidatos
  - `/company/candidates/add` - Añadir candidato
  - `/company/candidates/:id` - Detalle de candidato
  - `/company/positions` - Gestión de posiciones
  - `/company/settings` - Ajustes (workflows)
  - `/company/settings/workflows` - Configuración de workflows
  - `/company/workflow-board` - Dashboard Kanban

### 2. Servicios y API Clients (PRIORIDAD: ALTA)

#### 2.1 Company Auth Service
**Archivo:** `client-vite/src/services/companyAuthService.ts` (NUEVO)
- [ ] Crear servicio de autenticación
- [ ] Método `login(email, password)` → Token
- [ ] Método `logout()`
- [ ] Método `getCurrentUser()` → CompanyUserDto
- [ ] Método `refreshToken()` (si aplica)
- [ ] Integración con `/api/company/auth/login`

#### 2.2 Company Candidate Service
**Archivo:** `client-vite/src/services/companyCandidateService.ts` (NUEVO)
- [ ] CRUD de CompanyCandidate:
  - `addCandidate(companyId, candidateData)` - Crear relación + candidato básico
  - `getCandidatesByCompany(companyId, filters?)` - Listar candidatos
  - `getCandidateDetail(companyCandidateId)` - Detalle completo
  - `updateCandidate(companyCandidateId, data)` - Actualizar
  - `deleteCandidate(companyCandidateId)` - Eliminar
  - `inviteCandidate(companyCandidateId)` - Enviar invitación
  - `assignToWorkflow(companyCandidateId, workflowId)` - Asignar a flujo
  - `moveToStage(companyCandidateId, stageId)` - Mover etapa
  - `updateStatus(companyCandidateId, status)` - Cambiar estado
  - `addTags(companyCandidateId, tags)` - Añadir etiquetas
  - `updateInternalNotes(companyCandidateId, notes)` - Notas internas

#### 2.3 Candidate Comment Service
**Archivo:** `client-vite/src/services/candidateCommentService.ts` (NUEVO)
- [ ] CRUD de comentarios:
  - `addComment(companyCandidateId, comment)` - Crear comentario
  - `getComments(companyCandidateId)` - Listar comentarios
  - `updateComment(commentId, comment)` - Actualizar
  - `deleteComment(commentId)` - Eliminar
  - `getCommentById(commentId)` - Obtener por ID

#### 2.4 Company Workflow Service
**Archivo:** `client-vite/src/services/companyWorkflowService.ts` (NUEVO)
- [ ] Gestión de workflows:
  - `getWorkflowsByCompany(companyId)` - Listar workflows
  - `getWorkflowById(workflowId)` - Obtener workflow
  - `createWorkflow(companyId, workflowData)` - Crear
  - `updateWorkflow(workflowId, workflowData)` - Actualizar
  - `deleteWorkflow(workflowId)` - Eliminar
  - `setAsDefault(workflowId)` - Establecer default
  - `deactivateWorkflow(workflowId)` - Desactivar
  - `archiveWorkflow(workflowId)` - Archivar

#### 2.5 Workflow Stage Service
**Archivo:** `client-vite/src/services/workflowStageService.ts` (NUEVO)
- [ ] Gestión de etapas:
  - `getStagesByWorkflow(workflowId)` - Listar etapas
  - `getInitialStage(workflowId)` - Etapa inicial
  - `getFinalStages(workflowId)` - Etapas finales
  - `createStage(workflowId, stageData)` - Crear
  - `updateStage(stageId, stageData)` - Actualizar
  - `deleteStage(stageId)` - Eliminar
  - `reorderStages(workflowId, stageIdsInOrder)` - Reordenar
  - `activateStage(stageId)` - Activar
  - `deactivateStage(stageId)` - Desactivar

#### 2.6 Position Service (Revisar existente)
**Archivo:** `client-vite/src/services/positionService.ts` (REVISAR)
- [ ] Verificar si existe y qué endpoints usa
- [ ] Si no existe, crear con:
  - `getPositionsByCompany(companyId)` - Listar posiciones
  - `getPositionById(positionId)` - Obtener posición
  - `createPosition(companyId, positionData)` - Crear
  - `updatePosition(positionId, positionData)` - Actualizar
  - `deletePosition(positionId)` - Eliminar
  - `activatePosition(positionId)` - Activar
  - `deactivatePosition(positionId)` - Desactivar

#### 2.7 File Upload Service (para PDFs)
**Archivo:** `client-vite/src/services/fileUploadService.ts` (NUEVO o EXTENDER)
- [ ] Método `uploadCandidatePDF(file: File, candidateId: string)` → URL
- [ ] Manejo de multipart/form-data
- [ ] Progress tracking
- [ ] Error handling

### 3. Tipos TypeScript (PRIORIDAD: ALTA)

#### 3.1 Company Types
**Archivo:** `client-vite/src/types/company.ts` (EXTENDER)
- [ ] Revisar tipos existentes
- [ ] Añadir tipos faltantes:
  - `CompanyUser` - Usuario de empresa con permisos
  - `CompanyUserRole` - Enum: admin, recruiter, viewer
  - `CompanyUserPermissions` - Interface de permisos

#### 3.2 Candidate Types
**Archivo:** `client-vite/src/types/companyCandidate.ts` (NUEVO)
- [ ] `CompanyCandidate` - Relación empresa-candidato
- [ ] `CompanyCandidateStatus` - Enum: pending_invitation, pending_confirmation, active, rejected, archived
- [ ] `OwnershipStatus` - Enum: company_owned, user_owned
- [ ] `VisibilitySettings` - Interface de configuración de visibilidad
- [ ] `CandidateFilters` - Filtros para lista
- [ ] `CandidateListResponse` - Response de lista paginada
- [ ] `AddCandidateRequest` - Request para añadir candidato
- [ ] `UpdateCandidateRequest` - Request para actualizar

#### 3.3 Comment Types
**Archivo:** `client-vite/src/types/candidateComment.ts` (NUEVO)
- [ ] `CandidateComment` - Comentario sobre candidato
- [ ] `CreateCommentRequest` - Request para crear
- [ ] `UpdateCommentRequest` - Request para actualizar

#### 3.4 Workflow Types
**Archivo:** `client-vite/src/types/workflow.ts` (NUEVO)
- [ ] `CompanyWorkflow` - Workflow de empresa
- [ ] `WorkflowStatus` - Enum: ACTIVE, INACTIVE, ARCHIVED
- [ ] `WorkflowStage` - Etapa de workflow
- [ ] `StageType` - Enum: INITIAL, INTERMEDIATE, FINAL, CUSTOM
- [ ] `CreateWorkflowRequest` - Request para crear
- [ ] `UpdateWorkflowRequest` - Request para actualizar
- [ ] `CreateStageRequest` - Request para crear etapa
- [ ] `UpdateStageRequest` - Request para actualizar etapa
- [ ] `ReorderStagesRequest` - Request para reordenar

#### 3.5 Position Types
**Archivo:** `client-vite/src/types/position.ts` (NUEVO o REVISAR)
- [ ] Verificar si existe
- [ ] `Position` - Posición/vacante
- [ ] `PositionStatus` - Estados de posición
- [ ] `CreatePositionRequest` - Request para crear
- [ ] `UpdatePositionRequest` - Request para actualizar

### 4. Componentes Compartidos (PRIORIDAD: MEDIA)

#### 4.1 Layout Components
**Directorio:** `client-vite/src/components/company/layout/`
- [ ] `CompanyLayout.tsx` - Layout principal con sidebar
- [ ] `CompanySidebar.tsx` - Menú lateral de navegación
- [ ] `CompanyHeader.tsx` - Header con usuario y notificaciones
- [ ] `ProtectedCompanyRoute.tsx` - HOC para rutas protegidas

#### 4.2 Common Components
**Directorio:** `client-vite/src/components/company/common/`
- [ ] `CandidateCard.tsx` - Card de candidato para listas
- [ ] `StatusBadge.tsx` - Badge de estado (active, pending, etc.)
- [ ] `OwnershipBadge.tsx` - Badge de ownership (company_owned, user_owned)
- [ ] `PriorityIndicator.tsx` - Indicador de prioridad (low, medium, high)
- [ ] `TagsList.tsx` - Lista de tags editables
- [ ] `StageIndicator.tsx` - Indicador de etapa actual
- [ ] `ConfirmDialog.tsx` - Diálogo de confirmación reutilizable

### 5. Páginas del Dashboard (PRIORIDAD: ALTA)

#### 5.1 Dashboard Principal
**Archivo:** `client-vite/src/pages/company/CompanyDashboardPage.tsx`
- [ ] Crear página de dashboard principal
- [ ] Widgets de estadísticas:
  - Total de candidatos
  - Candidatos activos
  - Candidatos pendientes
  - Por etapa de workflow
- [ ] Lista de candidatos recientes
- [ ] Acciones rápidas
- [ ] Notificaciones/alertas

#### 5.2 Lista de Candidatos
**Archivo:** `client-vite/src/pages/company/CandidatesListPage.tsx`
- [ ] Tabla de candidatos con columnas:
  - Nombre/Avatar
  - Posición/Departamento
  - Estado (status badge)
  - Ownership (badge)
  - Etapa actual (workflow stage)
  - Prioridad
  - Tags
  - Fecha de creación
  - Acciones
- [ ] Filtros:
  - Búsqueda por nombre/email
  - Estado (status)
  - Ownership
  - Workflow/Etapa
  - Prioridad
  - Tags
  - Rango de fechas
- [ ] Paginación
- [ ] Ordenamiento por columnas
- [ ] Acciones en fila:
  - Ver detalle
  - Editar
  - Comentar
  - Mover a etapa
  - Eliminar
- [ ] Acciones masivas (checkboxes):
  - Asignar a workflow
  - Cambiar estado
  - Añadir tags
  - Exportar
- [ ] Botón "Añadir Candidato" (top-right)

#### 5.3 Añadir Candidato
**Archivo:** `client-vite/src/pages/company/AddCandidatePage.tsx`
- [ ] Formulario con campos básicos:
  - Nombre completo *
  - Email *
  - Teléfono
  - Posición
  - Departamento
  - Prioridad (select)
  - Tags (input multi)
  - Notas internas (textarea)
- [ ] Sección de subida de PDF:
  - Drag & drop area
  - File picker
  - Validación (solo PDF, tamaño máx)
  - Preview del nombre del archivo
  - Progress bar durante upload
- [ ] Botones:
  - "Guardar y Enviar Invitación"
  - "Guardar como Borrador"
  - "Cancelar"
- [ ] Validación de formulario (React Hook Form)
- [ ] Manejo de errores

#### 5.4 Detalle de Candidato
**Archivo:** `client-vite/src/pages/company/CandidateDetailPage.tsx`
- [ ] Layout con tabs/secciones:
  - **Información Básica**: Datos del candidato (según visibilitySettings)
  - **Comentarios**: Lista de comentarios con formulario para añadir
  - **Historial**: Timeline de cambios/eventos
  - **Documentos**: PDFs y archivos subidos
- [ ] Sidebar derecho con:
  - Status actual
  - Ownership status
  - Workflow y etapa actual
  - Prioridad
  - Tags editables
  - Notas internas (textarea editable)
  - Botones de acción:
    - Editar información
    - Enviar invitación
    - Mover a etapa (dropdown)
    - Cambiar status
    - Incluir en candidatura
    - Eliminar
- [ ] Sección de comentarios:
  - Lista de comentarios ordenados por fecha
  - Autor del comentario
  - Timestamp
  - Botones editar/eliminar (solo owner del comentario)
  - Formulario para añadir nuevo comentario (textarea + botón)

#### 5.5 Editar Candidato
**Archivo:** `client-vite/src/pages/company/EditCandidatePage.tsx`
- [ ] Formulario similar a AddCandidatePage pero con datos pre-cargados
- [ ] Solo editable si ownership_status = company_owned
- [ ] Si user_owned, mostrar mensaje de "Solo lectura"
- [ ] Botones "Guardar" y "Cancelar"

### 6. Gestión de Posiciones (PRIORIDAD: MEDIA)

#### 6.1 Lista de Posiciones
**Archivo:** `client-vite/src/pages/company/PositionsListPage.tsx`
- [ ] Tabla de posiciones con columnas:
  - Título
  - Departamento
  - Estado (activa/inactiva)
  - # de candidatos asignados
  - Fecha de creación
  - Acciones
- [ ] Filtros por departamento y estado
- [ ] Botón "Añadir Posición"
- [ ] Acciones en fila:
  - Ver candidatos
  - Editar
  - Activar/Desactivar
  - Eliminar

#### 6.2 Formulario de Posición
**Archivo:** `client-vite/src/components/company/positions/PositionForm.tsx`
- [ ] Componente reutilizable para crear/editar
- [ ] Campos:
  - Título *
  - Departamento
  - Descripción
  - Requisitos
  - Salario (rango)
  - Ubicación
  - Tipo de contrato
  - Estado
- [ ] Validaciones
- [ ] Botones "Guardar" y "Cancelar"

### 7. Configuración de Workflows (PRIORIDAD: ALTA)

#### 7.1 Lista de Workflows
**Archivo:** `client-vite/src/pages/company/settings/WorkflowsSettingsPage.tsx`
- [ ] Lista de workflows existentes
- [ ] Card por workflow mostrando:
  - Nombre
  - Estado (ACTIVE, INACTIVE, ARCHIVED)
  - Badge "Default" si is_default=true
  - # de etapas
  - # de candidatos activos en el workflow
  - Botones de acción
- [ ] Botón "Crear Workflow"
- [ ] Acciones por workflow:
  - Ver/Editar
  - Establecer como default
  - Desactivar
  - Archivar
  - Eliminar

#### 7.2 Editor de Workflow
**Archivo:** `client-vite/src/pages/company/settings/WorkflowEditorPage.tsx`
- [ ] Formulario de workflow:
  - Nombre *
  - Descripción
  - Estado (active/inactive)
  - is_default (checkbox)
- [ ] Sección de etapas (stages):
  - Lista ordenable (drag & drop con react-beautiful-dnd o similar)
  - Card por etapa mostrando:
    - Nombre
    - Tipo (INITIAL, INTERMEDIATE, FINAL, CUSTOM)
    - Orden
    - Estado (active/inactive)
    - Botones: Editar, Eliminar, Mover arriba/abajo
  - Botón "Añadir Etapa"
- [ ] Modal/Drawer para editar etapa:
  - Nombre *
  - Descripción
  - Tipo (select) *
  - Orden (auto-generado)
  - required_outcome (opcional)
  - estimated_duration_days (número)
  - is_active (checkbox)
  - Botones "Guardar" y "Cancelar"
- [ ] Validaciones:
  - Solo 1 etapa INITIAL permitida
  - Al menos 1 etapa FINAL requerida
  - Orden único
- [ ] Botones principales:
  - "Guardar Workflow"
  - "Guardar y Cerrar"
  - "Cancelar"

### 8. Dashboard Kanban (PRIORIDAD: ALTA)

#### 8.1 Workflow Board (Kanban)
**Archivo:** `client-vite/src/pages/company/WorkflowBoardPage.tsx`
- [ ] Selector de workflow (dropdown top-left)
- [ ] Layout de columnas horizontales (una por etapa)
- [ ] Cada columna muestra:
  - Título de la etapa
  - # de candidatos
  - Lista de cards de candidatos
- [ ] Drag & drop entre columnas (react-beautiful-dnd)
- [ ] CandidateCard en cada columna con:
  - Nombre
  - Avatar
  - Posición
  - Prioridad (badge)
  - Tags
  - Click para ver detalle
- [ ] Al soltar en nueva columna:
  - Confirmar movimiento
  - Llamar a `moveToStage(companyCandidateId, newStageId)`
- [ ] Filtros:
  - Búsqueda por nombre
  - Prioridad
  - Tags
- [ ] Botón "Vista de Lista" (alterna a CandidatesListPage)

### 9. Context y Estado Global (PRIORIDAD: MEDIA)

#### 9.1 Company Auth Context
**Archivo:** `client-vite/src/context/CompanyAuthContext.tsx`
- [ ] Crear contexto para autenticación de company
- [ ] Estado:
  - `user: CompanyUserDto | null`
  - `company: Company | null`
  - `isAuthenticated: boolean`
  - `isLoading: boolean`
  - `permissions: CompanyUserPermissions`
- [ ] Métodos:
  - `login(email, password)`
  - `logout()`
  - `checkAuth()`
- [ ] Provider wrapper

#### 9.2 Company Candidates Context (Opcional)
**Archivo:** `client-vite/src/context/CompanyCandidatesContext.tsx`
- [ ] Estado para caché de candidatos
- [ ] Métodos para CRUD
- [ ] Invalidación de caché después de mutaciones

### 10. Hooks Personalizados (PRIORIDAD: BAJA)

**Directorio:** `client-vite/src/hooks/company/`
- [ ] `useCompanyAuth.ts` - Hook para auth context
- [ ] `useCandidates.ts` - Hook para gestión de candidatos (con react-query)
- [ ] `useWorkflows.ts` - Hook para workflows
- [ ] `useComments.ts` - Hook para comentarios
- [ ] `usePositions.ts` - Hook para posiciones
- [ ] `useFileUpload.ts` - Hook para upload de archivos

### 11. Testing (PRIORIDAD: BAJA - DESPUÉS DE IMPLEMENTACIÓN)

- [ ] Unit tests para servicios
- [ ] Unit tests para componentes clave
- [ ] Integration tests para flujos principales
- [ ] E2E tests para user journey completo

---

## TAREAS BACKEND

### 1. CompanyCandidate Endpoints (PRIORIDAD: ALTA)

**Archivos:**
- `adapters/http/company_candidate/routers/company_candidate_router.py` (crear)
- Controller/Commands/Queries ya implementados según COMPANY.md

**Endpoints a implementar:**
- [ ] POST `/api/company/{company_id}/candidates` - Añadir candidato (crear relación + candidato básico)
- [ ] GET `/api/company/{company_id}/candidates` - Listar candidatos de empresa (con filtros)
- [ ] GET `/api/company/candidates/{company_candidate_id}` - Obtener candidato por ID
- [ ] PUT `/api/company/candidates/{company_candidate_id}` - Actualizar candidato
- [ ] DELETE `/api/company/candidates/{company_candidate_id}` - Eliminar candidato
- [ ] POST `/api/company/candidates/{company_candidate_id}/invite` - Enviar invitación
- [ ] POST `/api/company/candidates/{company_candidate_id}/confirm` - Confirmar invitación (candidato)
- [ ] POST `/api/company/candidates/{company_candidate_id}/reject` - Rechazar invitación (candidato)
- [ ] POST `/api/company/candidates/{company_candidate_id}/archive` - Archivar
- [ ] PUT `/api/company/candidates/{company_candidate_id}/workflow` - Asignar workflow
- [ ] PUT `/api/company/candidates/{company_candidate_id}/stage` - Cambiar etapa
- [ ] PUT `/api/company/candidates/{company_candidate_id}/status` - Cambiar status
- [ ] PUT `/api/company/candidates/{company_candidate_id}/tags` - Actualizar tags
- [ ] PUT `/api/company/candidates/{company_candidate_id}/notes` - Actualizar notas internas
- [ ] PUT `/api/company/candidates/{company_candidate_id}/visibility` - Actualizar visibility settings

**Verificar implementación de comandos/queries:**
- [ ] Verificar que todos los comandos necesarios existen
- [ ] Verificar que todos los queries necesarios existen
- [ ] Registrar en container.py si no están registrados
- [ ] Registrar router en main.py

### 2. CandidateComment Module (PRIORIDAD: ALTA)

**Estructura a crear:**
```
src/company_candidate/
  application/
    commands/
      create_comment_command.py
      update_comment_command.py
      delete_comment_command.py
    queries/
      get_comment_by_id_query.py
      list_comments_by_candidate_query.py
    dtos/
      comment_dto.py
  domain/
    entities/
      candidate_comment.py
    infrastructure/
      candidate_comment_repository_interface.py
  infrastructure/
    models/
      candidate_comment_model.py
    repositories/
      candidate_comment_repository.py
  presentation/
    controllers/
      candidate_comment_controller.py
    schemas/
      comment_request.py
      comment_response.py
    mappers/
      comment_mapper.py
```

**Endpoints a crear:**
- [ ] POST `/api/company/candidates/{company_candidate_id}/comments` - Crear comentario (201)
- [ ] GET `/api/company/candidates/{company_candidate_id}/comments` - Listar comentarios
- [ ] GET `/api/company/candidates/comments/{comment_id}` - Obtener comentario por ID
- [ ] PUT `/api/company/candidates/comments/{comment_id}` - Actualizar comentario
- [ ] DELETE `/api/company/candidates/comments/{comment_id}` - Eliminar comentario (204)

**Tareas:**
- [ ] Crear entity CandidateComment (domain)
- [ ] Crear model CandidateCommentModel (infrastructure)
- [ ] Crear repository interface y implementation
- [ ] Crear DTOs
- [ ] Crear Commands (Create, Update, Delete) con handlers
- [ ] Crear Queries (GetById, ListByCandidate) con handlers
- [ ] Crear schemas (request/response)
- [ ] Crear mapper
- [ ] Crear controller
- [ ] Crear router
- [ ] Registrar en container.py
- [ ] Registrar en main.py
- [ ] Crear migration para tabla `candidate_comments`

### 3. CandidateInvitation Module (PRIORIDAD: MEDIA)

**Estructura similar a CandidateComment**

**Endpoints a crear:**
- [ ] POST `/api/company/candidates/{company_candidate_id}/invitations` - Crear invitación (201)
- [ ] GET `/api/company/candidates/{company_candidate_id}/invitations` - Listar invitaciones
- [ ] GET `/api/company/candidates/invitations/{invitation_id}` - Obtener invitación por ID
- [ ] POST `/api/company/candidates/invitations/{invitation_id}/resend` - Re-enviar invitación
- [ ] POST `/api/company/candidates/invitations/{invitation_id}/cancel` - Cancelar invitación

**Tareas:**
- [ ] Crear entity CandidateInvitation (domain)
- [ ] Crear model CandidateInvitationModel (infrastructure)
- [ ] Crear repository interface y implementation
- [ ] Crear DTOs
- [ ] Crear Commands (Create, Resend, Cancel) con handlers
- [ ] Crear Queries (GetById, ListByCandidate) con handlers
- [ ] Crear schemas (request/response)
- [ ] Crear mapper
- [ ] Crear controller
- [ ] Crear router
- [ ] Registrar en container.py
- [ ] Registrar en main.py
- [ ] Crear migration para tabla `candidate_invitations`
- [ ] Integrar con sistema de emails (enviar invitación)

### 4. CandidateAccessLog Module (PRIORIDAD: BAJA)

**Estructura similar a CandidateComment**

**Endpoints a crear (solo lectura):**
- [ ] GET `/api/company/candidates/{company_candidate_id}/access-logs` - Listar logs
- [ ] GET `/api/company/candidates/access-logs/{log_id}` - Obtener log por ID

**Tareas:**
- [ ] Crear entity CandidateAccessLog (domain)
- [ ] Crear model CandidateAccessLogModel (infrastructure)
- [ ] Crear repository interface y implementation
- [ ] Crear DTOs
- [ ] Crear Queries (GetById, ListByCandidate) con handlers
- [ ] Crear schemas (response)
- [ ] Crear mapper
- [ ] Crear controller
- [ ] Crear router
- [ ] Registrar en container.py
- [ ] Registrar en main.py
- [ ] Crear migration para tabla `candidate_access_logs`
- [ ] Implementar middleware/event handler para registrar accesos automáticamente

### 5. File Upload Endpoints (PRIORIDAD: ALTA)

**Archivo:** `adapters/http/files/routers/file_upload_router.py` (crear o extender)

**Endpoints:**
- [ ] POST `/api/files/candidate-pdf` - Upload PDF de candidato
  - Multipart/form-data
  - Validación: solo PDF, tamaño máx 10MB
  - Guardar en storage (S3, local, etc.)
  - Retornar URL del archivo
- [ ] GET `/api/files/candidate-pdf/{file_id}` - Descargar PDF
- [ ] DELETE `/api/files/candidate-pdf/{file_id}` - Eliminar PDF

**Tareas:**
- [ ] Crear FileUploadService
- [ ] Configurar storage (local/S3)
- [ ] Crear endpoint de upload
- [ ] Crear endpoint de download
- [ ] Crear endpoint de delete
- [ ] Validaciones (tipo, tamaño)
- [ ] Manejo de errores

### 6. Position Module (PRIORIDAD: MEDIA)

**Verificar si ya existe en el proyecto**

Si no existe, crear estructura completa similar a Company:

**Endpoints necesarios:**
- [ ] POST `/api/company/{company_id}/positions` - Crear posición (201)
- [ ] GET `/api/company/{company_id}/positions` - Listar posiciones de empresa
- [ ] GET `/api/positions/{position_id}` - Obtener posición por ID
- [ ] PUT `/api/positions/{position_id}` - Actualizar posición
- [ ] DELETE `/api/positions/{position_id}` - Eliminar posición (204)
- [ ] POST `/api/positions/{position_id}/activate` - Activar posición
- [ ] POST `/api/positions/{position_id}/deactivate` - Desactivar posición

**Tareas (si no existe):**
- [ ] Crear entity Position (domain)
- [ ] Crear model PositionModel (infrastructure)
- [ ] Crear repository interface y implementation
- [ ] Crear DTOs
- [ ] Crear Commands (Create, Update, Delete, Activate, Deactivate) con handlers
- [ ] Crear Queries (GetById, ListByCompany) con handlers
- [ ] Crear schemas (request/response)
- [ ] Crear mapper
- [ ] Crear controller
- [ ] Crear router
- [ ] Registrar en container.py
- [ ] Registrar en main.py
- [ ] Crear migration para tabla `positions` (si no existe)

### 7. Analytics/Dashboard Endpoints (PRIORIDAD: BAJA)

**Archivo:** `adapters/http/company/routers/company_analytics_router.py` (crear)

**Endpoints:**
- [ ] GET `/api/company/{company_id}/analytics/summary` - Estadísticas generales
  - Total candidatos
  - Candidatos por estado
  - Candidatos por workflow/etapa
  - Candidatos activos
- [ ] GET `/api/company/{company_id}/analytics/workflow-stats` - Estadísticas por workflow
- [ ] GET `/api/company/{company_id}/analytics/recent-activity` - Actividad reciente

**Tareas:**
- [ ] Crear queries de analytics
- [ ] Crear handlers con lógica de agregación
- [ ] Crear DTOs de respuesta
- [ ] Crear controller
- [ ] Crear router
- [ ] Registrar en container.py
- [ ] Registrar en main.py

### 8. Notificaciones/Emails (PRIORIDAD: MEDIA)

**Archivo:** `src/shared/infrastructure/email/email_service.py` (crear o extender)

**Tareas:**
- [ ] Crear template de email de invitación
- [ ] Crear EmailService para enviar invitaciones
- [ ] Integrar con CandidateInvitation command handler
- [ ] Crear event handler para enviar email cuando se crea invitación

### 9. Permisos y Autorización (PRIORIDAD: ALTA)

**Archivo:** `src/shared/infrastructure/auth/permissions.py` (crear o extender)

**Tareas:**
- [ ] Crear decorador/middleware para validar permisos de CompanyUser
- [ ] Validar:
  - Usuario pertenece a la empresa
  - Usuario tiene permisos para la acción (según role y permissions JSON)
  - CompanyUser está activo
- [ ] Aplicar a todos los endpoints de company

### 10. Testing Backend (PRIORIDAD: BAJA)

- [ ] Unit tests para comandos/queries
- [ ] Unit tests para handlers
- [ ] Unit tests para repositories
- [ ] Integration tests para endpoints
- [ ] E2E tests

### 11. Documentación Backend (PRIORIDAD: BAJA)

- [ ] Actualizar COMPANY.md con nuevos módulos
- [ ] Documentar todos los endpoints en OpenAPI (FastAPI lo hace automáticamente)
- [ ] Crear guía de permisos y roles

---

## RESUMEN DE PRIORIDADES

### Backend - Prioridad 1 (Bloqueantes para Frontend)
1. CompanyCandidate endpoints (router + registration)
2. CandidateComment module completo
3. File Upload endpoints (PDF)
4. Permisos y autorización

### Backend - Prioridad 2 (Importante pero no bloqueante)
1. CandidateInvitation module
2. Position module (si no existe)
3. Notificaciones/Emails

### Backend - Prioridad 3 (Mejoras)
1. CandidateAccessLog module
2. Analytics endpoints
3. Testing
4. Documentación

### Frontend - Prioridad 1 (Core Functionality)
1. Autenticación (Login page + routing)
2. Servicios API (companyAuth, companyCandidate, comments, workflows)
3. Tipos TypeScript
4. Layout y routing protegido
5. Lista de candidatos
6. Añadir candidato (con PDF upload)
7. Detalle de candidato (con comentarios)
8. Dashboard Kanban

### Frontend - Prioridad 2 (Features Importantes)
1. Configuración de workflows (CRUD completo)
2. Dashboard principal (estadísticas)
3. Gestión de posiciones

### Frontend - Prioridad 3 (Mejoras)
1. Componentes compartidos adicionales
2. Context y estado global
3. Hooks personalizados
4. Testing

---

## DEPENDENCIAS Y ORDEN DE IMPLEMENTACIÓN

### Fase 1: Fundación (Backend + Frontend básico)
**Backend:**
1. CompanyCandidate router + registration
2. CandidateComment module
3. File Upload endpoints
4. Permisos básicos

**Frontend:**
1. Login page + routing
2. Servicios API básicos (auth, candidate)
3. Tipos TypeScript
4. Layout y routing

**Resultado:** Login funcional + navegación básica

### Fase 2: Gestión de Candidatos (Core Feature)
**Backend:**
1. Completar todos los endpoints de CompanyCandidate
2. Asegurar que los filtros funcionan

**Frontend:**
1. Lista de candidatos (tabla + filtros)
2. Añadir candidato (form + PDF upload)
3. Detalle de candidato (sin comentarios todavía)
4. Editar candidato

**Resultado:** CRUD completo de candidatos

### Fase 3: Comentarios
**Backend:**
- Ya está listo de Fase 1

**Frontend:**
1. Sección de comentarios en detalle de candidato
2. Form para añadir comentario
3. Edit/delete de comentarios

**Resultado:** Sistema de comentarios funcional

### Fase 4: Workflows (Config + Kanban)
**Backend:**
- Ya está implementado (verificar endpoints)

**Frontend:**
1. Configuración de workflows (lista + editor)
2. Dashboard Kanban (drag & drop)

**Resultado:** Gestión de flujos de trabajo + visualización Kanban

### Fase 5: Posiciones
**Backend:**
1. Position module (si no existe)

**Frontend:**
1. Lista de posiciones
2. Form de posición

**Resultado:** Gestión de posiciones funcional

### Fase 6: Dashboard y Analytics
**Backend:**
1. Analytics endpoints

**Frontend:**
1. Dashboard principal con estadísticas

**Resultado:** Dashboard con métricas

### Fase 7: Features Avanzadas
**Backend:**
1. CandidateInvitation module
2. Emails

**Frontend:**
1. UI para invitaciones
2. Notificaciones

**Resultado:** Sistema de invitaciones completo

### Fase 8: Testing y Pulido
- Testing backend
- Testing frontend
- Mejoras UX
- Documentación

---

## NOTAS TÉCNICAS

### Frontend

**Librerías recomendadas:**
- `react-beautiful-dnd` - Drag & drop para Kanban
- `react-hook-form` - Formularios
- `react-query` (o `@tanstack/react-query`) - Estado de servidor/caché
- `axios` o `fetch` - HTTP client (ya existe en api.ts)
- `react-router-dom` - Ya está en uso
- `tailwindcss` - Ya está en uso

**Estructura de archivos sugerida:**
```
client-vite/src/
  pages/
    company/
      CompanyDashboardPage.tsx
      CandidatesListPage.tsx
      AddCandidatePage.tsx
      EditCandidatePage.tsx
      CandidateDetailPage.tsx
      PositionsListPage.tsx
      WorkflowBoardPage.tsx
      settings/
        WorkflowsSettingsPage.tsx
        WorkflowEditorPage.tsx
    CompanyLoginPage.tsx
  components/
    company/
      layout/
        CompanyLayout.tsx
        CompanySidebar.tsx
        CompanyHeader.tsx
        ProtectedCompanyRoute.tsx
      candidates/
        CandidateCard.tsx
        CandidateTable.tsx
        CandidateFilters.tsx
        AddCandidateForm.tsx
        CandidateDetailView.tsx
        CommentsList.tsx
        CommentForm.tsx
      positions/
        PositionForm.tsx
        PositionCard.tsx
      workflows/
        WorkflowList.tsx
        WorkflowForm.tsx
        StageEditor.tsx
        WorkflowBoard.tsx
        StageColumn.tsx
      common/
        StatusBadge.tsx
        OwnershipBadge.tsx
        PriorityIndicator.tsx
        TagsList.tsx
        ConfirmDialog.tsx
  services/
    companyAuthService.ts
    companyCandidateService.ts
    candidateCommentService.ts
    companyWorkflowService.ts
    workflowStageService.ts
    positionService.ts
    fileUploadService.ts
  types/
    company.ts
    companyCandidate.ts
    candidateComment.ts
    workflow.ts
    position.ts
  context/
    CompanyAuthContext.tsx
    CompanyCandidatesContext.tsx
  hooks/
    company/
      useCompanyAuth.ts
      useCandidates.ts
      useWorkflows.ts
      useComments.ts
      usePositions.ts
      useFileUpload.ts
```

### Backend

**Pendiente verificar:**
- ¿Existe módulo de Position?
- ¿Existen endpoints de CompanyCandidate en router?
- ¿Está implementado el sistema de permisos?

**Patrón de nombres:**
- Routers en: `adapters/http/{module}/routers/`
- Controllers en: `src/{module}/presentation/controllers/`
- Comandos en: `src/{module}/application/commands/`
- Queries en: `src/{module}/application/queries/`

---

## ESTIMACIÓN DE ESFUERZO

### Backend
- **Fase 1 (Fundación)**: 3-4 días
- **Fase 2 (CompanyCandidate completo)**: 1-2 días
- **Fase 3 (Comments)**: 2-3 días
- **Fase 5 (Position)**: 2-3 días (si no existe)
- **Fase 7 (Invitations)**: 2-3 días
- **Testing**: 2-3 días
- **Total Backend**: ~12-18 días

### Frontend
- **Fase 1 (Fundación)**: 2-3 días
- **Fase 2 (CRUD Candidatos)**: 4-5 días
- **Fase 3 (Comentarios)**: 1-2 días
- **Fase 4 (Workflows + Kanban)**: 4-5 días
- **Fase 5 (Posiciones)**: 2-3 días
- **Fase 6 (Dashboard)**: 2-3 días
- **Fase 7 (Invitaciones)**: 2-3 días
- **Testing**: 2-3 días
- **Total Frontend**: ~17-25 días

**Total Proyecto**: ~30-45 días de desarrollo (dependiendo de la complejidad y si se trabaja en paralelo frontend/backend)

---

## SIGUIENTE PASO

Una vez aprobado este documento, se recomienda:

1. **Revisar el backend actual**: Verificar qué endpoints de CompanyCandidate ya existen
2. **Comenzar con Fase 1 Backend**: Router de CompanyCandidate + Comments + FileUpload
3. **Paralelamente, Fase 1 Frontend**: Login + Layout + Routing
4. **Seguir las fases en orden** para ir construyendo incrementalmente

**Nota**: Este documento se mantendrá actualizado a medida que se completen tareas, marcando con ✅ lo que está completado.
