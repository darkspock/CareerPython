# Sección de Empresas - Modelo Lógico

## Visión General

La sección de empresas permite a las organizaciones gestionar candidatos para sus procesos de selección, respetando la propiedad de los datos del candidato y su privacidad.

## Principios Fundamentales

1. **Los datos son del candidato**: El candidato es el propietario absoluto de su información (Candidate)
2. **Privacidad por defecto**: Los datos del perfil del candidato son PRIVADOS, la empresa NO puede verlos
3. **CRM Desacoplado**: CompanyCandidate es un "Lead" independiente, NO es una relación con Candidate
4. **Autorización explícita**: Solo cuando el candidato aplica formalmente (CompanyApplication) autoriza qué datos compartir
5. **Contexto de candidatura**: Los datos se comparten POR candidatura, no globalmente
6. **Dos flujos distintos**:
   - **Flujo 1**: Candidato aplica → CompanyCandidate con candidate_id (datos copiados limitados)
   - **Flujo 2**: Empresa agrega lead → CompanyCandidate sin candidate_id (empresa rellena lo que sabe)

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

### 3. Position (Posición/Vacante)

Posiciones o vacantes abiertas por la empresa.

```python
Position:
  - id: UUID
  - company_id: UUID (FK → Company)
  - title: String (ej: "Senior Backend Developer")
  - description: Text
  - department: String (opcional)
  - location: String
  - employment_type: Enum [full_time, part_time, contract, internship, temporary]
  - remote_type: Enum [on_site, remote, hybrid]
  - salary_range_min: Decimal (nullable)
  - salary_range_max: Decimal (nullable)
  - salary_currency: String (ej: "USD", "EUR")
  - requirements: Text
  - responsibilities: Text
  - benefits: Text (opcional)
  - status: Enum [draft, active, paused, closed, cancelled]
  - workflow_id: UUID (FK → CompanyWorkflow, nullable - workflow por defecto para aplicaciones)
  - created_by_user_id: UUID (FK → CompanyUser)
  - published_at: DateTime (nullable)
  - closed_at: DateTime (nullable)
  - created_at: DateTime
  - updated_at: DateTime
```

### 4. CompanyCandidate (Lead/Candidato en CRM de Empresa)

**IMPORTANTE**: CompanyCandidate NO es una relación, es una entidad independiente tipo "Lead" en un CRM.
Los datos del candidato registrado (Candidate) son PRIVADOS y la empresa NO puede verlos.

Existen dos flujos de creación:

**Flujo 1 - Candidato Aplica (candidate_id presente)**:
- El candidato aplica a una posición/empresa
- Se crea CompanyCandidate con candidate_id
- Se COPIAN solo los datos básicos que el candidato autoriza compartir
- Campos copiados: nombre, email, teléfono, país, linkedin
- La empresa NO puede ver el perfil completo del candidato (education, experience, projects)

**Flujo 2 - Empresa Agrega Lead (candidate_id = null)**:
- La empresa agrega un lead manualmente (prospecto)
- Se crea CompanyCandidate sin candidate_id
- La empresa rellena los datos que tiene del lead
- Se puede enviar invitación para que el lead se registre y vincule

```python
CompanyCandidate:
  - id: UUID
  - company_id: UUID (FK → Company)
  - candidate_id: UUID (FK → Candidate, NULLABLE - solo si candidato aplicó)

  # Datos básicos (copiados del candidato o ingresados por empresa)
  - first_name: String
  - last_name: String
  - email: String
  - phone: String (opcional)
  - country: String (opcional)
  - linkedin_url: String (opcional)

  # Datos de gestión de la empresa (privados)
  - source: Enum [application, manual_entry, referral, linkedin, other]
  - status: Enum [lead, contacted, in_process, offer_made, hired, rejected, archived]
  - created_by_user_id: UUID (FK → CompanyUser - quién lo agregó/gestionó)
  - workflow_id: UUID (FK → CompanyWorkflow, nullable)
  - current_stage_id: UUID (FK → WorkflowStage, nullable)

  # Datos adicionales CRM
  - tags: Array[String] (etiquetas privadas)
  - internal_notes: Text (notas internas)
  - position_interest: String (posición de interés)
  - department: String
  - priority: Enum [low, medium, high]
  - salary_expectation: String (opcional)
  - availability: String (opcional)

  # Invitación (si es lead sin candidate_id)
  - invitation_sent_at: DateTime (nullable)
  - invitation_token: String (nullable - para vincular cuenta)
  - invitation_expires_at: DateTime (nullable)

  # Timestamps
  - created_at: DateTime
  - updated_at: DateTime
  - archived_at: DateTime (soft delete)
```

