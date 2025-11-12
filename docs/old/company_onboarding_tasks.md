# Company Onboarding Implementation Tasks

**Basado en**: `docs/company_onboarding.md`  
**Análisis**: `docs/company_onboarding_analysis.md`  
**Fecha**: 2025-01-09

---

## Resumen

Implementar el sistema de onboarding perfecto con diferenciación por tipo de empresa, siguiendo el documento `company_onboarding.md`. Las tareas están organizadas en fases, dejando la integración de IA para el final.

---

## Fase 1: Company Type System (Fundación)

**Prioridad**: 🔴 **ALTA** - Requerido para todas las demás fases  
**Estimación**: 2-3 días

### Tarea 1.1: Crear Enum CompanyTypeEnum

**Archivo**: `src/company/domain/enums/company_type_enum.py`

**Contenido**:
```python
class CompanyTypeEnum(str, Enum):
    STARTUP_SMALL = "startup_small"
    MID_SIZE = "mid_size"
    ENTERPRISE = "enterprise"
    RECRUITMENT_AGENCY = "recruitment_agency"
```

**Criterios de aceptación**:
- ✅ Enum creado con 4 valores
- ✅ Hereda de `str, Enum`
- ✅ Documentación de cada tipo

---

### Tarea 1.2: Agregar campo company_type a entidad Company

**Archivo**: `src/company/domain/entities/company.py`

**Cambios**:
- Agregar campo `company_type: Optional[CompanyTypeEnum]` al dataclass
- Default: `CompanyTypeEnum.MID_SIZE` en método `create()`
- Actualizar método `update()` si es necesario

**Criterios de aceptación**:
- ✅ Campo agregado a la entidad
- ✅ Default correcto en factory method
- ✅ Validación si es necesario

---

### Tarea 1.3: Agregar columna company_type a CompanyModel

**Archivo**: `src/company/infrastructure/models/company_model.py`

**Cambios**:
- Agregar columna `company_type` con tipo `Enum(CompanyTypeEnum)`
- Default: `CompanyTypeEnum.MID_SIZE.value`
- Nullable: `False`

**Criterios de aceptación**:
- ✅ Columna agregada al modelo
- ✅ Tipo correcto (Enum)
- ✅ Default correcto

---

### Tarea 1.4: Crear migración de base de datos

**Comando**: `make revision m="add company_type to companies"`

**Archivo**: `alembic/versions/XXX_add_company_type_to_companies.py`

**Cambios**:
- Agregar columna `company_type` a tabla `companies`
- Default: `'mid_size'`
- Actualizar registros existentes a `'mid_size'`

**Criterios de aceptación**:
- ✅ Migración creada
- ✅ Default aplicado
- ✅ Datos existentes actualizados
- ✅ Migración ejecutada sin errores

---

### Tarea 1.5: Actualizar CreateCompanyCommand

**Archivo**: `src/company/application/commands/create_company_command.py`

**Cambios**:
- Agregar parámetro `company_type: Optional[CompanyTypeEnum] = None` al command
- Si es `None`, usar `CompanyTypeEnum.MID_SIZE` como default
- Pasar `company_type` al factory method `Company.create()`

**Criterios de aceptación**:
- ✅ Parámetro agregado al command
- ✅ Default correcto
- ✅ Se pasa correctamente a la entidad

---

### Tarea 1.6: Actualizar RegisterCompanyWithUserCommand

**Archivo**: `src/company/application/commands/register_company_with_user_command.py`

**Cambios**:
- Agregar parámetro `company_type: Optional[CompanyTypeEnum] = None` al command
- Pasar `company_type` a `CreateCompanyCommand`

**Criterios de aceptación**:
- ✅ Parámetro agregado
- ✅ Se pasa correctamente al CreateCompanyCommand

---

### Tarea 1.7: Actualizar LinkUserToCompanyCommand

**Archivo**: `src/company/application/commands/link_user_to_company_command.py`

**Cambios**:
- Agregar parámetro `company_type: Optional[CompanyTypeEnum] = None` al command
- Pasar `company_type` a `CreateCompanyCommand`

**Criterios de aceptación**:
- ✅ Parámetro agregado
- ✅ Se pasa correctamente al CreateCompanyCommand

---

### Tarea 1.8: Actualizar tipos TypeScript (Frontend)

**Archivo**: `client-vite/src/types/company.ts`

