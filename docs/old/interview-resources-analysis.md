# Análisis: InterviewResource vs InterviewFullResource

## Resumen Ejecutivo

Necesitamos dos tipos de Resources para Interview:
- **`InterviewResource`**: Tiene los mismos campos que el DTO (solo datos del interview). Se usa para **edición** porque el formulario solo necesita los campos del interview que se pueden modificar.
- **`InterviewFullResource`**: Contiene información agregada/denormalizada:
  - Interview (datos básicos del interview)
  - Candidate (información del candidato: name, email, etc.)
  - JobPosition (información de la posición: title, etc.)
  - Workflow (información del workflow)
  - Score (puntuación y resumen)
  - Stage (información del workflow stage)

**Principio**: 
1. **Para edición**: Se usa `InterviewResource` porque:
   - El formulario solo necesita los campos del interview que se pueden modificar
   - No necesita información denormalizada de otras entidades
   - El usuario modifica y envía de vuelta (PUT) solo los campos del interview

2. **Para listados/detalle**: Se usa `InterviewFullResource` porque:
   - La tabla necesita mostrar información denormalizada (`candidate_name`, `job_position_title`, etc.)
   - El detalle necesita mostrar información completa de todas las entidades relacionadas
   - Incluye información agregada (score, workflow, stage)

**Conclusión**: 
- **Edición** → `InterviewResource` (solo campos del interview)
- **Listados/Detalle** → `InterviewFullResource` (con información denormalizada y agregada)

## Endpoints y Uso en Frontend

### 1. GET `/api/company/interviews` (List)

**Uso en Frontend**: `CompanyInterviewsPage.tsx` - Tabla de entrevistas

**Campos específicos usados** (líneas 903-1070):
```typescript
// En la tabla muestra:
interview.title                                    // ✅ Necesita (línea 905)
interview.candidate_name                           // ✅ Necesita
interview.job_position_title                      // ✅ Necesita
interview.scheduled_at                             // ✅ Necesita
interview.deadline_date                            // ✅ Necesita
interview.status                                   // ✅ Necesita
interview.interviewer_names                        // ✅ Necesita
interview.required_role_names                      // ✅ Necesita
interview.is_incomplete                            // ✅ Necesita (para warning icon)
interview.score                                    // ✅ Necesita (línea 1023) - solo para mostrar
interview.link_token                               // ✅ Necesita (línea 1064) - para copiar link
```

**Resource a usar**: ❌ **`InterviewFullResource`** (completo con información denormalizada)
- Actualmente retorna `InterviewListResource` con lista de `InterviewResource` (solo campos del interview)
- **PROBLEMA**: El listado necesita mostrar información denormalizada:
  - `candidate_name`, `candidate_email` (información del Candidate)
  - `job_position_title` (información del JobPosition)
  - `interviewer_names` (información de los entrevistadores)
  - `required_role_names` (información de los roles)
  - `interview_template_name`, `workflow_stage_name` (información de template y stage)
- **SOLUCIÓN**: Cambiar a `InterviewListResource` con lista de `InterviewFullResource`

---

### 2. GET `/api/company/interviews/{id}` (Edit)

**Uso en Frontend**: 
- `EditInterviewPage.tsx` - Formulario de edición completo

**Campos específicos usados** (líneas 122-133):
```typescript
setFormData({
  title: data.title || undefined,                    // ✅ Necesita
  description: data.description || undefined,        // ✅ Necesita
  scheduled_at: data.scheduled_at,                   // ✅ Necesita
  deadline_date: data.deadline_date,                 // ✅ Necesita
  process_type: data.process_type,                   // ✅ Necesita
  required_roles: data.required_roles,              // ✅ Necesita
  interviewers: data.interviewers || [],             // ✅ Necesita
  interviewer_notes: data.interviewer_notes,         // ✅ Necesita (campos del interview)
  feedback: data.feedback,                           // ✅ Necesita (campos del interview)
  score: data.score,                                 // ✅ Necesita (campos del interview)
});
```

**Resource a usar**: ✅ **`InterviewResource`** (solo campos del interview)
- Actualmente usa `InterviewResource` (correcto)
- **RAZÓN**: Para edición se usa `InterviewResource` porque:
  - El formulario solo necesita los campos del interview que se pueden modificar
  - No necesita información denormalizada de otras entidades (candidate, job_position, etc.)
  - El usuario modifica y envía de vuelta (PUT) solo los campos del interview
  - `InterviewResource` tiene los mismos campos que el DTO (todos los campos editables del interview)
