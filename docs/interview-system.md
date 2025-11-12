# Interview System

> **Estado**: ✅ Backend Completo - Ver `interview-system-final-summary.md` para resumen detallado

## Especificación del Sistema

### Tipos de Plantillas (InterviewTemplateTypeEnum)
- `EXTENDED_PROFILE` = "EXTENDED_PROFILE"
- `POSITION_INTERVIEW` = "POSITION_INTERVIEW"
- `SCREENING` = "SCREENING"
- `CUSTOM` = "CUSTOM"

### Tipos de Entrevistas (InterviewTypeEnum)
- `EXTENDED_PROFILE` = "EXTENDED_PROFILE"
- `POSITION_INTERVIEW` = "POSITION_INTERVIEW"
- `CUSTOM` = "CUSTOM"

### Plantillas
- Las plantillas ayudan a hacer entrevistas.
- Las plantillas pueden ser mejoradas por la IA. Es un check.
- Las plantillas tienen secciones, las secciones preguntas.
- Las plantillas de tipo scoring, tienen puntajes. Las preguntas van a tener puntajes de 1 a 10.
- Existen dos modos de scoring: **Distancia** y **Absoluto**.
  - **Distancia**: Es mejor cuanto más próximo a los requisitos es.
  - **Absoluto**: Es mejor cuanto más alto es.

### Entrevistas
- Las entrevistas las puede hacer:
  - El propio usuario sólo
  - El usuario con la IA
  - El usuario con un entrevistador
- El usuario recibe un link con la entrevista, tiene que estar logeado en la plataforma para poder responder.
- En el caso de una entrevista con un entrevistador:
  - Se permite entrevistadores externos que también tienen que tener un user con la plataforma. Pero role guest.
- Las entrevistas tienen un estado.

### Stages
- Cuando se mueven los candidatos entre stages. Si el stage tiene entrevista, se muestran los links para enviar al usuario.
- En un futuro se enviará un email con el link.
- Por ahora se muestra el link con un botón para copiarlo.
- Si la entrevista está pendiente, no debe permitir el cambio de stage. Hay que meterlo con el sistema de validación de stages.

---

## Estado Actual de la Implementación

### ✅ Implementado

#### 1. Estructura Base de Plantillas
- ✅ Entidad `InterviewTemplate` con campos básicos
- ✅ Secciones (`InterviewTemplateSection`) implementadas
- ✅ Preguntas (`InterviewTemplateQuestion`) implementadas
- ✅ Relación: Template → Sections → Questions
- ✅ Enum `InterviewTemplateStatusEnum` (ENABLED, DRAFT, DISABLED)
- ✅ Campo `allow_ai_questions` en template y sections

#### 2. Estructura Base de Entrevistas
- ✅ Entidad `Interview` con campos básicos
- ✅ Estados de entrevista (`InterviewStatusEnum`): PENDING, IN_PROGRESS, FINISHED, DISCARDED, PAUSED
- ✅ Métodos de transición de estado: `start()`, `finish()`, `pause()`, `resume()`, `discard()`
- ✅ Relación con candidatos, job positions, applications y workflow stages
- ✅ Campo `interviewers` (lista de nombres)
- ✅ Campo `score` (0-100) a nivel de entrevista

#### 3. Scoring Básico
- ✅ Score general de entrevista (0-100)
- ✅ Score por respuesta (`InterviewAnswer.score`)
- ✅ Comandos para puntuar respuestas (`ScoreInterviewAnswerCommand`)
- ✅ Queries para obtener resumen de scores (`GetInterviewScoreSummaryQuery`)

#### 4. Integración con Workflow Stages
- ✅ Campo `interview_configurations` en `WorkflowStage`
- ✅ Campo `workflow_stage_id` en `Interview`
- ✅ Sistema de validación de stages con JsonLogic (`validation_rules`)

#### 5. Modos de Entrevista
- ✅ Enum `InterviewModeEnum`: AUTOMATIC, AI, MANUAL

#### 6. Mejora de Plantillas por IA (en ejecución)
- ✅ Campo `allow_ai_questions` en template y sections
- ✅ Campo `allow_ai_override_questions` en sections
- ✅ Campo `allow_ai_followup` en questions
- ✅ Permite que la IA genere preguntas adicionales o diferentes durante la ejecución

---

### ❌ Pendiente / Incompleto

