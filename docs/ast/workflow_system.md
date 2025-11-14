# Sistema Unificado de Workflow
**CareerPython ATS - Documento de Negocio**  
*Fecha:* 2025-11-10 | *Versión:* 1.0

---

## Visión General

El **Sistema Unificado de Workflow** es el motor central que gestiona todos los procesos de negocio en CareerPython ATS. Es un sistema genérico y flexible que permite a las empresas definir, personalizar y ejecutar workflows para diferentes tipos de entidades (candidatos, posiciones de trabajo, onboarding, etc.).

### Filosofía del Sistema

- **Unificación**: Un solo motor gestiona todos los tipos de workflows
- **Flexibilidad**: Totalmente personalizable por empresa
- **Automatización**: Transiciones automáticas entre fases y stages
- **Validación**: Reglas de negocio que garantizan la integridad del proceso
- **Escalabilidad**: Soporta desde startups hasta empresas multinacionales

---

## Conceptos Fundamentales

### 1. Workflow (Flujo de Trabajo)

Un **Workflow** es una plantilla que define una secuencia de etapas (stages) por las que pasa una entidad durante un proceso de negocio.

**Ejemplos de Workflows:**
- **"Sourcing Workflow"**: Pending → Screening → Qualified → Not Suitable → On Hold
- **"Evaluation Workflow"**: HR Interview → Manager Interview → Assessment → Executive Interview → Selected → Rejected
- **"Job Positions Workflow"**: Draft → Under Review → Approved → Published → Closed → Cancelled

#### Propiedades de un Workflow

| Propiedad | Descripción | Ejemplo |
|-----------|-------------|---------|
| `id` | Identificador único | `01K9QDANEQFCK9AZ7VS26MPTFJ` |
| `company_id` | Empresa propietaria | `01K9QC95C7NJ1SW2Y1APNH1KZ7` |
| `workflow_type` | Tipo de workflow | `CANDIDATE_APPLICATION`, `JOB_POSITION_OPENING`, `CANDIDATE_ONBOARDING` |
| `name` | Nombre del workflow | "Sourcing Workflow" |
| `description` | Descripción del propósito | "Screening and filtering candidates" |
| `display` | Vista por defecto | `KANBAN` o `LIST` |
| `phase_id` | Fase a la que pertenece | `2c33c6c9-1403-4d30-a087-13bf3d18c386` |
| `status` | Estado del workflow | `DRAFT`, `ACTIVE`, `ARCHIVED` |
| `is_default` | Es el workflow por defecto | `true` o `false` |

---

### 2. Tipos de Workflow

El sistema soporta tres tipos principales de workflows mediante el enum `WorkflowTypeEnum`:

#### 2.1. CANDIDATE_APPLICATION (CA)
**Propósito**: Gestionar el proceso de selección de candidatos desde la aplicación hasta la contratación.

**Características**:
- Organizado en **fases** (Sourcing, Evaluation, Offer & Pre-Onboarding)
- Transiciones automáticas entre fases cuando se alcanza un stage `SUCCESS`
- Múltiples workflows por fase (uno por defecto)
- Vista Kanban o List según la fase

**Ejemplo de uso**:
```
Candidato aplica → Fase 1: Sourcing → Stage: Pending
                    ↓
                  Screening
                    ↓
                  Qualified (SUCCESS) → Transición automática a Fase 2
                    ↓
                  Fase 2: Evaluation → Stage: HR Interview
                    ↓
                  ... (continúa el proceso)
```

#### 2.2. JOB_POSITION_OPENING (PO)
**Propósito**: Gestionar el ciclo de vida completo de una posición de trabajo desde el borrador hasta su publicación y cierre.

**Características**:
- Generalmente una sola fase
- Workflow único por empresa (o múltiples si se configuran)
- Vista Kanban por defecto
- Stages específicos: Draft, Under Review, Approved, Published, Closed, Cancelled

