# Análisis de Requerimientos: interview-system2.md

> **Fecha de Análisis**: Enero 2025  
> **Documento Analizado**: `intreview-system2.md`  
> **Estado del Sistema**: Backend completo según `interview-system-final-summary.md`

---

## 📋 Resumen Ejecutivo

Este documento analiza los requerimientos propuestos en `interview-system2.md` y los compara con el estado actual del sistema de entrevistas. El documento propone cambios significativos en:

1. **Estructura de Enums**: Separación entre proceso del candidato y tipo de entrevista
2. **Campos Obligatorios/Opcionales**: Nuevos requisitos para la entidad Interview
3. **Mejoras de UI**: Rediseño completo del listado de entrevistas
4. **Funcionalidades de Calendario**: Integración de calendario y gestión de fechas
5. **Asignación de Entrevistadores**: Mejoras en la gestión de entrevistadores

---

## 🔍 Análisis Detallado por Sección

### 1. Cambios en Enums

#### 1.1. Propuesta: InterviewProcessTypeEnum (NUEVO)

**Requerimiento:**
```python
InterviewProcessTypeEnum:
* CANDIDATE_SIGN_UP
* CANDIDATE_APPLICATION
* SCREENING
* INTERVIEW
* FEEDBACK (Final)
```

**Estado Actual:**
- ❌ **NO EXISTE** `InterviewProcessTypeEnum` (Crear)
- ✅ Existe `WorkflowStage` que podría relacionarse con procesos (descartado)
- ✅ Existe `Phase` en el sistema de workflows pero es diferente concepto (descartado)

**Análisis:**
- El concepto de "proceso" en el documento se refiere al **momento del proceso de selección** en que se realiza la entrevista
- Actualmente esto se maneja indirectamente a través de `workflow_stage_id`
- La propuesta introduce un concepto más explícito y claro
- ⚠️ **IMPORTANTE**: Se usa "proceso" en lugar de "fase" para evitar confusión con los conceptos existentes de `Phase` y `Workflow` en el sistema

**Recomendación:**
- ✅ **CREAR** `InterviewProcessTypeEnum` en `src/interview_bc/interview/domain/enums/interview_enums.py`
- Agregar campo `process_type: Optional[InterviewProcessTypeEnum]` a la entidad `Interview`
- Considerar migración de datos existentes basándose en `workflow_stage_id` o `interview_type` actual

---

#### 1.2. Propuesta: InterviewTypeEnum (MODIFICAR)

**Requerimiento:**
```python
InterviewTypeEnum:
* CUSTOM
* TECHNICAL
* BEHAVIORAL
* CULTURAL_FIT
* KNOWLEDGE_CHECK
* EXPERIENCE_CHECK
```

**Estado Actual:**
```python
# src/interview_bc/interview/domain/enums/interview_enums.py
class InterviewTypeEnum(Enum):
    EXTENDED_PROFILE = "EXTENDED_PROFILE"
    POSITION_INTERVIEW = "POSITION_INTERVIEW"
    CUSTOM = "CUSTOM"
    TECHNICAL = "TECHNICAL"
    BEHAVIORAL = "BEHAVIORAL"
    CULTURAL_FIT = "CULTURAL_FIT"
```

**Análisis:**
- ✅ Ya existen: `CUSTOM`, `TECHNICAL`, `BEHAVIORAL`, `CULTURAL_FIT`
- ❌ **FALTAN**: `KNOWLEDGE_CHECK`, `EXPERIENCE_CHECK`
- ⚠️ **DEPRECADOS**: `EXTENDED_PROFILE`, `POSITION_INTERVIEW` (según propuesta, estos deberían ser `process_type`)

**Recomendación:**
- ✅ Agregar `KNOWLEDGE_CHECK` y `EXPERIENCE_CHECK` a `InterviewTypeEnum`
- ⚠️ Mantener `EXTENDED_PROFILE` y `POSITION_INTERVIEW` como deprecated para compatibilidad
- 📝 Documentar que estos valores legacy deben migrarse a `process_type` en el futuro
- Considerar script de migración para convertir valores antiguos

---

### 2. Campos Obligatorios y Opcionales

#### 2.1. Requerimientos Propuestos

**Obligatorios:**
- ✅ `CandidateId` - **YA IMPLEMENTADO**
- ❌ `Lista de CompanyRole` - **NO IMPLEMENTADO**

**Opcionales:**
- ❌ `Lista de CompanyUserId` - **PARCIALMENTE IMPLEMENTADO**

