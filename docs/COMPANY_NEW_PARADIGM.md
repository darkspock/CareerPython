# Company Module - Nuevo Paradigma (CRM con Lead → Application)

**Fecha**: 2025-01-XX
**Versión**: 2.0

## Cambio Fundamental

### ❌ Paradigma ANTERIOR (Incorrecto)

- CompanyCandidate era una "relación" entre Company y Candidate
- La empresa podía ver datos del Candidate (con ownership y visibility_settings)
- Había dos tipos de ownership: company_owned y user_owned

### ✅ Paradigma NUEVO (Correcto)

- **CompanyCandidate = Lead** (entidad independiente, NO es relación)
- **CompanyApplication = Candidatura formal** (equivalente a "Opportunity" en CRM)
- Los datos del Candidate son **PRIVADOS** - la empresa NO puede verlos
- CompanyCandidate solo contiene datos básicos limitados
- Los datos completos se comparten SOLO en CompanyApplication (cuando candidato aplica formalmente)

---

## Conceptos Clave

### 1. CompanyCandidate (Lead)

**Es como "Lead" en un CRM tradicional** (prospecto, contacto inicial).

**Datos que contiene**:
- Datos básicos COPIADOS o ingresados: nombre, email, teléfono, país, linkedin
- Datos de gestión CRM: tags, notas internas, prioridad, source, status
- workflow_id / current_stage_id (para prospección)
- `candidate_id` (nullable - solo si el lead está registrado)

**NO contiene**:
- Education, experience, projects, skills del Candidate
- Esos datos están en la tabla `candidate` y son PRIVADOS

**Dos formas de creación**:
1. **Empresa agrega lead manualmente** → candidate_id = NULL, empresa rellena lo que sabe
2. **Candidato aplica** → candidate_id presente, se COPIAN datos básicos limitados

### 2. CompanyApplication (Candidatura Formal / Opportunity)

**Es como "Opportunity" en un CRM tradicional** (candidatura a posición específica).

**Requiere**:
- `company_candidate_id` (el lead que aplica)
- `candidate_id` (debe existir - el candidato debe estar registrado)
- `position_id` (posición a la que aplica)
- `shared_data` (JSON con permisos de visibilidad que el candidato autoriza)

**En shared_data el candidato autoriza compartir**:
- Education, experience, projects, skills, certifications, languages
- Resume_url (CV específico para esa candidatura)

**La empresa puede ver los datos privados del Candidate SOLO en el contexto de esta application específica.**

### 3. Position (Posición/Vacante)

Entidad nueva que representa las vacantes de la empresa.

- Título, descripción, ubicación, tipo de empleo
- Salary range
- Status: draft, active, paused, closed
- workflow_id (workflow por defecto para aplicaciones a esta posición)

---

## Flujos de Negocio

### Flujo 1: Empresa agrega Lead manualmente

```
1. Recruiter busca prospecto en LinkedIn
2. Recruiter crea lead en el sistema:
   - Rellena: nombre, email, teléfono, país, linkedin
   - Añade: tags, notas, prioridad, source=linkedin
3. Sistema crea CompanyCandidate con candidate_id = NULL
4. Recruiter puede:
   - EDITAR todos los datos (es company-owned)
   - Mover por workflow de prospección
   - Enviar invitación para registrarse
5. Si lead se registra:
   - Se crea Candidate + User
   - Se vincula: CompanyCandidate.candidate_id = nuevo_candidate_id
   - Los datos del Candidate siguen siendo PRIVADOS
   - El lead puede ahora aplicar formalmente a posiciones
```

### Flujo 2: Candidato aplica a posición

```
1. Candidato (ya registrado) ve posición publicada
2. Hace clic en "Aplicar"
3. Sistema muestra: "¿Qué datos básicos deseas compartir?"
   - Checkboxes: nombre ✓, email ✓, teléfono, país ✓, linkedin
4. Candidato confirma
5. Sistema crea CompanyCandidate con:
   - candidate_id = candidato
   - COPIA solo los datos seleccionados
   - source = application
   - status = lead (aún no es candidatura formal)
6. Empresa ve nuevo lead en CRM con datos básicos limitados
7. Empresa NO puede ver education, experience, projects, etc.
```