- **CORRECTO**: Ya está usando `InterviewResource` ✅

---

### 2b. GET `/api/company/interviews/{id}/view` (View/Detail) - NUEVO ENDPOINT

**Uso en Frontend**: 
- `CompanyInterviewDetailPage.tsx` - Vista detallada completa

**Campos específicos usados** (líneas 195-320):
```typescript
// Usa:
interview.title                                    // ✅ Necesita
interview.description                              // ✅ Necesita
interview.status                                  // ✅ Necesita
interview.interview_type                          // ✅ Necesita
interview.scheduled_at                            // ✅ Necesita
interview.started_at                              // ✅ Necesita
interview.completed_at                            // ✅ Necesita
interview.score                                   // ✅ Necesita
interview.notes                                   // ✅ Necesita
// + Información denormalizada:
candidate_name                                    // ✅ Necesita (de Candidate)
job_position_title                                // ✅ Necesita (de JobPosition)
interviewer_names                                 // ✅ Necesita (de CompanyUser/User)
workflow_stage_name                               // ✅ Necesita (de WorkflowStage)
// + Información agregada:
score_summary                                     // ✅ Necesita (información agregada)
```

**Resource a usar**: ❌ **`InterviewFullResource`** (completo con información denormalizada)
- **PROBLEMA**: Actualmente no existe este endpoint separado
- **SOLUCIÓN**: Crear nuevo endpoint `GET /api/company/interviews/{id}/view` que retorne `InterviewFullResource`
- **RAZÓN**: Para vista/detalle se necesita:
  - Todos los campos del interview
  - Información denormalizada (candidate_name, job_position_title, etc.)
  - Información agregada (score_summary, workflow_info, etc.)

---

### 3. GET `/api/company/interviews/calendar`

**Uso en Frontend**: `CompanyInterviewsPage.tsx` - Vista de calendario

**Datos necesarios**:
- `id`, `candidate_name`, `scheduled_at`, `deadline_date`
- `status`, `interview_type`
- Datos básicos para mostrar en calendario
- **Información denormalizada**: `candidate_name` (no solo ID)

**Resource a usar**: ❌ **`InterviewFullResource`** (completo con información denormalizada)
- Actualmente retorna `List[InterviewResource]` (solo campos del interview)
- **PROBLEMA**: El calendario necesita mostrar información denormalizada (`candidate_name`, `job_position_title`, etc.)
- **SOLUCIÓN**: Cambiar a `List[InterviewFullResource]`

---

### 4. GET `/api/company/interviews/overdue`

**Uso en Frontend**: `CompanyInterviewsPage.tsx` - Lista de entrevistas vencidas

**Datos necesarios**:
- `id`, `candidate_name`, `deadline_date`, `status`
- Datos básicos para mostrar en lista
- **Información denormalizada**: `candidate_name`, `job_position_title` (no solo IDs)

**Resource a usar**: ❌ **`InterviewFullResource`** (completo con información denormalizada)
- Actualmente retorna `List[InterviewResource]` (solo campos del interview)
- **PROBLEMA**: La lista necesita mostrar información denormalizada (`candidate_name`, `job_position_title`, etc.)
- **SOLUCIÓN**: Cambiar a `List[InterviewFullResource]`

---

### 5. GET `/api/company/interviews/statistics`

**Uso en Frontend**: `CompanyInterviewsPage.tsx` - Métricas/estadísticas

**Datos necesarios**: Solo estadísticas, no interview data

**Resource a usar**: ✅ `InterviewStatsResource`
- Ya está correcto

---

### 6. POST/PUT `/api/company/interviews` (Create/Update)

**Uso en Frontend**: `CreateInterviewPage.tsx`, `EditInterviewPage.tsx`

**Datos necesarios**: Solo mensaje de éxito

**Resource a usar**: ✅ `InterviewActionResource`
- Ya está correcto

---

### 7. POST `/api/company/interviews/{id}/start` y `/finish`

**Uso en Frontend**: `CompanyInterviewDetailPage.tsx`

**Datos necesarios**: Solo mensaje de éxito

**Resource a usar**: ✅ `InterviewActionResource`
- Ya está correcto

---

### 8. GET `/api/company/interviews/{id}/score-summary`

**Uso en Frontend**: `CompanyInterviewDetailPage.tsx`

**Datos necesarios**: Resumen de puntuación

**Resource a usar**: ✅ `InterviewScoreSummaryResource`
- Ya está correcto

---

### 9. POST `/api/company/interviews/{id}/generate-link`