**Estado Actual:**

```python
# src/interview_bc/interview/domain/entities/interview.py
@dataclass
class Interview:
    id: InterviewId
    candidate_id: CandidateId  # ✅ OBLIGATORIO
    # ... otros campos ...
    interviewers: List[str] = field(default_factory=list)  # ⚠️ Solo nombres, no roles
```

**Sistema de Entrevistadores Actual:**
- ✅ Existe `InterviewInterviewer` que relaciona `user_id` con `interview_id`
- ✅ Permite entrevistadores externos con rol `GUEST`
- ❌ **NO** hay campo para "lista de roles" obligatoria
- ⚠️ `interviewers` es `List[str]` (nombres), no roles ni IDs

**Sistema de CompanyRole:**
- ✅ Existe entidad `CompanyRole` en `src/company_bc/company_role/domain/entities/company_role.py`
- ✅ Los `CompanyRole` son roles personalizados de la compañía (ej: "Technical Lead", "HR Manager")
- ✅ Los usuarios pueden tener múltiples `CompanyRole` a través de `CompanyUserCompanyRoleModel`
- ❌ **NO** hay relación entre `Interview` y `CompanyRole`

**Análisis:**
- El requerimiento de "Lista de Roles" se refiere a **`CompanyRole`** (roles personalizados de la compañía)
- Una entrevista debe especificar qué roles de la compañía deben participar (ej: requiere un "Technical Lead" y un "HR Manager")
- Esto permite definir qué tipos de entrevistadores se necesitan sin especificar usuarios concretos
- Los usuarios asignados (`CompanyUserId`) deben tener al menos uno de los `CompanyRole` requeridos

**Análisis de Implementación: Tabla vs JSON**

**Caso de Uso Específico:**
- El listado debe mostrar si para cada role requerido se ha asignado una persona
- Necesitamos saber qué roles están requeridos y cuáles tienen entrevistador asignado
- Los roles son IDs de `CompanyRole` (entidad existente)

**Opción 1: Tabla de Relación Many-to-Many (`interview_company_roles`)**

**Ventajas:**
- ✅ Integridad referencial: Foreign keys garantizan que los roles existan
- ✅ Queries eficientes: Fácil filtrar entrevistas por role específico
- ✅ Escalabilidad: Índices en `company_role_id` para búsquedas rápidas
- ✅ Normalización: Estructura clara y mantenible
- ✅ Validaciones a nivel de BD: Unique constraint para evitar duplicados

**Desventajas:**
- ❌ Complejidad adicional: Nueva tabla y relaciones
- ❌ Más queries JOIN: Para obtener roles de una entrevista
- ❌ Overhead de mantenimiento: Migraciones más complejas

**Opción 2: Campo JSON (`required_roles: List[str]`)**

**Ventajas:**
- ✅ Simplicidad: Un solo campo en la tabla `interviews`
- ✅ Menos queries: Los roles vienen con la entrevista directamente
- ✅ Menos overhead: No hay tabla adicional ni relaciones
- ✅ Patrón existente: Ya se usa JSON para `interviewers: List[str]` en el mismo modelo

**Desventajas:**
- ❌ Sin integridad referencial: No garantiza que los roles existan
- ❌ Queries complejas: Filtrar por role requiere operaciones JSON (menos eficiente)
- ❌ Sin índices directos: PostgreSQL tiene soporte JSON pero menos eficiente que índices normales
- ❌ Validación manual: Debe hacerse en aplicación, no en BD

**Análisis de Requerimientos:**

1. **Filtrado por Role:**
   - Según `interview-system2.md`, se necesita filtro por role en el listado
   - Con JSON: `WHERE required_roles @> '["role_id"]'` (funciona pero menos eficiente)
   - Con tabla: `JOIN interview_company_roles WHERE company_role_id = ?` (más eficiente)

2. **Volumen de Datos:**
   - Típicamente una entrevista tendrá 1-5 roles requeridos
   - JSON es adecuado para este volumen pequeño
   - Tabla es más adecuada si se esperan muchos roles o queries frecuentes

3. **Integridad Referencial:**
   - Si un `CompanyRole` se elimina, ¿qué pasa con las entrevistas que lo requieren?
   - Con tabla: Puede usar `ON DELETE SET NULL` o `CASCADE`
   - Con JSON: No hay protección automática, requiere validación manual

