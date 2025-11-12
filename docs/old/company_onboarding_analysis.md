# Análisis del Documento company_onboarding.md

**Fecha**: 2025-01-09  
**Documento analizado**: `docs/company_onboarding.md`  
**Versión del documento**: 1.0

---

## Resumen Ejecutivo

El documento `company_onboarding.md` describe un proceso de onboarding completo y personalizado basado en el tipo de empresa. El sistema actual ya tiene una base sólida implementada, pero faltan varias características clave para alcanzar la visión descrita en el documento.

**Estado General**: 
- ✅ **ONBOARDING básico**: Implementado (roles + páginas)
- ✅ **WORKFLOWS**: Implementado (fases y workflows por defecto)
- ✅ **SAMPLE DATA**: Implementado (datos de ejemplo opcionales)
- ❌ **Company Type System**: No implementado
- ❌ **Diferenciación por tipo**: No implementada
- ❌ **AI Integration**: No implementada
- ❌ **Contenido personalizado por tipo**: No implementado

---

## Análisis Detallado por Sección

### 1. Step 0: Company Type Selection

**Estado**: ❌ **NO IMPLEMENTADO**

**Requisitos del documento**:
- Wizard pregunta durante creación: "What best describes your company?"
- 4 tipos: Startup/Small Business, Mid-Size Company, Enterprise/Large Corporation, Recruitment Agency
- Default: Mid-Size Company
- AI Suggestion: Si el usuario omite, AI predice basado en nombre

**Estado actual**:
- No existe un enum o entidad para `CompanyType`
- No existe campo `company_type` en la entidad `Company`
- No existe wizard o pregunta durante el registro
- No existe integración de AI para sugerir tipo

**Archivos relacionados**:
- `src/company/domain/entities/company.py` - No tiene campo `company_type`
- `src/company/infrastructure/models/company_model.py` - No tiene columna `company_type`
- `client-vite/src/types/company.ts` - Tiene `CompanyIndustry` pero no `CompanyType`

**Acciones necesarias**:
1. Crear enum `CompanyTypeEnum` en `src/company/domain/enums/`
2. Agregar campo `company_type` a la entidad `Company`
3. Agregar columna `company_type` a `CompanyModel` (migración)
4. Agregar pregunta en el wizard de registro (frontend)
5. Implementar lógica de AI para sugerir tipo (opcional, futuro)

---

### 2. ONBOARDING – Basic Configuration (Roles + Pages)

**Estado**: ✅ **PARCIALMENTE IMPLEMENTADO**

#### 2.1 Roles

**Requisitos del documento**:
- 7 roles base: HR Manager, Recruiter, Tech Lead, Hiring Manager, Interviewer, Department Head, CTO
- Diferenciación por tipo de empresa:
  - **Startup/Small**: Combinar HR Manager + Recruiter → HR Generalist, agregar Founder
  - **Mid-Size**: Agregar Talent Acquisition Specialist
  - **Enterprise**: Agregar Diversity & Inclusion Officer, Legal Reviewer
  - **Agency**: Agregar Client Manager, Sourcer

**Estado actual**:
- ✅ `InitializeOnboardingCommand` crea 7 roles base correctamente
- ❌ No hay diferenciación por tipo de empresa
- ❌ No se crean roles adicionales según el tipo

**Archivo**: `src/company/application/commands/initialize_onboarding_command.py` (líneas 48-96)

**Acciones necesarias**:
1. Modificar `InitializeOnboardingCommand` para aceptar `company_type`
2. Crear lógica condicional en `_create_default_roles()` para ajustar roles según tipo
3. Implementar combinación de roles para Startup (HR Generalist)
4. Agregar roles adicionales según tipo

#### 2.2 Default Pages

**Requisitos del documento**:
- 5 páginas: `public_company_description`, `job_position_description`, `data_protection`, `terms_of_use`, `thank_you_application`
- Comportamiento por inicialización:
  - **Basic (no sample)**: DRAFT, empty
  - **With Sample Data**: PUBLISHED (o DRAFT), pre-filled
- Diferenciación por tipo:
  - **Startup/Small**: Energetic, short, emojis
  - **Mid-Size**: Professional, growth-focused
  - **Enterprise**: Formal, compliant, EEO, legal disclaimers
  - **Agency**: Client-centric, `{{client_name}}` placeholder

**Estado actual**:
- ✅ `InitializeOnboardingCommand` crea 5 páginas en DRAFT con contenido vacío
- ✅ `InitializeSampleDataCommand` actualiza páginas con contenido de ejemplo
- ❌ No hay diferenciación de contenido por tipo de empresa
- ❌ No hay generación automática de contenido basado en tipo

**Archivos**:
- `src/company/application/commands/initialize_onboarding_command.py` (líneas 98-166)
- `src/company/application/commands/initialize_sample_data_command.py` (probablemente existe)