**Cambios**:
- Agregar tipo `CompanyType`:
  ```typescript
  export type CompanyType = 
    | 'startup_small'
    | 'mid_size'
    | 'enterprise'
    | 'recruitment_agency';
  ```
- Agregar campo `company_type?: CompanyType` a interface `Company`
- Crear constante `COMPANY_TYPE_OPTIONS` para el formulario

**Criterios de aceptación**:
- ✅ Tipo creado
- ✅ Campo agregado a interface
- ✅ Opciones para formulario creadas

---

### Tarea 1.9: Agregar wizard de selección en frontend

**Archivo**: `client-vite/src/components/registration/CompanyDataForm.tsx`

**Cambios**:
- Agregar pregunta: "What best describes your company?"
- Mostrar 4 opciones con descripciones:
  - Startup / Small Business (1–50 employees, fast hiring, multi-role users)
  - Mid-Size Company (51–500 employees, structured but flexible)
  - Enterprise / Large Corporation (501+ employees, compliance-heavy, complex approvals)
  - Recruitment Agency (Any size, high-volume, client-focused)
- Default: Mid-Size Company
- Agregar campo al formulario y al request

**Criterios de aceptación**:
- ✅ Pregunta agregada al formulario
- ✅ 4 opciones con descripciones
- ✅ Default correcto
- ✅ Valor se envía en el request

---

### Tarea 1.10: Actualizar schemas de presentación

**Archivos**:
- `src/company/presentation/schemas/create_company_request.py`
- `src/company/presentation/schemas/update_company_request.py`
- `src/company/presentation/schemas/company_response.py`

**Cambios**:
- Agregar campo `company_type: Optional[CompanyTypeEnum]` a los schemas
- Validación si es necesario

**Criterios de aceptación**:
- ✅ Campo agregado a todos los schemas
- ✅ Validación correcta

---

## Fase 2: Diferenciación de Roles

**Prioridad**: 🟡 **MEDIA**  
**Estimación**: 1-2 días

### Tarea 2.1: Modificar InitializeOnboardingCommand para aceptar company_type

**Archivo**: `src/company/application/commands/initialize_onboarding_command.py`

**Cambios**:
- Agregar parámetro `company_type: Optional[CompanyTypeEnum] = None` al command
- Si es `None`, obtener de `CompanyRepository` usando `company_id`
- Pasar `company_type` a `_create_default_roles()`

**Criterios de aceptación**:
- ✅ Parámetro agregado
- ✅ Se obtiene de la empresa si no se proporciona
- ✅ Se pasa a método de creación de roles

---

### Tarea 2.2: Implementar lógica de roles por tipo

**Archivo**: `src/company/application/commands/initialize_onboarding_command.py`

**Cambios en `_create_default_roles()`**:

**Roles base (todos los tipos)**:
- HR Manager
- Recruiter
- Tech Lead
- Hiring Manager
- Interviewer
- Department Head
- CTO

**Startup/Small**:
- ❌ NO crear "HR Manager" y "Recruiter" por separado
- ✅ Crear "HR Generalist" (combinación de ambos)
- ✅ Agregar "Founder"

**Mid-Size**:
- ✅ Todos los roles base
- ✅ Agregar "Talent Acquisition Specialist"

**Enterprise**:
- ✅ Todos los roles base
- ✅ Agregar "Diversity & Inclusion Officer"
- ✅ Agregar "Legal Reviewer"

**Recruitment Agency**:
- ✅ Todos los roles base
- ✅ Agregar "Client Manager"
- ✅ Agregar "Sourcer"

**Criterios de aceptación**:
- ✅ Lógica condicional implementada
- ✅ Roles correctos según tipo
- ✅ Startup combina HR Manager + Recruiter en HR Generalist
- ✅ Roles adicionales creados según tipo

---

## Fase 3: Diferenciación de Contenido de Páginas

**Prioridad**: 🟡 **MEDIA**  
**Estimación**: 2-3 días

### Tarea 3.1: Crear templates de contenido

**Archivo**: `src/company/application/templates/page_content_templates.py`

**Estructura**:
```python
PAGE_CONTENT_TEMPLATES = {
    CompanyTypeEnum.STARTUP_SMALL: {
        PageType.PUBLIC_COMPANY_DESCRIPTION: {
            "title": "About Our Company",
            "html_content": "...",  # Energetic, short, emojis
        },
        # ... otras páginas
    },
    # ... otros tipos
}
```