4. **Caso de Uso Específico: "Determinar si para cada role hemos asignado una persona":**
   - Necesitamos cruzar: `required_roles` (de Interview) con `InterviewInterviewer` (usuarios asignados)
   - Con JSON: Query más compleja, requiere unir con `CompanyUserCompanyRole` para ver roles de usuarios
   - Con tabla: JOIN más directo: `interview_company_roles` ↔ `company_user_company_roles` ↔ `interview_interviewers`

5. **Patrón Existente en el Código:**
   - Ya existe `interviewers: List[str]` como JSON (nombres de entrevistadores)
   - Esto sugiere que el equipo está cómodo con JSON para listas simples
   - Sin embargo, `interviewers` es solo metadata, mientras que `required_roles` necesita validación y queries

**Decisión Recomendada: JSON (con justificación)**

**Justificación:**
1. **Volumen pequeño**: Típicamente 1-5 roles por entrevista, JSON es adecuado
2. **Patrón existente**: Ya se usa JSON para `interviewers` en el mismo modelo
3. **Simplicidad**: Menos complejidad de infraestructura
4. **Rendimiento aceptable**: Para el volumen esperado, las queries JSON de PostgreSQL son suficientes
5. **Validación en aplicación**: Ya tenemos validaciones en domain layer, podemos validar que los roles existan

**Implementación Recomendada:**
- ✅ Campo `required_roles: List[str]` como JSON en `InterviewModel`
- ✅ Validación en domain layer: Verificar que todos los `CompanyRoleId` existan
- ✅ Índice GIN en PostgreSQL para `required_roles` si se necesita filtrar frecuentemente
- ✅ Query helper en repositorio para filtrar por role usando operadores JSON de PostgreSQL

**Recomendación:**
- ✅ Usar campo JSON `required_roles: List[CompanyRoleId]` en lugar de tabla de relación
- ✅ Agregar validación en creación que la lista no esté vacía (obligatorio)
- ✅ Validar al asignar entrevistadores que tengan al menos uno de los roles requeridos
- ✅ Considerar índice GIN si las queries por role son frecuentes
- Para `Lista de CompanyUserId` opcional:
  - Ya existe a través de `InterviewInterviewer` (relación entrevista-usuario)
  - Mejorar para permitir asignación directa de usuarios de la compañía
  - Validar que los usuarios asignados tengan al menos uno de los `CompanyRole` requeridos

---

### 3. Mejoras en el Listado de Entrevistas

#### 3.1. Rediseño de Cabecera

**Requerimientos:**

**Izquierda - Métricas con Links:**
- Pendientes de planificar (sin fecha o sin entrevistador asignado)
- Planificadas (con fecha y entrevistador)
- En proceso (fecha = hoy)
- Finalizadas recientes (últimos 30 días)
- Pasadas fecha límite (nombre pendiente)
- Pendiente de feedback o scoring

**Derecha - Calendario:**
- Mostrar calendario
- Indicar número de entrevistas por día
- Link para filtrar por día

**Estado Actual:**
- ✅ **LISTADO BÁSICO IMPLEMENTADO**: Existe `CompanyInterviewsPage.tsx` en `/company/interviews`
- ✅ Backend tiene endpoints para listar entrevistas
- ✅ Backend tiene filtros básicos
- ✅ Frontend tiene listado funcional con tabla, paginación y filtros básicos (status, type)
- ❌ **REDISEÑO NO IMPLEMENTADO**: Las mejoras propuestas (cabecera con métricas, calendario, filtros avanzados) no están implementadas

**Análisis:**
- El listado actual funciona pero no tiene las mejoras propuestas en `interview-system2.md`
- Para implementar el rediseño, backend necesita endpoints/queries adicionales para:
  - Contar entrevistas por estado/categoría (métricas de cabecera)
  - Obtener entrevistas por rango de fechas (para calendario)
  - Obtener entrevistas agrupadas por día (para calendario)
  - Detectar entrevistas pasadas fecha límite
  - Detectar entrevistas sin fecha o sin entrevistador asignado

**Recomendación:**
- Crear queries específicas:
  - `GetInterviewStatisticsQuery` - Para métricas de la cabecera
  - `GetInterviewsByDateRangeQuery` - Para calendario
  - `GetOverdueInterviewsQuery` - Para entrevistas pasadas fecha límite
- Implementar en frontend con shadcn/ui components

---

#### 3.2. Filtros Propuestos

