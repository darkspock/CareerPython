# Sección de Empresas - Modelo Lógico

## Visión General

La sección de empresas permite a las organizaciones gestionar candidatos para sus procesos de selección, respetando la propiedad de los datos del candidato y su privacidad.

## Principios Fundamentales

1. **Los datos son del candidato**: El candidato es el propietario de su información
2. **Multi-empresa**: Un candidato puede estar vinculado a múltiples empresas
3. **Ownership confirmado**: Cuando un usuario toma ownership, controla sus datos
4. **Empresa como observador**: Una vez el usuario toma ownership, la empresa solo puede ver y comentar

## Modelo de Datos

### 1. Company (Empresa)

Representa una organización que usa la plataforma para gestionar candidatos.

```python
Company:
  - id: UUID
  - name: String (nombre de la empresa)
  - domain: String (dominio corporativo, ej: "company.com")
  - logo_url: String (opcional)
  - settings: JSON (configuración específica)
  - status: Enum [active, suspended, deleted]
  - created_at: DateTime
  - updated_at: DateTime
```

### 2. CompanyUser (Usuario de Empresa)

Usuarios que trabajan para una empresa (reclutadores, HR, managers).

```python
CompanyUser:
  - id: UUID
  - company_id: UUID (FK → Company)
  - user_id: UUID (FK → User)
  - role: Enum [admin, recruiter, viewer]
  - permissions: JSON
    {
      "can_create_candidates": bool,
      "can_invite_candidates": bool,
      "can_add_comments": bool,
      "can_manage_users": bool,
      "can_view_analytics": bool
    }
  - status: Enum [active, inactive]
  - created_at: DateTime
  - updated_at: DateTime
```

**Roles:**
- **admin**: Gestión completa de la empresa y usuarios
- **recruiter**: Puede crear candidatos, invitar, comentar
- **viewer**: Solo visualización

### 3. CompanyCandidate (Relación Empresa-Candidato)

Tabla de relación entre empresa y candidato con control de ownership.

```python
CompanyCandidate:
  - id: UUID
  - company_id: UUID (FK → Company)
  - candidate_id: UUID (FK → Candidate)
  - status: Enum [pending_invitation, pending_confirmation, active, rejected, archived]
  - ownership_status: Enum [company_owned, user_owned]
  - created_by_user_id: UUID (FK → CompanyUser - quién creó la relación)
  - workflow_id: UUID (FK → CompanyWorkflow, nullable - flujo de trabajo asignado)
  - current_stage_id: UUID (FK → WorkflowStage, nullable - etapa actual del flujo)
  - invited_at: DateTime
  - confirmed_at: DateTime (cuando el usuario confirmó)
  - rejected_at: DateTime
  - archived_at: DateTime
  - visibility_settings: JSON (qué puede ver la empresa)
    {
      "education": bool,
      "experience": bool,
      "projects": bool,
      "skills": bool,
      "certifications": bool,
      "languages": bool,
      "contact_info": bool
    }
  - tags: Array[String] (etiquetas privadas de la empresa)
  - internal_notes: Text (notas internas de la empresa)
  - position: String (posición para la que se considera)
  - department: String
  - priority: Enum [low, medium, high]
  - created_at: DateTime
  - updated_at: DateTime
```

### 4. CandidateComment (Comentarios de Empresa)

Comentarios que la empresa hace sobre un candidato.

```python
CandidateComment:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate)
  - author_user_id: UUID (FK → CompanyUser)
  - comment: Text
  - visibility: Enum [private, shared_with_candidate]
  - context: String (opcional: "interview", "screening", "review")
  - created_at: DateTime
  - updated_at: DateTime
  - deleted_at: DateTime (soft delete)
```

### 5. CandidateInvitation (Invitaciones)

Invitaciones pendientes para candidatos nuevos o confirmaciones para existentes.

```python
CandidateInvitation:
  - id: UUID
  - email: String
  - company_id: UUID (FK → Company)
  - candidate_id: UUID (FK → Candidate, nullable)
  - invited_by_user_id: UUID (FK → CompanyUser)
  - token: String (token único para aceptar/rechazar)
  - invitation_type: Enum [new_user, existing_user]
  - status: Enum [pending, accepted, rejected, expired]
  - message: Text (mensaje personalizado de invitación)
  - expires_at: DateTime
  - accepted_at: DateTime
  - rejected_at: DateTime
  - created_at: DateTime
```

### 6. CandidateAccessLog (Auditoría)