### Flujo 3: Lead → Candidatura Formal

```
1. Recruiter tiene lead en CRM (CompanyCandidate)
2. Recruiter: "Incluir en candidatura para [Position]"
3. Sistema verifica que lead tenga candidate_id (esté registrado)
4. Sistema envía notificación al candidato:
   "¿Deseas aplicar a [Position]? ¿Qué datos deseas compartir?"
5. Candidato autoriza datos:
   □ Educación
   □ Experiencia
   □ Proyectos
   □ Habilidades
   □ Selecciona CV específico
6. Sistema crea CompanyApplication:
   - company_candidate_id = lead
   - candidate_id = candidato
   - position_id = posición
   - shared_data = JSON con permisos
   - workflow_id = workflow de selección
   - current_stage_id = etapa inicial
7. Empresa puede ver datos autorizados SOLO en contexto de esta application
```

### Flujo 4: Empresa gestiona Leads (CRM)

```
Dashboard Kanban muestra:
- Columnas por workflow stages de prospección
- Cards de leads (CompanyCandidate)
- Drag & drop para mover entre stages
- Filtros por: status, source, tags, prioridad

Acciones sobre lead:
- Ver/Editar datos básicos
- Añadir comentarios internos
- Mover a otra stage
- Enviar invitación (si no tiene candidate_id)
- Convertir a candidatura (si tiene candidate_id)
- Archivar

Empresa NO puede ver:
- Education, experience, projects del Candidate
- Otros CompanyCandidates del mismo Candidate en otras empresas
```

---

## Diferencias Clave con el Paradigma Anterior

| Aspecto | Anterior (❌) | Nuevo (✅) |
|---------|--------------|-----------|
| CompanyCandidate | Relación con Candidate | Entidad independiente (Lead) |
| Datos visibles | Según visibility_settings | Solo datos básicos copiados |
| Ownership | company_owned / user_owned | No existe ownership, es un lead |
| Privacidad | Configurab le por candidato | Por defecto privado, solo basic info |
| Datos completos | En CompanyCandidate | En CompanyApplication |
| Candidatura | Implícita en CompanyCandidate | Explícita en CompanyApplication |
| Workflows | Uno para todo el proceso | Dos: prospección (Lead) y selección (Application) |

---

## Cambios en el Modelo de Datos

### CompanyCandidate - Campos Nuevos/Modificados

**Campos eliminados**:
- ❌ `ownership_status` (ya no existe ownership)
- ❌ `visibility_settings` (los datos son básicos por defecto)
- ❌ `confirmed_at`, `rejected_at` (simplificado)

**Campos añadidos**:
- ✅ `first_name`, `last_name` (datos básicos)
- ✅ `phone`, `country`, `linkedin_url` (datos básicos)
- ✅ `source` (application, manual_entry, referral, linkedin, other)
- ✅ `position_interest` (posición de interés)
- ✅ `salary_expectation`, `availability`
- ✅ `invitation_sent_at`, `invitation_token`, `invitation_expires_at`

**Status modificado**:
- Antes: `pending_invitation`, `pending_confirmation`, `active`, `rejected`, `archived`
- Ahora: `lead`, `contacted`, `in_process`, `offer_made`, `hired`, `rejected`, `archived`

### CompanyApplication - Entidad NUEVA

```python
CompanyApplication:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate)
  - candidate_id: UUID (FK → Candidate, required)
  - company_id: UUID (FK → Company)
  - position_id: UUID (FK → Position)
  - workflow_id: UUID (workflow de selección)
  - current_stage_id: UUID
  - shared_data: JSON (permisos de visibilidad)
  - status: Enum [active, offer_made, accepted, rejected, withdrawn, archived]
  - applied_at: DateTime
  - source: Enum [direct_application, invitation_response, referral, linkedin]
  - tags: Array[String]
  - internal_notes: Text
  - priority: Enum [low, medium, high]
  - salary_offered: Decimal
  - created_at, updated_at, archived_at
```

### Position - Entidad NUEVA

