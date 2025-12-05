# Análisis de Migración: Interview e Interview Template de Admin a Company

## Resumen Ejecutivo

Este documento analiza todas las funcionalidades de **Interview** e **Interview Template** existentes en el módulo de Admin (backend y frontend) para planificar su migración al módulo de Company con componentes Shadcn UI.

### Alcance
- **Backend**: 30 endpoints relacionados con interviews e interview templates en `/admin`
- **Frontend**: 3 componentes principales en `/admin`
- **Objetivo**: Migrar a `/company` con Shadcn UI components

---

## 1. Backend - Rutas de Admin

### 1.1 Interview Template Management (17 endpoints)

#### Templates CRUD
| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| GET | `/admin/interview-templates` | Listar templates con filtros | Admin |
| POST | `/admin/interview-templates` | Crear template | Admin |
| GET | `/admin/interview-templates/{template_id}` | Obtener template por ID | Admin |
| PUT | `/admin/interview-templates/{template_id}` | Actualizar template | Admin |
| POST | `/admin/interview-templates/{template_id}/enable` | Habilitar template | Admin |
| POST | `/admin/interview-templates/{template_id}/disable` | Deshabilitar template | Admin |
| DELETE | `/admin/interview-templates/{template_id}` | Eliminar template | Admin |

**Filtros disponibles:**
- `search_term`: Búsqueda por nombre
- `type`: EXTENDED_PROFILE | POSITION_INTERVIEW
- `status`: ENABLED | DRAFT | DISABLED
- `job_category`: Categoría del trabajo
- `section`: EXPERIENCE | EDUCATION | PROJECT | SOFT_SKILL | GENERAL
- `page`, `page_size`: Paginación

#### Sections Management (7 endpoints)
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/admin/interview-template-sections` | Crear sección |
| PUT | `/admin/interview-template-sections/{section_id}` | Actualizar sección |
| POST | `/admin/interview-template-sections/{section_id}/enable` | Habilitar sección |
| POST | `/admin/interview-template-sections/{section_id}/disable` | Deshabilitar sección |
| DELETE | `/admin/interview-template-sections/{section_id}` | Eliminar sección |
| POST | `/admin/interview-template-sections/{section_id}/move-up` | Mover sección arriba |
| POST | `/admin/interview-template-sections/{section_id}/move-down` | Mover sección abajo |

#### Questions Management (5 endpoints)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/admin/interview-template-sections/{section_id}/questions` | Listar preguntas de una sección |
| POST | `/admin/interview-template-questions` | Crear pregunta |
| PUT | `/admin/interview-template-questions/{question_id}` | Actualizar pregunta |
| POST | `/admin/interview-template-questions/{question_id}/enable` | Habilitar pregunta |
| POST | `/admin/interview-template-questions/{question_id}/disable` | Deshabilitar pregunta |
| DELETE | `/admin/interview-template-questions/{question_id}` | Eliminar pregunta |

**Controller**: `InterviewTemplateController` (`adapters/http/admin_app/controllers/inverview_template_controller.py`)

---

### 1.2 Interview Management (13 endpoints)

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| GET | `/admin/interview` | Listar interviews con filtros | Admin |
| GET | `/admin/interview/stats` | Estadísticas de interviews | Admin |
| GET | `/admin/interview/{interview_id}` | Obtener interview por ID | Admin |
| POST | `/admin/interview` | Crear interview | Admin |
| PUT | `/admin/interview/{interview_id}` | Actualizar interview | Admin |
| POST | `/admin/interview/{interview_id}/start` | Iniciar interview | Admin |
| POST | `/admin/interview/{interview_id}/finish` | Finalizar interview | Admin |
| GET | `/admin/interview/candidate/{candidate_id}` | Interviews de un candidato | Admin |
| GET | `/admin/interview/scheduled` | Interviews programados | Admin |
| GET | `/admin/interview/{interview_id}/score-summary` | Resumen de puntuación | Admin |