#### 1. Tipos de Plantillas (InterviewTemplateTypeEnum)
**Estado**: ✅ Completado
- ✅ `EXTENDED_PROFILE` - Implementado
- ✅ `POSITION_INTERVIEW` - Implementado
- ✅ `SCREENING` - **IMPLEMENTADO**
- ✅ `CUSTOM` - **IMPLEMENTADO**

**Ubicación**: `src/interview_bc/interview_template/domain/enums/interview_template.py`

#### 2. Tipos de Entrevistas (InterviewTypeEnum)
**Estado**: ✅ Completado
- ✅ `EXTENDED_PROFILE` - **IMPLEMENTADO**
- ✅ `POSITION_INTERVIEW` - **IMPLEMENTADO**
- ✅ `CUSTOM` - Implementado
- ⚠️ Valores legacy mantenidos para compatibilidad hacia atrás (deprecated):
  - `JOB_POSITION` (deprecated, usar `POSITION_INTERVIEW`)
  - `PLATFORM_ONBOARDING` (deprecated)
  - `COMPANY_ONBOARDING` (deprecated)
  - `PREMIUM_ONBOARDING` (deprecated)

**Ubicación**: `src/interview_bc/interview/domain/enums/interview_enums.py`

#### 3. Mejora de Plantillas por IA
**Estado**: ✅ Implementado

**Aclaración**: El requisito "Las plantillas pueden ser mejoradas por la IA. Es un check" se refiere a permitir que la IA haga más preguntas o diferentes preguntas durante la ejecución de la entrevista, NO a modificar el template.

**Implementación actual:**
- ✅ Campo `allow_ai_questions: bool` en `InterviewTemplate` 
- ✅ Campo `allow_ai_questions: bool` en `InterviewTemplateSection`
- ✅ Campo `allow_ai_override_questions: bool` en `InterviewTemplateSection` (permite reformular preguntas existentes)
- ✅ Campo `allow_ai_followup: bool` en `InterviewTemplateQuestion` (permite preguntas de seguimiento)

**Funcionalidad:**
- Cuando `allow_ai_questions` está activo, la IA puede generar preguntas adicionales durante la ejecución
- Cuando `allow_ai_override_questions` está activo, la IA puede reformular/modificar preguntas existentes
- Cuando `allow_ai_followup` está activo, la IA puede generar preguntas de seguimiento basadas en respuestas

**Ubicación**: `src/interview_bc/interview_template/domain/entities/interview_template.py`

#### 4. Sistema de Scoring Avanzado
**Estado**: ✅ Completado
- ✅ Score básico implementado (0-100 para entrevistas sin scoring_mode)
- ✅ **IMPLEMENTADO**: Modo de scoring (Distancia vs Absoluto) en plantillas - `ScoringModeEnum` creado
- ✅ **IMPLEMENTADO**: Campo `scoring_mode` en `InterviewTemplate`
- ✅ **IMPLEMENTADO**: Validación de scores 1-10 para plantillas con scoring_mode - Validación dinámica según template
- ✅ **IMPLEMENTADO**: Lógica de cálculo según modo de scoring - `InterviewScoreCalculator` implementado

**Ubicaciones**:
- ✅ Plantilla: `src/interview_bc/interview_template/domain/entities/interview_template.py` - Campo agregado
- ✅ Respuesta: `src/interview_bc/interview/application/commands/score_interview_answer.py` - Validación 1-10 implementada
- ✅ Cálculo: `src/interview_bc/interview/application/services/interview_score_calculator.py` - Lógica DISTANCE vs ABSOLUTE implementada

#### 5. Links de Entrevistas
**Estado**: ✅ Completado (Backend)
- ✅ **IMPLEMENTADO**: Generación de links únicos para entrevistas - Método `generate_link_token()`
- ✅ **IMPLEMENTADO**: Token único por entrevista para acceso seguro - Campo `link_token` y `link_expires_at`
- ✅ **IMPLEMENTADO**: Métodos de dominio - `get_shareable_link()`, `is_link_valid()`
- ✅ **IMPLEMENTADO**: Command `GenerateInterviewLinkCommand` para generar links
- ✅ **IMPLEMENTADO**: Endpoint `POST /api/company/interviews/{interview_id}/generate-link`
- ✅ **IMPLEMENTADO**: Endpoint `GET /api/candidate/interviews/{interview_id}/access?token={token}` - Acceso por token
- ✅ **IMPLEMENTADO**: Query `GetInterviewByTokenQuery` para validar token y obtener entrevista
- ✅ **IMPLEMENTADO**: Validación de token y expiración en repositorio
- ✅ **IMPLEMENTADO**: Schemas actualizados con campos de link
- ⏳ **PENDIENTE**: UI para mostrar/copiar links en stages - Requiere frontend