**Requerimientos:**
- Búsqueda por nombre de persona
- Filtro por `InterviewProcessTypeEnum`
- Filtro por `InterviewTypeEnum`
- Filtro por `InterviewStatusEnum`
- Filtro por fecha o rango de fechas
- Filtro por `JobPosition` (activos + terminados últimos 30 días)
- Filtro por Entrevistador

**Estado Actual:**
- ✅ **FILTROS BÁSICOS IMPLEMENTADOS**: Status e InterviewType funcionan en `CompanyInterviewsPage.tsx`
- ✅ Backend tiene algunos filtros básicos
- ❌ **FILTROS AVANZADOS NO IMPLEMENTADOS**: Faltan los filtros propuestos
- ❌ No hay búsqueda por nombre de candidato
- ❌ No hay filtro por `InterviewProcessTypeEnum` (no existe aún)
- ❌ No hay filtro por fecha/rango de fechas
- ❌ No hay filtro por JobPosition
- ❌ No hay filtro por Entrevistador

**Recomendación:**
- Crear `ListInterviewsQuery` con todos los filtros
- Agregar búsqueda por nombre de candidato (join con tabla candidates)
- Implementar filtros en frontend con componentes shadcn/ui

---

#### 3.3. Funcionalidades de Fecha

**Requerimientos:**
- Fecha de calendario (ya existe `scheduled_at`)
- Fecha límite opcional (nueva)
- Click en fecha N/A para mostrar calendario
- Click en fecha existente para editar
- Especificar hora también

**Estado Actual:**
```python
# Entidad Interview
scheduled_at: Optional[datetime] = None  # ✅ Existe
# ❌ NO existe deadline_date o similar
```

**Análisis:**
- ✅ `scheduled_at` ya existe y puede incluir hora
- ❌ Falta campo `deadline_date` (fecha límite opcional)
- ⚠️ Frontend necesita componente de calendario mejorado

**Recomendación:**
- Agregar campo `deadline_date: Optional[datetime]` a `Interview`
- Crear migración para agregar columna
- Actualizar DTOs y schemas
- Implementar componente de calendario en frontend con selección de fecha y hora

---

#### 3.4. Mejoras en Columnas del Listado

**Requerimientos:**
- Fusionar columnas "Entrevista" y "Tipo" en una sola
- Mostrar tipo en tamaño más pequeño (9-10pt) debajo del nombre
- Mostrar persona asignada (entrevistador) o role si no hay
- Click para asignar entrevistador
- Popup para asignar (múltiples, al menos uno por role)
- Componente reutilizable para asignación

**Estado Actual:**
- ✅ **LISTADO BÁSICO IMPLEMENTADO**: `CompanyInterviewsPage.tsx` muestra columnas básicas
- ✅ Backend tiene sistema de entrevistadores (`InterviewInterviewer`)
- ✅ Backend tiene endpoints para invitar entrevistadores
- ❌ **MEJORAS PROPUESTAS NO IMPLEMENTADAS**: 
  - Columnas "Entrevista" y "Tipo" no están fusionadas
  - No se muestra persona asignada o role
  - No hay click para asignar entrevistador
  - No hay componente reutilizable de asignación

**Recomendación:**
- Crear componente `InterviewerAssignmentDialog` reutilizable
- Implementar en frontend con shadcn/ui
- Usar endpoints existentes de invitación de entrevistadores

---

#### 3.5. Modificaciones en Pantallas de Crear y Editar Entrevistas

**Requerimientos según `interview-system2.md`:**
- Campo obligatorio: Lista de `CompanyRole` (required_roles)
- Campo opcional: Lista de `CompanyUserId` (entrevistadores asignados)
- Campo opcional: `deadline_date` (fecha límite)
- Actualizar tipos de entrevista según nuevos enums
- Agregar `process_type` (InterviewProcessTypeEnum)

**Estado Actual:**

**CreateInterviewPage.tsx (`/company/interviews/create`):**
- ✅ Existe pantalla de creación
- ✅ Campos actuales:
  - `candidate_id` (obligatorio)
  - `interview_type` (select con valores: POSITION_INTERVIEW, RESUME_ENHANCEMENT, TECHNICAL, BEHAVIORAL, CULTURAL_FIT)
  - `interview_mode` (AUTOMATIC, AI, MANUAL)
  - `job_position_id` (opcional)
  - `interview_template_id` (opcional)
  - `title` (opcional)
  - `description` (opcional)
  - `scheduled_at` (opcional, datetime-local)
  - `interviewers` (opcional, lista de nombres como strings)