Registro de accesos de empresas a perfiles de candidatos.

```python
CandidateAccessLog:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate)
  - user_id: UUID (FK → CompanyUser)
  - action: Enum [view_profile, view_education, view_experience, add_comment, update_tags]
  - ip_address: String
  - user_agent: String
  - created_at: DateTime
```

### 7. CompanyWorkflow (Flujos de Trabajo)

Flujos de trabajo personalizables para diferentes tipos de procesos de selección.

```python
CompanyWorkflow:
  - id: UUID
  - company_id: UUID (FK → Company)
  - name: String (ej: "Proceso Técnico", "Proceso Ventas")
  - description: Text
  - is_default: Boolean (si es el flujo por defecto para nuevos candidatos)
  - status: Enum [active, archived]
  - created_by_user_id: UUID (FK → CompanyUser)
  - created_at: DateTime
  - updated_at: DateTime
```

### 8. WorkflowStage (Etapas del Flujo)

Etapas/estados personalizados dentro de un flujo de trabajo.

```python
WorkflowStage:
  - id: UUID
  - workflow_id: UUID (FK → CompanyWorkflow)
  - name: String (ej: "Revisión Inicial", "Entrevista Técnica", "Oferta Enviada")
  - description: Text
  - order: Integer (orden de la etapa en el flujo, 1, 2, 3...)
  - mapped_status: ApplicationStatusEnum (mapeo al enum estándar)
    # Valores posibles:
    # - applied: Candidato aplicó
    # - reviewing: En proceso de revisión
    # - interviewed: Entrevistado
    # - rejected: Rechazado
    # - accepted: Aceptado
    # - withdrawn: Candidato se retiró
  - color: String (color hex para visualización, ej: "#4CAF50")
  - is_initial: Boolean (etapa inicial del flujo)
  - is_final: Boolean (etapa final - accepted/rejected/withdrawn)
  - requires_action: Boolean (requiere acción del equipo)
  - created_at: DateTime
  - updated_at: DateTime
```

### 9. WorkflowStageTransition (Transiciones entre Etapas)

Define las transiciones permitidas entre etapas.

```python
WorkflowStageTransition:
  - id: UUID
  - workflow_id: UUID (FK → CompanyWorkflow)
  - from_stage_id: UUID (FK → WorkflowStage)
  - to_stage_id: UUID (FK → WorkflowStage)
  - name: String (ej: "Aprobar", "Rechazar", "Avanzar a siguiente fase")
  - requires_comment: Boolean (requiere comentario al hacer la transición)
  - created_at: DateTime
```

### 10. CandidateStageHistory (Historial de Etapas)

Registro histórico de movimientos de candidatos por las etapas.

```python
CandidateStageHistory:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate)
  - workflow_id: UUID (FK → CompanyWorkflow)
  - from_stage_id: UUID (FK → WorkflowStage, nullable - null si es la etapa inicial)
  - to_stage_id: UUID (FK → WorkflowStage)
  - changed_by_user_id: UUID (FK → CompanyUser)
  - comment: Text (opcional)
  - duration_in_previous_stage: Integer (tiempo en minutos en la etapa anterior)
  - created_at: DateTime
```

## Flujos de Trabajo Personalizables

### Concepto

Cada empresa puede crear múltiples flujos de trabajo (workflows) para diferentes tipos de procesos de selección. Por ejemplo:
- **Proceso Técnico**: Para desarrolladores, ingenieros
- **Proceso Ventas**: Para roles comerciales
- **Proceso Ejecutivo**: Para posiciones de liderazgo
- **Proceso Temporal**: Para contrataciones temporales

### Mapeo a ApplicationStatusEnum

Cada etapa personalizada (WorkflowStage) está mapeada a un `ApplicationStatusEnum` estándar:

```python
ApplicationStatusEnum:
  - applied: "Aplicó" - Candidato fue agregado/aplicó
  - reviewing: "En Revisión" - Se está evaluando
  - interviewed: "Entrevistado" - Ya pasó por entrevistas
  - rejected: "Rechazado" - No continuará en el proceso
  - accepted: "Aceptado" - Oferta aceptada
  - withdrawn: "Retirado" - Candidato se retiró del proceso
```

Este mapeo permite:
1. **Flexibilidad**: Cada empresa usa sus propios nombres de etapas
2. **Reportes estándar**: Generar métricas comparables entre empresas
3. **Analytics**: Análisis de funnel de conversión estándar
4. **Integraciones**: APIs pueden trabajar con enum estándar