**Filtros disponibles:**
- `candidate_id`: Filtrar por candidato
- `job_position_id`: Filtrar por posición
- `interview_type`: Tipo de interview
- `status`: Estado del interview
- `created_by`: Creador
- `from_date`, `to_date`: Rango de fechas
- `limit`, `offset`: Paginación

**Controller**: `InterviewController` (`adapters/http/admin_app/controllers/interview_controller.py`)

---

## 2. Frontend - Componentes de Admin

### 2.1 Interview Templates Management

**Archivo**: `client-vite/src/components/admin/InterviewTemplatesManagement.tsx`

**Funcionalidades:**
- ✅ Listar templates con tabla
- ✅ Filtros: search_term, type, status
- ✅ Acciones: Edit, Enable/Disable, Delete
- ✅ Navegación a crear/editar template

**Componentes UI actuales:**
- ❌ **NO usa Shadcn** - Usa HTML nativo:
  - `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<td>`
  - `<select>` nativo para filtros
  - `<button>` nativo
  - Tooltip custom (no Shadcn)
  - Loading spinner custom

**Endpoints utilizados:**
- `GET /admin/interview-templates` (con query params)
- `DELETE /admin/interview-templates/{template_id}`
- `POST /admin/interview-templates/{template_id}/enable`
- `POST /admin/interview-templates/{template_id}/disable`

**Estado:**
- ✅ Funcional
- ❌ No usa Shadcn UI
- ❌ No tiene paginación visible (aunque el backend la soporta)

---

### 2.2 Interview Template Editor

**Archivo**: `client-vite/src/components/admin/InterviewTemplateEditor.tsx`

**Funcionalidades:**
- ✅ Crear/Editar template completo
- ✅ Gestión de secciones (CRUD)
- ✅ Gestión de preguntas por sección (CRUD)
- ✅ Reordenar secciones (move up/down)
- ✅ Enable/Disable de secciones y preguntas
- ✅ Formularios modales para secciones y preguntas

**Componentes UI actuales:**
- ❌ **NO usa Shadcn** - Usa HTML nativo:
  - `<form>`, `<input>`, `<textarea>`, `<select>`
  - `<button>` nativo
  - Modales custom con `fixed inset-0`
  - Tooltip custom
  - Loading spinner custom

**Endpoints utilizados:**
- `GET /admin/interview-templates/{template_id}`
- `POST /admin/interview-templates`
- `PUT /admin/interview-templates/{template_id}`
- `POST /admin/interview-template-sections`
- `PUT /admin/interview-template-sections/{section_id}`
- `DELETE /admin/interview-template-sections/{section_id}`
- `POST /admin/interview-template-sections/{section_id}/enable`
- `POST /admin/interview-template-sections/{section_id}/disable`
- `POST /admin/interview-template-sections/{section_id}/move-up`
- `POST /admin/interview-template-sections/{section_id}/move-down`
- `GET /admin/interview-template-sections/{section_id}/questions`
- `POST /admin/interview-template-questions`
- `PUT /admin/interview-template-questions/{question_id}`
- `DELETE /admin/interview-template-questions/{question_id}`

**Estado:**
- ✅ Funcional
- ❌ No usa Shadcn UI
- ⚠️ Manejo de errores básico (alert/console.warn)

---

### 2.3 Interview Page

**Archivo**: `client-vite/src/pages/InterviewPage.tsx`

**Funcionalidades:**
- ⚠️ **Parcialmente deshabilitado** - Muestra mensaje de "temporarily disabled"
- ✅ Carga interview activo
- ✅ Botones para iniciar nuevo interview
- ✅ Quick stats cards (con datos mock)

**Componentes UI actuales:**
- ❌ **NO usa Shadcn** - Usa HTML nativo:
  - `<button>` nativo
  - Cards custom con `bg-white border`
  - Loading spinner custom
  - ErrorAlert component (no Shadcn)

**Endpoints utilizados:**
- `api.getActiveInterview()` (endpoint no identificado en admin router)