**Nota sobre privacidad**:
- Los datos education, experience, projects, skills del Candidate son PRIVADOS
- Solo se comparten cuando el candidato aplica a una candidatura (CompanyApplication)
- CompanyCandidate es el "Lead" antes de la aplicación formal

### 5. CandidateComment (Comentarios de Empresa)

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

### 6. CandidateInvitation (Invitaciones a Leads)

**SIMPLIFICADO**: Solo se usa para invitar leads (CompanyCandidate sin candidate_id) a registrarse.
Ya NO se usa para vincular candidatos existentes, eso se maneja en el flujo de aplicación.

```python
CandidateInvitation:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate - el lead que se invita)
  - email: String (copiado de CompanyCandidate.email)
  - company_id: UUID (FK → Company)
  - invited_by_user_id: UUID (FK → CompanyUser)
  - token: String (token único para el link de registro)
  - status: Enum [pending, accepted, rejected, expired, cancelled]
  - message: Text (mensaje personalizado opcional)
  - expires_at: DateTime (ej: 7 días)
  - accepted_at: DateTime (nullable)
  - rejected_at: DateTime (nullable)
  - created_at: DateTime
```

**Flujo de invitación**:
1. Empresa crea lead (CompanyCandidate sin candidate_id)
2. Empresa envía invitación con link único
3. Lead recibe email con link: `/register?invitation_token=xxx`
4. Lead se registra, crea cuenta (Candidate)
5. Sistema vincula: `CompanyCandidate.candidate_id = nuevo_candidate_id`
6. Invitación pasa a status "accepted"

### 7. CandidateAccessLog (Auditoría)

Registro de accesos y acciones sobre CompanyCandidate (leads/candidatos del CRM).

**NOTA**: Ya no registra acceso a datos privados del Candidate porque la empresa NO tiene acceso a ellos.

```python
CandidateAccessLog:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate)
  - user_id: UUID (FK → CompanyUser)
  - action: Enum [view_lead, update_lead, add_comment, change_stage, send_invitation, add_tags]
  - details: JSON (detalles adicionales de la acción)
  - ip_address: String
  - user_agent: String
  - created_at: DateTime
```

### 8. CompanyApplication (Candidatura Formal - "Opportunity")

**NUEVO CONCEPTO**: Esta es la candidatura formal a una posición específica.
Es el equivalente a "Opportunity" en un CRM (Lead → Opportunity).

CompanyCandidate es el "Lead", CompanyApplication es la "Candidatura/Opportunity".

```python
CompanyApplication:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate - el lead que aplica)
  - candidate_id: UUID (FK → Candidate - debe existir)
  - company_id: UUID (FK → Company)
  - position_id: UUID (FK → Position - posición a la que aplica)

  # Workflow
  - workflow_id: UUID (FK → CompanyWorkflow, nullable)
  - current_stage_id: UUID (FK → WorkflowStage, nullable)

  # Datos compartidos por el candidato (autorización de visibilidad)
  - shared_data: JSON
    {
      "basic_info": bool,      # nombre, email, teléfono, país, linkedin
      "education": bool,       # títulos académicos
      "experience": bool,      # experiencia laboral
      "projects": bool,        # proyectos
      "skills": bool,          # habilidades
      "certifications": bool,  # certificaciones
      "languages": bool,       # idiomas
      "resume_url": string     # URL del CV específico compartido
    }

  # Estado de la candidatura
  - status: Enum [active, offer_made, accepted, rejected, withdrawn, archived]
  - applied_at: DateTime
  - source: Enum [direct_application, invitation_response, referral, linkedin]

  # Datos de seguimiento
  - tags: Array[String]
  - internal_notes: Text
  - priority: Enum [low, medium, high]
  - salary_offered: Decimal (nullable)

  # Timestamps
  - created_at: DateTime
  - updated_at: DateTime
  - archived_at: DateTime (soft delete)
```