**Acciones necesarias**:
1. Crear templates de contenido por tipo de empresa
2. Modificar `_create_default_pages()` para aceptar `company_type` y generar contenido inicial
3. Implementar generación de contenido con tono apropiado según tipo
4. Agregar soporte para placeholders (ej: `{{client_name}}` para Agency)

---

### 3. WORKFLOWS – Default Hiring Processes

**Estado**: ✅ **IMPLEMENTADO** (pero sin diferenciación por tipo)

#### 3.1 Job Position Workflow

**Requisitos del documento**:
- Workflow: "Job Positions Workflow" (Kanban)
- 6 stages: Draft, Under Review, Approved, Published, Closed, Cancelled
- Diferenciación por tipo:
  - **Startup**: Skip "Under Review" → 4 stages
  - **Mid-Size**: Add "Budget Approval"
  - **Enterprise**: Add "Compliance Review"
  - **Agency**: Add "Client Approval"

**Estado actual**:
- ✅ `InitializeCompanyPhasesCommand` crea workflow de Job Positions con 6 stages estándar
- ❌ No hay diferenciación por tipo de empresa
- ❌ No se ajustan stages según tipo

**Archivo**: `src/phase/application/commands/initialize_company_phases_command.py` (líneas 308-351)

**Acciones necesarias**:
1. Modificar `_create_job_position_workflow()` para aceptar `company_type`
2. Implementar lógica condicional para crear stages según tipo
3. Startup: Remover "Under Review"
4. Mid-Size: Agregar "Budget Approval"
5. Enterprise: Agregar "Compliance Review"
6. Agency: Agregar "Client Approval"

#### 3.2 Candidate Application Workflows

**Requisitos del documento**:
- **Phase 1: Sourcing** (Kanban): 5 stages (Pending, Screening, Qualified, Not Suitable, On Hold)
- **Phase 2: Evaluation** (Kanban): 6 stages (HR Interview, Manager Interview, Assessment Test, Executive Interview, Selected, Rejected)
- **Phase 3: Offer & Pre-Onboarding** (List): 5 stages (Offer Proposal, Negotiation, Document Submission, Document Verification, Lost)
- Diferenciación por tipo:
  - **Startup**: Sourcing 3 stages (fast), Evaluation 4 stages, Offer 3 stages
  - **Mid-Size**: Standard + Team Fit Interview
  - **Enterprise**: + Background Check, + Panel + Reference, + Contract Review
  - **Agency**: + Client Matching, + Client Interview, + Placement Fee

**Estado actual**:
- ✅ `InitializeCompanyPhasesCommand` crea las 3 fases correctamente
- ✅ Stages coinciden con el documento (5, 6, 5 respectivamente)
- ❌ No hay diferenciación por tipo de empresa
- ❌ No se ajustan stages según tipo

**Archivos**:
- `src/phase/application/commands/initialize_company_phases_command.py`:
  - `_create_sourcing_workflow()` (líneas 152-193)
  - `_create_evaluation_workflow()` (líneas 195-238)
  - `_create_offer_workflow()` (líneas 240-281)

**Acciones necesarias**:
1. Modificar los 3 métodos de creación de workflows para aceptar `company_type`
2. Implementar lógica condicional para crear stages según tipo
3. Startup: Reducir stages (Sourcing: 3, Evaluation: 4, Offer: 3)
4. Mid-Size: Agregar "Team Fit Interview" en Evaluation
5. Enterprise: Agregar stages adicionales en cada fase
6. Agency: Agregar stages específicos de cliente

#### 3.3 Stage Configuration

**Requisitos del documento**:
- Roles por stage
- Emails automáticos (Unlayer templates)
- Deadlines (ej: 3 días Sourcing, 7 días Evaluation)
- Cost (ej: $100 interview, $50 test)
- Custom Fields (ver sección 3.4)

**Estado actual**:
- ⚠️ Stages se crean sin configuración de roles, emails, deadlines, cost
- ⚠️ Custom fields existen pero no se crean automáticamente durante onboarding

**Acciones necesarias**:
1. Agregar configuración de roles por stage durante creación
2. Integrar con sistema de email templates (Unlayer)
3. Agregar deadlines por defecto según tipo de stage
4. Agregar cost estimation por stage
5. Crear custom fields recomendados durante onboarding (ver sección 3.4)

#### 3.4 Recommended Custom Fields

**Requisitos del documento**:
- Campos recomendados por categoría:
  - **Compensation**: Salary Range, Current Salary, Salary Expectation
  - **Availability**: Start Date, Notice Period
  - **Evaluation**: Technical Score, Cultural Fit Score, Feedback
  - **Offer**: Salary Offer, Benefits Package, Start Date
  - **Documents**: Document Status, Missing Docs
  - **Source**: Recruitment Source, Recruiter Notes