- ❌ **FALTA**: Campo obligatorio `required_roles` (Lista de CompanyRole)
- ❌ **FALTA**: Campo opcional `deadline_date`
- ❌ **FALTA**: Campo `process_type` (InterviewProcessTypeEnum)
- ❌ **FALTA**: Actualizar `interview_type` con nuevos valores (KNOWLEDGE_CHECK, EXPERIENCE_CHECK)
- ❌ **FALTA**: Eliminar valores deprecated (EXTENDED_PROFILE, POSITION_INTERVIEW)
- ⚠️ **MEJORAR**: `interviewers` debería ser lista de `CompanyUserId` en lugar de nombres

**EditInterviewPage.tsx (`/company/interviews/{id}/edit`):**
- ✅ Existe pantalla de edición
- ✅ Campos actuales editables:
  - `title` (opcional)
  - `description` (opcional)
  - `scheduled_at` (opcional, datetime-local)
  - `interviewers` (opcional, lista de nombres como strings)
- ❌ **FALTA**: Campo `required_roles` (editable)
- ❌ **FALTA**: Campo `deadline_date` (editable)
- ❌ **FALTA**: Campo `process_type` (editable)
- ⚠️ **MEJORAR**: `interviewers` debería ser lista de `CompanyUserId` en lugar de nombres

**Análisis:**
- Las pantallas actuales no reflejan los nuevos requerimientos del documento
- Necesitan actualización significativa para incluir los nuevos campos obligatorios
- El campo `required_roles` es crítico ya que es obligatorio según los requerimientos
- La asignación de entrevistadores necesita cambiar de nombres (strings) a usuarios reales (CompanyUserId)

**Recomendación:**
- Actualizar `CreateInterviewPage.tsx`:
  - Agregar selector múltiple para `required_roles` (obligatorio, lista de CompanyRole)
  - Agregar campo `deadline_date` (opcional, datetime-local)
  - Agregar selector para `process_type` (InterviewProcessTypeEnum)
  - Actualizar selector de `interview_type` con nuevos valores y eliminar deprecated
  - Reemplazar `interviewers` (nombres) por selector de usuarios de la compañía (CompanyUserId)
  - Validar que `required_roles` no esté vacío antes de enviar
- Actualizar `EditInterviewPage.tsx`:
  - Agregar campos editables: `required_roles`, `deadline_date`, `process_type`
  - Reemplazar `interviewers` (nombres) por selector de usuarios de la compañía
  - Mostrar valores actuales de todos los campos
- Crear componente reutilizable `CompanyRoleSelector` para selección múltiple de roles
- Crear componente reutilizable `CompanyUserSelector` para selección múltiple de usuarios
- Validar que los usuarios seleccionados tengan al menos uno de los roles requeridos

---

## 📊 Matriz de Estado de Implementación

| Requerimiento | Estado Backend | Estado Frontend | Prioridad |
|--------------|---------------|-----------------|-----------|
| **InterviewProcessTypeEnum** | ❌ No existe | ❌ N/A | 🔴 Alta |
| **InterviewTypeEnum** (KNOWLEDGE_CHECK, EXPERIENCE_CHECK) | ⚠️ Parcial | ❌ N/A | 🟡 Media |
| **Lista de CompanyRole obligatoria** | ❌ No existe | ❌ N/A | 🔴 Alta |
| **Lista de CompanyUserId opcional** | ✅ Existe (InterviewInterviewer) | ⚠️ Parcial | 🟢 Baja |
| **deadline_date** | ❌ No existe | ❌ N/A | 🟡 Media |
| **Rediseño cabecera listado** | ⚠️ Parcial (faltan queries) | ⚠️ Listado básico existe, rediseño no | 🔴 Alta |
| **Calendario en cabecera** | ⚠️ Parcial (faltan queries) | ❌ No existe | 🔴 Alta |
| **Filtros avanzados** | ⚠️ Parcial | ⚠️ Filtros básicos existen, avanzados no | 🟡 Media |
| **Búsqueda por nombre** | ❌ No existe | ❌ N/A | 🟡 Media |
| **Click en fecha para calendario** | ✅ Existe (scheduled_at) | ❌ No existe | 🟡 Media |
| **Asignación de entrevistadores** | ✅ Existe | ⚠️ Parcial | 🟡 Media |
| **Componente reutilizable asignación** | N/A | ❌ No existe | 🟢 Baja |