**Ubicaciones**:
- ✅ Domain: `src/interview_bc/interview/domain/entities/interview.py` - Campos y métodos agregados
- ✅ Application: `src/interview_bc/interview/application/commands/generate_interview_link.py`
- ✅ Presentation: `adapters/http/company_app/interview/routers/company_interview_router.py`

#### 6. Entrevistadores Externos (Guest Role)
**Estado**: ✅ Completado (Backend)
- ✅ Campo `interviewers` existe (lista de nombres) - Mantenido para compatibilidad
- ✅ **IMPLEMENTADO**: Rol `GUEST` agregado a `CompanyUserRole` para entrevistadores externos
- ✅ **IMPLEMENTADO**: Entidad `InterviewInterviewer` para relación entrevista-usuario
- ✅ **IMPLEMENTADO**: Tabla `interview_interviewers` con relación a usuarios
- ✅ **IMPLEMENTADO**: Command `InviteInterviewerCommand` para invitar entrevistadores
- ✅ **IMPLEMENTADO**: Command `AcceptInterviewerInvitationCommand` para aceptar invitaciones
- ✅ **IMPLEMENTADO**: Query `GetInterviewersByInterviewQuery` para obtener entrevistadores
- ✅ **IMPLEMENTADO**: Endpoints para invitar, aceptar y listar entrevistadores
- ⏳ **PENDIENTE**: Validación de permisos de entrevistador - Requiere lógica de autorización adicional
- ⏳ **PENDIENTE**: Envío de email de invitación - Requiere integración con sistema de notificaciones

**Ubicaciones**:
- ✅ Domain: `src/company_bc/company/domain/enums/company_user_role.py` - Rol GUEST agregado
- ✅ Domain: `src/interview_bc/interview/domain/entities/interview_interviewer.py` - Entidad creada
- ✅ Infrastructure: `src/interview_bc/interview/Infrastructure/models/interview_interviewer_model.py` - Modelo creado
- ✅ Infrastructure: `src/interview_bc/interview/Infrastructure/repositories/interview_interviewer_repository.py` - Repositorio creado
- ✅ Application: `src/interview_bc/interview/application/commands/invite_interviewer.py` - Command creado
- ✅ Application: `src/interview_bc/interview/application/queries/get_interviewers_by_interview.py` - Query creada
- ✅ Presentation: `adapters/http/company_app/interview/routers/company_interview_router.py` - Endpoints agregados
- ✅ Migration: `alembic/versions/add_interview_interviewers_table.py` - Migración creada

#### 7. Modos de Entrevista (Usuario solo, con IA, con Entrevistador)
**Estado**: ✅ Completado (Backend)
- ✅ Enum `InterviewModeEnum` existe (AUTOMATIC, AI, MANUAL)
- ✅ **IMPLEMENTADO**: Campo `interview_mode` en entidad `Interview`
- ✅ **IMPLEMENTADO**: Campo agregado a modelo SQLAlchemy y repositorio
- ✅ **IMPLEMENTADO**: Migración creada para agregar campo a base de datos
- ✅ **IMPLEMENTADO**: DTOs y schemas actualizados
- ⏳ **PENDIENTE**: UI para seleccionar modo de entrevista (requiere frontend)
- ⏳ **PENDIENTE**: Validación según modo seleccionado (lógica de negocio adicional)

**Ubicación**: 
- Domain: `src/interview_bc/interview/domain/entities/interview.py`
- Enum: `src/interview_bc/interview/domain/enums/interview_enums.py`
- Migration: `alembic/versions/add_interview_mode.py`