- Campos específicos por tipo:
  - **Startup**: Equity Offer
  - **Mid-Size**: Relocation Assistance
  - **Enterprise**: Diversity Metrics (mandatory en Sourcing)
  - **Agency**: Client Fit Score, Bill Rate

**Estado actual**:
- ✅ Sistema de custom fields existe (`CustomField`, `CustomFieldValue`)
- ❌ No se crean campos automáticamente durante onboarding
- ❌ No hay campos recomendados por tipo de empresa

**Acciones necesarias**:
1. Crear comando `CreateRecommendedCustomFieldsCommand`
2. Integrar con `InitializeOnboardingCommand` o crear paso separado
3. Crear campos base para todos los tipos
4. Agregar campos específicos según `company_type`
5. Marcar campos como mandatory según tipo (ej: Diversity Metrics en Enterprise)

---

### 4. SAMPLE DATA – Optional Evaluation Mode

**Requisitos del documento**:
- 50 candidates, 10 job positions, 10 users, 10 applications
- Diferenciación por tipo:
  - **Startup**: 20 candidates, 5 positions
  - **Mid-Size**: Standard
  - **Enterprise**: 100 candidates
  - **Agency**: Standard + client tags

**Estado actual**:
- ✅ `InitializeSampleDataCommand` existe
- ⚠️ Probablemente crea datos estándar sin diferenciación por tipo

**Acciones necesarias**:
1. Verificar implementación actual de `InitializeSampleDataCommand`
2. Modificar para aceptar `company_type`
3. Ajustar cantidades según tipo
4. Agregar client tags para Agency
5. Generar contenido realista con AI (opcional, futuro)

---

## Comparación: Documento vs. Implementación Actual

| Característica | Documento | Implementación Actual | Estado |
|---------------|-----------|----------------------|--------|
| **Company Type Selection** | Wizard con 4 tipos + AI | No existe | ❌ |
| **Roles Base (7)** | HR Manager, Recruiter, etc. | ✅ Implementado | ✅ |
| **Roles por Tipo** | Diferenciación (HR Generalist, etc.) | No diferenciado | ❌ |
| **Pages Base (5)** | public_company_description, etc. | ✅ Implementado | ✅ |
| **Contenido Pages por Tipo** | Tono diferenciado | Contenido vacío/genérico | ❌ |
| **Job Position Workflow** | 6 stages estándar | ✅ 6 stages | ✅ |
| **Job Position Stages por Tipo** | Ajustes según tipo | No diferenciado | ❌ |
| **Candidate Workflows (3 fases)** | Sourcing, Evaluation, Offer | ✅ Implementado | ✅ |
| **Candidate Stages por Tipo** | Ajustes según tipo | No diferenciado | ❌ |
| **Custom Fields Recomendados** | Lista completa | No se crean automáticamente | ❌ |
| **Custom Fields por Tipo** | Campos específicos | No diferenciado | ❌ |
| **Sample Data** | 50 candidates, etc. | Probablemente existe | ⚠️ |
| **Sample Data por Tipo** | Cantidades ajustadas | Probablemente no diferenciado | ❌ |
| **AI Integration** | Sugerencias de tipo y contenido | No implementado | ❌ |

---

## Plan de Implementación Recomendado

### Fase 1: Company Type System (Fundación)
**Prioridad**: 🔴 **ALTA** (requerido para todo lo demás)

1. **Crear enum `CompanyTypeEnum`**
   - Ubicación: `src/company/domain/enums/company_type_enum.py`
   - Valores: `STARTUP_SMALL`, `MID_SIZE`, `ENTERPRISE`, `RECRUITMENT_AGENCY`

2. **Agregar campo a entidad `Company`**
   - Campo: `company_type: Optional[CompanyTypeEnum]`
   - Default: `CompanyTypeEnum.MID_SIZE`

3. **Migración de base de datos**
   - Agregar columna `company_type` a tabla `companies`
   - Default: `'mid_size'`

4. **Actualizar comandos de creación**
   - `CreateCompanyCommand`: Agregar `company_type: Optional[CompanyTypeEnum]`
   - `RegisterCompanyWithUserCommand`: Agregar pregunta en wizard (frontend)

5. **Frontend: Wizard de selección**
   - Agregar pregunta en `CompanyDataForm`
   - Mostrar opciones con descripciones
   - AI suggestion (opcional, futuro)

### Fase 2: Diferenciación de Roles
**Prioridad**: 🟡 **MEDIA**

1. **Modificar `InitializeOnboardingCommand`**
   - Aceptar `company_type: CompanyTypeEnum`
   - Lógica condicional en `_create_default_roles()`