```python
Position:
  - id: UUID
  - company_id: UUID (FK → Company)
  - title: String
  - description: Text
  - department, location: String
  - employment_type: Enum [full_time, part_time, contract, internship, temporary]
  - remote_type: Enum [on_site, remote, hybrid]
  - salary_range_min, salary_range_max: Decimal
  - salary_currency: String
  - requirements, responsibilities, benefits: Text
  - status: Enum [draft, active, paused, closed, cancelled]
  - workflow_id: UUID (workflow por defecto)
  - created_by_user_id: UUID
  - published_at, closed_at: DateTime
  - created_at, updated_at: DateTime
```

### CandidateInvitation - Simplificado

**Antes**: Se usaba tanto para invitar nuevos como confirmar existentes
**Ahora**: Solo para invitar leads (CompanyCandidate sin candidate_id) a registrarse

```python
CandidateInvitation:
  - id: UUID
  - company_candidate_id: UUID (FK → CompanyCandidate)
  - email: String
  - company_id: UUID
  - invited_by_user_id: UUID
  - token: String (único para link de registro)
  - status: Enum [pending, accepted, rejected, expired, cancelled]
  - message: Text (opcional)
  - expires_at: DateTime
  - accepted_at, rejected_at: DateTime
  - created_at: DateTime
```

---

## Impacto en Frontend

### Dashboard de Company

**Vista de Leads (CompanyCandidate)**:
- Lista/Kanban de leads
- Datos mostrados: nombre, email, teléfono, país, linkedin, tags, prioridad
- Indicador si tiene candidate_id (está registrado)
- Acciones: Editar, Comentar, Mover stage, Enviar invitación, Convertir a candidatura

**Vista de Candidaturas (CompanyApplication)**:
- Lista de aplicaciones formales por posición
- Mostrar datos autorizados por candidato (según shared_data)
- Workflow de selección (entrevistas, evaluación, oferta)
- Ver CV compartido

**Vista de Posiciones (Position)**:
- CRUD de posiciones
- Ver # de aplicaciones por posición
- Configurar workflow de selección

### Páginas a Implementar

1. **Leads Management**:
   - Lista de leads (tabla + filtros)
   - Añadir lead manual
   - Detalle de lead (con comentarios)
   - Kanban de prospección

2. **Posiciones**:
   - Lista de posiciones
   - Crear/editar posición
   - Ver aplicaciones de una posición

3. **Candidaturas (Applications)**:
   - Lista de candidaturas por posición
   - Detalle de candidatura (con datos autorizados)
   - Workflow de selección (entrevistas, etc.)
   - Kanban de selección

4. **Settings**:
   - Configurar workflows de prospección
   - Configurar workflows de selección

---

## Impacto en Backend

### Módulos a Implementar/Actualizar

1. **CompanyCandidate** (actualizar):
   - Eliminar lógica de ownership
   - Eliminar lógica de visibility_settings
   - Añadir campos básicos (first_name, last_name, phone, country, linkedin)
   - Actualizar estados (lead, contacted, in_process, etc.)
   - Actualizar comandos/queries

2. **CompanyApplication** (NUEVO):
   - Entidad completa
   - Commands: Create, Update, ChangeStage, MakeOffer, Accept, Reject, Withdraw, Archive
   - Queries: GetById, ListByPosition, ListByCandidate, ListByCompany
   - Lógica de shared_data (autorización de visibilidad)

3. **Position** (NUEVO):
   - Entidad completa
   - Commands: Create, Update, Publish, Pause, Close, Cancel, Delete
   - Queries: GetById, ListByCompany, ListActive

4. **CandidateInvitation** (simplificar):
   - Eliminar invitation_type (solo hay un tipo ahora)
   - Vincular a company_candidate_id en lugar de candidate_id

### Endpoints a Implementar

**CompanyCandidate (Lead)**:
- POST `/api/company/{company_id}/leads` - Crear lead
- GET `/api/company/{company_id}/leads` - Listar leads
- GET `/api/company/leads/{lead_id}` - Obtener lead
- PUT `/api/company/leads/{lead_id}` - Actualizar lead
- DELETE `/api/company/leads/{lead_id}` - Eliminar lead
- POST `/api/company/leads/{lead_id}/send-invitation` - Enviar invitación
- POST `/api/company/leads/{lead_id}/convert-to-application` - Convertir a candidatura