#### 8. Validación de Entrevistas Pendientes en Stages
**Estado**: ✅ Completado
- ✅ Sistema de validación de stages existe (`validation_rules` con JsonLogic)
- ✅ **IMPLEMENTADO**: Servicio `InterviewValidationService` para validar entrevistas pendientes
- ✅ **IMPLEMENTADO**: Query `GetPendingInterviewsByCandidateAndStageQuery` para obtener entrevistas pendientes
- ✅ **IMPLEMENTADO**: Integración con `ChangeStageCommandHandler` - Bloquea cambio de stage si hay entrevistas pendientes
- ✅ **IMPLEMENTADO**: Mensaje de error descriptivo cuando hay entrevistas pendientes
- ✅ **IMPLEMENTADO**: Endpoint `GET /api/company/interviews/candidate/{candidate_id}/stage/{workflow_stage_id}/pending`

**Ubicaciones**:
- ✅ Validation: `src/shared_bc/customization/field_validation/application/services/interview_validation_service.py`
- ✅ Workflow: `src/company_bc/company_candidate/application/commands/change_stage_command.py`
- ✅ Query: `src/interview_bc/interview/application/queries/get_pending_interviews_by_candidate_and_stage.py`

#### 9. UI para Links de Entrevistas en Stages
**Estado**: ❌ No implementado
- ✅ UI de stages existe (`WorkflowBoardPage`, `CandidateDetailPage`)
- ❌ **FALTA**: Componente para mostrar links de entrevistas cuando stage tiene `interview_configurations`
- ❌ **FALTA**: Botón para copiar link
- ❌ **FALTA**: Indicador visual de entrevistas pendientes
- ❌ **FALTA**: Lista de entrevistas asociadas al stage

**Ubicaciones**:
- Frontend: `client-vite/src/pages/workflow/`
- Frontend: `client-vite/src/pages/company/CandidateDetailPage.tsx`

#### 10. Envío de Email con Link (Futuro)
**Estado**: ⏳ Marcado como futuro
- ✅ Sistema de email existe (`EmailServiceInterface`)
- ❌ **FALTA**: Template de email para invitación a entrevista
- ❌ **FALTA**: Endpoint para enviar email con link
- ❌ **FALTA**: UI para trigger de envío de email

**Ubicación**: `src/notification_bc/notification/`

---

## Resumen de Tareas Pendientes

### ✅ Completado - Prioridad Alta
1. ✅ **Completar tipos de plantillas** - Agregados SCREENING y CUSTOM a InterviewTemplateTypeEnum
2. ✅ **Alinear tipos de entrevistas** - Actualizado InterviewTypeEnum con EXTENDED_PROFILE y POSITION_INTERVIEW
3. ✅ **Sistema de scoring avanzado** - Creado ScoringModeEnum (DISTANCE, ABSOLUTE) y agregado scoring_mode a InterviewTemplate
4. ✅ **Generación y validación de links** - Implementado sistema completo de links con tokens únicos
5. ✅ **Validación de entrevistas pendientes** - Implementado servicio y validación en ChangeStageCommandHandler

### ✅ Completado - Application & Presentation Layer
6. ✅ **Command GenerateInterviewLink** - Comando para generar links de entrevistas
7. ✅ **Query GetPendingInterviewsByCandidateAndStage** - Query para obtener entrevistas pendientes
8. ✅ **Query GetInterviewByToken** - Query para obtener entrevista por token de link
9. ✅ **Controller y endpoints** - Métodos y endpoints para generar links y obtener entrevistas pendientes
10. ✅ **Endpoint de acceso por token** - `GET /api/candidate/interviews/{interview_id}/access?token={token}`
11. ✅ **Schemas actualizados** - Todos los schemas incluyen campos de link y scoring_mode
12. ✅ **DTOs actualizados** - DTOs incluyen link_token, link_expires_at y scoring_mode

### ✅ Completado - Modos de Entrevista
15. ✅ **Diferenciación de modos de entrevista** - Campo `interview_mode` agregado a entidad Interview

### ✅ Completado - Sistema de Entrevistadores Externos
14. ✅ **Rol GUEST agregado** - Agregado a `CompanyUserRole` para entrevistadores externos
15. ✅ **Entidad InterviewInterviewer** - Relación entrevista-usuario implementada
16. ✅ **Command InviteInterviewer** - Comando para invitar entrevistadores
17. ✅ **Command AcceptInvitation** - Comando para aceptar invitaciones
18. ✅ **Query GetInterviewersByInterview** - Query para obtener entrevistadores
19. ✅ **Endpoints de gestión** - Endpoints para invitar, aceptar y listar entrevistadores
20. ✅ **Migración creada** - Tabla interview_interviewers creada

