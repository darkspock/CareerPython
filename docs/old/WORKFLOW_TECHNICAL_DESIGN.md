# Sistema de Flujos de Trabajo - Diseño Técnico

**Versión**: 2.0
**Fecha**: 2025-10-26
**Basado en**: WORKFLOW3.md, WORKFLOW2.md, WORKFLOW_SYSTEM_ARCHITECTURE.md

---

## Tabla de Contenidos

1. [Arquitectura General](#arquitectura-general)
2. [Modelo de Datos](#modelo-de-datos)
3. [Flujos de Trabajo](#flujos-de-trabajo)
4. [Campos Personalizados](#campos-personalizados)
5. [Sistema de Roles y Tareas](#sistema-de-roles-y-tareas)
6. [Sistema de Emails](#sistema-de-emails)
7. [Sistema de Permisos](#sistema-de-permisos)
8. [APIs](#apis)
9. [Eventos de Dominio](#eventos-de-dominio)
10. [Implementación Frontend](#implementación-frontend)

---

## Arquitectura General

### Principios de Diseño

El sistema sigue Clean Architecture con CQRS:

```
Presentation Layer (Controllers, Routers, Schemas)
    ↓
Application Layer (Commands, Queries, Handlers, DTOs)
    ↓
Domain Layer (Entities, Value Objects, Events)
    ↓
Infrastructure Layer (Repositories, Models, External Services)
```

### Módulos del Sistema

```
src/
├── workflow/                           # Flujos de trabajo
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── company_workflow.py
│   │   │   └── workflow_stage.py
│   │   ├── value_objects/
│   │   │   ├── workflow_id.py
│   │   │   ├── workflow_stage_id.py
│   │   │   └── workflow_type.py
│   │   ├── enums/
│   │   │   ├── stage_type.py
│   │   │   └── workflow_status.py
│   │   └── infrastructure/
│   │       └── workflow_repository_interface.py
│   ├── application/
│   │   ├── commands/
│   │   ├── queries/
│   │   ├── handlers/
│   │   └── dtos/
│   ├── infrastructure/
│   │   ├── models/
│   │   └── repositories/
│   └── presentation/
│       ├── controllers/
│       ├── routers/
│       ├── schemas/
│       └── mappers/
│
├── candidate_application/              # Aplicaciones de candidatos
│   ├── domain/
│   │   ├── entities/
│   │   │   └── candidate_application.py
│   │   ├── value_objects/
│   │   │   ├── application_id.py
│   │   │   ├── application_data.py   # JSON data
│   │   │   └── shared_data.py         # JSON shared data
│   │   └── enums/
│   │       └── application_status.py
│   └── ...
│
├── position_stage_assignment/          # Asignaciones usuario-etapa
│   ├── domain/
│   │   ├── entities/
│   │   │   └── position_stage_assignment.py
│   │   └── value_objects/
│   │       └── assigned_user_ids.py   # Array de user IDs
│   └── ...
│
├── talent_pool/                        # Pool de talento
│   ├── domain/
│   │   ├── entities/
│   │   │   └── company_talent_pool.py
│   │   └── value_objects/
│   └── ...
│
├── email_template/                     # Plantillas de email
│   ├── domain/
│   │   ├── entities/
│   │   │   └── email_template.py
│   │   └── value_objects/
│   └── ...
│
└── workflow_custom_field/              # Campos personalizados
    ├── domain/
    │   ├── entities/
    │   │   ├── custom_field.py
    │   │   └── field_configuration.py
    │   ├── value_objects/
    │   │   ├── field_type.py
    │   │   └── field_visibility.py
    │   └── enums/
    └── ...
```

---

## Modelo de Datos

### Entity Relationship Diagram

```
Company
  ↓ 1:N
CompanyWorkflow
  ↓ 1:N
WorkflowStage ←─────┐
  ↓                 │
  ├─→ CustomField   │
  │   (N:N)         │
  │                 │
Position             │
  ↓                 │
  ├─→ Workflow (FK) │
  └─→ PositionStageAssignment
        ↓           │
        └─→ Stage ──┘
        └─→ UserIDs[]

CompanyCandidate
  ↓
CandidateApplication
  ├─→ Position
  ├─→ Workflow (copy)
  ├─→ CurrentStage
  ├─→ ApplicationData (JSON)
  └─→ SharedData (JSON)

CompanyTalentPool
  ├─→ CompanyCandidate
  └─→ Comments
```

### Tablas Principales

#### 1. `company_workflows`

```sql
CREATE TABLE company_workflows (
    id VARCHAR(255) PRIMARY KEY,
    company_id VARCHAR(255) NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    workflow_type VARCHAR(50) NOT NULL, -- 'prospecting' | 'selection'
    status VARCHAR(50) NOT NULL,        -- 'active' | 'inactive' | 'archived'
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_company_workflow_name UNIQUE(company_id, name)
);

CREATE INDEX idx_company_workflows_company ON company_workflows(company_id);
CREATE INDEX idx_company_workflows_type ON company_workflows(workflow_type);
CREATE INDEX idx_company_workflows_status ON company_workflows(status);
```

#### 2. `workflow_stages`

```sql
CREATE TABLE workflow_stages (
    id VARCHAR(255) PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL REFERENCES company_workflows(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    stage_type VARCHAR(50) NOT NULL,    -- 'initial' | 'intermediate' | 'final' | 'custom'
    order_index INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,

    -- Campos de configuración avanzada
    required_outcome VARCHAR(100),      -- Resultado requerido para avanzar
    estimated_duration_days INTEGER,    -- Duración estimada
    deadline_days INTEGER,              -- Días límite
    estimated_cost DECIMAL(10,2),       -- Costo estimado

    -- Campos de asignación predeterminada
    default_roles JSONB,                -- ['Tech Lead', 'HR Manager']
    default_assigned_users JSONB,       -- ['user_id_1', 'user_id_2']

    -- Campos de email
    email_template_id VARCHAR(255) REFERENCES email_templates(id),
    custom_email_text TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_workflow_stage_order UNIQUE(workflow_id, order_index)
);

CREATE INDEX idx_workflow_stages_workflow ON workflow_stages(workflow_id);
CREATE INDEX idx_workflow_stages_order ON workflow_stages(workflow_id, order_index);
```

#### 3. `workflow_custom_fields`

Define los campos personalizados de cada workflow.

```sql
CREATE TABLE workflow_custom_fields (
    id VARCHAR(255) PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL REFERENCES company_workflows(id) ON DELETE CASCADE,
    field_key VARCHAR(100) NOT NULL,    -- Identificador único del campo
    field_name VARCHAR(255) NOT NULL,   -- Nombre mostrado
    field_type VARCHAR(50) NOT NULL,    -- Tipo de campo (ver más abajo)
    field_config JSONB,                 -- Configuración específica del tipo
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_workflow_field_key UNIQUE(workflow_id, field_key)
);

CREATE INDEX idx_workflow_custom_fields_workflow ON workflow_custom_fields(workflow_id);
```

**Tipos de campos (`field_type`):**
- `text_short`: Texto corto
- `text_long`: Área de texto
- `dropdown`: Lista desplegable
- `checkbox`: Casillas de verificación
- `radio`: Botones de radio
- `date`: Fecha
- `datetime`: Fecha y hora
- `time`: Hora
- `file`: Archivo adjunto
- `currency`: Moneda
- `integer`: Número entero
- `float`: Número decimal
- `percentage`: Porcentaje

**Ejemplos de `field_config`:**
```json
// Dropdown
{
    "options": ["Junior", "Mid", "Senior", "Lead"],
    "allow_multiple": false
}

// Checkbox
{
    "options": ["Python", "Java", "JavaScript", "Go"]
}

// Currency
{
    "currency": "USD",
    "min": 0,
    "max": 1000000
}

// File
{
    "allowed_extensions": [".pdf", ".doc", ".docx"],
    "max_size_mb": 5
}
```

#### 4. `stage_field_configurations`

Define cómo se comporta cada campo en cada etapa.

```sql
CREATE TABLE stage_field_configurations (
    id VARCHAR(255) PRIMARY KEY,
    stage_id VARCHAR(255) NOT NULL REFERENCES workflow_stages(id) ON DELETE CASCADE,
    custom_field_id VARCHAR(255) NOT NULL REFERENCES workflow_custom_fields(id) ON DELETE CASCADE,
    visibility VARCHAR(50) NOT NULL,    -- 'hidden' | 'mandatory' | 'recommended' | 'optional'
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_stage_field UNIQUE(stage_id, custom_field_id)
);

CREATE INDEX idx_stage_field_configs_stage ON stage_field_configurations(stage_id);
CREATE INDEX idx_stage_field_configs_field ON stage_field_configurations(custom_field_id);
```

#### 5. `job_positions`

```sql
ALTER TABLE job_positions ADD COLUMN workflow_id VARCHAR(255) REFERENCES company_workflows(id);

CREATE INDEX idx_job_positions_workflow ON job_positions(workflow_id);
```

#### 6. `position_stage_assignments`

Mapea usuarios a etapas específicas de una posición.

```sql
CREATE TABLE position_stage_assignments (
    id VARCHAR(255) PRIMARY KEY,
    position_id VARCHAR(255) NOT NULL REFERENCES job_positions(id) ON DELETE CASCADE,
    stage_id VARCHAR(255) NOT NULL REFERENCES workflow_stages(id),
    assigned_user_ids JSONB NOT NULL DEFAULT '[]', -- Array de CompanyUser IDs
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_position_stage UNIQUE(position_id, stage_id)
);

CREATE INDEX idx_position_stage_assignments_position ON position_stage_assignments(position_id);
CREATE INDEX idx_position_stage_assignments_stage ON position_stage_assignments(stage_id);
```

#### 7. `candidate_applications`

```sql
ALTER TABLE candidate_applications
ADD COLUMN workflow_id VARCHAR(255) REFERENCES company_workflows(id),
ADD COLUMN current_stage_id VARCHAR(255) REFERENCES workflow_stages(id),
ADD COLUMN application_data JSONB DEFAULT '{}',      -- Datos capturados durante el proceso
ADD COLUMN shared_data JSONB DEFAULT '{}',            -- Datos que el candidato autorizó compartir
ADD COLUMN stage_entered_at TIMESTAMP,                -- Cuándo entró a la etapa actual
ADD COLUMN stage_deadline TIMESTAMP,                  -- Fecha límite de la etapa actual
ADD COLUMN task_status VARCHAR(50) DEFAULT 'pending'; -- 'pending' | 'in_progress' | 'completed' | 'blocked'

CREATE INDEX idx_candidate_applications_workflow ON candidate_applications(workflow_id);
CREATE INDEX idx_candidate_applications_stage ON candidate_applications(current_stage_id);
CREATE INDEX idx_candidate_applications_deadline ON candidate_applications(stage_deadline);
CREATE INDEX idx_candidate_applications_task_status ON candidate_applications(task_status);
```

**Estructura de `application_data`:**
```json
{
    "custom_field_key_1": "value",
    "custom_field_key_2": ["multiple", "values"],
    "salary_expectation": 120000,
    "available_start_date": "2025-02-01",
    "technical_test_score": 85,
    "interview_notes": "Excellent communication skills",
    "stage_history": [
        {
            "stage_id": "stage_1",
            "stage_name": "Screening",
            "entered_at": "2025-01-15T10:00:00Z",
            "exited_at": "2025-01-17T14:30:00Z",
            "duration_hours": 52.5,
            "changed_by": "user_id_1",
            "data_snapshot": {}
        }
    ]
}
```

**Estructura de `shared_data`:**
```json
{
    "include_education": true,
    "include_experience": true,
    "include_projects": false,
    "include_skills": true,
    "include_languages": true,
    "resume_ids": ["resume_1", "resume_2"],
    "portfolio_url": "https://example.com/portfolio"
}
```

#### 8. `company_talent_pool`

```sql
CREATE TABLE company_talent_pool (
    id VARCHAR(255) PRIMARY KEY,
    company_id VARCHAR(255) NOT NULL REFERENCES companies(id),
    company_candidate_id VARCHAR(255) NOT NULL REFERENCES company_candidates(id),
    comments TEXT,
    tags JSONB DEFAULT '[]',
    added_at TIMESTAMP NOT NULL DEFAULT NOW(),
    added_by_user_id VARCHAR(255) REFERENCES company_users(id),

    CONSTRAINT unique_talent_pool_candidate UNIQUE(company_id, company_candidate_id)
);

CREATE INDEX idx_talent_pool_company ON company_talent_pool(company_id);
CREATE INDEX idx_talent_pool_candidate ON company_talent_pool(company_candidate_id);
```

#### 9. `email_templates`

```sql
CREATE TABLE email_templates (
    id VARCHAR(255) PRIMARY KEY,
    company_id VARCHAR(255) NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,                 -- HTML con placeholders
    variables JSONB DEFAULT '[]',       -- Variables disponibles
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_company_template_name UNIQUE(company_id, name)
);

CREATE INDEX idx_email_templates_company ON email_templates(company_id);
```

**Variables soportadas:**
- `{{candidate_name}}`: Nombre completo del candidato
- `{{candidate_first_name}}`: Primer nombre
- `{{position_title}}`: Título de la posición
- `{{company_name}}`: Nombre de la empresa
- `{{stage_name}}`: Nombre de la etapa
- `{{custom_text}}`: Texto personalizado adicional

#### 10. `company_users` (extensión)

```sql
ALTER TABLE company_users ADD COLUMN roles JSONB DEFAULT '[]';

-- Roles comunes:
-- ["HR Manager", "Tech Lead", "Recruiter", "Hiring Manager", "Interviewer", "Department Head"]
```

---

## Flujos de Trabajo

### Tipos de Workflow

#### 1. Prospecting (Sourcing)

**Propósito**: Gestión de leads y candidatos que aún no han aplicado a posiciones específicas.

**Etapas fijas** (no personalizables por ahora):
1. `Pending`: Candidato recién ingresado
2. `Screening`: Revisión inicial
3. `Discarded`: Descartado
4. `On Hold`: En espera
5. `To Talent Pool`: Mover al pool de talento

**Flujo:**
```
Pending → Screening → {
    ✅ To Talent Pool → Guardar en company_talent_pool
    ❌ Discarded → Marcar como descartado
    ⏸️ On Hold → Mantener en espera
}
```

**Transición a Evaluation:**
Cuando un candidato es aceptado en Screening, puede:
- Aplicar a una posición específica (crear `CandidateApplication`)
- Pasar a workflow de tipo `selection`

#### 2. Selection (Evaluation)

**Propósito**: Proceso formal de selección para una posición específica.

**Etapas personalizables:**
- La empresa define las etapas según su proceso
- Puede tener entre 2 y 20 etapas (recomendado: 4-8)

**Ejemplos de etapas:**
- HR Interview
- Technical Test
- Technical Interview
- Team Lead Interview
- Reference Check
- Offer
- Hired

#### 3. Offer and Pre-Onboarding

**Propósito**: Formalización de la oferta y preparación para onboarding.

**Etapas sugeridas (personalizables):**
1. `Offer Proposal`: Preparación de oferta
2. `Negotiation`: Negociación de términos
3. `Document Submission`: Envío de documentos
4. `Document Verification`: Verificación de documentos
5. `Contract Signing`: Firma del contrato
6. `Hired`: Contratado (final)

### WorkflowStage Entity

```python
@dataclass
class WorkflowStage:
    id: WorkflowStageId
    workflow_id: WorkflowId
    name: str
    description: Optional[str]
    stage_type: StageType  # initial, intermediate, final, custom
    order: int
    is_active: bool

    # Advanced configuration
    required_outcome: Optional[str]
    estimated_duration_days: Optional[int]
    deadline_days: Optional[int]
    estimated_cost: Optional[Decimal]

    # Assignment defaults
    default_roles: List[str]
    default_assigned_users: List[str]

    # Email configuration
    email_template_id: Optional[EmailTemplateId]
    custom_email_text: Optional[str]

    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        workflow_id: WorkflowId,
        name: str,
        stage_type: StageType,
        order: int,
        description: Optional[str] = None,
        estimated_duration_days: Optional[int] = None,
        deadline_days: Optional[int] = None,
        estimated_cost: Optional[Decimal] = None,
        default_roles: Optional[List[str]] = None,
        default_assigned_users: Optional[List[str]] = None,
        email_template_id: Optional[EmailTemplateId] = None,
        custom_email_text: Optional[str] = None
    ) -> "WorkflowStage":
        """Factory method para crear una nueva etapa"""

        # Validaciones
        if deadline_days and deadline_days < 1:
            raise ValueError("deadline_days must be positive")

        if estimated_cost and estimated_cost < 0:
            raise ValueError("estimated_cost must be non-negative")

        if estimated_duration_days and estimated_duration_days < 1:
            raise ValueError("estimated_duration_days must be positive")

        return cls(
            id=WorkflowStageId.generate(),
            workflow_id=workflow_id,
            name=name,
            description=description,
            stage_type=stage_type,
            order=order,
            is_active=True,
            required_outcome=None,
            estimated_duration_days=estimated_duration_days,
            deadline_days=deadline_days,
            estimated_cost=estimated_cost,
            default_roles=default_roles or [],
            default_assigned_users=default_assigned_users or [],
            email_template_id=email_template_id,
            custom_email_text=custom_email_text,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        estimated_duration_days: Optional[int] = None,
        deadline_days: Optional[int] = None,
        estimated_cost: Optional[Decimal] = None,
        default_roles: Optional[List[str]] = None,
        default_assigned_users: Optional[List[str]] = None,
        email_template_id: Optional[EmailTemplateId] = None,
        custom_email_text: Optional[str] = None
    ) -> None:
        """Actualizar campos de la etapa"""

        if name:
            self.name = name
        if description is not None:
            self.description = description
        if estimated_duration_days:
            self.estimated_duration_days = estimated_duration_days
        if deadline_days:
            if deadline_days < 1:
                raise ValueError("deadline_days must be positive")
            self.deadline_days = deadline_days
        if estimated_cost is not None:
            if estimated_cost < 0:
                raise ValueError("estimated_cost must be non-negative")
            self.estimated_cost = estimated_cost
        if default_roles is not None:
            self.default_roles = default_roles
        if default_assigned_users is not None:
            self.default_assigned_users = default_assigned_users
        if email_template_id is not None:
            self.email_template_id = email_template_id
        if custom_email_text is not None:
            self.custom_email_text = custom_email_text

        self.updated_at = datetime.now(UTC)
```

---

## Campos Personalizados

### CustomField Entity

```python
@dataclass
class CustomField:
    id: CustomFieldId
    workflow_id: WorkflowId
    field_key: str              # Identificador único (snake_case)
    field_name: str             # Nombre mostrado
    field_type: FieldType
    field_config: Dict[str, Any]
    order: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        workflow_id: WorkflowId,
        field_key: str,
        field_name: str,
        field_type: FieldType,
        field_config: Dict[str, Any],
        order: int
    ) -> "CustomField":
        """Factory method"""

        # Validar field_key
        if not re.match(r'^[a-z][a-z0-9_]*$', field_key):
            raise ValueError("field_key must be snake_case")

        # Validar field_config según field_type
        cls._validate_config(field_type, field_config)

        return cls(
            id=CustomFieldId.generate(),
            workflow_id=workflow_id,
            field_key=field_key,
            field_name=field_name,
            field_type=field_type,
            field_config=field_config,
            order=order,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

    @staticmethod
    def _validate_config(field_type: FieldType, config: Dict[str, Any]) -> None:
        """Validar configuración según tipo"""

        if field_type in [FieldType.DROPDOWN, FieldType.CHECKBOX, FieldType.RADIO]:
            if "options" not in config or not config["options"]:
                raise ValueError("options required for choice fields")

        if field_type == FieldType.CURRENCY:
            if "currency" not in config:
                raise ValueError("currency required for currency field")

        if field_type == FieldType.FILE:
            if "allowed_extensions" not in config:
                raise ValueError("allowed_extensions required for file field")
```

### FieldConfiguration Entity

Define visibilidad de un campo en una etapa específica.

```python
@dataclass
class FieldConfiguration:
    id: FieldConfigurationId
    stage_id: WorkflowStageId
    custom_field_id: CustomFieldId
    visibility: FieldVisibility  # hidden, mandatory, recommended, optional
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        stage_id: WorkflowStageId,
        custom_field_id: CustomFieldId,
        visibility: FieldVisibility
    ) -> "FieldConfiguration":
        return cls(
            id=FieldConfigurationId.generate(),
            stage_id=stage_id,
            custom_field_id=custom_field_id,
            visibility=visibility,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
```

### Tipos de Campos

```python
class FieldType(Enum):
    TEXT_SHORT = "text_short"
    TEXT_LONG = "text_long"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    FILE = "file"
    CURRENCY = "currency"
    INTEGER = "integer"
    FLOAT = "float"
    PERCENTAGE = "percentage"

class FieldVisibility(Enum):
    HIDDEN = "hidden"
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"
```

---

## Sistema de Roles y Tareas

### CompanyUser Roles

Los roles se almacenan en `company_users.roles` como array JSONB.

**Roles comunes:**
- `HR Manager`: Gestiona proceso de RH
- `Tech Lead`: Lidera evaluaciones técnicas
- `Recruiter`: Reclutador
- `Hiring Manager`: Gerente contratante
- `Interviewer`: Entrevistador general
- `Department Head`: Jefe de departamento

### Task Priority System

```python
@dataclass
class TaskPriority:
    base_priority: int = 100
    deadline_weight: int = 0
    position_weight: int = 0
    candidate_weight: int = 0

    @property
    def total_score(self) -> int:
        return (
            self.base_priority +
            self.deadline_weight +
            self.position_weight +
            self.candidate_weight
        )

    @classmethod
    def calculate(
        cls,
        application: CandidateApplication,
        current_date: datetime
    ) -> "TaskPriority":
        """Calcular prioridad de una aplicación"""

        deadline_weight = cls._calculate_deadline_weight(
            application.stage_deadline,
            current_date
        )

        position_weight = application.position.priority * 10  # 0-5 stars → 0-50
        candidate_weight = application.candidate.priority * 5  # 0-5 stars → 0-25

        return cls(
            deadline_weight=deadline_weight,
            position_weight=position_weight,
            candidate_weight=candidate_weight
        )

    @staticmethod
    def _calculate_deadline_weight(deadline: Optional[datetime], now: datetime) -> int:
        """Calcular peso por fecha límite"""

        if not deadline:
            return 0

        days_until_deadline = (deadline - now).days

        if days_until_deadline < 0:  # Overdue
            return 50
        elif days_until_deadline == 0:  # Due today
            return 30
        elif days_until_deadline <= 2:  # Due in 1-2 days
            return 20
        elif days_until_deadline <= 5:  # Due in 3-5 days
            return 10
        else:  # Due in 6+ days
            return 0
```

### Task Assignment

```python
@dataclass
class TaskAssignment:
    application: CandidateApplication
    priority: TaskPriority
    assignment_type: AssignmentType  # direct, role_based

class AssignmentType(Enum):
    DIRECT = "direct"          # Usuario asignado específicamente
    ROLE_BASED = "role_based"  # Usuario tiene rol coincidente
```

### Task Queries

#### GetMyAssignedTasksQuery

Retorna aplicaciones donde el usuario está directamente asignado a la etapa actual.

```python
@dataclass
class GetMyAssignedTasksQuery:
    user_id: str
    filters: Optional[TaskFilters] = None

class GetMyAssignedTasksQueryHandler:
    def handle(self, query: GetMyAssignedTasksQuery) -> List[TaskDto]:
        """
        SELECT ca.*
        FROM candidate_applications ca
        JOIN position_stage_assignments psa
            ON psa.position_id = ca.position_id
            AND psa.stage_id = ca.current_stage_id
        WHERE ca.task_status = 'pending'
            AND psa.assigned_user_ids @> jsonb_build_array(query.user_id)
        ORDER BY ca.priority DESC, ca.stage_entered_at ASC
        """
        pass
```

#### GetAvailableTasksQuery

Retorna aplicaciones en etapas que coinciden con los roles del usuario pero sin usuario asignado.

```python
@dataclass
class GetAvailableTasksQuery:
    user_id: str
    filters: Optional[TaskFilters] = None

class GetAvailableTasksQueryHandler:
    def handle(self, query: GetAvailableTasksQuery) -> List[TaskDto]:
        """
        1. Obtener roles del usuario
        2. Buscar etapas cuyo default_roles coincida con algún rol del usuario
        3. Filtrar aplicaciones en esas etapas sin usuario específico asignado
        4. Ordenar por prioridad
        """
        pass
```

---

## Sistema de Emails

### EmailTemplate Entity

```python
@dataclass
class EmailTemplate:
    id: EmailTemplateId
    company_id: CompanyId
    name: str
    subject: str
    body: str  # HTML
    variables: List[str]
    created_at: datetime
    updated_at: datetime

    def render(
        self,
        context: Dict[str, Any],
        custom_text: Optional[str] = None
    ) -> str:
        """Renderizar template con variables"""

        rendered = self.body

        # Reemplazar variables
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))

        # Agregar texto personalizado
        if custom_text:
            custom_placeholder = "{{custom_text}}"
            if custom_placeholder in rendered:
                rendered = rendered.replace(custom_placeholder, custom_text)
            else:
                # Agregar al final si no hay placeholder
                rendered += f"\n\n{custom_text}"

        return rendered
```

### Email Variables

```python
class EmailVariables:
    CANDIDATE_NAME = "candidate_name"
    CANDIDATE_FIRST_NAME = "candidate_first_name"
    POSITION_TITLE = "position_title"
    COMPANY_NAME = "company_name"
    STAGE_NAME = "stage_name"
    CUSTOM_TEXT = "custom_text"

    @classmethod
    def build_context(
        cls,
        candidate: Candidate,
        position: Position,
        company: Company,
        stage: WorkflowStage,
        custom_text: Optional[str] = None
    ) -> Dict[str, Any]:
        return {
            cls.CANDIDATE_NAME: candidate.full_name,
            cls.CANDIDATE_FIRST_NAME: candidate.first_name,
            cls.POSITION_TITLE: position.title,
            cls.COMPANY_NAME: company.name,
            cls.STAGE_NAME: stage.name,
            cls.CUSTOM_TEXT: custom_text or ""
        }
```

### SendStageTransitionEmailHandler

Event handler que envía email cuando cambia la etapa.

```python
class SendStageTransitionEmailHandler:
    def __init__(
        self,
        email_template_repository: EmailTemplateRepository,
        email_service: EmailService,
        workflow_repository: WorkflowRepository
    ):
        self.email_template_repo = email_template_repository
        self.email_service = email_service
        self.workflow_repo = workflow_repository

    def handle(self, event: ApplicationStageChangedEvent) -> None:
        """
        1. Obtener nueva etapa
        2. Verificar si tiene email_template_id
        3. Si tiene, renderizar template
        4. Agregar custom_email_text si existe
        5. Enviar email al candidato
        6. Registrar en historial
        """

        # Obtener etapa
        stage = self.workflow_repo.get_stage_by_id(event.new_stage_id)

        if not stage.email_template_id:
            return  # No hay template configurado

        # Obtener template
        template = self.email_template_repo.get_by_id(stage.email_template_id)

        # Construir contexto
        context = EmailVariables.build_context(
            candidate=event.candidate,
            position=event.position,
            company=event.company,
            stage=stage,
            custom_text=stage.custom_email_text
        )

        # Renderizar
        body = template.render(context, stage.custom_email_text)
        subject = self._render_subject(template.subject, context)

        # Enviar
        self.email_service.send(
            to=event.candidate.email,
            subject=subject,
            body=body
        )

        # TODO: Registrar en historial de aplicación
```

---

## Sistema de Permisos

### Stage Permission Service

```python
class StagePermissionService:
    def __init__(
        self,
        position_assignment_repo: PositionStageAssignmentRepository,
        company_user_repo: CompanyUserRepository
    ):
        self.assignment_repo = position_assignment_repo
        self.user_repo = company_user_repo

    def can_user_process_stage(
        self,
        user_id: str,
        application: CandidateApplication
    ) -> bool:
        """Verificar si usuario puede procesar esta aplicación"""

        # Verificar si es admin de la empresa
        user = self.user_repo.get_by_id(user_id)
        if user.is_admin:
            return True

        # Verificar si está asignado a la etapa actual
        assignment = self.assignment_repo.get_by_position_and_stage(
            position_id=application.position_id,
            stage_id=application.current_stage_id
        )

        if not assignment:
            return False

        return user_id in assignment.assigned_user_ids

    def get_assigned_users_for_stage(
        self,
        position_id: str,
        stage_id: str
    ) -> List[str]:
        """Obtener usuarios asignados a una etapa"""

        assignment = self.assignment_repo.get_by_position_and_stage(
            position_id=position_id,
            stage_id=stage_id
        )

        if not assignment:
            return []

        return assignment.assigned_user_ids
```

### Permission Checks en Commands

```python
class ChangeStageCommandHandler:
    def __init__(
        self,
        application_repo: CandidateApplicationRepository,
        permission_service: StagePermissionService,
        event_bus: EventBus
    ):
        self.application_repo = application_repo
        self.permission_service = permission_service
        self.event_bus = event_bus

    def execute(self, command: ChangeStageCommand) -> None:
        # Obtener aplicación
        application = self.application_repo.get_by_id(command.application_id)

        # Verificar permiso
        if not self.permission_service.can_user_process_stage(
            user_id=command.user_id,
            application=application
        ):
            raise PermissionDeniedError(
                "User not assigned to current stage"
            )

        # Validar transición
        self._validate_transition(application, command.new_stage_id)

        # Mover a nueva etapa
        previous_stage_id = application.current_stage_id
        application.move_to_stage(
            new_stage_id=command.new_stage_id,
            changed_by=command.user_id
        )

        # Guardar
        self.application_repo.save(application)

        # Emitir evento
        event = ApplicationStageChangedEvent(
            application_id=application.id,
            previous_stage_id=previous_stage_id,
            new_stage_id=command.new_stage_id,
            changed_by_user_id=command.user_id,
            changed_at=datetime.now(UTC)
        )
        self.event_bus.publish(event)
```

---

## APIs

### Workflow Management

```
GET    /api/company/{company_id}/workflows
POST   /api/company/{company_id}/workflows
GET    /api/workflows/{workflow_id}
PUT    /api/workflows/{workflow_id}
DELETE /api/workflows/{workflow_id}
POST   /api/workflows/{workflow_id}/activate
POST   /api/workflows/{workflow_id}/deactivate
POST   /api/workflows/{workflow_id}/archive

GET    /api/workflows/{workflow_id}/stages
POST   /api/workflows/{workflow_id}/stages
GET    /api/stages/{stage_id}
PUT    /api/stages/{stage_id}
DELETE /api/stages/{stage_id}
POST   /api/stages/{stage_id}/move-up
POST   /api/stages/{stage_id}/move-down
```

### Custom Fields

```
GET    /api/workflows/{workflow_id}/custom-fields
POST   /api/workflows/{workflow_id}/custom-fields
PUT    /api/custom-fields/{field_id}
DELETE /api/custom-fields/{field_id}

GET    /api/stages/{stage_id}/field-configurations
PUT    /api/stages/{stage_id}/fields/{field_id}/visibility
```

### Position Stage Assignments

```
GET    /api/positions/{position_id}/stage-assignments
POST   /api/positions/{position_id}/stage-assignments      (batch)
PUT    /api/positions/{position_id}/stages/{stage_id}/users
POST   /api/positions/{position_id}/stages/{stage_id}/users/{user_id}
DELETE /api/positions/{position_id}/stages/{stage_id}/users/{user_id}
GET    /api/positions/{position_id}/stages/{stage_id}/can-process
```

### Application Processing

```
GET    /api/company/{company_id}/applications
GET    /api/positions/{position_id}/applications
GET    /api/applications/{application_id}
POST   /api/applications/{application_id}/change-stage
GET    /api/applications/{application_id}/can-change-stage
GET    /api/applications/{application_id}/history

POST   /api/applications/{application_id}/comments
GET    /api/applications/{application_id}/comments

POST   /api/applications/{application_id}/messages
GET    /api/applications/{application_id}/messages
```

### Task Management

```
GET    /api/company-users/{user_id}/tasks/assigned
GET    /api/company-users/{user_id}/tasks/available
GET    /api/company-users/{user_id}/tasks/all
POST   /api/applications/{app_id}/claim
POST   /api/applications/{app_id}/unclaim
PUT    /api/applications/{app_id}/task-status
```

### Email Templates

```
GET    /api/company/{company_id}/email-templates
POST   /api/company/{company_id}/email-templates
GET    /api/email-templates/{template_id}
PUT    /api/email-templates/{template_id}
DELETE /api/email-templates/{template_id}
POST   /api/email-templates/{template_id}/preview
POST   /api/email-templates/{template_id}/test-send
```

### Analytics

```
GET    /api/workflows/{workflow_id}/analytics
GET    /api/workflows/{workflow_id}/bottlenecks
GET    /api/workflows/{workflow_id}/cost-analysis
GET    /api/positions/{position_id}/hiring-metrics
```

---

## Eventos de Dominio

### ApplicationStageChangedEvent

```python
@dataclass
class ApplicationStageChangedEvent(DomainEvent):
    application_id: str
    previous_stage_id: str
    new_stage_id: str
    changed_by_user_id: str
    changed_at: datetime

    # Contexto adicional para event handlers
    candidate: Candidate
    position: Position
    company: Company
```

**Event Handlers:**
- `SendStageTransitionEmailHandler`: Envía email automático si está configurado
- `UpdateApplicationHistoryHandler`: Registra cambio en historial
- `RecalculateDeadlineHandler`: Recalcula deadline de la nueva etapa
- `NotifyAssignedUsersHandler`: Notifica a usuarios de la nueva etapa

### PositionCreatedEvent

```python
@dataclass
class PositionCreatedEvent(DomainEvent):
    position_id: str
    company_id: str
    workflow_id: Optional[str]
    created_by_user_id: str
    created_at: datetime
```

**Event Handlers:**
- `CreateDefaultStageAssignmentsHandler`: Crea asignaciones por defecto basadas en workflow

### CandidateApplicationCreatedEvent

```python
@dataclass
class CandidateApplicationCreatedEvent(DomainEvent):
    application_id: str
    candidate_id: str
    position_id: str
    workflow_id: str
    initial_stage_id: str
    created_at: datetime
```

**Event Handlers:**
- `SendApplicationConfirmationEmailHandler`: Envía email de confirmación al candidato
- `NotifyRecruitersHandler`: Notifica a reclutadores asignados

---

## Implementación Frontend

### Estructura de Componentes

```
client-vite/src/
├── pages/
│   └── company/
│       ├── WorkflowsSettingsPage.tsx       # Lista de workflows
│       ├── CreateWorkflowPage.tsx          # Crear workflow
│       ├── EditWorkflowPage.tsx            # Editar workflow
│       ├── PositionsPage.tsx               # Lista de posiciones
│       ├── CreatePositionPage.tsx          # Crear posición con workflow
│       ├── EditPositionPage.tsx            # Editar posición
│       ├── ApplicationsKanbanPage.tsx      # Tablero kanban
│       ├── ApplicationDetailPage.tsx       # Detalle de aplicación
│       ├── MyTasksPage.tsx                 # Tablero de tareas
│       └── WorkflowAnalyticsPage.tsx       # Analytics
│
├── components/
│   └── company/
│       ├── workflow/
│       │   ├── WorkflowCard.tsx
│       │   ├── WorkflowStageList.tsx
│       │   ├── StageForm.tsx
│       │   ├── CustomFieldEditor.tsx
│       │   └── FieldVisibilityMatrix.tsx
│       ├── position/
│       │   ├── WorkflowSelector.tsx
│       │   ├── StageAssignmentEditor.tsx
│       │   └── UserMultiSelect.tsx
│       ├── application/
│       │   ├── ApplicationCard.tsx
│       │   ├── KanbanColumn.tsx
│       │   ├── StageTransitionButton.tsx
│       │   ├── ApplicationHistory.tsx
│       │   └── CustomFieldsForm.tsx
│       ├── tasks/
│       │   ├── TaskCard.tsx
│       │   ├── TaskFilters.tsx
│       │   ├── PriorityBadge.tsx
│       │   └── DeadlineIndicator.tsx
│       └── email/
│           ├── EmailTemplateEditor.tsx
│           ├── TemplateVariables.tsx
│           └── EmailPreview.tsx
│
└── services/
    ├── workflowService.ts
    ├── stageService.ts
    ├── customFieldService.ts
    ├── positionStageAssignmentService.ts
    ├── applicationService.ts
    ├── taskService.ts
    └── emailTemplateService.ts
```

### Servicios API

#### workflowService.ts

```typescript
export const workflowService = {
    listWorkflows: (companyId: string) =>
        api.get(`/company/${companyId}/workflows`),

    createWorkflow: (companyId: string, data: CreateWorkflowRequest) =>
        api.post(`/company/${companyId}/workflows`, data),

    getWorkflow: (workflowId: string) =>
        api.get(`/workflows/${workflowId}`),

    updateWorkflow: (workflowId: string, data: UpdateWorkflowRequest) =>
        api.put(`/workflows/${workflowId}`, data),

    deleteWorkflow: (workflowId: string) =>
        api.delete(`/workflows/${workflowId}`),

    activateWorkflow: (workflowId: string) =>
        api.post(`/workflows/${workflowId}/activate`),

    deactivateWorkflow: (workflowId: string) =>
        api.post(`/workflows/${workflowId}/deactivate`),
};
```

### Tipos TypeScript

```typescript
// Workflow types
export interface Workflow {
    id: string;
    company_id: string;
    name: string;
    description?: string;
    workflow_type: 'prospecting' | 'selection';
    status: 'active' | 'inactive' | 'archived';
    is_default: boolean;
    stages: WorkflowStage[];
    active_candidates_count: number;
    active_positions_count: number;
    created_at: string;
    updated_at: string;
}

export interface WorkflowStage {
    id: string;
    workflow_id: string;
    name: string;
    description?: string;
    stage_type: 'initial' | 'intermediate' | 'final' | 'custom';
    order: number;
    is_active: boolean;
    required_outcome?: string;
    estimated_duration_days?: number;
    deadline_days?: number;
    estimated_cost?: number;
    default_roles: string[];
    default_assigned_users: string[];
    email_template_id?: string;
    custom_email_text?: string;
    created_at: string;
    updated_at: string;
}

// Custom field types
export interface CustomField {
    id: string;
    workflow_id: string;
    field_key: string;
    field_name: string;
    field_type: FieldType;
    field_config: Record<string, any>;
    order: number;
    created_at: string;
    updated_at: string;
}

export type FieldType =
    | 'text_short'
    | 'text_long'
    | 'dropdown'
    | 'checkbox'
    | 'radio'
    | 'date'
    | 'datetime'
    | 'time'
    | 'file'
    | 'currency'
    | 'integer'
    | 'float'
    | 'percentage';

export type FieldVisibility =
    | 'hidden'
    | 'mandatory'
    | 'recommended'
    | 'optional';

// Application types
export interface CandidateApplication {
    id: string;
    candidate_id: string;
    position_id: string;
    workflow_id: string;
    current_stage_id: string;
    application_data: Record<string, any>;
    shared_data: SharedData;
    stage_entered_at: string;
    stage_deadline?: string;
    task_status: 'pending' | 'in_progress' | 'completed' | 'blocked';
    status: string;
    priority: number;
    created_at: string;
    updated_at: string;
}

export interface SharedData {
    include_education: boolean;
    include_experience: boolean;
    include_projects: boolean;
    include_skills: boolean;
    include_languages: boolean;
    resume_ids: string[];
    portfolio_url?: string;
}

// Task types
export interface Task {
    application: CandidateApplication;
    candidate_name: string;
    candidate_photo?: string;
    position_title: string;
    current_stage_name: string;
    priority_score: number;
    deadline?: string;
    days_in_stage: number;
    assignment_type: 'direct' | 'role_based';
    can_process: boolean;
}

// Assignment types
export interface PositionStageAssignment {
    id: string;
    position_id: string;
    stage_id: string;
    assigned_user_ids: string[];
    created_at: string;
    updated_at: string;
}
```

---

## Migraciones

### Orden de Ejecución

1. `add_workflow_type_to_company_workflows.sql`
2. `add_stage_configuration_fields.sql`
3. `create_workflow_custom_fields.sql`
4. `create_stage_field_configurations.sql`
5. `add_workflow_id_to_positions.sql`
6. `create_position_stage_assignments.sql`
7. `add_workflow_fields_to_candidate_applications.sql`
8. `create_company_talent_pool.sql`
9. `create_email_templates.sql`
10. `add_roles_to_company_users.sql`

---

## Testing Strategy

### Unit Tests

```python
# Test WorkflowStage entity
def test_create_workflow_stage_with_valid_data():
    stage = WorkflowStage.create(
        workflow_id=WorkflowId("wf_123"),
        name="Technical Interview",
        stage_type=StageType.INTERMEDIATE,
        order=2,
        deadline_days=5,
        estimated_cost=Decimal("100.00")
    )

    assert stage.name == "Technical Interview"
    assert stage.deadline_days == 5
    assert stage.estimated_cost == Decimal("100.00")

def test_create_stage_with_negative_deadline_fails():
    with pytest.raises(ValueError):
        WorkflowStage.create(
            workflow_id=WorkflowId("wf_123"),
            name="Test",
            stage_type=StageType.INTERMEDIATE,
            order=1,
            deadline_days=-1
        )
```

### Integration Tests

```python
def test_create_position_with_workflow_creates_assignments():
    # Arrange
    workflow = create_test_workflow_with_stages()

    # Act
    position = create_position(workflow_id=workflow.id)

    # Assert
    assignments = position_assignment_repo.list_by_position(position.id)
    assert len(assignments) == len(workflow.stages)

def test_change_stage_without_permission_fails():
    # Arrange
    application = create_test_application()
    unauthorized_user = create_test_user()

    # Act & Assert
    with pytest.raises(PermissionDeniedError):
        change_stage_command_handler.execute(
            ChangeStageCommand(
                application_id=application.id,
                new_stage_id="next_stage",
                user_id=unauthorized_user.id
            )
        )
```

### E2E Tests

```typescript
describe('Complete Hiring Workflow', () => {
    it('should process candidate through all stages', async () => {
        // 1. Create workflow
        const workflow = await createWorkflow({
            name: 'Test Hiring',
            stages: [
                { name: 'Screening', order: 0 },
                { name: 'Interview', order: 1 },
                { name: 'Hired', order: 2 }
            ]
        });

        // 2. Create position with workflow
        const position = await createPosition({
            title: 'Developer',
            workflow_id: workflow.id
        });

        // 3. Assign users to stages
        await assignUsersToStages(position.id, [
            { stage_id: workflow.stages[0].id, user_ids: [recruiter.id] },
            { stage_id: workflow.stages[1].id, user_ids: [manager.id] }
        ]);

        // 4. Candidate applies
        const application = await candidateApplies(position.id);

        // 5. Recruiter moves to interview
        await loginAs(recruiter);
        await moveToNextStage(application.id);

        // 6. Manager moves to hired
        await loginAs(manager);
        await moveToNextStage(application.id);

        // 7. Verify final state
        const finalApp = await getApplication(application.id);
        expect(finalApp.current_stage_id).toBe(workflow.stages[2].id);
    });
});
```

---

## Performance Considerations

### Database Indexes

```sql
-- Para búsquedas frecuentes
CREATE INDEX idx_applications_stage_deadline ON candidate_applications(stage_deadline)
    WHERE task_status = 'pending';

CREATE INDEX idx_applications_workflow_stage ON candidate_applications(workflow_id, current_stage_id);

CREATE INDEX idx_stage_assignments_lookup ON position_stage_assignments(position_id, stage_id);

-- Para queries de tareas
CREATE INDEX idx_applications_task_priority ON candidate_applications(
    (application_data->>'priority_score')::int DESC,
    stage_entered_at ASC
) WHERE task_status = 'pending';
```

### Caching Strategy

```python
# Cache workflow + stages por 1 hora (cambia poco)
@cache(ttl=3600)
def get_workflow_with_stages(workflow_id: str) -> WorkflowWithStagesDto:
    pass

# Cache permisos de usuario por 5 minutos
@cache(ttl=300)
def get_user_stage_permissions(user_id: str, stage_id: str) -> bool:
    pass

# Cache roles de usuario por 10 minutos
@cache(ttl=600)
def get_user_roles(user_id: str) -> List[str]:
    pass
```

### Query Optimization

```python
# Eager loading para evitar N+1 queries
def list_tasks_for_user(user_id: str) -> List[TaskDto]:
    return (
        session.query(CandidateApplication)
        .options(
            joinedload(CandidateApplication.candidate),
            joinedload(CandidateApplication.position),
            joinedload(CandidateApplication.current_stage)
        )
        .join(PositionStageAssignment)
        .filter(...)
        .all()
    )
```

---

## Security Considerations

### Authorization

```python
# Siempre verificar permisos antes de operaciones sensibles
class ChangeStageController:
    @require_auth
    def change_stage(self, application_id: str, request: ChangeStageRequest):
        # Verificar que el usuario pertenece a la misma empresa
        application = self.app_repo.get_by_id(application_id)
        if application.company_id != current_user.company_id:
            raise ForbiddenError()

        # Verificar permiso específico de etapa
        if not self.permission_service.can_user_process_stage(
            user_id=current_user.id,
            application=application
        ):
            raise ForbiddenError("Not assigned to current stage")

        # Proceder con el comando
        self.command_bus.execute(...)
```

### Data Privacy

```python
# Solo compartir datos autorizados por el candidato
class ApplicationDto:
    @staticmethod
    def from_entity(
        application: CandidateApplication,
        include_candidate_data: bool = False
    ) -> "ApplicationDto":
        dto = ApplicationDto(
            id=application.id.value,
            position_id=application.position_id.value,
            status=application.status,
            # ...
        )

        if include_candidate_data:
            # Filtrar según shared_data
            dto.candidate_data = filter_shared_data(
                candidate=application.candidate,
                shared_data=application.shared_data
            )

        return dto

def filter_shared_data(candidate: Candidate, shared_data: SharedData) -> Dict:
    result = {}

    if shared_data.include_education:
        result['education'] = candidate.education

    if shared_data.include_experience:
        result['experience'] = candidate.experience

    # ... más campos según autorización

    return result
```

---

## Deployment Checklist

### Backend

- [ ] Ejecutar todas las migraciones en orden
- [ ] Verificar índices creados
- [ ] Seed templates de email por defecto
- [ ] Seed workflows de ejemplo
- [ ] Configurar servicio de email (SMTP)
- [ ] Verificar event bus configurado
- [ ] Verificar dependency injection container actualizado
- [ ] Ejecutar tests de integración
- [ ] Verificar logs de errores

### Frontend

- [ ] Build de producción
- [ ] Verificar variables de entorno
- [ ] Verificar rutas configuradas
- [ ] Verificar permisos de acceso por role
- [ ] Testing E2E
- [ ] Verificar responsive design

---

## Conclusión

Este diseño técnico implementa un sistema completo de flujos de trabajo flexible y escalable que:

1. Permite personalización total de procesos de selección
2. Maneja permisos granulares por usuario y etapa
3. Soporta campos personalizados con validaciones dinámicas
4. Automatiza comunicación con candidatos
5. Prioriza tareas inteligentemente
6. Proporciona métricas y analytics
7. Mantiene clean architecture y CQRS
8. Escala horizontalmente

La implementación por fases permite entregar valor incrementalmente mientras se mantiene la calidad del código y la arquitectura.