**Ejemplo de uso**:
```
Posición creada → Stage: Draft
                   ↓
                 Under Review
                   ↓
                 Approved
                   ↓
                 Published (SUCCESS) → Posición visible públicamente
                   ↓
                 Closed (ARCHIVED) → Posición cerrada
```

#### 2.3. CANDIDATE_ONBOARDING (CO)
**Propósito**: Gestionar el proceso de incorporación de candidatos contratados.

**Características**:
- Workflow específico para onboarding
- Stages de documentación, verificación, y bienvenida
- Integración con procesos post-contratación

---

### 3. Phase (Fase)

Una **Phase** es un contenedor lógico que agrupa workflows relacionados y representa una etapa macro del proceso de selección.

**Características**:
- Cada fase tiene un `workflow_type` (solo workflows del mismo tipo pueden pertenecer a una fase)
- Tiene un `sort_order` para definir el orden de ejecución
- Tiene una `default_view` (KANBAN o LIST)
- Tiene un `objective` (texto descriptivo para IA)

**Ejemplo de Fases para CANDIDATE_APPLICATION**:

| Fase | Objetivo | Vista | Orden |
|------|----------|-------|-------|
| **Sourcing** | Screening and descarte process - identify qualified candidates | KANBAN | 0 |
| **Evaluation** | Interview and assessment process | KANBAN | 1 |
| **Offer & Pre-Onboarding** | Offer negotiation and document verification | LIST | 2 |

**Relación Phase → Workflow**:
- Una fase puede tener múltiples workflows
- Uno de ellos puede ser marcado como `is_default`
- Cuando se crea una nueva entidad (candidato, posición), se asigna automáticamente al workflow por defecto de la fase correspondiente

---

### 4. WorkflowStage (Etapa del Workflow)

Un **WorkflowStage** es una etapa individual dentro de un workflow. Representa un estado específico en el proceso.

#### 4.1. Tipos de Stages

El sistema define los siguientes tipos mediante `WorkflowStageTypeEnum`:

| Tipo | Descripción | Uso Típico | Validación |
|------|-------------|------------|------------|
| **INITIAL** | Etapa inicial del workflow | Punto de entrada | Solo uno por workflow |
| **PROGRESS** | Etapa intermedia | Procesos en curso | Múltiples permitidos |
| **SUCCESS** | Etapa de éxito/completado | Finalización exitosa | Solo uno por workflow |
| **FAIL** | Etapa de fallo/rechazo | Rechazos, descartes | Múltiples permitidos |
| **HOLD** | Etapa en espera | Pausas temporales | Múltiples permitidos |
| **ARCHIVED** | Etapa archivada | Cierres, finalizaciones | Múltiples permitidos |

#### 4.2. Reglas de Validación de Stages

El sistema implementa las siguientes **reglas de negocio** que se validan tanto en backend como en frontend:

##### Regla 1: Solo un INITIAL por Workflow
- **Razón**: Cada workflow debe tener un único punto de entrada claro
- **Validación**: Al crear o actualizar un stage, si el tipo es `INITIAL` y ya existe otro `INITIAL`, se rechaza la operación
- **Mensaje de error**: `"Only one INITIAL stage is allowed per workflow"`

##### Regla 2: Solo un SUCCESS por Workflow
- **Razón**: Cada workflow debe tener un único punto de finalización exitosa
- **Validación**: Al crear o actualizar un stage, si el tipo es `SUCCESS` y ya existe otro `SUCCESS`, se rechaza la operación
- **Mensaje de error**: `"Only one SUCCESS stage is allowed per workflow"`

##### Regla 3: Siempre debe existir un SUCCESS
- **Razón**: Un workflow sin punto de éxito no tiene sentido en el contexto de selección
- **Validación**: Al guardar un workflow, debe tener al menos un stage de tipo `SUCCESS`
- **Mensaje de error**: `"A workflow must have at least one SUCCESS stage"`