**Diferencia entre CompanyCandidate y CompanyApplication**:
- **CompanyCandidate** = Lead en CRM (prospect, contacto inicial, datos limitados)
- **CompanyApplication** = Opportunity en CRM (candidatura formal a posición, con datos completos autorizados)

**Flujo Lead → Application**:
1. Empresa tiene lead (CompanyCandidate)
2. Lead aplica a posición específica o empresa invita a candidatura
3. Se crea CompanyApplication vinculado al CompanyCandidate
4. Candidato autoriza qué datos compartir para esa candidatura específica
5. Empresa puede ver datos autorizados SOLO en el contexto de esa application

### 9. CompanyWorkflow (Flujos de Trabajo)

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

### 10. WorkflowStage (Etapas del Flujo)

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
  - is_success: Boolean 
  - requires_action: Boolean (requiere acción del equipo)
  - created_at: DateTime
  - updated_at: DateTime
```

### 11. WorkflowStageTransition (Transiciones entre Etapas)

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

### 12. CandidateStageHistory (Historial de Etapas)

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

### Flujo 1: Empresa agrega Lead manualmente (sin candidate_id)

**Caso**: La empresa tiene un prospecto (de LinkedIn, referido, etc.) que NO está registrado en la plataforma.

```
1. Recruiter ingresa datos del lead:
   - Nombre, email, teléfono (opcional)
   - País, LinkedIn (opcional)
   - Posición de interés, departamento, prioridad
   - Tags, notas internas
   - Source: manual_entry, referral, linkedin, etc.

2. Sistema crea:
   - CompanyCandidate (candidate_id = NULL, status = lead)
   - Los datos son ingresados/controlados por la empresa

3. Recruiter puede:
   - EDITAR todos los datos del lead (es company-owned)
   - Agregar comentarios internos
   - Mover por workflow (etapas de prospección)
   - Enviar invitación para que se registre

4. Si decide enviar invitación:
   - Sistema crea CandidateInvitation con token único
   - Envía email con link: /register?invitation_token=xxx
   - CompanyCandidate.invitation_sent_at = now

5. Si lead se registra:
   - Lead completa registro → crea Candidate + User
   - Sistema vincula: CompanyCandidate.candidate_id = nuevo_candidate_id
   - Status puede cambiar a: contacted, in_process, etc.
   - Los datos básicos del Candidate NO son visibles para la empresa
   - CompanyCandidate sigue siendo independiente con sus datos CRM

6. Si lead NO se registra:
   - CompanyCandidate sigue como lead sin candidate_id
   - Empresa sigue gestionándolo como prospecto en el CRM
```

**Importante**: Los datos del CompanyCandidate NO se sincronizan con Candidate. Son entidades separadas.

### Flujo 2: Candidato aplica a posición (se crea CompanyCandidate con candidate_id)

**Caso**: Un candidato registrado en la plataforma aplica a una posición de una empresa.

```
1. Candidato navega a posición publicada
2. Candidato hace clic en "Aplicar"
3. Sistema muestra form para seleccionar:
   - Qué datos básicos compartir (de los permitidos)
   - Campos disponibles: nombre, email, teléfono, país, linkedin
   - Por defecto: solo nombre, email, país

4. Candidato confirma aplicación

5. Sistema crea:
   - CompanyCandidate con:
     * candidate_id = candidato que aplicó
     * company_id = empresa de la posición
     * COPIA los datos básicos seleccionados (nombre, email, teléfono, país, linkedin)
     * source = application
     * status = lead (aún no es candidatura formal)

6. Empresa ve nuevo lead en su CRM con:
   - Datos básicos copiados
   - Indicador de que es un candidato registrado (candidate_id presente)
   - NO puede ver: education, experience, projects, skills

7. Si empresa quiere avanzar con el candidato:
   - Puede convertir el lead en candidatura formal
   - Ver "Flujo 4: De Lead a Candidatura Formal (Application)"
```

**Importante**: Aplicar NO significa compartir todo el perfil. Solo datos básicos limitados.

### Flujo 3: Empresa invita Lead a registrarse

```
1. Empresa tiene lead (CompanyCandidate sin candidate_id)
2. Recruiter hace clic en "Enviar invitación"
3. Sistema crea CandidateInvitation:
   - company_candidate_id = lead
   - token = UUID único
   - expires_at = now + 7 días
   - status = pending