---

## 🎯 Plan de Acción Recomendado

### ⚠️ PREPARACIÓN: Limpieza de Datos

**ANTES DE COMENZAR LA IMPLEMENTACIÓN:**
- [ ] **ELIMINAR TODOS LOS DATOS DE ENTREVISTAS** de la base de datos
- [ ] Esto incluye:
  - Tabla `interviews`
  - Tabla `interview_answers`
  - Tabla `interview_interviewers`
  - Cualquier otra tabla relacionada con entrevistas
- [ ] Estamos en fase de desarrollo, no hay datos de producción que preservar
- [ ] Esto permite implementar cambios sin preocuparse por compatibilidad hacia atrás
- [ ] Los cambios en enums y estructura pueden hacerse directamente sin mantener valores deprecated

### Fase 1: Domain Layer (Backend - Crítico)

#### 1.1. Crear InterviewProcessTypeEnum
- [ ] Crear enum en `src/interview_bc/interview/domain/enums/interview_enums.py`
- [ ] Agregar valores: `CANDIDATE_SIGN_UP`, `CANDIDATE_APPLICATION`, `SCREENING`, `INTERVIEW`, `FEEDBACK`
- [ ] Agregar campo `process_type: Optional[InterviewProcessTypeEnum]` a entidad `Interview`
- [ ] Actualizar factory method `create()`

#### 1.2. Actualizar InterviewTypeEnum
- [ ] Agregar `KNOWLEDGE_CHECK` y `EXPERIENCE_CHECK`
- [ ] Eliminar `EXTENDED_PROFILE` y `POSITION_INTERVIEW` (no son necesarios, estamos en desarrollo)
- [ ] Estos valores pueden eliminarse directamente ya que no hay datos de producción

#### 1.3. Agregar deadline_date
- [ ] Agregar campo `deadline_date: Optional[datetime]` a entidad `Interview`
- [ ] Agregar método `set_deadline()` si es necesario
- [ ] Crear migración

#### 1.4. Implementar "Lista de CompanyRole" Obligatoria
- [ ] Agregar campo `required_roles: List[CompanyRoleId]` como JSON a entidad `Interview`
- [ ] Agregar campo `required_roles: List[str]` como JSON a `InterviewModel`
- [ ] Validar en creación que la lista no esté vacía (obligatorio)
- [ ] Validar en domain layer que todos los `CompanyRoleId` existan (consultar repositorio)
- [ ] Crear método de dominio para validar que usuarios asignados tengan roles requeridos
- [ ] Considerar índice GIN en PostgreSQL para `required_roles` si se necesita filtrar frecuentemente

### Fase 2: Infrastructure Layer (Backend)

- [ ] Actualizar `InterviewModel` con nuevos campos
- [ ] Actualizar `InterviewRepository` con mapeos
- [ ] Crear migraciones para:
  - `process_type` (enum + columna)
  - `deadline_date` (columna)
  - `required_roles` (columna JSON)
  - Índice GIN opcional para `required_roles` si se necesita filtrar frecuentemente

### Fase 3: Application Layer (Backend)

#### 3.1. Queries para Listado Mejorado
- [ ] `GetInterviewStatisticsQuery` - Métricas de cabecera
- [ ] `GetInterviewsByDateRangeQuery` - Para calendario
- [ ] `GetOverdueInterviewsQuery` - Entrevistas pasadas fecha límite
- [ ] `ListInterviewsQuery` mejorado con todos los filtros
- [ ] Búsqueda por nombre de candidato
- [ ] Filtro por `CompanyRole` usando operadores JSON de PostgreSQL (`@>` o `?|`)

#### 3.2. Commands
- [ ] Actualizar `CreateInterviewCommand` con `required_roles: List[CompanyRoleId]` (obligatorio)
- [ ] `UpdateInterviewDeadlineCommand` (si es necesario)
- [ ] `UpdateInterviewRequiredRolesCommand` para actualizar roles requeridos
- [ ] Validar en `InviteInterviewerCommand` que el usuario tenga al menos uno de los roles requeridos

### Fase 4: Presentation Layer (Backend)

- [ ] Actualizar DTOs con nuevos campos
- [ ] Actualizar schemas de request/response
- [ ] Crear endpoints para estadísticas
- [ ] Crear endpoints para calendario
- [ ] Actualizar endpoints existentes

### Fase 5: Frontend (UI)