**Contenido por tipo**:
- **Startup/Small**: Energetic, short, emojis ("Join our rocket ship! 🚀")
- **Mid-Size**: Professional, growth-focused ("Career paths + benefits")
- **Enterprise**: Formal, compliant (EEO, legal disclaimers)
- **Agency**: Client-centric ("Partner with us" + `{{client_name}}` placeholder)

**Criterios de aceptación**:
- ✅ Archivo creado con estructura de templates
- ✅ Contenido diferenciado por tipo
- ✅ Tono apropiado para cada tipo
- ✅ Placeholders para Agency (ej: `{{client_name}}`)

---

### Tarea 3.2: Crear sistema de reemplazo de placeholders

**Archivo**: `src/company/application/utils/template_utils.py`

**Funcionalidad**:
- Función `replace_placeholders(content: str, context: Dict[str, str]) -> str`
- Reemplazar `{{variable}}` con valores del contexto
- Ejemplo: `{{client_name}}` → `context.get("client_name", "")`

**Criterios de aceptación**:
- ✅ Función creada
- ✅ Reemplaza placeholders correctamente
- ✅ Maneja valores faltantes

---

### Tarea 3.3: Modificar _create_default_pages() para usar templates

**Archivo**: `src/company/application/commands/initialize_onboarding_command.py`

**Cambios**:
- Modificar `_create_default_pages()` para aceptar `company_type`
- Obtener template según `company_type` y `page_type`
- Si no hay template, usar contenido vacío (comportamiento actual)
- Aplicar reemplazo de placeholders si es necesario
- Crear página con contenido del template

**Criterios de aceptación**:
- ✅ Usa templates según tipo
- ✅ Contenido diferenciado por tipo
- ✅ Fallback a contenido vacío si no hay template
- ✅ Placeholders reemplazados

---

### Tarea 3.4: Actualizar InitializeSampleDataCommand para usar templates

**Archivo**: `src/company/application/commands/initialize_sample_data_command.py`

**Cambios**:
- Obtener `company_type` de la empresa
- Al actualizar páginas con contenido de ejemplo, usar templates según tipo
- Mantener comportamiento actual pero con contenido diferenciado

**Criterios de aceptación**:
- ✅ Usa templates según tipo
- ✅ Contenido de ejemplo diferenciado
- ✅ No rompe funcionalidad existente

---

## Fase 4: Diferenciación de Workflows

**Prioridad**: 🟡 **MEDIA**  
**Estimación**: 3-4 días

### Tarea 4.1: Modificar InitializeCompanyPhasesCommand para aceptar company_type

**Archivo**: `src/phase/application/commands/initialize_company_phases_command.py`

**Cambios**:
- Agregar parámetro `company_type: Optional[CompanyTypeEnum] = None` al command
- Si es `None`, obtener de `CompanyRepository` usando `company_id`
- Pasar `company_type` a todos los métodos de creación de workflows

**Criterios de aceptación**:
- ✅ Parámetro agregado
- ✅ Se obtiene de la empresa si no se proporciona
- ✅ Se pasa a métodos de creación

---

### Tarea 4.2: Ajustar Job Position Workflow según tipo

**Archivo**: `src/phase/application/commands/initialize_company_phases_command.py`

**Método**: `_create_job_position_workflow()`

**Stages estándar (todos)**:
- Draft (INITIAL)
- Under Review (PROGRESS)
- Approved (PROGRESS)
- Published (SUCCESS)
- Closed (SUCCESS)
- Cancelled (FAIL)

**Ajustes por tipo**:
- **Startup/Small**: ❌ Remover "Under Review" → 5 stages total
- **Mid-Size**: ✅ Agregar "Budget Approval" (PROGRESS) después de "Under Review"
- **Enterprise**: ✅ Agregar "Compliance Review" (PROGRESS) después de "Approved"
- **Recruitment Agency**: ✅ Agregar "Client Approval" (PROGRESS) después de "Under Review"

**Criterios de aceptación**:
- ✅ Lógica condicional implementada
- ✅ Stages correctos según tipo
- ✅ Startup tiene 5 stages (sin "Under Review")
- ✅ Otros tipos tienen stages adicionales correctos

---

### Tarea 4.3: Ajustar Sourcing Workflow según tipo

**Archivo**: `src/phase/application/commands/initialize_company_phases_command.py`

**Método**: `_create_sourcing_workflow()`

**Stages estándar (todos)**:
- Pending (INITIAL)
- Screening (PROGRESS)
- Qualified (SUCCESS)
- Not Suitable (FAIL)
- On Hold (PROGRESS)