4. Sistema envía email al lead:
   - Asunto: "Invitación de [Company] para unirte a la plataforma"
   - Link: https://platform.com/register?invitation_token=xxx
   - Mensaje personalizado (opcional)

5a. Lead hace clic y se registra:
   - Completa registro normal (Candidate + User)
   - Sistema detecta invitation_token en querystring
   - Vincula: CompanyCandidate.candidate_id = new_candidate_id
   - CandidateInvitation.status = accepted
   - Lead ahora puede aplicar formalmente a posiciones

5b. Lead no responde:
   - CandidateInvitation.status = expired (después de 7 días)
   - CompanyCandidate sigue como lead sin candidate_id
   - Empresa puede re-enviar invitación

5c. Lead rechaza:
   - Lead puede hacer clic en "No me interesa"
   - CandidateInvitation.status = rejected
   - CompanyCandidate.status = rejected
```

### Flujo 4: De Lead a Candidatura Formal (Application)

**Caso**: La empresa quiere mover un lead a candidatura formal para una posición específica.

```
1. Recruiter tiene lead en el CRM (CompanyCandidate)
2. Recruiter hace clic en "Incluir en candidatura"
3. Sistema muestra:
   - Posiciones activas de la empresa
   - Workflow a usar

4. Recruiter selecciona posición y confirma

5. Sistema verifica:
   - CompanyCandidate tiene candidate_id? (está registrado?)
   - Si NO: error, debe invitarse primero
   - Si SÍ: continúa

6. Sistema envía notificación al candidato:
   - "La empresa X te invita a candidatura para [Position]"
   - "¿Qué datos deseas compartir?"

7. Candidato autoriza datos a compartir:
   - Selecciona checkboxes:
     □ Educación
     □ Experiencia laboral
     □ Proyectos
     □ Habilidades
     □ Certificaciones
     □ Idiomas
   - Selecciona CV específico a compartir

8. Sistema crea CompanyApplication:
   - company_candidate_id = lead
   - candidate_id = candidato registrado
   - position_id = posición seleccionada
   - shared_data = JSON con permisos
   - workflow_id = workflow de la posición
   - current_stage_id = etapa inicial
   - status = active

9. Empresa ahora puede ver:
   - Datos autorizados del Candidate (según shared_data)
   - Solo en el contexto de esa application específica
   - CV compartido

10. CompanyCandidate.status puede cambiar a: in_process
```

**Importante**: Los datos privados del Candidate solo se comparten en el contexto de CompanyApplication, NO en CompanyCandidate.

### Flujo 5: Empresa gestiona Leads en CRM

```
Empresa puede:
  - Ver lista de leads (CompanyCandidate)
  - Filtrar por: status, source, tags, prioridad
  - Ver dashboard Kanban por workflow stages
  - EDITAR datos del lead (nombre, email, teléfono, país, linkedin, notas, tags)
  - Agregar comentarios internos (CandidateComment)
  - Mover entre stages de workflow (prospección)
  - Enviar invitación a registrarse (si no tiene candidate_id)
  - Convertir a candidatura formal (si tiene candidate_id)
  - Archivar leads

Empresa NO puede:
  - Ver education, experience, projects del Candidate
  - Editar datos privados del Candidate
  - Ver otros CompanyCandidates del mismo Candidate en otras empresas
```

### Flujo 6: Gestión de Workflows y Movimiento de Leads

#### 6.1. Creación de Workflow

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

#### 6.2. Asignación de Lead a Workflow

```
1. Al crear/agregar lead (CompanyCandidate):
   - Si empresa tiene workflow por defecto para leads:
     - Asignar workflow_id
     - Asignar current_stage_id a la etapa inicial (is_initial = true)
   - Si no hay workflow por defecto:
     - workflow_id = null
     - current_stage_id = null
     - Se puede asignar manualmente después

2. Sistema crea registro en CandidateStageHistory:
   - from_stage_id = null
   - to_stage_id = etapa inicial
   - comment = "Lead agregado al proceso"