**Uso en Frontend**: `CompanyInterviewsPage.tsx`

**Datos necesarios**: Link generado y metadata

**Resource a usar**: ✅ `InterviewLinkResource`
- Ya está correcto

---

## Problemas Identificados

### ❌ Problema Principal

**Endpoint**: `GET /api/company/interviews/{id}`

**Problema**: 
- Actualmente retorna `InterviewResource` (ligero)
- `EditInterviewPage.tsx` necesita TODOS los campos para el formulario:
  - `title`, `description`
  - `interviewer_notes`, `candidate_notes`
  - `feedback`, `score`
  - `free_answers`
  - Todos los campos completos

**Impacto**: 
- El frontend puede no tener acceso a todos los campos necesarios para edición
- Puede causar errores al intentar editar campos que no están en el Resource ligero

---

## Solución Propuesta

### 1. Renombrar `InterviewManagementResponse` → `InterviewFullResource`

**Ubicación**: `adapters/http/company_app/interview/schemas/interview_management.py`

**Cambios**:
- Renombrar clase `InterviewManagementResponse` → `InterviewFullResource`
- Mantener todos los campos actuales (es el Resource completo)
- Mantener métodos `from_dto()` y `from_list_dto()`

### 2. Definir `InterviewResource` vs `InterviewFullResource`

**`InterviewResource`** (solo campos del interview - para edición):
- Tiene los mismos campos que el DTO (`InterviewDto`)
- Solo datos del interview que se pueden modificar:
  - `id`, `candidate_id`, `job_position_id`, `application_id`, etc.
  - `title`, `description`, `status`, `interview_type`, `interview_mode`, `process_type`
  - `scheduled_at`, `deadline_date`, `started_at`, `finished_at`
  - `required_roles` (IDs), `interviewers` (IDs)
  - `interviewer_notes`, `candidate_notes`, `feedback`, `score`
  - `link_token`, `link_expires_at`
  - `created_at`, `updated_at`, `created_by`, `updated_by`
- **NO incluye**: Información denormalizada de otras entidades (candidate name, job position title, etc.)
- **Uso**: Edición (formulario que modifica solo campos del interview)

**`InterviewFullResource`** (con información agregada/denormalizada - para listados/detalle):
- Contiene `InterviewResource` + información agregada:
  - **Interview**: Todos los campos del interview (como `InterviewResource`)
  - **Candidate**: `candidate_name`, `candidate_email` (información denormalizada)
  - **JobPosition**: `job_position_title` (información denormalizada)
  - **Workflow**: Información del workflow relacionado
  - **Score**: Puntuación y resumen agregado
  - **Stage**: `workflow_stage_name` (información denormalizada)
  - **Otros**: `interviewer_names`, `required_role_names`, `interview_template_name` (nombres denormalizados)
- **Uso**: Listados, detalle completo (donde se necesita mostrar información de entidades relacionadas)

**Conclusión**: 
- **Edición** → `InterviewResource` (solo campos editables del interview)
- **Listados/Detalle** → `InterviewFullResource` (con información denormalizada y agregada)

### 3. Actualizar Controller

**Método 1**: `get_interview_by_id()` (para edición)
- Retornar `InterviewResource` (solo campos del interview)
- Usado por `EditInterviewPage.tsx`
- Conversión directa desde `InterviewDto`

**Método 2**: `get_interview_view()` (nuevo - para vista/detalle)
- Retornar `InterviewFullResource` (con información denormalizada)
- Usado por `CompanyInterviewDetailPage.tsx`
- Conversión desde `InterviewDto` + queries adicionales para obtener información denormalizada

### 4. Actualizar Router

**Endpoint 1**: `GET /api/company/interviews/{id}` (edición)
- `response_model=InterviewResource`
- Tipo de retorno: `InterviewResource`
- Usado por: `EditInterviewPage.tsx`

**Endpoint 2**: `GET /api/company/interviews/{id}/view` (nuevo - vista/detalle)
- `response_model=InterviewFullResource`
- Tipo de retorno: `InterviewFullResource`
- Usado por: `CompanyInterviewDetailPage.tsx`

---

## Plan de Implementación

### Paso 1: Renombrar `InterviewManagementResponse` → `InterviewFullResource`
- [ ] Renombrar clase en `interview_management.py`
- [ ] Actualizar imports en controller
- [ ] Actualizar imports en router