### Ejemplos de Flujos

#### Flujo Técnico (Desarrollo de Software)

```
Workflow: "Proceso Técnico"

Etapas:
1. CV Recibido (mapped_status: applied)
2. Revisión Técnica (mapped_status: reviewing)
3. Prueba Técnica Enviada (mapped_status: reviewing)
4. Prueba Técnica Evaluada (mapped_status: reviewing)
5. Entrevista Técnica (mapped_status: interviewed)
6. Entrevista Cultural (mapped_status: interviewed)
7. Oferta Enviada (mapped_status: interviewed)
8. Oferta Aceptada (mapped_status: accepted) [FINAL]
9. Rechazado (mapped_status: rejected) [FINAL]
10. Candidato se Retiró (mapped_status: withdrawn) [FINAL]

Transiciones permitidas:
- CV Recibido → Revisión Técnica, Rechazado
- Revisión Técnica → Prueba Técnica Enviada, Rechazado
- Prueba Técnica Enviada → Prueba Técnica Evaluada
- Prueba Técnica Evaluada → Entrevista Técnica, Rechazado
- Entrevista Técnica → Entrevista Cultural, Rechazado
- Entrevista Cultural → Oferta Enviada, Rechazado
- Oferta Enviada → Oferta Aceptada, Rechazado, Candidato se Retiró
- Cualquier etapa → Candidato se Retiró
```

#### Flujo Ventas

```
Workflow: "Proceso Ventas"

Etapas:
1. Lead Recibido (mapped_status: applied)
2. Screening Telefónico (mapped_status: reviewing)
3. Entrevista con Manager (mapped_status: interviewed)
4. Presentación de Caso (mapped_status: interviewed)
5. Entrevista con Director (mapped_status: interviewed)
6. Referencias Verificadas (mapped_status: interviewed)
7. Oferta Extendida (mapped_status: interviewed)
8. Contratado (mapped_status: accepted) [FINAL]
9. No Califica (mapped_status: rejected) [FINAL]
10. Declinó Oferta (mapped_status: withdrawn) [FINAL]

Transiciones permitidas:
- Lead Recibido → Screening Telefónico, No Califica
- Screening Telefónico → Entrevista con Manager, No Califica
- Entrevista con Manager → Presentación de Caso, No Califica
- Presentación de Caso → Entrevista con Director, No Califica
- Entrevista con Director → Referencias Verificadas, No Califica
- Referencias Verificadas → Oferta Extendida, No Califica
- Oferta Extendida → Contratado, Declinó Oferta, No Califica
- Cualquier etapa → Declinó Oferta
```

### Visualización del Flujo

Las etapas se pueden visualizar como un pipeline/kanban:

```
[CV Recibido: 15] → [Revisión: 8] → [Prueba: 5] → [Entrevista: 3] → [Oferta: 1]
     ↓                  ↓               ↓              ↓
[Rechazados: 45]
```

### Reportes y Métricas

Gracias al mapeo a `ApplicationStatusEnum`, se pueden generar reportes estándar:

#### Métricas por Empresa
```sql
-- Tasa de conversión general
SELECT
  COUNT(*) FILTER (WHERE ws.mapped_status = 'applied') as total_aplicados,
  COUNT(*) FILTER (WHERE ws.mapped_status = 'accepted') as total_aceptados,
  (COUNT(*) FILTER (WHERE ws.mapped_status = 'accepted')::float /
   COUNT(*) FILTER (WHERE ws.mapped_status = 'applied')) * 100 as tasa_conversion
FROM company_candidate cc
JOIN workflow_stage ws ON cc.current_stage_id = ws.id
WHERE cc.company_id = ?
```

#### Tiempo promedio por etapa
```sql
SELECT
  ws.mapped_status,
  AVG(csh.duration_in_previous_stage) as avg_duration_minutes
FROM candidate_stage_history csh
JOIN workflow_stage ws ON csh.to_stage_id = ws.id
GROUP BY ws.mapped_status
```

#### Funnel de conversión
```sql
SELECT
  ws.mapped_status,
  COUNT(*) as candidatos,
  COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as porcentaje
FROM company_candidate cc
JOIN workflow_stage ws ON cc.current_stage_id = ws.id
WHERE cc.company_id = ?
GROUP BY ws.mapped_status
ORDER BY
  CASE ws.mapped_status
    WHEN 'applied' THEN 1
    WHEN 'reviewing' THEN 2
    WHEN 'interviewed' THEN 3
    WHEN 'accepted' THEN 4
    WHEN 'rejected' THEN 5
    WHEN 'withdrawn' THEN 6
  END
```