#### 5.1. Rediseño de Listado
- [ ] Implementar nueva cabecera con métricas
- [ ] Implementar calendario en cabecera
- [ ] Implementar filtros avanzados
- [ ] Mejorar columnas del listado

#### 5.2. Modificaciones en Pantallas de Crear/Editar
- [ ] Actualizar `CreateInterviewPage.tsx`:
  - [ ] Agregar selector múltiple para `required_roles` (obligatorio)
  - [ ] Agregar campo `deadline_date` (opcional)
  - [ ] Agregar selector para `process_type`
  - [ ] Actualizar selector de `interview_type` con nuevos valores
  - [ ] Reemplazar `interviewers` (nombres) por selector de usuarios
  - [ ] Validar que `required_roles` no esté vacío
- [ ] Actualizar `EditInterviewPage.tsx`:
  - [ ] Agregar campos editables: `required_roles`, `deadline_date`, `process_type`
  - [ ] Reemplazar `interviewers` (nombres) por selector de usuarios
  - [ ] Mostrar valores actuales de todos los campos
- [ ] Crear componente `CompanyRoleSelector` (selección múltiple)
- [ ] Crear componente `CompanyUserSelector` (selección múltiple)
- [ ] Validar que usuarios seleccionados tengan roles requeridos

#### 5.3. Componentes Reutilizables
- [ ] `InterviewerAssignmentDialog` component
- [ ] `InterviewCalendar` component
- [ ] `InterviewFilters` component
- [ ] `CompanyRoleSelector` component
- [ ] `CompanyUserSelector` component

#### 5.4. Funcionalidades de Fecha
- [ ] Click en fecha N/A para mostrar calendario
- [ ] Click en fecha existente para editar
- [ ] Selector de fecha y hora mejorado

---

## ⚠️ Puntos de Atención

### 1. Estado del Proyecto: Fase de Desarrollo
- ⚠️ **IMPORTANTE**: Estamos en fase de desarrollo
- ✅ **Eliminar todos los datos de entrevistas antes de comenzar la implementación**
- Esto permite implementar cambios sin preocuparse por compatibilidad hacia atrás
- No es necesario mantener valores deprecated ni scripts de migración complejos
- Los cambios en enums y estructura pueden hacerse directamente

### 2. Compatibilidad hacia atrás (No aplicable en desarrollo)
- ~~Los cambios en enums pueden afectar datos existentes~~ → **No aplicable: datos eliminados**
- ~~Necesario script de migración para convertir valores antiguos~~ → **No necesario**
- ~~Considerar mantener valores deprecated temporalmente~~ → **No necesario**

### 2. Clarificación de Requerimientos
- ✅ **"Lista de Roles"** aclarado: Se refiere a `CompanyRole` (roles personalizados de la compañía)
- **"Pasadas fecha límite"** necesita nombre apropiado (sugerencia: "OVERDUE" o "VENCIDAS")

### 3. Performance
- Las queries de estadísticas y calendario pueden ser costosas
- Considerar índices en base de datos
- Considerar caché para métricas frecuentes

### 4. UX/UI
- El rediseño propuesto es significativo
- Requiere validación con usuarios
- Considerar implementación gradual

---

## 📝 Notas Técnicas

### Relación con Sistema Actual

**Workflow Stages vs Interview Process:**
- Actualmente las entrevistas se relacionan con `workflow_stage_id`
- La propuesta de `InterviewProcessTypeEnum` representa el **momento del proceso de selección** en que se realiza la entrevista
- Es un concepto diferente a `Phase` y `WorkflowStage` del sistema de workflows
- Necesario definir cómo se relacionan ambos conceptos

**Entrevistadores y Roles:**
- Sistema actual usa `InterviewInterviewer` (relación entrevista-usuario)
- Campo `interviewers: List[str]` (nombres) parece legacy
- Recomendación: Migrar completamente a `InterviewInterviewer` y deprecar `interviewers`
- **Nuevo requerimiento**: Campo obligatorio `required_roles` en `Interview` (lista de `CompanyRoleId`)
- Los `CompanyRole` son roles personalizados de la compañía (ej: "Technical Lead", "HR Manager")
- Los usuarios (`CompanyUser`) pueden tener múltiples `CompanyRole` a través de `CompanyUserCompanyRoleModel`
- La validación debe asegurar que los entrevistadores asignados tengan al menos uno de los roles requeridos