##### Regla 4: Si hay PROGRESS, debe haber INITIAL
- **Razón**: Si hay etapas intermedias, debe haber un punto de entrada
- **Validación**: Si un workflow tiene stages de tipo `PROGRESS` pero no tiene `INITIAL`, se rechaza
- **Mensaje de error**: `"If a workflow has PROGRESS stages, it must have an INITIAL stage"`

#### 4.3. Propiedades de un WorkflowStage

| Propiedad | Descripción | Ejemplo |
|-----------|-------------|---------|
| `id` | Identificador único | `01K9QC95F07EZV00GR8X79KSZ1` |
| `workflow_id` | Workflow al que pertenece | `01K9QC95EYF2CD77VGJFD98TT8` |
| `name` | Nombre del stage | "HR Interview" |
| `description` | Descripción de la etapa | "Human Resources interview" |
| `stage_type` | Tipo de stage | `INITIAL`, `PROGRESS`, `SUCCESS`, `FAIL`, `HOLD`, `ARCHIVED` |
| `order` | Orden en el workflow | `0`, `1`, `2`, ... |
| `allow_skip` | ¿Se puede saltar esta etapa? | `true` o `false` |
| `estimated_duration_days` | Días estimados en esta etapa | `5` |
| `is_active` | ¿Está activa? | `true` o `false` |
| `kanban_display` | Cómo se muestra en Kanban | `COLUMN`, `ROW`, `NONE` |
| `next_phase_id` | Fase siguiente (solo SUCCESS/FAIL) | `2c33c6c9-1403-4d30-a087-13bf3d18c386` |
| `style` | Estilo visual (icono, colores) | `{icon: "👥", text_color: "#92400e", background_color: "#fef3c7"}` |
| `validation_rules` | Reglas JsonLogic obligatorias | `{...}` |
| `recommended_rules` | Reglas JsonLogic recomendadas | `{...}` |
| `default_role_ids` | Roles asignados por defecto | `["HR_MANAGER", "RECRUITER"]` |
| `default_assigned_users` | Usuarios asignados por defecto | `["01K9QC95C7NJ1SW2Y1APNH1KZ7"]` |
| `email_template_id` | Template de email al entrar | `"welcome_email_template"` |
| `custom_email_text` | Texto adicional para email | `"Welcome to our process!"` |
| `deadline_days` | Días límite para completar | `7` |
| `estimated_cost` | Coste estimado | `100.00` |

---

### 5. Transiciones Automáticas entre Fases

Cuando un candidato alcanza un stage de tipo `SUCCESS` que tiene configurado un `next_phase_id`, el sistema **automáticamente**:

1. **Transiciona al candidato a la fase siguiente**
2. **Asigna el workflow por defecto de la nueva fase**
3. **Coloca al candidato en el stage `INITIAL` del nuevo workflow**

**Ejemplo**:
```
Fase 1: Sourcing
  Workflow: Sourcing Workflow
    Stage: Qualified (SUCCESS, next_phase_id = "Fase 2")
      ↓ [Transición automática]
Fase 2: Evaluation
  Workflow: Evaluation Workflow (por defecto)
    Stage: HR Interview (INITIAL)
```

**Comportamiento en Kanban**:
- En el tablero Kanban de la Fase 1, la columna `SUCCESS` muestra:
  - Candidatos que están en el stage `SUCCESS` de la Fase 1
  - **Y también** candidatos que están en el stage `INITIAL` de la Fase 2 (si el `SUCCESS` tiene `next_phase_id`)
- Estos candidatos de la Fase 2 son **arrastrables** dentro del tablero de la Fase 1
- Si se mueven a otro stage de la Fase 1, el sistema actualiza automáticamente el `phase_id` del candidato

---

### 6. Configuración de Visualización (Kanban Display)

Cada stage puede configurarse para mostrarse de diferentes formas en el tablero Kanban:

| Valor | Descripción | Uso Típico |
|-------|-------------|------------|
| **COLUMN** | Columna vertical en Kanban | Stages principales del proceso |
| **ROW** | Fila horizontal en Kanban | Stages secundarios (Not Suitable, On Hold, Cancelled) |
| **NONE** | Oculto en Kanban | Stages que no se muestran visualmente |

**Ejemplo de configuración**:
```
Sourcing Workflow:
  - Pending (INITIAL, COLUMN) → Columna principal
  - Screening (PROGRESS, COLUMN) → Columna principal
  - Qualified (SUCCESS, COLUMN) → Columna principal
  - Not Suitable (FAIL, ROW) → Fila horizontal
  - On Hold (PROGRESS, ROW) → Fila horizontal
```

---

### 7. Reglas de Validación y Recomendación (JsonLogic)

Cada stage puede tener reglas de validación y recomendación definidas en **JsonLogic**, un formato estándar para expresar lógica de negocio.

#### 7.1. Validation Rules (Reglas Obligatorias)
- **Propósito**: Impedir el avance si no se cumplen ciertas condiciones
- **Ejemplo**: "No se puede pasar a 'Selected' si el score técnico es menor a 70"
- **Comportamiento**: Si la validación falla, el sistema **bloquea** el cambio de stage

#### 7.2. Recommended Rules (Reglas Recomendadas)
- **Propósito**: Sugerir acciones pero permitir el avance
- **Ejemplo**: "Se recomienda tener al menos 2 entrevistas antes de 'Selected'"
- **Comportamiento**: Si la recomendación no se cumple, el sistema **muestra una advertencia** pero permite continuar

---

### 8. Sistema de Roles y Asignaciones

#### 8.1. Default Role IDs
Cada stage puede tener roles asignados por defecto. Cuando un candidato entra en un stage:
- Los usuarios con esos roles reciben notificaciones
- Se les asigna automáticamente la tarea relacionada

**Ejemplo**:
```
Stage: "Technical Assessment"
  default_role_ids: ["TECH_LEAD", "SENIOR_DEVELOPER"]
  → Al entrar un candidato, los Tech Leads y Senior Developers son notificados
```

#### 8.2. Default Assigned Users
Además de roles, se pueden asignar usuarios específicos:
- Útil para casos especiales o asignaciones puntuales
- Tiene prioridad sobre los roles (si ambos están configurados)

---

### 9. Flujo Completo del Sistema

#### 9.1. Inicialización de una Empresa

Cuando se crea una nueva empresa, el sistema **automáticamente** crea:

1. **Fases por defecto** (para `CANDIDATE_APPLICATION`):
   - Fase 1: Sourcing (Kanban)
   - Fase 2: Evaluation (Kanban)
   - Fase 3: Offer & Pre-Onboarding (List)

2. **Workflows por defecto** (uno por fase):
   - Sourcing Workflow (Fase 1)
   - Evaluation Workflow (Fase 2)
   - Offer and Pre-Onboarding Workflow (Fase 3)

3. **Stages por defecto** (según el tipo de empresa):
   - Startup: Configuración simplificada
   - Mid-Size: Configuración estándar
   - Enterprise: Configuración con etapas adicionales
   - Agency: Configuración orientada a clientes

4. **Workflow de Job Positions** (para `JOB_POSITION_OPENING`):
   - Una sola fase: "Job Positions"
   - Workflow: "Job Positions Workflow"
   - Stages: Draft → Under Review → Approved → Published → Closed → Cancelled

#### 9.2. Personalización por Empresa

Las empresas pueden:
- **Crear nuevas fases** con sus propios workflows
- **Modificar workflows existentes** (agregar/eliminar stages)
- **Crear workflows adicionales** para la misma fase
- **Configurar reglas de validación** por stage
- **Personalizar estilos visuales** (iconos, colores)
- **Definir transiciones entre fases** (configurando `next_phase_id`)