## Flujos de Negocio

### Flujo 1: Empresa crea candidato con email NO existente

```
1. Recruiter ingresa email y datos básicos del candidato
2. Sistema verifica que el email NO existe en la plataforma
3. Sistema crea:
   - Candidate (con datos básicos)
   - CompanyCandidate (status: pending_invitation, ownership: company_owned)
   - CandidateInvitation (type: new_user, status: pending)
4. Sistema envía email de invitación con token
5. Candidato hace clic en link y se registra
6. Sistema:
   - Actualiza User con el email
   - Vincula Candidate con User
   - Actualiza CompanyCandidate (status: active, ownership: user_owned, confirmed_at: now)
   - Actualiza CandidateInvitation (status: accepted, accepted_at: now)
7. Empresa ahora tiene acceso de solo lectura + comentarios
```

### Flujo 2: Empresa intenta crear candidato con email EXISTENTE

```
1. Recruiter ingresa email que YA existe en la plataforma
2. Sistema detecta que el email existe y tiene un User/Candidate
3. Sistema crea:
   - CompanyCandidate (status: pending_confirmation, ownership: user_owned)
   - CandidateInvitation (type: existing_user, status: pending, candidate_id: existing_candidate)
4. Sistema envía email de CONFIRMACIÓN al candidato
   "La empresa X quiere agregarte a su sistema. ¿Aceptas?"
5a. Candidato ACEPTA:
   - CompanyCandidate (status: active, confirmed_at: now)
   - CandidateInvitation (status: accepted, accepted_at: now)
   - Empresa tiene acceso según visibility_settings
5b. Candidato RECHAZA:
   - CompanyCandidate (status: rejected, rejected_at: now)
   - CandidateInvitation (status: rejected, rejected_at: now)
   - Empresa NO tiene acceso al candidato
```

### Flujo 3: Candidato gestiona su privacidad

```
1. Candidato ve lista de empresas vinculadas
2. Para cada empresa puede:
   - Configurar visibility_settings (qué información compartir)
   - Ver comentarios marcados como "shared_with_candidate"
   - Revocar acceso (archiva la relación CompanyCandidate)
   - Ver CandidateAccessLog (quién vio qué)
```

### Flujo 4: Empresa gestiona candidatos

```
Cuando ownership_status = company_owned:
  - Empresa puede EDITAR datos del candidato
  - Empresa puede ELIMINAR candidato
  - Empresa puede agregar comentarios privados

Cuando ownership_status = user_owned:
  - Empresa puede VER datos (según visibility_settings)
  - Empresa puede COMENTAR (privado o compartido)
  - Empresa puede agregar TAGS internos
  - Empresa puede actualizar INTERNAL_NOTES
  - Empresa NO puede editar datos del candidato
```

### Flujo 5: Gestión de Workflows y Movimiento de Candidatos

#### 5.1. Creación de Workflow

```
1. Admin de empresa crea nuevo Workflow
   - Define nombre y descripción (ej: "Proceso Técnico")
   - Marca si es workflow por defecto

2. Admin crea las etapas (WorkflowStage)
   - Define cada etapa con nombre y descripción
   - Asigna orden (1, 2, 3...)
   - Mapea cada etapa a ApplicationStatusEnum
   - Asigna color para visualización
   - Marca etapa inicial (is_initial = true)
   - Marca etapas finales (is_final = true para accepted/rejected/withdrawn)

3. Admin define transiciones permitidas (WorkflowStageTransition)
   - Define desde qué etapa hacia qué etapa se puede mover
   - Nombra la acción (ej: "Aprobar", "Rechazar", "Pasar a entrevista")
   - Indica si requiere comentario obligatorio

4. Sistema valida:
   - Existe al menos una etapa inicial
   - Existen etapas finales
   - Todas las etapas están conectadas (no hay islas)
   - Los mapped_status son válidos

5. Workflow queda activo y disponible
```

#### 5.2. Asignación de Candidato a Workflow

```
1. Al crear/agregar candidato a empresa:
   - Si empresa tiene workflow por defecto:
     - Asignar workflow_id
     - Asignar current_stage_id a la etapa inicial (is_initial = true)
   - Si no hay workflow por defecto:
     - workflow_id = null
     - current_stage_id = null
     - Se puede asignar manualmente después

2. Sistema crea registro en CandidateStageHistory:
   - from_stage_id = null
   - to_stage_id = etapa inicial
   - comment = "Candidato agregado al proceso"
```