### ⏳ Pendiente - Prioridad Media
13. ⏳ **UI para mostrar/copiar links en stages** - Componente frontend para mostrar links en stages (requiere frontend)
14. ⏳ **Validación de permisos de entrevistador** - Lógica de autorización adicional para entrevistadores
15. ⏳ **Envío de email de invitación** - Integración con sistema de notificaciones

### ✅ Completado - Validación de Scores
17. ✅ **Validación de scores 1-10** - Implementada validación dinámica según scoring_mode del template

### ✅ Completado - Lógica de Scoring
19. ✅ **Lógica de cálculo según modo de scoring** - Implementado `InterviewScoreCalculator` con lógica DISTANCE vs ABSOLUTE

### ✅ Completado - Sistema de Entrevistadores Externos
17. ✅ **Rol GUEST para entrevistadores externos** - Agregado a CompanyUserRole
18. ✅ **Entidad InterviewInterviewer** - Creada con métodos de dominio (accept_invitation, is_accepted)
19. ✅ **Repositorio InterviewInterviewer** - Implementado con métodos CRUD y queries específicas
20. ✅ **Command InviteInterviewer** - Invitar entrevistador a entrevista
21. ✅ **Command AcceptInterviewerInvitation** - Aceptar invitación de entrevistador
22. ✅ **Query GetInterviewersByInterview** - Obtener lista de entrevistadores de una entrevista
23. ✅ **Endpoints de gestión de entrevistadores** - Invitar, aceptar y listar entrevistadores
24. ✅ **Migración add_interview_interviewers_table** - Tabla y relaciones creadas
25. ✅ **Método helper is_user_interviewer** - Verificar si usuario es entrevistador

### ✅ Completado - Validación de Permisos de Entrevistador
26. ✅ **Servicio InterviewPermissionService** - Servicio para validar permisos de entrevistadores
27. ✅ **Validación en InviteInterviewerCommand** - Solo usuarios de la compañía (ADMIN, OWNER, RECRUITER) pueden invitar
28. ✅ **Validación en AcceptInterviewerInvitationCommand** - Solo el usuario invitado puede aceptar su propia invitación
29. ✅ **Métodos de validación** - can_user_invite_interviewer, can_user_accept_invitation, can_user_access_interview, can_user_modify_interview
30. ✅ **Excepción InterviewPermissionDeniedError** - Excepción específica para errores de permisos
31. ✅ **Integración en endpoints** - Validación de permisos en endpoints de invitación y aceptación
32. ✅ **Validación de pertenencia a compañía** - Métodos does_interview_belong_to_company, can_user_access_interview_by_company, can_user_modify_interview_by_company
33. ✅ **Verificación por job_position y candidate** - El servicio verifica pertenencia a través de job_position.company_id o company_candidate

### ⏳ Pendiente - Prioridad Baja (No Crítico)
32. ⏳ **Envío de email con link** - Marcado como futuro en especificación
33. ⏳ **UI para mostrar/copiar links en stages** - Requiere frontend

---

## Archivos Clave a Modificar

### Domain Layer
- `src/interview_bc/interview_template/domain/enums/interview_template.py` - Agregar SCREENING y CUSTOM
- `src/interview_bc/interview/domain/enums/interview_enums.py` - Alinear tipos de entrevistas
- `src/interview_bc/interview_template/domain/entities/interview_template.py` - Agregar scoring_mode, ai_enhanced
- `src/interview_bc/interview/domain/entities/interview.py` - Agregar link/token, mejorar modos
- `src/interview_bc/interview_template/domain/entities/interview_template_question.py` - Validar scores 1-10

### Application Layer
- `src/interview_bc/interview/application/commands/` - Comandos para generar links, invitar entrevistadores
- `src/interview_bc/interview/application/queries/` - Queries para entrevistas pendientes, links

### Infrastructure Layer
- `src/interview_bc/interview/Infrastructure/models/interview_model.py` - Agregar campos de link/token
- `src/interview_bc/interview_template/infrastructure/models/interview_template_model.py` - Agregar scoring_mode

### Presentation Layer
- `adapters/http/company_app/` - Endpoints para links, compartir entrevistas
- `client-vite/src/pages/workflow/` - UI para links en stages
- `client-vite/src/components/interview/` - Componentes para compartir/copiar links

### Validation
- `src/shared_bc/customization/field_validation/` - Agregar regla de validación de entrevistas pendientes