**Decisión de Implementación: JSON vs Tabla para `required_roles`:**
- ✅ **Decisión**: Usar campo JSON `required_roles: List[str]` en lugar de tabla de relación
- **Justificación**: 
  - Volumen pequeño (1-5 roles típicamente)
  - Patrón existente en el código (`interviewers` ya usa JSON)
  - Simplicidad de implementación
  - Rendimiento aceptable con índices GIN si es necesario
- **Validación**: Se hace en domain layer verificando que todos los `CompanyRoleId` existan
- **Queries**: Usar operadores JSON de PostgreSQL (`@>` para contiene, `?|` para cualquier elemento)
- **Índices**: Considerar índice GIN si las queries por role son frecuentes

### Arquitectura

**Siguiendo las reglas del proyecto:**
- ✅ Domain Layer primero (enums, entidades)
- ✅ Infrastructure Layer segundo (modelos, repositorios, migraciones)
- ✅ Application & Presentation Layer tercero (commands, queries, endpoints)
- ✅ Frontend al final

---

## 🔗 Referencias

- `docs/interview-system.md` - Especificación original del sistema
- `docs/interview-system-final-summary.md` - Resumen de implementación actual
- `docs/interview-system-implementation-summary.md` - Detalles de implementación
- `docs/interview-validations-execution.md` - Validaciones implementadas
- `src/interview_bc/interview/domain/enums/interview_enums.py` - Enums actuales
- `src/interview_bc/interview/domain/entities/interview.py` - Entidad actual

---

## ✅ Checklist de Implementación

### Backend - Domain Layer
- [x] Crear `InterviewProcessTypeEnum`
- [x] Actualizar `InterviewTypeEnum` (agregar KNOWLEDGE_CHECK, EXPERIENCE_CHECK)
- [x] Agregar `process_type` a `Interview`
- [x] Agregar `deadline_date` a `Interview`
- [x] Agregar `required_roles: List[CompanyRoleId]` a `Interview` (obligatorio, JSON)
- [x] Crear métodos de validación para roles requeridos
- [x] Validar que todos los `CompanyRoleId` existan al crear/actualizar
- [x] Agregar `interview_mode` a `update_details` de la entidad

### Backend - Infrastructure Layer
- [x] Actualizar `InterviewModel`
- [x] Crear migraciones (cambiar enums a VARCHAR, agregar JSONB para required_roles)
- [x] Actualizar repositorio con nuevos filtros
- [x] Implementar `count_by_filters` para paginación
- [x] Implementar filtro por `candidate_name` con JOIN

### Backend - Application Layer
- [x] Crear queries para estadísticas (`GetInterviewStatisticsQuery`)
- [x] Crear queries para calendario (`GetInterviewsByDateRangeQuery`)
- [x] Crear queries para entrevistas vencidas (`GetOverdueInterviewsQuery`)
- [x] Mejorar `ListInterviewsQuery` con filtros avanzados
- [x] Actualizar `CreateInterviewCommand` con nuevos campos
- [x] Crear `UpdateInterviewCommand` y handler
- [x] Actualizar `InviteInterviewerCommand` para validar roles requeridos

### Backend - Presentation Layer
- [x] Actualizar DTOs (`InterviewDto`, `InterviewStatisticsDto`)
- [x] Actualizar schemas (`InterviewCreateRequest`, `InterviewUpdateRequest`, `InterviewManagementResponse`)
- [x] Crear endpoints nuevos (statistics, calendar, overdue)
- [x] Actualizar endpoints existentes (list, create, update)
- [x] Implementar paginación correcta con total count

### Frontend
- [x] Rediseño de cabecera con métricas interactivas
- [x] Calendario en cabecera
- [x] Filtros avanzados (candidate_name, process_type, required_role_id, etc.)
- [x] Actualizar `CreateInterviewPage` con nuevos campos
- [x] Actualizar `EditInterviewPage` con nuevos campos
- [x] Mejoras en columnas de tabla (Asignado, Fecha Límite)
- [x] Validación frontend: usuarios seleccionados deben tener roles requeridos

---

**Próximos Pasos:**
1. ⚠️ **ELIMINAR TODOS LOS DATOS DE ENTREVISTAS** antes de comenzar (estamos en fase de desarrollo)
2. Revisar este análisis con el equipo
3. Aclarar requerimientos ambiguos (especialmente "Lista de Roles") - ✅ Ya aclarado: CompanyRole
4. Priorizar tareas según necesidades del negocio
5. Comenzar implementación siguiendo el orden de fases