**Estado:**
- ⚠️ Parcialmente funcional
- ❌ No usa Shadcn UI
- ❌ InterviewList component deshabilitado

---

## 3. Análisis de Componentes UI Actuales

### 3.1 Componentes que NO usan Shadcn

| Componente | Ubicación | Reemplazo Shadcn |
|------------|-----------|------------------|
| `<table>` | InterviewTemplatesManagement | `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableCell` |
| `<select>` | Ambos componentes | `Select`, `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectItem` |
| `<button>` | Todos | `Button` (con variants: default, outline, ghost, destructive) |
| `<input>` | InterviewTemplateEditor | `Input` |
| `<textarea>` | InterviewTemplateEditor | `Textarea` |
| Modal custom | InterviewTemplateEditor | `Dialog`, `DialogTrigger`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogDescription`, `DialogFooter` |
| Tooltip custom | Ambos | `Tooltip`, `TooltipTrigger`, `TooltipContent`, `TooltipProvider` |
| Loading spinner | Todos | `Skeleton` o componente de loading |
| Error alert | InterviewPage | `Alert`, `AlertDescription` |
| Cards | InterviewPage | `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent` |

### 3.2 Componentes que SÍ usan Shadcn (referencia)

- `CandidatesListPage.tsx` ya migrado con:
  - `Button`, `Card`, `CardContent`, `Table`, `Select`, `Tooltip`
  - Puede servir como referencia

---

## 4. Plan de Migración a Company

### 4.1 Estructura de Rutas Company

**Backend:**
```
/api/company/interview-templates/*
/api/company/interviews/*
```

**Frontend:**
```
/company/interview-templates
/company/interview-templates/create
/company/interview-templates/edit/:templateId
/company/interviews
/company/interviews/:interviewId
```

### 4.2 Cambios Necesarios

#### Backend

1. **Crear nuevo router** (`adapters/http/company_app/interview/routers/company_interview_template_router.py`)
   - Replicar endpoints de admin
   - Cambiar autenticación: `get_company_id_from_token` + `get_company_user_id_from_token`
   - Prefijo: `/api/company/interview-templates`

2. **Crear nuevo router** (`adapters/http/company_app/interview/routers/company_interview_router.py`)
   - Replicar endpoints de admin
   - Cambiar autenticación: `get_company_id_from_token` + `get_company_user_id_from_token`
   - Prefijo: `/api/company/interviews`
   - ⚠️ **Filtro importante**: Solo mostrar interviews de la company del usuario

3. **Reutilizar controllers existentes:**
   - `InterviewTemplateController` (puede reutilizarse)
   - `InterviewController` (puede reutilizarse, pero filtrar por company_id)

4. **Registrar routers en `main.py`**

#### Frontend

1. **Crear servicio** (`client-vite/src/services/companyInterviewTemplateService.ts`)
   - Cambiar base path de `/admin/interview-templates` a `/api/company/interview-templates`
   - Métodos: `listTemplates`, `getTemplate`, `createTemplate`, `updateTemplate`, `deleteTemplate`, `enableTemplate`, `disableTemplate`
   - Métodos de secciones: `createSection`, `updateSection`, `deleteSection`, `enableSection`, `disableSection`, `moveSectionUp`, `moveSectionDown`
   - Métodos de preguntas: `getQuestionsBySection`, `createQuestion`, `updateQuestion`, `deleteQuestion`, `enableQuestion`, `disableQuestion`

2. **Crear servicio** (`client-vite/src/services/companyInterviewService.ts`)
   - Cambiar base path de `/admin/interview` a `/api/company/interviews`
   - Métodos: `listInterviews`, `getInterview`, `createInterview`, `updateInterview`, `startInterview`, `finishInterview`, `getInterviewsByCandidate`, `getScheduledInterviews`, `getScoreSummary`

3. **Migrar componentes con Shadcn:**

   **a) InterviewTemplatesManagement → CompanyInterviewTemplatesPage**
   - Ubicación: `client-vite/src/pages/company/InterviewTemplatesPage.tsx`
   - Reemplazar:
     - `<table>` → `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableCell`
     - `<select>` → `Select`, `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectItem`
     - `<button>` → `Button`
     - Tooltip custom → `Tooltip` de Shadcn
     - Loading spinner → `Skeleton` o componente de loading
   - Agregar paginación visible (usar componente de paginación si existe)

   **b) InterviewTemplateEditor → CompanyInterviewTemplateEditorPage**
   - Ubicación: `client-vite/src/pages/company/InterviewTemplateEditorPage.tsx`
   - Reemplazar:
     - `<form>`, `<input>` → `Input`
     - `<textarea>` → `Textarea`
     - `<select>` → `Select`
     - `<button>` → `Button`
     - Modal custom → `Dialog`
     - Tooltip custom → `Tooltip`
   - Usar `react-toastify` para errores (como en `EditWorkflowPage.tsx`)

   **c) InterviewPage → CompanyInterviewsPage**
   - Ubicación: `client-vite/src/pages/company/InterviewsPage.tsx`
   - Reemplazar:
     - Cards custom → `Card`, `CardHeader`, `CardTitle`, `CardContent`
     - `<button>` → `Button`
     - ErrorAlert → `Alert` de Shadcn
   - Implementar lista de interviews (actualmente deshabilitada)

4. **Agregar rutas en `App.tsx`:**
   ```tsx
   <Route path="interview-templates" element={<CompanyInterviewTemplatesPage />} />
   <Route path="interview-templates/create" element={<CompanyInterviewTemplateEditorPage />} />
   <Route path="interview-templates/edit/:templateId" element={<CompanyInterviewTemplateEditorPage />} />
   <Route path="interviews" element={<CompanyInterviewsPage />} />
   <Route path="interviews/:interviewId" element={<CompanyInterviewDetailPage />} />
   ```

5. **Agregar al menú lateral** (`CompanyLayout.tsx`):
   - Opción "Interview Templates" en el menú
   - Opción "Interviews" en el menú

---

## 5. Checklist de Migración

### Fase 1: Backend

- [ ] Crear `adapters/http/company_app/interview/routers/company_interview_template_router.py`
- [ ] Crear `adapters/http/company_app/interview/routers/company_interview_router.py`
- [ ] Crear `adapters/http/company_app/interview/controllers/` (si es necesario, o reutilizar)
- [ ] Crear `adapters/http/company_app/interview/schemas/` (si es necesario, o reutilizar)
- [ ] Registrar routers en `main.py`
- [ ] Agregar filtro por `company_id` en queries de interviews
- [ ] Probar endpoints con Postman/Thunder Client

### Fase 2: Frontend - Servicios

- [ ] Crear `client-vite/src/services/companyInterviewTemplateService.ts`
- [ ] Crear `client-vite/src/services/companyInterviewService.ts`
- [ ] Probar servicios con endpoints

### Fase 3: Frontend - Componentes con Shadcn

- [ ] Migrar `InterviewTemplatesManagement` → `CompanyInterviewTemplatesPage` con Shadcn
- [ ] Migrar `InterviewTemplateEditor` → `CompanyInterviewTemplateEditorPage` con Shadcn
- [ ] Migrar `InterviewPage` → `CompanyInterviewsPage` con Shadcn
- [ ] Crear `CompanyInterviewDetailPage` (nuevo, para ver detalles de un interview)
- [ ] Agregar rutas en `App.tsx`
- [ ] Agregar opciones al menú lateral

### Fase 4: Testing y Refinamiento

- [ ] Probar flujo completo de creación de template
- [ ] Probar gestión de secciones y preguntas
- [ ] Probar creación y gestión de interviews
- [ ] Verificar que solo se muestran datos de la company del usuario
- [ ] Verificar responsive design
- [ ] Verificar manejo de errores con toasts
- [ ] Agregar traducciones (i18n) si es necesario

---

## 6. Consideraciones Especiales

### 6.1 Filtrado por Company

- **Backend**: Todos los endpoints de interviews deben filtrar por `company_id` del usuario autenticado
- **Frontend**: No es necesario filtrar manualmente, el backend ya lo hace

### 6.5 Company ID en Interview Templates

**⚠️ IMPORTANTE**: Las plantillas van a nivel de company. Sin embargo, actualmente:

1. **La entidad de dominio** (`InterviewTemplate`) SÍ tiene `company_id: Optional[CompanyId]`
2. **El modelo SQLAlchemy** (`InterviewTemplateModel`) NO tiene la columna `company_id` en la BD
3. **El repositorio** NO mapea `company_id` (pone `None` con comentario "Add company_id mapping later if needed")
4. **El controller de admin** siempre pone `company_id=None` al crear templates

**Tareas críticas necesarias:**
- [ ] Crear migración para agregar columna `company_id` a la tabla `interview_templates`
- [ ] Actualizar `InterviewTemplateModel` para incluir `company_id: Mapped[Optional[str]]`
- [ ] Actualizar repositorio para mapear `company_id` en `_to_domain()` y `_to_model()`
- [ ] Actualizar queries para filtrar por `company_id` cuando se liste templates
- [ ] En el controller de company, hacer que `company_id` sea OBLIGATORIO (no Optional) y usar el `company_id` del usuario autenticado
- [ ] Actualizar `ListInterviewTemplatesQuery` para aceptar y filtrar por `company_id`

### 6.2 Permisos

- Verificar si hay roles específicos para gestionar interviews (ej: solo HR puede crear templates)
- Si no existen, considerar agregar validación de roles en el backend

### 6.3 Integración con Candidatos

- Los interviews están vinculados a candidatos (`candidate_id`)
- Asegurar que los candidatos mostrados en los selects pertenecen a la company del usuario

### 6.4 Integración con Job Positions

- Los interviews pueden estar vinculados a job positions (`job_position_id`)
- Asegurar que las posiciones mostradas pertenecen a la company del usuario

---

## 7. Referencias

### Archivos Backend
- `adapters/http/admin_app/routes/admin_router.py` (líneas 114-390 para templates, 1111-1294 para interviews)
- `adapters/http/admin_app/controllers/inverview_template_controller.py`
- `adapters/http/admin_app/controllers/interview_controller.py`
- `adapters/http/admin_app/schemas/interview_template.py`
- `adapters/http/admin_app/schemas/interview_management.py`

### Archivos Frontend
- `client-vite/src/components/admin/InterviewTemplatesManagement.tsx`
- `client-vite/src/components/admin/InterviewTemplateEditor.tsx`
- `client-vite/src/pages/InterviewPage.tsx`
- `client-vite/src/pages/company/CandidatesListPage.tsx` (referencia de migración a Shadcn)

### Componentes Shadcn Disponibles
- `Button`, `Card`, `Table`, `Select`, `Input`, `Textarea`, `Dialog`, `Tooltip`, `Alert`, `Skeleton`

---

## 8. Estimación de Esfuerzo

- **Backend**: 4-6 horas
  - Crear routers: 2 horas
  - Ajustar filtros y autenticación: 1-2 horas
  - Testing: 1-2 horas

- **Frontend - Servicios**: 1-2 horas
  - Crear servicios: 1 hora
  - Testing: 1 hora

- **Frontend - Componentes**: 12-16 horas
  - InterviewTemplatesManagement: 4-5 horas
  - InterviewTemplateEditor: 6-8 horas
  - InterviewsPage: 2-3 horas

- **Testing y Refinamiento**: 4-6 horas

**Total estimado**: 21-30 horas

---

## 9. Notas Finales

- Los componentes actuales de admin **NO usan Shadcn**, por lo que la migración será completa
- Se puede usar `CandidatesListPage.tsx` como referencia de cómo migrar a Shadcn
- Los endpoints de admin están bien estructurados y pueden reutilizarse casi directamente
- El filtrado por `company_id` es crítico para la seguridad y privacidad de datos