#### 9.3. Uso del Sistema

**Para Candidatos**:
1. Candidato aplica → Se crea `CompanyCandidate` → Se asigna al workflow por defecto de la Fase 1
2. Candidato entra en stage `INITIAL` → Se notifican roles asignados
3. Usuario mueve candidato a siguiente stage → Se ejecutan validaciones
4. Candidato alcanza stage `SUCCESS` con `next_phase_id` → Transición automática a Fase 2
5. Proceso continúa hasta completar todas las fases

**Para Posiciones de Trabajo**:
1. Usuario crea posición → Se asigna al workflow de Job Positions
2. Posición entra en stage `Draft` (INITIAL)
3. Usuario mueve posición a `Under Review` → `Approved` → `Published` (SUCCESS)
4. Posición visible públicamente
5. Usuario mueve a `Closed` (ARCHIVED) cuando se cierra la posición

---

## Ejemplos de Configuración

### Ejemplo 1: Workflow de Sourcing (CANDIDATE_APPLICATION)

```yaml
Workflow:
  name: "Sourcing Workflow"
  workflow_type: CANDIDATE_APPLICATION
  phase_id: "Fase 1: Sourcing"
  display: KANBAN
  status: ACTIVE
  is_default: true

Stages:
  - name: "Pending"
    stage_type: INITIAL
    order: 0
    kanban_display: COLUMN
    style: {icon: "📋", text_color: "#92400e", background_color: "#fef3c7"}
    
  - name: "Screening"
    stage_type: PROGRESS
    order: 1
    kanban_display: COLUMN
    default_role_ids: ["RECRUITER"]
    estimated_duration_days: 3
    style: {icon: "🔍", text_color: "#1e40af", background_color: "#dbeafe"}
    
  - name: "Qualified"
    stage_type: SUCCESS
    order: 2
    kanban_display: COLUMN
    next_phase_id: "Fase 2: Evaluation"  # ← Transición automática
    style: {icon: "✅", text_color: "#065f46", background_color: "#d1fae5"}
    
  - name: "Not Suitable"
    stage_type: FAIL
    order: 3
    kanban_display: ROW  # ← Fila horizontal
    style: {icon: "❌", text_color: "#991b1b", background_color: "#fee2e2"}
    
  - name: "On Hold"
    stage_type: PROGRESS
    order: 4
    kanban_display: ROW  # ← Fila horizontal
    style: {icon: "⏸️", text_color: "#92400e", background_color: "#fef3c7"}
```

### Ejemplo 2: Workflow de Job Positions (JOB_POSITION_OPENING)

```yaml
Workflow:
  name: "Job Positions Workflow"
  workflow_type: JOB_POSITION_OPENING
  phase_id: "Job Positions"
  display: KANBAN
  status: ACTIVE
  is_default: true

Stages:
  - name: "Draft"
    stage_type: INITIAL
    order: 0
    kanban_display: COLUMN
    style: {icon: "📝", text_color: "#92400e", background_color: "#fef3c7"}
    
  - name: "Under Review"
    stage_type: PROGRESS
    order: 1
    kanban_display: COLUMN
    default_role_ids: ["HR_MANAGER"]
    style: {icon: "🔍", text_color: "#1e40af", background_color: "#dbeafe"}
    
  - name: "Approved"
    stage_type: PROGRESS
    order: 2
    kanban_display: COLUMN
    style: {icon: "✅", text_color: "#065f46", background_color: "#d1fae5"}
    
  - name: "Published"
    stage_type: SUCCESS  # ← Único SUCCESS
    order: 3
    kanban_display: COLUMN
    style: {icon: "🌐", text_color: "#065f46", background_color: "#d1fae5"}
    
  - name: "Closed"
    stage_type: ARCHIVED  # ← ARCHIVED (no SUCCESS)
    order: 4
    kanban_display: COLUMN
    style: {icon: "🔒", text_color: "#6b7280", background_color: "#f3f4f6"}
    
  - name: "Cancelled"
    stage_type: FAIL
    order: 5
    kanban_display: ROW
    style: {icon: "❌", text_color: "#991b1b", background_color: "#fee2e2"}
```