#### 5.3. Movimiento de Candidato entre Etapas

```
1. Recruiter selecciona candidato
2. Sistema muestra etapa actual y transiciones disponibles
3. Recruiter selecciona acción (ej: "Aprobar para entrevista técnica")
4. Si requiere comentario:
   - Sistema solicita comentario
   - Recruiter ingresa comentario
5. Sistema valida:
   - Transición existe en WorkflowStageTransition
   - Usuario tiene permisos
   - Comentario presente si es requerido
6. Sistema actualiza CompanyCandidate:
   - current_stage_id = nueva etapa
   - updated_at = now
7. Sistema crea registro en CandidateStageHistory:
   - from_stage_id = etapa anterior
   - to_stage_id = nueva etapa
   - changed_by_user_id = recruiter
   - comment = comentario ingresado
   - duration_in_previous_stage = diferencia en minutos
   - created_at = now
8. Sistema publica evento: CandidateStageChanged
9. Si nueva etapa es final:
   - Sistema puede enviar notificación al candidato
   - Sistema puede archivar el candidato si es rejected/withdrawn
```

#### 5.4. Cambio de Workflow

```
1. Recruiter decide cambiar candidato a otro workflow
   (ej: de "Proceso Junior" a "Proceso Senior")
2. Sistema muestra workflows disponibles
3. Recruiter selecciona nuevo workflow
4. Sistema solicita seleccionar etapa inicial del nuevo workflow
5. Sistema actualiza CompanyCandidate:
   - workflow_id = nuevo workflow
   - current_stage_id = etapa seleccionada
6. Sistema crea registro en CandidateStageHistory:
   - workflow_id = nuevo workflow
   - from_stage_id = null
   - to_stage_id = etapa inicial del nuevo workflow
   - comment = "Cambiado a workflow: [nombre]"
```

## Estados y Transiciones

### Estados de CompanyCandidate

```
pending_invitation → (usuario se registra) → active
pending_confirmation → (usuario acepta) → active
pending_confirmation → (usuario rechaza) → rejected
active → (empresa archiva) → archived
active → (usuario revoca) → archived
```

### Estados de Ownership

```
company_owned:
  - Candidato creado por empresa, usuario NO ha reclamado ownership
  - Empresa tiene control total

user_owned:
  - Usuario ha tomado ownership (registro o confirmación)
  - Empresa solo lectura + comentarios
```

## Permisos y Reglas de Negocio

### Reglas de Creación

1. Una empresa NO puede crear múltiples relaciones con el mismo candidato
2. Si existe relación "rejected", empresa puede reinvitar después de 30 días
3. Si existe relación "archived", empresa puede reactivar con confirmación del usuario
4. Invitaciones expiran después de 30 días

### Reglas de Acceso

1. **company_owned + pending_invitation**:
   - Empresa: Read/Write completo

2. **company_owned + active** (usuario aún no registrado):
   - Empresa: Read/Write completo

3. **user_owned + active**:
   - Empresa: Read (según visibility_settings)
   - Empresa: Write solo en comments, tags, internal_notes

4. **user_owned + rejected**:
   - Empresa: Sin acceso

5. **user_owned + archived**:
   - Empresa: Sin acceso

### Reglas de Comentarios

1. Comentarios con visibility = "private": Solo la empresa puede ver
2. Comentarios con visibility = "shared_with_candidate": Candidato puede ver
3. Candidato puede responder a comentarios compartidos
4. Empresa puede editar/eliminar sus comentarios (soft delete)

### Reglas de Privacidad

1. Candidato puede revocar acceso a una empresa en cualquier momento
2. Al revocar, CompanyCandidate pasa a "archived"
3. Empresa mantiene comentarios y notas internas
4. Empresa pierde acceso a datos del candidato
5. Candidato puede ver historial de accesos (CandidateAccessLog)

## Notificaciones

### Email de Invitación (nuevo usuario)
```
Asunto: Has sido invitado por [Company Name] a CareerPython

Hola,

[Company Name] te ha invitado a unirte a CareerPython para gestionar tu perfil profesional.

Al registrarte, tendrás control total sobre tu información y podrás:
- Gestionar tu perfil profesional
- Controlar qué empresas ven tu información
- Aplicar a otras oportunidades

[Botón: Crear mi cuenta]

Este enlace expira en 30 días.
```