```

**Nota**: Los workflows para CompanyCandidate suelen ser de "prospección" (contacto inicial, calificación, etc.)
Los workflows para CompanyApplication son de "selección" (entrevistas, evaluaciones, oferta, etc.)

#### 6.3. Movimiento de Lead entre Etapas

```
1. Recruiter selecciona lead (CompanyCandidate)
2. Sistema muestra etapa actual y transiciones disponibles
3. Recruiter selecciona acción (ej: "Pasar a Contactado", "Calificar", "Descartar")
4. Si requiere comentario:
   - Sistema solicita comentario
   - Recruiter ingresa comentario
5. Sistema valida:
   - Transición existe en WorkflowStageTransition
   - Usuario tiene permisos
   - Comentario presente si es requerido
6. Sistema actualiza CompanyCandidate:
   - current_stage_id = nueva etapa
   - status = puede cambiar según la etapa (lead → contacted → in_process)
   - updated_at = now
7. Sistema crea registro en CandidateStageHistory:
   - from_stage_id = etapa anterior
   - to_stage_id = nueva etapa
   - changed_by_user_id = recruiter
   - comment = comentario ingresado
   - duration_in_previous_stage = diferencia en minutos
   - created_at = now
8. Sistema publica evento: LeadStageChanged
9. Si nueva etapa es final de "prospección":
   - Puede convertirse en candidatura formal (si tiene candidate_id)
   - O archivarse si no califica
```

#### 6.4. Cambio de Workflow

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

### Estados de CompanyCandidate (Lead)

```
Nuevos estados basados en CRM:

lead → contacted → in_process → offer_made → hired
  ↓         ↓            ↓            ↓          ↓
rejected  rejected    rejected    rejected   archived
```

**Estados explicados**:
- `lead`: Prospecto inicial (nuevo en el sistema)
- `contacted`: Ya se ha contactado al lead
- `in_process`: En proceso de evaluación/candidatura formal activa
- `offer_made`: Se ha hecho una oferta
- `hired`: Contratado (estado final positivo)
- `rejected`: Descartado/no califica (estado final negativo)
- `archived`: Archivado (histórico, no activo)

### Estados de CompanyApplication (Candidatura Formal)

```
active → offer_made → accepted
  ↓           ↓           ↓
rejected  rejected    archived
  ↓           ↓