### Paso 2: Verificar/Crear `InterviewResource`
- [ ] Verificar que `InterviewResource` tiene los mismos campos que `InterviewDto` (solo campos del interview)
- [ ] Si no existe, crear `InterviewResource` con todos los campos del `InterviewDto`
- [ ] Implementar `from_dto()` para conversión desde `InterviewDto`
- [ ] **NO incluir**: Información denormalizada (candidate_name, job_position_title, etc.)

### Paso 3: Actualizar Controller
- [ ] Mantener `get_interview_by_id()` retornando `InterviewResource` (para edición)
- [ ] Crear nuevo método `get_interview_view()` que retorne `InterviewFullResource` (para vista/detalle)
- [ ] Cambiar `list_interviews()` para retornar `InterviewListResource` con `InterviewFullResource[]` (necesita información denormalizada)
- [ ] Actualizar métodos que retornan listas (`get_interview_calendar`, `get_overdue_interviews`) para usar `InterviewFullResource` (necesitan información denormalizada)

### Paso 4: Actualizar Router
- [ ] Mantener `GET /api/company/interviews/{id}` retornando `InterviewResource` (para edición)
- [ ] Crear nuevo endpoint `GET /api/company/interviews/{id}/view` retornando `InterviewFullResource` (para vista/detalle)
- [ ] Cambiar `GET /api/company/interviews` a `InterviewListResource` con `InterviewFullResource[]` (necesita información denormalizada)
- [ ] Cambiar `GET /api/company/interviews/calendar` a `List[InterviewFullResource]` (necesita información denormalizada)
- [ ] Cambiar `GET /api/company/interviews/overdue` a `List[InterviewFullResource]` (necesita información denormalizada)

### Paso 5: Actualizar Frontend
- [ ] `EditInterviewPage.tsx`: Usar `GET /api/company/interviews/{id}` (retorna `InterviewResource`) ✅ Ya está correcto
- [ ] `CompanyInterviewDetailPage.tsx`: Cambiar a usar `GET /api/company/interviews/{id}/view` (retorna `InterviewFullResource`)
- [ ] Verificar que `CompanyInterviewsPage.tsx` funciona con `InterviewFullResource` (tiene acceso a `candidate_name`, `job_position_title`, etc.)

---

## Estructura Final de Resources

```python
# Resource para edición (solo campos del interview)
class InterviewResource(BaseModel):
    # Mismos campos que InterviewDto (solo datos del interview)
    id: str
    candidate_id: str
    job_position_id: Optional[str]
    application_id: Optional[str]
    interview_template_id: Optional[str]
    workflow_stage_id: Optional[str]
    process_type: Optional[str]
    interview_type: str
    interview_mode: Optional[str]
    status: str
    title: Optional[str]
    description: Optional[str]
    scheduled_at: Optional[datetime]
    deadline_date: Optional[datetime]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    duration_minutes: Optional[int]
    required_roles: List[str]  # IDs
    interviewers: List[str]  # IDs
    interviewer_notes: Optional[str]
    candidate_notes: Optional[str]
    feedback: Optional[str]
    score: Optional[float]
    free_answers: Optional[str]
    link_token: Optional[str]
    link_expires_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]
    # NO incluye: candidate_name, job_position_title, interviewer_names, etc.
    
    @classmethod
    def from_dto(cls, dto: InterviewDto) -> "InterviewResource":
        # Conversión directa desde DTO (solo campos del interview)
        pass

# Resource completo (con información agregada/denormalizada)
class InterviewFullResource(BaseModel):
    # Contiene InterviewResource + información agregada
    # Campos del interview (como InterviewResource)
    id: str
    candidate_id: str
    job_position_id: Optional[str]
    # ... todos los campos de InterviewResource
    
    # Información agregada/denormalizada
    candidate_name: Optional[str]  # ✅ De Candidate
    candidate_email: Optional[str]  # ✅ De Candidate
    job_position_title: Optional[str]  # ✅ De JobPosition
    interviewer_names: List[str]  # ✅ De CompanyUser/User
    required_role_names: List[str]  # ✅ De CompanyRole
    interview_template_name: Optional[str]  # ✅ De InterviewTemplate
    workflow_stage_name: Optional[str]  # ✅ De WorkflowStage
    score_summary: Optional[dict]  # ✅ Información agregada de Score
    workflow_info: Optional[dict]  # ✅ Información del Workflow
    
    @classmethod
    def from_list_dto(cls, dto: InterviewListDto) -> "InterviewFullResource":
        # Conversión desde ReadModel (ya tiene todos los datos denormalizados)
        pass
    
    @classmethod
    def from_dto(cls, query_bus: QueryBus, dto: InterviewDto) -> "InterviewFullResource":
        # Conversión completa desde DTO (hace queries adicionales para obtener información denormalizada)
        pass
```