### Email de Confirmación (usuario existente)
```
Asunto: [Company Name] quiere agregarte a su sistema

Hola [Candidate Name],

[Company Name] quiere agregarte a su sistema de gestión de candidatos.

Si aceptas, la empresa podrá:
- Ver tu perfil profesional (según tu configuración de privacidad)
- Agregar comentarios sobre tu candidatura
- Mantenerte informado sobre oportunidades

Tú mantienes el control total de tu información.

[Botón: Aceptar] [Botón: Rechazar]

Puedes configurar qué información compartes después de aceptar.
```

### Notificación de Nuevo Comentario Compartido
```
[Company Name] ha agregado un comentario sobre tu perfil.

Ver comentario →
```

## Dashboard de Empresa

### Vista Principal - Lista
```
- Lista de candidatos (tabla)
- Filtros:
  - Por workflow
  - Por etapa actual
  - Por status (active, pending, archived)
  - Por tags
  - Por posición
  - Por ownership_status
  - Por fecha de creación
- Búsqueda por nombre/email
- Estadísticas globales:
  - Total candidatos activos
  - Invitaciones pendientes
  - Candidatos por posición
  - Actividad reciente
  - Tasa de conversión general
```

### Vista Kanban/Pipeline
```
Vista visual del workflow seleccionado:

[CV Recibido: 15]  [Revisión: 8]  [Entrevista: 5]  [Oferta: 2]  [Aceptados: 1]
     │                  │               │               │             │
  [Card]            [Card]          [Card]         [Card]        [Card]
  [Card]            [Card]          [Card]         [Card]
  [Card]            [Card]          [Card]
    ...               ...             ...

Funcionalidad:
- Drag & drop para mover candidatos entre etapas
- Al soltar: Modal con transiciones disponibles
- Si requires_comment: Solicitar comentario
- Contador de candidatos por etapa
- Colores personalizados por etapa
- Filtros por tags, posición, prioridad
- Tiempo promedio en cada etapa

Card muestra:
- Nombre del candidato
- Foto avatar
- Posición
- Tags
- Tiempo en etapa actual
- Priority badge
- Ownership badge
```

### Vista de Candidato Individual
```
Cabecera:
- Foto, nombre, posición objetivo
- Status badge (active, pending, etc)
- Ownership badge (indica si es readonly)
- Workflow actual y etapa
- Timeline visual del recorrido por las etapas

Tabs:
1. Perfil: Ver información según visibility_settings
2. Workflow:
   - Etapa actual destacada
   - Acciones disponibles (botones de transición)
   - Historial de movimientos (CandidateStageHistory)
   - Tiempo en cada etapa
   - Timeline visual
3. Comentarios: Histórico de comentarios del equipo
4. Actividad: Timeline completo de interacciones
5. Notas: Internal notes y tags

Acciones (según ownership):
- Editar (solo si company_owned)
- Mover a siguiente etapa (según transiciones disponibles)
- Cambiar workflow
- Agregar comentario
- Agregar tag
- Actualizar posición/departamento
- Archivar candidato
```

### Vista de Gestión de Workflows
```
Lista de workflows de la empresa:

[Workflow: Proceso Técnico] [Activo] [Por defecto] [Editar]
  - 45 candidatos activos
  - Tasa de conversión: 12%
  - Tiempo promedio: 18 días

Acciones:
- Crear nuevo workflow
- Editar workflow existente
- Ver estadísticas detalladas
- Archivar workflow

Editor de Workflow:
1. Información básica
   - Nombre
   - Descripción
   - Marcar como por defecto

2. Etapas
   - Lista de etapas ordenadas
   - Agregar/editar/eliminar etapas
   - Para cada etapa:
     * Nombre
     * Descripción
     * Orden
     * Mapeo a ApplicationStatusEnum
     * Color
     * Is initial / Is final
     * Requires action

3. Transiciones
   - Matriz visual de transiciones permitidas
   - Agregar/eliminar transiciones
   - Para cada transición:
     * Nombre de la acción
     * Requires comment

4. Vista previa
   - Diagrama visual del flujo
   - Validaciones en tiempo real
```

## Dashboard de Candidato

### Mis Empresas
```
Lista de empresas vinculadas:
- Logo y nombre de empresa
- Status de la relación
- Posición para la que se considera
- Configuración de visibilidad
- Acciones:
  - Configurar privacidad
  - Ver comentarios compartidos
  - Ver historial de accesos
  - Revocar acceso
```

## Consideraciones Técnicas