2. **Implementar roles por tipo**
   - Startup: HR Generalist (combinar HR Manager + Recruiter), agregar Founder
   - Mid-Size: Agregar Talent Acquisition Specialist
   - Enterprise: Agregar Diversity & Inclusion Officer, Legal Reviewer
   - Agency: Agregar Client Manager, Sourcer

### Fase 3: Diferenciación de Contenido de Páginas
**Prioridad**: 🟡 **MEDIA**

1. **Crear templates de contenido**
   - Archivo: `src/company/application/templates/page_content_templates.py`
   - Templates por tipo y por página

2. **Modificar `_create_default_pages()`**
   - Generar contenido inicial según `company_type`
   - Aplicar tono apropiado (energetic, professional, formal, client-centric)

3. **Soporte para placeholders**
   - Sistema de reemplazo de variables (ej: `{{client_name}}`)

### Fase 4: Diferenciación de Workflows
**Prioridad**: 🟡 **MEDIA**

1. **Modificar `InitializeCompanyPhasesCommand`**
   - Aceptar `company_type: CompanyTypeEnum`
   - Pasar `company_type` a métodos de creación de workflows

2. **Ajustar Job Position Workflow**
   - Startup: Remover "Under Review"
   - Mid-Size: Agregar "Budget Approval"
   - Enterprise: Agregar "Compliance Review"
   - Agency: Agregar "Client Approval"

3. **Ajustar Candidate Workflows**
   - Startup: Reducir stages (Sourcing: 3, Evaluation: 4, Offer: 3)
   - Mid-Size: Agregar "Team Fit Interview"
   - Enterprise: Agregar stages adicionales
   - Agency: Agregar stages de cliente

### Fase 5: Custom Fields Recomendados
**Prioridad**: 🟢 **BAJA** (puede ser manual por ahora)

1. **Crear comando `CreateRecommendedCustomFieldsCommand`**
   - Campos base para todos los tipos
   - Campos específicos según `company_type`

2. **Integrar con onboarding**
   - Opcional: checkbox "Create recommended custom fields?"

### Fase 6: Sample Data Diferenciado
**Prioridad**: 🟢 **BAJA**

1. **Revisar `InitializeSampleDataCommand`**
2. **Ajustar cantidades según tipo**
3. **Agregar client tags para Agency**

### Fase 7: AI Integration (Futuro)
**Prioridad**: 🔵 **FUTURO**

1. **AI para sugerir company type**
   - Basado en nombre de empresa
   - Basado en descripción

2. **AI para generar contenido**
   - Auto-generar descripciones de páginas
   - Sugerir campos personalizados

---

## Archivos a Modificar/Crear

### Nuevos Archivos
1. `src/company/domain/enums/company_type_enum.py` - Enum de tipos
2. `src/company/application/templates/page_content_templates.py` - Templates de contenido
3. `src/company/application/commands/create_recommended_custom_fields_command.py` - Comando para custom fields
4. `alembic/versions/XXX_add_company_type_to_companies.py` - Migración

### Archivos a Modificar
1. `src/company/domain/entities/company.py` - Agregar campo `company_type`
2. `src/company/infrastructure/models/company_model.py` - Agregar columna
3. `src/company/application/commands/create_company_command.py` - Agregar parámetro
4. `src/company/application/commands/register_company_with_user_command.py` - Agregar parámetro
5. `src/company/application/commands/initialize_onboarding_command.py` - Diferenciación por tipo
6. `src/phase/application/commands/initialize_company_phases_command.py` - Diferenciación por tipo
7. `client-vite/src/types/company.ts` - Agregar `CompanyType`
8. `client-vite/src/components/registration/CompanyDataForm.tsx` - Agregar wizard

---

## Conclusión

El documento `company_onboarding.md` describe una visión ambiciosa y bien estructurada del proceso de onboarding. El sistema actual tiene una base sólida con los 3 niveles de inicialización (ONBOARDING, WORKFLOWS, SAMPLE DATA) implementados, pero falta la **diferenciación por tipo de empresa**, que es el elemento clave que hace el onboarding "perfecto" según el documento.

**Recomendación**: Implementar primero el sistema de tipos de empresa (Fase 1), ya que es la fundación para todas las demás diferenciaciones. Luego, implementar las fases 2-4 que son las más visibles para el usuario. Las fases 5-7 pueden ser opcionales o implementadas más adelante.

**Estimación de esfuerzo**:
- Fase 1: 2-3 días
- Fase 2: 1-2 días
- Fase 3: 2-3 días
- Fase 4: 3-4 días
- Fase 5: 2-3 días
- Fase 6: 1-2 días
- Fase 7: Futuro (depende de integración AI)

**Total estimado**: 11-17 días de desarrollo (sin Fase 7)

