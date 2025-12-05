# Cuándo se Ejecutan las Validaciones de Entrevistas

## 📍 Estado Actual de las Validaciones

### ✅ Validaciones Implementadas y Activas

#### 1. **Invitar Entrevistador** (`InviteInterviewerCommandHandler`)
**Cuándo se ejecuta:** Cuando se llama al endpoint `POST /api/company/interviews/{interview_id}/interviewers/invite`

**Flujo:**
```
1. Usuario hace request → Router → Controller → CommandBus
2. CommandHandler.execute() se ejecuta
3. ✅ VALIDACIÓN: permission_service.can_user_invite_interviewer()
   - Verifica que el usuario pertenece a la compañía
   - Verifica que el usuario está activo
   - Verifica que el rol es ADMIN, OWNER o RECRUITER
4. Si falla → Lanza InterviewPermissionDeniedError → HTTP 403
5. Si pasa → Crea la relación InterviewInterviewer
```

**Ubicación:** `src/interview_bc/interview/application/commands/invite_interviewer.py:55`

---

#### 2. **Aceptar Invitación** (`AcceptInterviewerInvitationCommandHandler`)
**Cuándo se ejecuta:** Cuando se llama al endpoint `POST /api/company/interviews/interviewers/{interviewer_id}/accept`

**Flujo:**
```
1. Usuario hace request → Router → Controller → CommandBus
2. CommandHandler.execute() se ejecuta
3. ✅ VALIDACIÓN: permission_service.can_user_accept_invitation()
   - Verifica que el usuario que acepta es el mismo que fue invitado
4. Si falla → Lanza InterviewPermissionDeniedError → HTTP 403
5. Si pasa → Marca la invitación como aceptada
```

**Ubicación:** `src/interview_bc/interview/application/commands/accept_interviewer_invitation.py:44`

---

### ⚠️ Validaciones NO Implementadas (TODOs)

Las siguientes validaciones **NO se están ejecutando** actualmente, aunque los métodos están disponibles:

#### 1. **Obtener Entrevista** (`GET /api/company/interviews/{interview_id}`)
**Estado:** ❌ NO VALIDA
**TODO en:** `adapters/http/company_app/interview/routers/company_interview_router.py:155`

**Debería validar:**
```python
# Debería usar:
permission_service.can_user_access_interview_by_company(
    user_id=company_user_id,
    company_id=company_id,
    interview=interview
)
```

**Riesgo:** Un usuario podría acceder a entrevistas de otras compañías si conoce el ID.

---

#### 2. **Crear Entrevista** (`POST /api/company/interviews`)
**Estado:** ❌ NO VALIDA
**TODO en:** `adapters/http/company_app/interview/routers/company_interview_router.py:172`

**Debería validar:**
```python
# Antes de crear, verificar que:
# - candidate_id pertenece a la compañía (a través de CompanyCandidate)
# - job_position_id pertenece a la compañía (a través de JobPosition.company_id)
```

**Riesgo:** Un usuario podría crear entrevistas con candidatos o posiciones de otras compañías.

---

#### 3. **Actualizar Entrevista** (`PUT /api/company/interviews/{interview_id}`)
**Estado:** ❌ NO VALIDA
**TODO en:** `adapters/http/company_app/interview/routers/company_interview_router.py:204`

**Debería validar:**
```python
# Debería usar:
permission_service.can_user_modify_interview_by_company(
    user_id=company_user_id,
    company_id=company_id,
    interview=interview
)
```

**Riesgo:** Un usuario podría modificar entrevistas de otras compañías.

---

#### 4. **Iniciar Entrevista** (`POST /api/company/interviews/{interview_id}/start`)
**Estado:** ❌ NO VALIDA
**TODO en:** `adapters/http/company_app/interview/routers/company_interview_router.py:223`

**Debería validar:**
```python
# Debería usar:
permission_service.can_user_modify_interview_by_company(
    user_id=company_user_id,
    company_id=company_id,
    interview=interview
)
```