**Ajustes por tipo**:
- **Startup/Small**: Solo 3 stages: Pending, Qualified, Not Suitable
- **Mid-Size**: Standard (5 stages)
- **Enterprise**: Standard + Background Check (PROGRESS) antes de Qualified
- **Recruitment Agency**: Standard + Client Matching (PROGRESS) antes de Qualified

**Criterios de aceptación**:
- ✅ Lógica condicional implementada
- ✅ Startup tiene 3 stages
- ✅ Otros tipos tienen stages correctos
- ✅ Stages adicionales en Enterprise y Agency

---

### Tarea 4.4: Ajustar Evaluation Workflow según tipo

**Archivo**: `src/phase/application/commands/initialize_company_phases_command.py`

**Método**: `_create_evaluation_workflow()`

**Stages estándar (todos)**:
- HR Interview (INITIAL)
- Manager Interview (PROGRESS)
- Assessment Test (PROGRESS)
- Executive Interview (PROGRESS)
- Selected (SUCCESS)
- Rejected (FAIL)

**Ajustes por tipo**:
- **Startup/Small**: Solo 4 stages: HR Interview, Manager Interview, Selected, Rejected
- **Mid-Size**: Standard + Team Fit Interview (PROGRESS) después de Manager Interview
- **Enterprise**: Standard + Panel Interview (PROGRESS) + Reference Check (PROGRESS)
- **Recruitment Agency**: Standard + Client Interview (PROGRESS) después de Manager Interview

**Criterios de aceptación**:
- ✅ Lógica condicional implementada
- ✅ Startup tiene 4 stages
- ✅ Otros tipos tienen stages correctos
- ✅ Stages adicionales según tipo

---

### Tarea 4.5: Ajustar Offer Workflow según tipo

**Archivo**: `src/phase/application/commands/initialize_company_phases_command.py`

**Método**: `_create_offer_workflow()`

**Stages estándar (todos)**:
- Offer Proposal (INITIAL)
- Negotiation (PROGRESS)
- Document Submission (PROGRESS)
- Document Verification (SUCCESS)
- Lost (FAIL)

**Ajustes por tipo**:
- **Startup/Small**: Solo 3 stages: Offer Proposal, Document Verification, Lost
- **Mid-Size**: Standard (5 stages)
- **Enterprise**: Standard + Contract Review (PROGRESS) después de Negotiation
- **Recruitment Agency**: Standard + Placement Fee (PROGRESS) después de Negotiation

**Criterios de aceptación**:
- ✅ Lógica condicional implementada
- ✅ Startup tiene 3 stages
- ✅ Otros tipos tienen stages correctos
- ✅ Stages adicionales según tipo

---

## Fase 5: Custom Fields Recomendados

**Prioridad**: 🟢 **BAJA**  
**Estimación**: 2-3 días

### Tarea 5.1: Crear comando CreateRecommendedCustomFieldsCommand

**Archivo**: `src/company_workflow/application/commands/create_recommended_custom_fields_command.py`

**Estructura**:
```python
@dataclass(frozen=True)
class CreateRecommendedCustomFieldsCommand(Command):
    company_id: CompanyId
    company_type: Optional[CompanyTypeEnum] = None
    workflow_id: Optional[WorkflowId] = None  # Si None, crear en todos los workflows
```

**Funcionalidad**:
- Crear custom fields recomendados según `company_type`
- Campos base para todos los tipos
- Campos específicos según tipo
- Asignar a workflows/stages apropiados

**Criterios de aceptación**:
- ✅ Comando creado
- ✅ Handler implementado
- ✅ Crea campos base
- ✅ Crea campos específicos según tipo

---

### Tarea 5.2: Definir campos base (todos los tipos)

**Categorías y campos**:

**Compensation**:
- Salary Range (Text/Number, Internal, All stages)
- Current Salary (Number, Internal, Sourcing)
- Salary Expectation (Number, Internal, Offer)

**Availability**:
- Start Date (Date, Internal, Offer)
- Notice Period (Text, Internal, Offer)

**Evaluation**:
- Technical Score (Number 0-100, Internal, Assessment)
- Cultural Fit Score (Number 0-100, Internal, Interviews)
- Feedback (Textarea, Internal, All)

**Offer**:
- Salary Offer (Number, Internal, Offer)
- Benefits Package (Textarea, Internal, Offer)
- Start Date (Date, Internal, Offer)