withdrawn withdrawn
```

**Estados explicados**:
- `active`: Candidatura activa en proceso de selección
- `offer_made`: Oferta enviada al candidato
- `accepted`: Candidato aceptó la oferta (contratado - estado final positivo)
- `rejected`: Empresa rechazó al candidato (estado final negativo)
- `withdrawn`: Candidato se retiró del proceso (estado final)
- `archived`: Candidatura archivada (proceso finalizado, histórico)

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

---

## 📊 Estado de Implementación

**Última actualización**: 2025-10-22

### ✅ Módulos Completados

#### 1. Company (CRUD Básico) - ✅ COMPLETADO
- ✅ Domain Layer: Entity, ValueObjects, Enums, Exceptions
- ✅ Infrastructure: Repository, Model
- ✅ Application: Commands (Create, Update, Suspend, Activate, Delete) + Queries (GetById, GetByDomain, List)
- ✅ Presentation: Controller, Router, Schemas
- ✅ Endpoints: 7 endpoints operativos
- ✅ Migraciones: Tabla `companies` creada

#### 2. CompanyUser (Gestión de Usuarios) - ✅ COMPLETADO
- ✅ Domain Layer: Entity, ValueObjects, Enums, Exceptions
- ✅ Infrastructure: Repository, Model
- ✅ Application: Commands (Create, Update, UpdateRole, Activate, Deactivate, Remove) + Queries (GetById, GetByCompanyAndUser, ListByCompany)
- ✅ Presentation: Controller, Router, Schemas
- ✅ Authentication: Login endpoint `/company/auth/login` (OAuth2 compliant)
- ✅ Endpoints: 8 endpoints + login
- ✅ Migraciones: Tabla `company_users` creada
- ✅ JWT Token con contexto de empresa (company_id, role)

#### 3. CompanyCandidate (Relación Empresa-Candidato) - ✅ COMPLETADO
- ✅ Domain Layer: Entity, 6 Enums, 5 ValueObjects, 7 Exceptions
- ✅ Infrastructure: Repository, Model
- ✅ Application:
  - Commands (8): Create, Update, Confirm, Reject, Archive, TransferOwnership, AssignWorkflow, ChangeStage
  - Queries (4): GetById, GetByCompanyAndCandidate, ListByCompany, ListByCandidate
- ✅ Presentation: Controller, Router, Schemas, Mappers
- ✅ Endpoints: 11 endpoints operativos
- ✅ Migraciones: Tabla `company_candidates` creada
- ✅ Business Logic: Ownership control, visibility settings, workflow integration

#### 4. CompanyWorkflow (Flujos de Trabajo) - ✅ COMPLETADO
- ✅ Domain Layer: Entity, 3 Enums, ValueObjects, Exceptions
- ✅ Infrastructure: Repository, Model
- ✅ Application:
  - Commands (7): Create, Update, Activate, Deactivate, Archive, SetAsDefault, UnsetAsDefault
  - Queries (2): GetById, ListByCompany
- ✅ Presentation: Controller, Router, Schemas, Mappers
- ✅ Endpoints: 10 endpoints operativos
- ✅ Migraciones: Tabla `company_workflows` creada
- ✅ Business Logic: Workflow status management, default workflow per company

#### 5. WorkflowStage (Etapas de Flujo) - ✅ COMPLETADO
- ✅ Domain Layer: Entity, 3 Enums, ValueObjects, Exceptions
- ✅ Infrastructure: Repository, Model
- ✅ Application:
  - Commands (6): CreateStage, UpdateStage, DeleteStage, ReorderStages, ActivateStage, DeactivateStage
  - Queries (4): GetStageById, ListStagesByWorkflow, GetInitialStage, GetFinalStages
- ✅ Presentation: Controller, Router, Schemas, Mappers
- ✅ Endpoints: 10 endpoints operativos
- ✅ Migraciones: Tabla `workflow_stages` creada
- ✅ Business Logic: Stage ordering, stage types (initial, intermediate, final)

### 🔄 Módulos Pendientes

#### 6. CandidateInvitation (Sistema de Invitaciones) - ⏳ PENDIENTE
**Prioridad**: Alta
- ❌ Domain Layer: Entity, Enums, ValueObjects, Exceptions
- ❌ Infrastructure: Repository, Model
- ❌ Application: Commands + Queries
- ❌ Presentation: Controller, Router, Schemas
- ❌ Email Service: Templates y envío
- ❌ Token Management: Generación y validación
- **Funcionalidad**: Invitar candidatos nuevos o existentes, aceptar/rechazar invitaciones

#### 7. CandidateComment (Comentarios) - ⏳ PENDIENTE
**Prioridad**: Alta
- ❌ Domain Layer: Entity, Enums, ValueObjects, Exceptions
- ❌ Infrastructure: Repository, Model
- ❌ Application: Commands (Create, Update, Delete) + Queries (List, GetById)
- ❌ Presentation: Controller, Router, Schemas
- **Funcionalidad**: Comentarios privados/compartidos, soft delete, contexto (interview, screening)

#### 8. CandidateAccessLog (Auditoría) - ⏳ PENDIENTE
**Prioridad**: Media
- ❌ Domain Layer: Entity, Enums, ValueObjects
- ❌ Infrastructure: Repository, Model
- ❌ Application: Commands (LogAccess) + Queries (ListLogs, GetLogsByCandidate)
- ❌ Presentation: Controller, Router (solo admin)
- **Funcionalidad**: GDPR compliance, tracking de accesos, reportes de auditoría

### 📈 Estadísticas del Proyecto

**Tablas Creadas**: 4/7 (57%)
- ✅ companies
- ✅ company_users
- ✅ company_candidates
- ✅ company_workflows
- ✅ workflow_stages
- ❌ candidate_invitations
- ❌ candidate_comments
- ❌ candidate_access_logs

**Endpoints Implementados**: ~46 endpoints
- Company: 7 endpoints
- CompanyUser: 8 endpoints + login
- CompanyCandidate: 11 endpoints
- CompanyWorkflow: 10 endpoints
- WorkflowStage: 10 endpoints

**Arquitectura**: 100% Clean Architecture + CQRS
- ✅ Separación de capas (Domain, Application, Infrastructure, Presentation)
- ✅ Commands (write) separados de Queries (read)
- ✅ Dependency Injection completo
- ✅ Repository Pattern
- ✅ Immutable Entities
- ✅ Domain Events (preparado)

**Testing**: ⏳ Pendiente
- ❌ Unit Tests
- ❌ Integration Tests
- ❌ E2E Tests

### 🔐 Sistema de Autenticación

**Endpoints de Login Implementados**:
- ✅ `POST /candidate/auth/login` - Autenticación de candidatos
- ✅ `POST /admin/auth/login` - Autenticación de administradores
- ✅ `POST /company/auth/login` - Autenticación de usuarios de empresa

**Características**:
- OAuth2PasswordRequestForm (estándar OAuth2)
- JWT Tokens con contexto (user_id, company_id, role)
- Bcrypt para passwords
- Token expiration configurable

### 📝 Próximos Pasos

1. **Inmediato**:
   - Implementar `CandidateInvitation` (crítico para onboarding)
   - Implementar `CandidateComment` (funcionalidad core)

2. **Corto Plazo**:
   - Implementar `CandidateAccessLog` (GDPR compliance)
   - Tests unitarios para módulos existentes

3. **Mediano Plazo**:
   - WorkflowStageTransition (lógica avanzada de workflows)
   - Dashboard y analytics
   - Email notifications

4. **Largo Plazo**:
   - Reporting avanzado
   - Export de datos
   - Integraciones (ATS externos)

---

## Development Status & Roadmap

### 📊 Estado Actual

**Backend**: Parcialmente implementado
- ✅ Company, CompanyUser, CompanyWorkflow, WorkflowStage (completos)
- ⚠️ CompanyCandidate (existente, requiere actualización)
- ❌ Position (pendiente)
- ❌ CompanyApplication (pendiente)
- ❌ Lead (fuera de scope V1)

**Frontend**: No existe implementación de dashboard de company
- ❌ Login page para company users
- ❌ Dashboard de ATS
- ❌ Gestión de candidatos
- ❌ Gestión de posiciones
- ❌ Gestión de candidaturas
- ❌ Kanban boards

**Servicios existentes**:
- `client-vite/src/services/companyService.ts` - Admin-focused (NO sirve para company dashboard)

---

### 🎯 Estrategia de Implementación

**DECISIÓN**: Implementar **ATS (Gestión de Candidatos)** primero, dejar **Head Hunting** para V2.

**Razón**:
- ATS es el core product (gestión de candidaturas)
- Head Hunting es un add-on premium
- Queremos validar el producto base primero

---

### 📚 Documentación de Referencia

#### Para Implementación Inmediata:
📋 **[COMPANY_IMPLEMENTATION_ROADMAP.md](COMPANY_IMPLEMENTATION_ROADMAP.md)** - Plan de desarrollo

Este documento contiene:
- ✅ Fases de desarrollo priorizadas (ATS primero)
- ✅ Tareas detalladas por fase
- ✅ Estimaciones de tiempo (37 días total)
- ✅ Checklist completo
- ✅ Cronograma
- ✅ Definición de MVP

#### Para Entender el Modelo Completo:
📄 **[COMPANY_FINAL_MODEL.md](COMPANY_FINAL_MODEL.md)** - Modelo de 3 niveles completo

Este documento explica:
- Lead → CompanyCandidate → CompanyApplication (3 niveles)
- Dos productos: Head Hunting + ATS
- Flujos de negocio detallados
- GDPR compliance
- Templates de email
- Mockups de UI

⚠️ **NOTA**: Head Hunting (Lead) está documentado pero NO se implementará en V1.

#### Documentos Antiguos (referencia histórica):
- ⚠️ [COMPANY_NEW_PARADIGM.md](COMPANY_NEW_PARADIGM.md) - Cambio de paradigma (histórico)
- ⚠️ [COMPANY_FRONTEND_TASKS.md](COMPANY_FRONTEND_TASKS.md) - Tareas antiguas (desactualizado)

---

### 🚀 Próximo Paso

**Fase 1**: CompanyCandidate Backend (3-4 días)
- Actualizar entity existente
- Añadir campos: `lead_id`, `source`, `resume_url`, etc.
- Commands y Queries completos
- API endpoints
- Migration

Ver detalles en: [COMPANY_IMPLEMENTATION_ROADMAP.md](COMPANY_IMPLEMENTATION_ROADMAP.md)

---

**Notas de Implementación**:
- Todos los handlers están registrados en `core/container.py`
- Todos los routers están cableados en `main.py`
- Las migraciones están en `alembic/versions/`
- Versión actual de migración: `468a891f5208`