### Índices Recomendados
```sql
-- Índices principales
CREATE INDEX idx_company_candidate_company ON company_candidate(company_id);
CREATE INDEX idx_company_candidate_candidate ON company_candidate(candidate_id);
CREATE INDEX idx_company_candidate_status ON company_candidate(status);
CREATE INDEX idx_company_candidate_workflow ON company_candidate(workflow_id);
CREATE INDEX idx_company_candidate_stage ON company_candidate(current_stage_id);
CREATE INDEX idx_company_candidate_workflow_stage ON company_candidate(workflow_id, current_stage_id);

-- Índices para invitaciones
CREATE INDEX idx_candidate_invitation_email ON candidate_invitation(email);
CREATE INDEX idx_candidate_invitation_token ON candidate_invitation(token);
CREATE INDEX idx_candidate_invitation_company ON candidate_invitation(company_id);
CREATE INDEX idx_candidate_invitation_status ON candidate_invitation(status);

-- Índices para comentarios
CREATE INDEX idx_candidate_comment_company_candidate ON candidate_comment(company_candidate_id);
CREATE INDEX idx_candidate_comment_author ON candidate_comment(author_user_id);

-- Índices para workflows
CREATE INDEX idx_workflow_stage_workflow ON workflow_stage(workflow_id);
CREATE INDEX idx_workflow_stage_mapped_status ON workflow_stage(mapped_status);
CREATE INDEX idx_workflow_transition_workflow ON workflow_stage_transition(workflow_id);
CREATE INDEX idx_workflow_transition_from ON workflow_stage_transition(from_stage_id);
CREATE INDEX idx_workflow_transition_to ON workflow_stage_transition(to_stage_id);

-- Índices para historial
CREATE INDEX idx_candidate_history_company_candidate ON candidate_stage_history(company_candidate_id);
CREATE INDEX idx_candidate_history_workflow ON candidate_stage_history(workflow_id);
CREATE INDEX idx_candidate_history_to_stage ON candidate_stage_history(to_stage_id);
CREATE INDEX idx_candidate_history_created ON candidate_stage_history(created_at);

-- Índices compuestos para reportes
CREATE INDEX idx_company_candidate_reporting ON company_candidate(company_id, workflow_id, current_stage_id) WHERE status = 'active';
```

### Validaciones
```python
# Antes de crear CompanyCandidate
- Verificar que no existe relación activa
- Validar permisos del CompanyUser
- Validar email format
- Si se asigna workflow, verificar que pertenece a la empresa
- Si se asigna stage, verificar que pertenece al workflow

# Antes de confirmar invitación
- Verificar token válido y no expirado
- Verificar que invitation status = pending

# Antes de acceso a datos
- Verificar ownership_status
- Verificar visibility_settings
- Registrar en CandidateAccessLog

# Antes de crear/modificar Workflow
- Validar que existe al menos una etapa inicial (is_initial = true)
- Validar que existen etapas finales (is_final = true)
- Validar que todos los mapped_status son valores válidos de ApplicationStatusEnum
- Validar que no hay workflows duplicados con mismo nombre en la empresa

# Antes de crear WorkflowStage
- Validar que workflow existe y pertenece a la empresa
- Validar que order es único dentro del workflow
- Validar que mapped_status es válido
- Si is_initial = true, verificar que no existe otra etapa inicial en el workflow
- Validar que color es formato hex válido

# Antes de crear WorkflowStageTransition
- Validar que workflow, from_stage y to_stage existen
- Validar que from_stage y to_stage pertenecen al mismo workflow
- Validar que no existe transición duplicada
- Validar que no crea ciclos infinitos sin etapa final

# Antes de mover candidato a nueva etapa
- Verificar que transición existe en WorkflowStageTransition
- Verificar que usuario tiene permisos
- Si requires_comment = true, verificar que comentario está presente
- Verificar que candidato está en la etapa from_stage
- Verificar que candidato no está en etapa final (unless allowing reopen)
```

### Eventos de Dominio
```python
# Eventos principales
- CompanyCandidateCreated
- CandidateInvitationSent
- CandidateInvitationAccepted
- CandidateInvitationRejected
- OwnershipTransferred (company_owned → user_owned)
- CommentAdded
- AccessRevoked
- VisibilitySettingsUpdated

# Eventos de workflow
- WorkflowCreated
- WorkflowUpdated
- WorkflowArchived
- WorkflowStageCreated
- WorkflowStageUpdated
- WorkflowStageDeleted
- WorkflowTransitionCreated
- WorkflowTransitionDeleted

# Eventos de candidato en workflow
- CandidateAssignedToWorkflow
- CandidateStageChanged
  {
    company_candidate_id: UUID,
    workflow_id: UUID,
    from_stage_id: UUID,
    from_stage_name: String,
    from_mapped_status: ApplicationStatusEnum,
    to_stage_id: UUID,
    to_stage_name: String,
    to_mapped_status: ApplicationStatusEnum,
    changed_by_user_id: UUID,
    comment: String,
    duration_in_previous_stage: Integer
  }
- CandidateReachedFinalStage
- CandidateWorkflowChanged
```