**Documents**:
- Document Status (Select, Internal, Verification)
- Missing Docs (Text, Internal, Submission)

**Source**:
- Recruitment Source (Select, Internal, Sourcing)
- Recruiter Notes (Textarea, Internal, All)

**Criterios de aceptación**:
- ✅ Todos los campos base definidos
- ✅ Tipos correctos
- ✅ Visibilidad correcta (Internal)
- ✅ Stages sugeridos correctos

---

### Tarea 5.3: Definir campos específicos por tipo

**Startup/Small**:
- Equity Offer (Number/%, Internal, Offer)

**Mid-Size**:
- Relocation Assistance (Yes/No + Details, Internal, Offer)

**Enterprise**:
- Diversity Metrics (Select: Underrepresented, Internal, Sourcing) - **MANDATORY**

**Recruitment Agency**:
- Client Fit Score (Number 0-100, Internal, All)
- Bill Rate (Currency, Internal, Offer)

**Criterios de aceptación**:
- ✅ Campos específicos definidos
- ✅ Tipos correctos
- ✅ Diversity Metrics es mandatory en Enterprise
- ✅ Campos asignados a stages correctos

---

### Tarea 5.4: Integrar con InitializeOnboardingCommand (opcional)

**Archivo**: `src/company/application/commands/initialize_onboarding_command.py`

**Cambios**:
- Agregar parámetro `create_custom_fields: bool = False`
- Si `True`, llamar a `CreateRecommendedCustomFieldsCommand` después de crear roles y páginas

**Criterios de aceptación**:
- ✅ Parámetro agregado
- ✅ Comando se ejecuta condicionalmente
- ✅ Campos se crean correctamente

---

## Fase 6: Sample Data Diferenciado

**Prioridad**: 🟢 **BAJA**  
**Estimación**: 1-2 días

### Tarea 6.1: Revisar InitializeSampleDataCommand actual

**Archivo**: `src/company/application/commands/initialize_sample_data_command.py`

**Acción**: Leer y entender la implementación actual

**Criterios de aceptación**:
- ✅ Entendimiento completo de la implementación
- ✅ Identificadas las partes a modificar

---

### Tarea 6.2: Modificar para aceptar company_type

**Archivo**: `src/company/application/commands/initialize_sample_data_command.py`

**Cambios**:
- Agregar parámetro `company_type: Optional[CompanyTypeEnum] = None`
- Si es `None`, obtener de `CompanyRepository`
- Ajustar cantidades según tipo

**Criterios de aceptación**:
- ✅ Parámetro agregado
- ✅ Se obtiene de la empresa si no se proporciona

---

### Tarea 6.3: Ajustar cantidades según tipo

**Cantidades por tipo**:
- **Startup/Small**: 20 candidates, 5 positions, 10 users, 10 applications
- **Mid-Size**: 50 candidates, 10 positions, 10 users, 10 applications (standard)
- **Enterprise**: 100 candidates, 10 positions, 10 users, 10 applications
- **Recruitment Agency**: 50 candidates, 10 positions, 10 users, 10 applications + client tags

**Criterios de aceptación**:
- ✅ Cantidades ajustadas según tipo
- ✅ Startup tiene menos datos
- ✅ Enterprise tiene más candidates
- ✅ Agency tiene client tags

---

### Tarea 6.4: Agregar client tags para Agency

**Archivo**: `src/company/application/commands/initialize_sample_data_command.py`

**Cambios**:
- Si `company_type == CompanyTypeEnum.RECRUITMENT_AGENCY`
- Agregar tags de clientes a candidates y positions
- Ejemplo: `["Client A", "Client B", "Client C"]`

**Criterios de aceptación**:
- ✅ Tags agregados solo para Agency
- ✅ Tags realistas
- ✅ Asignados a candidates y positions

---

## Fase 7: AI Integration (FUTURO - AL FINAL)

**Prioridad**: 🔵 **FUTURO**  
**Estimación**: Variable (depende de integración)

### Tarea 7.1: AI para sugerir company type

**Archivo**: `src/company/application/services/ai_company_type_service.py` (nuevo)

**Funcionalidad**:
- Analizar nombre de empresa
- Analizar descripción (si existe)
- Sugerir `CompanyTypeEnum` más probable
- Retornar sugerencia con confianza (0-1)

**Criterios de aceptación**:
- ✅ Servicio creado
- ✅ Analiza nombre y descripción
- ✅ Retorna sugerencia con confianza
- ✅ Integración con API de AI (OpenAI, etc.)