**Position**:
- POST `/api/company/{company_id}/positions` - Crear posición
- GET `/api/company/{company_id}/positions` - Listar posiciones
- GET `/api/positions/{position_id}` - Obtener posición
- PUT `/api/positions/{position_id}` - Actualizar posición
- DELETE `/api/positions/{position_id}` - Eliminar posición
- POST `/api/positions/{position_id}/publish` - Publicar posición
- POST `/api/positions/{position_id}/pause` - Pausar posición
- POST `/api/positions/{position_id}/close` - Cerrar posición

**CompanyApplication**:
- POST `/api/positions/{position_id}/apply` - Candidato aplica (público)
- GET `/api/company/{company_id}/applications` - Listar aplicaciones
- GET `/api/positions/{position_id}/applications` - Aplicaciones de una posición
- GET `/api/applications/{application_id}` - Obtener aplicación
- PUT `/api/applications/{application_id}` - Actualizar aplicación
- POST `/api/applications/{application_id}/change-stage` - Cambiar etapa
- POST `/api/applications/{application_id}/make-offer` - Hacer oferta
- POST `/api/applications/{application_id}/accept` - Aceptar (candidato)
- POST `/api/applications/{application_id}/reject` - Rechazar (empresa)
- POST `/api/applications/{application_id}/withdraw` - Retirar (candidato)
- POST `/api/applications/{application_id}/archive` - Archivar

---

## Migration Strategy

### Fase 1: Crear Nuevas Entidades

1. Crear tabla `positions`
2. Crear tabla `company_applications`
3. Actualizar tabla `company_candidates` (añadir campos básicos, modificar status enum)
4. Actualizar tabla `candidate_invitations` (simplificar)

### Fase 2: Migrar Datos Existentes (si hay)

1. CompanyCandidate con ownership=company_owned:
   - Mantener como lead
   - status = lead
   - Los datos ya están en CompanyCandidate

2. CompanyCandidate con ownership=user_owned:
   - Mantener como lead con candidate_id
   - Copiar datos básicos de Candidate si no existen
   - status = contacted o in_process

### Fase 3: Eliminar Columnas Obsoletas

1. Eliminar `ownership_status` de CompanyCandidate
2. Eliminar `visibility_settings` de CompanyCandidate
3. Actualizar enum de `status`

### Fase 4: Implementar Nuevos Módulos

1. Backend: Position module
2. Backend: CompanyApplication module
3. Frontend: Páginas de Leads
4. Frontend: Páginas de Posiciones
5. Frontend: Páginas de Candidaturas

---

## Resumen de Cambios

### Lo que NO cambia

- Company, CompanyUser, CompanyWorkflow, WorkflowStage siguen igual
- CandidateComment sigue igual (comentarios sobre CompanyCandidate/Lead)
- Sistema de workflows sigue igual

### Lo que cambia radicalmente

- **CompanyCandidate**: De "relación" a "Lead independiente"
- **Privacidad**: Candidate data es privado por defecto
- **Visibilidad**: Solo datos básicos en Lead, datos completos en Application
- **Workflows**: Dos tipos (prospección vs selección)
- **Candidatura**: Explícita en CompanyApplication (no implícita)

### Nuevas entidades

- **Position**: Vacantes de la empresa
- **CompanyApplication**: Candidatura formal a posición específica

---

## Próximos Pasos

1. **Revisar y aprobar** este nuevo paradigma
2. **Actualizar COMPANY_FRONTEND_TASKS.md** con el nuevo modelo
3. **Crear migraciones** de base de datos
4. **Implementar backend** (Position, CompanyApplication, actualizar CompanyCandidate)
5. **Implementar frontend** (Leads, Positions, Applications)

---

**Nota final**: Este cambio es fundamental para garantizar la privacidad del candidato y alinear el sistema con las mejores prácticas de CRM (Lead → Opportunity → Deal).