**Riesgo:** Un usuario podría iniciar entrevistas de otras compañías.

---

#### 5. **Finalizar Entrevista** (`POST /api/company/interviews/{interview_id}/finish`)
**Estado:** ❌ NO VALIDA
**TODO en:** `adapters/http/company_app/interview/routers/company_interview_router.py:247`

**Debería validar:**
```python
# Debería usar:
permission_service.can_user_modify_interview_by_company(
    user_id=company_user_id,
    company_id=company_id,
    interview=interview
)
```

**Riesgo:** Un usuario podría finalizar entrevistas de otras compañías.

---

#### 6. **Generar Link** (`POST /api/company/interviews/{interview_id}/generate-link`)
**Estado:** ❌ NO VALIDA
**TODO en:** `adapters/http/company_app/interview/routers/company_interview_router.py:333`

**Debería validar:**
```python
# Debería usar:
permission_service.can_user_modify_interview_by_company(
    user_id=company_user_id,
    company_id=company_id,
    interview=interview
)
```

**Riesgo:** Un usuario podría generar links de entrevistas de otras compañías.

---

#### 7. **Obtener Entrevistas Pendientes** (`GET /api/company/interviews/candidate/{candidate_id}/stage/{workflow_stage_id}/pending`)
**Estado:** ❌ NO VALIDA
**TODO en:** `adapters/http/company_app/interview/routers/company_interview_router.py:353`

**Debería validar:**
```python
# Verificar que candidate_id pertenece a la compañía
# Verificar que workflow_stage_id pertenece a la compañía
```

**Riesgo:** Un usuario podría ver entrevistas pendientes de otras compañías.

---

#### 8. **Obtener Entrevistadores** (`GET /api/company/interviews/{interview_id}/interviewers`)
**Estado:** ❌ NO VALIDA
**TODO en:** `adapters/http/company_app/interview/routers/company_interview_router.py:412`

**Debería validar:**
```python
# Debería usar:
permission_service.can_user_access_interview_by_company(
    user_id=company_user_id,
    company_id=company_id,
    interview=interview
)
```

**Riesgo:** Un usuario podría ver entrevistadores de entrevistas de otras compañías.

---

## 🔄 Flujo de Ejecución de Validaciones

### Validaciones en Command Handlers (✅ Implementadas)

```
Request HTTP
    ↓
Router (FastAPI)
    ↓
Controller
    ↓
CommandBus.execute(command)
    ↓
CommandHandler.execute()
    ↓
✅ VALIDACIÓN: permission_service.can_user_*()
    ↓
Si pasa → Ejecuta acción
Si falla → Lanza InterviewPermissionDeniedError → HTTP 403
```

### Validaciones en Endpoints (❌ Faltan)

```
Request HTTP
    ↓
Router (FastAPI)
    ↓
❌ FALTA VALIDACIÓN aquí
    ↓
Controller
    ↓
CommandBus/QueryBus
    ↓
Handler (sin validación de pertenencia a compañía)
```

---

## 🎯 Resumen

### ✅ Validaciones Activas (2)
1. Invitar entrevistador
2. Aceptar invitación

### ❌ Validaciones Faltantes (8+)
1. Obtener entrevista
2. Crear entrevista
3. Actualizar entrevista
4. Iniciar entrevista
5. Finalizar entrevista
6. Generar link
7. Obtener entrevistas pendientes
8. Obtener entrevistadores
9. Y otros endpoints...

---

## 💡 Recomendación

**Las validaciones deberían ejecutarse en dos lugares:**

1. **En los Routers/Controllers** (antes de llamar a handlers):
   - Validar pertenencia a compañía
   - Validar permisos de acceso/modificación
   - Lanzar HTTP 403 si falla

2. **En los Command Handlers** (ya implementado):
   - Validar permisos específicos de la acción
   - Lanzar excepciones de dominio si falla

**Ventajas de validar en Router/Controller:**
- Respuesta HTTP más rápida (sin ejecutar handlers)
- Código más claro y centralizado
- Fácil de auditar y mantener