---

### Tarea 7.2: Integrar sugerencia AI en wizard frontend

**Archivo**: `client-vite/src/components/registration/CompanyDataForm.tsx`

**Cambios**:
- Al escribir nombre de empresa, llamar a API de sugerencia
- Mostrar sugerencia: "Based on 'TechFlow Inc.', we suggest: Startup / Small Business"
- Permitir aceptar o rechazar sugerencia

**Criterios de aceptación**:
- ✅ Llamada a API implementada
- ✅ Sugerencia mostrada al usuario
- ✅ Usuario puede aceptar/rechazar

---

### Tarea 7.3: AI para generar contenido de páginas

**Archivo**: `src/company/application/services/ai_content_generation_service.py` (nuevo)

**Funcionalidad**:
- Generar contenido HTML para páginas según tipo
- Usar nombre de empresa, descripción, tipo
- Aplicar tono apropiado (energetic, professional, formal, client-centric)
- Retornar contenido generado

**Criterios de aceptación**:
- ✅ Servicio creado
- ✅ Genera contenido según tipo
- ✅ Tono apropiado
- ✅ Integración con API de AI

---

### Tarea 7.4: Integrar generación AI en InitializeOnboardingCommand

**Archivo**: `src/company/application/commands/initialize_onboarding_command.py`

**Cambios**:
- Agregar parámetro `use_ai_content: bool = False`
- Si `True`, usar `ai_content_generation_service` en lugar de templates estáticos
- Fallback a templates si AI falla

**Criterios de aceptación**:
- ✅ Parámetro agregado
- ✅ Usa AI si está habilitado
- ✅ Fallback a templates
- ✅ Manejo de errores

---

### Tarea 7.5: AI para sugerir custom fields

**Archivo**: `src/company/application/services/ai_custom_fields_service.py` (nuevo)

**Funcionalidad**:
- Analizar tipo de empresa, industria, descripción
- Sugerir custom fields adicionales no en la lista recomendada
- Retornar lista de sugerencias con descripción

**Criterios de aceptación**:
- ✅ Servicio creado
- ✅ Analiza contexto de empresa
- ✅ Sugiere campos relevantes
- ✅ Integración con API de AI

---

## Resumen de Tareas por Fase

| Fase | Tareas | Prioridad | Estimación |
|------|--------|-----------|------------|
| **Fase 1: Company Type System** | 10 tareas | 🔴 ALTA | 2-3 días |
| **Fase 2: Diferenciación de Roles** | 2 tareas | 🟡 MEDIA | 1-2 días |
| **Fase 3: Contenido de Páginas** | 4 tareas | 🟡 MEDIA | 2-3 días |
| **Fase 4: Diferenciación de Workflows** | 5 tareas | 🟡 MEDIA | 3-4 días |
| **Fase 5: Custom Fields Recomendados** | 4 tareas | 🟢 BAJA | 2-3 días |
| **Fase 6: Sample Data Diferenciado** | 4 tareas | 🟢 BAJA | 1-2 días |
| **Fase 7: AI Integration** | 5 tareas | 🔵 FUTURO | Variable |

**Total (sin Fase 7)**: 29 tareas, ~11-17 días  
**Total (con Fase 7)**: 34 tareas, ~11-17 días + tiempo de AI

---

## Orden de Implementación Recomendado

1. **Fase 1** (Fundación) - Debe ir primero
2. **Fase 2** (Roles) - Depende de Fase 1
3. **Fase 3** (Páginas) - Depende de Fase 1
4. **Fase 4** (Workflows) - Depende de Fase 1
5. **Fase 5** (Custom Fields) - Opcional, puede ir después
6. **Fase 6** (Sample Data) - Opcional, puede ir después
7. **Fase 7** (AI) - Al final, cuando todo lo demás esté funcionando

---

## Notas Importantes

- **Fase 1 es crítica**: Todas las demás fases dependen de ella
- **Fases 2-4 son las más visibles**: Impactan directamente la experiencia del usuario
- **Fases 5-6 son opcionales**: Pueden implementarse más tarde
- **Fase 7 requiere integración externa**: Necesita API de AI (OpenAI, etc.) y configuración

---

## Testing

Cada fase debe incluir:
- ✅ Tests unitarios para lógica de negocio
- ✅ Tests de integración para comandos
- ✅ Tests de migración de base de datos
- ✅ Tests de frontend para wizard y formularios