---

## Validaciones del Sistema

### Validaciones en Backend

Las validaciones se implementan en:
- `CreateStageCommandHandler`: Valida al crear un nuevo stage
- `UpdateStageCommandHandler`: Valida al actualizar un stage existente

**Errores lanzados**:
- `ValueError`: Si se viola alguna regla de validación

### Validaciones en Frontend

Las validaciones se implementan en:
- `CreateWorkflowPage`: Valida antes de crear workflow y stages
- `EditWorkflowPage`: Valida antes de actualizar workflow y stages

**Mensajes de error mostrados**:
- `"Only one INITIAL stage is allowed per workflow. Found X INITIAL stages: [nombres]"`
- `"Only one SUCCESS stage is allowed per workflow. Found X SUCCESS stages: [nombres]"`
- `"A workflow must have at least one SUCCESS stage"`
- `"If a workflow has PROGRESS stages, it must have an INITIAL stage"`

---

## Diferenciación por Tipo de Empresa

El sistema se adapta según el tipo de empresa durante la inicialización:

| Tipo | Características |
|------|----------------|
| **Startup/Small** | Workflows simplificados, menos stages, procesos rápidos |
| **Mid-Size** | Configuración estándar, workflows balanceados |
| **Enterprise** | Workflows complejos, stages adicionales (compliance, aprobaciones) |
| **Agency** | Workflows orientados a clientes, stages de matching |

---

## Integración con Otros Sistemas

### Sistema de Comentarios
- Cada stage puede tener comentarios asociados
- Los comentarios pueden ser visibles o internos según configuración

### Sistema de Revisión (Reviews)
- Stages pueden tener reviews con scores (0-10)
- Reviews visibles para usuarios con permisos

### Sistema de Actividades (Activity Log)
- Cada cambio de stage se registra en el historial
- Incluye: usuario, fecha, stage anterior, stage nuevo, comentario

### Sistema de Notificaciones
- Notificaciones automáticas al entrar en un stage
- Emails configurados por stage (`email_template_id`)

---

## Mejores Prácticas

### 1. Nomenclatura
- Usar nombres descriptivos y claros para workflows y stages
- Evitar nombres genéricos como "Stage 1", "Stage 2"

### 2. Orden de Stages
- Mantener un orden lógico que refleje el flujo real del proceso
- Usar `order` para organizar visualmente en Kanban

### 3. Transiciones entre Fases
- Configurar `next_phase_id` solo en stages `SUCCESS` o `FAIL`
- Asegurar que la fase siguiente tenga un workflow por defecto

### 4. Validaciones
- Usar `validation_rules` para garantizar calidad del proceso
- Usar `recommended_rules` para guiar sin bloquear

### 5. Roles y Asignaciones
- Asignar roles apropiados a cada stage
- Evitar asignar demasiados roles (ruido en notificaciones)

---

## Conclusión

El **Sistema Unificado de Workflow** es el corazón de CareerPython ATS, proporcionando:

- ✅ **Flexibilidad total** para adaptarse a cualquier proceso de selección
- ✅ **Automatización inteligente** con transiciones entre fases
- ✅ **Validaciones robustas** que garantizan la integridad del proceso
- ✅ **Escalabilidad** desde startups hasta empresas multinacionales
- ✅ **Personalización completa** por empresa y tipo de negocio

El sistema está diseñado para crecer con las necesidades de cada empresa, permitiendo desde configuraciones simples hasta procesos complejos con múltiples fases, workflows y reglas de validación.

---

**Última actualización**: 2025-11-10  
**Versión del documento**: 1.0  
**Autor**: CareerPython Development Team