## Migración y Datos Existentes

Si ya existen candidatos en el sistema:
1. Se mantienen como candidatos independientes (sin CompanyCandidate)
2. Un admin puede vincularlos a empresas creando CompanyCandidate con status=active y ownership=user_owned
3. Se requiere confirmación del usuario si no la dio previamente

## Próximos Pasos de Implementación

### Fase 1: Fundamentos (Semanas 1-2)
1. Crear módulo `company` con estructura DDD
   - Entidad Company
   - CompanyUser y sistema de roles
   - Repositorios y queries básicas

2. Crear módulo `company_candidate` para la relación
   - Entidad CompanyCandidate
   - Sistema de ownership (company_owned/user_owned)
   - Repositorios y queries

3. Implementar sistema de invitaciones y confirmaciones
   - CandidateInvitation entity
   - Flujo para nuevos usuarios
   - Flujo para usuarios existentes
   - Generación y validación de tokens

### Fase 2: Workflows (Semanas 3-4)
4. Crear módulo `company_workflow`
   - Entidad CompanyWorkflow
   - Entidad WorkflowStage con mapeo a ApplicationStatusEnum
   - WorkflowStageTransition
   - Validaciones de integridad del flujo

5. Implementar sistema de movimiento de candidatos
   - CandidateStageHistory
   - Comandos para mover candidatos entre etapas
   - Validaciones de transiciones
   - Cálculo de duración en etapas

6. Sistema de eventos para workflows
   - CandidateStageChanged event
   - Handlers para notificaciones
   - Handlers para archivado automático

### Fase 3: Permisos y Acceso (Semana 5)
7. Agregar sistema de permisos y visibility settings
   - Validaciones de ownership_status
   - Gestión de visibility_settings
   - CandidateAccessLog
   - Middleware de autorización

8. Sistema de comentarios
   - CandidateComment entity
   - Comentarios privados vs compartidos
   - CRUD de comentarios

### Fase 4: API y Backend (Semanas 6-7)
9. Crear endpoints de API para empresas
   - CRUD de Company
   - Gestión de CompanyUsers
   - Gestión de candidatos
   - Endpoints de workflows
   - Endpoints de transiciones
   - Endpoints de reportes y métricas

### Fase 5: Frontend (Semanas 8-10)
10. Implementar dashboard de empresa
    - Vista principal con lista de candidatos
    - Vista kanban/pipeline por workflow
    - Vista detalle de candidato
    - Gestión de workflows y etapas
    - Drag & drop para mover candidatos
    - Reportes y analytics visuales

11. Implementar sección "Mis Empresas" en perfil de candidato
    - Lista de empresas vinculadas
    - Gestión de visibility_settings
    - Ver comentarios compartidos
    - Historial de accesos
    - Revocar acceso

### Fase 6: Notificaciones y Comunicación (Semana 11)
12. Sistema de notificaciones por email
    - Email de invitación para nuevos usuarios
    - Email de confirmación para usuarios existentes
    - Notificaciones de cambio de etapa
    - Notificaciones de comentarios compartidos
    - Plantillas HTML personalizables

### Fase 7: Analytics y Auditoría (Semana 12)
13. Audit log y analytics
    - Dashboard de métricas de empresa
    - Reportes de funnel de conversión
    - Tiempo promedio por etapa
    - Tasa de conversión por workflow
    - Exportación de datos

### Fase 8: Testing y QA (Semanas 13-14)
14. Testing completo de flujos
    - Unit tests de entidades y value objects
    - Tests de comandos y queries
    - Tests de validaciones de workflows
    - Tests de transiciones
    - Integration tests de API
    - E2E tests de flujos completos
    - Load testing de reportes

### Fase 9: Documentación y Deploy (Semana 15)
15. Documentación y despliegue
    - Documentación de API (OpenAPI/Swagger)
    - Guías de usuario para empresas
    - Scripts de migración de datos
    - Despliegue a producción
    - Monitoreo y alertas