---

## Resumen de Cambios por Endpoint

| Endpoint | Resource Actual | Resource Propuesto | Razón |
|----------|----------------|-------------------|-------|
| `GET /api/company/interviews` | `InterviewListResource` (con `InterviewResource[]`) | ❌ → `InterviewFullResource[]` | Listado necesita información denormalizada (candidate_name, job_position_title, etc.) |
| `GET /api/company/interviews/{id}` | `InterviewResource` | ✅ Mantener `InterviewResource` | Para edición (solo campos editables del interview) |
| `GET /api/company/interviews/{id}/view` | ❌ No existe | ✅ Crear nuevo → `InterviewFullResource` | Para vista/detalle (campos del interview + información denormalizada) |
| `GET /api/company/interviews/calendar` | `List[InterviewResource]` | ❌ → `List[InterviewFullResource]` | Calendario necesita información denormalizada |
| `GET /api/company/interviews/overdue` | `List[InterviewResource]` | ❌ → `List[InterviewFullResource]` | Lista necesita información denormalizada |
| `GET /api/company/interviews/statistics` | `InterviewStatsResource` | ✅ Sin cambios | Solo estadísticas |
| `POST /api/company/interviews` | `InterviewActionResource` | ✅ Sin cambios | Solo mensaje |
| `PUT /api/company/interviews/{id}` | `InterviewActionResource` | ✅ Sin cambios | Solo mensaje |
| `POST /api/company/interviews/{id}/start` | `InterviewActionResource` | ✅ Sin cambios | Solo mensaje |
| `POST /api/company/interviews/{id}/finish` | `InterviewActionResource` | ✅ Sin cambios | Solo mensaje |
| `GET /api/company/interviews/{id}/score-summary` | `InterviewScoreSummaryResource` | ✅ Sin cambios | Resumen específico |
| `POST /api/company/interviews/{id}/generate-link` | `InterviewLinkResource` | ✅ Sin cambios | Link específico |

---

## Notas Adicionales

1. **`InterviewListDto`** ya tiene todos los datos denormalizados del ReadModel, por lo que `InterviewResource.from_list_dto()` puede obtener todos los campos básicos sin queries adicionales.

2. **`InterviewDto`** necesita queries adicionales para obtener datos completos (candidate, job_position), por lo que `InterviewFullResource.from_dto()` debe usar `QueryBus` para hacer esas queries.

3. **Principio de Listados**: Para listados siempre usar `InterviewFullResource` porque:
   - La tabla necesita mostrar información denormalizada (nombres, no solo IDs)
   - `candidate_name`, `job_position_title`, `interviewer_names`, `required_role_names` son esenciales para la UI
   - El ReadModel ya trae toda esta información denormalizada, así que no hay overhead

4. **Principio de Edición**: Para edición usar `InterviewResource` porque:
   - El formulario solo necesita los campos del interview que se pueden modificar
   - Tiene los mismos campos que el DTO (todos los campos editables del interview)
   - No necesita información denormalizada de otras entidades
   - El usuario modifica y envía de vuelta (PUT request) solo los campos del interview

5. **Principio de Detalle**: Para detalle completo usar `InterviewFullResource` porque:
   - Necesita mostrar información de todas las entidades relacionadas
   - Incluye información agregada (score, workflow, stage)
   - Tiene información denormalizada para mostrar en la UI

6. **Solución para `GET /api/company/interviews/{id}`**: Tener dos endpoints separados:
   - **`GET /api/company/interviews/{id}`**: Retorna `InterviewResource` (solo campos del interview)
     - Para edición: ✅ Perfecto (solo campos editables)
     - Usado por: `EditInterviewPage.tsx`
   - **`GET /api/company/interviews/{id}/view`**: Retorna `InterviewFullResource` (campos del interview + información denormalizada)
     - Para vista/detalle: ✅ Perfecto (tiene toda la información)
     - Usado por: `CompanyInterviewDetailPage.tsx`
   - **Ventajas**:
     - Separación clara de responsabilidades
     - Edición solo obtiene lo necesario (más eficiente)
     - Vista obtiene toda la información en una sola llamada

7. **Si se necesita más información**: En casos específicos donde se necesite información adicional:
   - Se pueden enviar múltiples resources en la respuesta (ej: `{ interview: InterviewFullResource, related_data: OtherResource }`)
   - Se pueden crear endpoints específicos que retornen la información necesaria

