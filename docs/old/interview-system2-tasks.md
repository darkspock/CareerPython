# Lista de Tareas: Implementación de Requerimientos interview-system2.md

> **Fecha de Creación**: Enero 2025  
> **Basado en**: `interview-system2-analysis.md`  
> **Estado**: Pendiente de implementación

---

## ⚠️ PREPARACIÓN: Limpieza de Datos

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

---

## Fase 1: Domain Layer (Backend - Crítico)

### 1.1. Crear InterviewProcessTypeEnum

- [ ] Crear enum en `src/interview_bc/interview/domain/enums/interview_enums.py`
- [ ] Agregar valores: `CANDIDATE_SIGN_UP`, `CANDIDATE_APPLICATION`, `SCREENING`, `INTERVIEW`, `FEEDBACK`
- [ ] Agregar campo `process_type: Optional[InterviewProcessTypeEnum]` a entidad `Interview`
- [ ] Actualizar factory method `create()` para incluir `process_type`

### 1.2. Actualizar InterviewTypeEnum

- [ ] Agregar `KNOWLEDGE_CHECK` y `EXPERIENCE_CHECK` a `InterviewTypeEnum`
- [ ] Eliminar `EXTENDED_PROFILE` y `POSITION_INTERVIEW` (no son necesarios, estamos en desarrollo)
- [ ] Estos valores pueden eliminarse directamente ya que no hay datos de producción
- [ ] Actualizar todos los lugares donde se usan estos valores deprecated

### 1.3. Agregar deadline_date

- [ ] Agregar campo `deadline_date: Optional[datetime]` a entidad `Interview`
- [ ] Agregar método `set_deadline()` si es necesario
- [ ] Actualizar factory method `create()` para incluir `deadline_date`

### 1.4. Implementar "Lista de CompanyRole" Obligatoria

- [ ] Agregar campo `required_roles: List[CompanyRoleId]` como JSON a entidad `Interview`
- [ ] Validar en creación que la lista no esté vacía (obligatorio)
- [ ] Validar en domain layer que todos los `CompanyRoleId` existan (consultar repositorio)
- [ ] Crear método de dominio para validar que usuarios asignados tengan roles requeridos
- [ ] Actualizar factory method `create()` para incluir `required_roles` (obligatorio)

---

## Fase 2: Infrastructure Layer (Backend)

### 2.1. Actualizar InterviewModel

- [ ] Agregar campo `process_type` a `InterviewModel` (enum)
- [ ] Agregar campo `deadline_date` a `InterviewModel` (DateTime, nullable)
- [ ] Agregar campo `required_roles` a `InterviewModel` (JSON, List[str])
- [ ] Actualizar relaciones si es necesario

### 2.2. Actualizar InterviewRepository

- [ ] Actualizar método `_to_domain()` para mapear nuevos campos
- [ ] Actualizar método `_to_model()` para mapear nuevos campos
- [ ] Agregar validación de `required_roles` en queries si es necesario

### 2.3. Crear Migraciones

- [ ] Crear migración para agregar `process_type` (enum + columna)
- [ ] Crear migración para agregar `deadline_date` (columna DateTime nullable)
- [ ] Crear migración para agregar `required_roles` (columna JSON)
- [ ] Crear índice GIN opcional para `required_roles` si se necesita filtrar frecuentemente
- [ ] Ejecutar migraciones: `make migrate`

---

## Fase 3: Application Layer (Backend)

### 3.1. Queries para Listado Mejorado

- [ ] Crear `GetInterviewStatisticsQuery` - Para métricas de la cabecera
  - Contar entrevistas pendientes de planificar
  - Contar entrevistas planificadas
  - Contar entrevistas en proceso (fecha = hoy)
  - Contar entrevistas finalizadas recientes (últimos 30 días)
  - Contar entrevistas pasadas fecha límite
  - Contar entrevistas pendientes de feedback o scoring
- [ ] Crear `GetInterviewsByDateRangeQuery` - Para calendario
- [ ] Crear `GetOverdueInterviewsQuery` - Entrevistas pasadas fecha límite
- [ ] Mejorar `ListInterviewsQuery` con todos los filtros:
  - Búsqueda por nombre de candidato
  - Filtro por `InterviewProcessTypeEnum`
  - Filtro por `InterviewTypeEnum`
  - Filtro por `InterviewStatusEnum`
  - Filtro por fecha o rango de fechas
  - Filtro por `JobPosition` (activos + terminados últimos 30 días)
  - Filtro por Entrevistador
  - Filtro por `CompanyRole` usando operadores JSON de PostgreSQL (`@>` o `?|`)

### 3.2. Commands

- [ ] Actualizar `CreateInterviewCommand` con nuevos campos:
  - `required_roles: List[CompanyRoleId]` (obligatorio)
  - `process_type: Optional[InterviewProcessTypeEnum]`
  - `deadline_date: Optional[datetime]`
- [ ] Actualizar `CreateInterviewCommandHandler`:
  - Validar que `required_roles` no esté vacío
  - Validar que todos los `CompanyRoleId` existan
- [ ] Crear `UpdateInterviewDeadlineCommand` (si es necesario)
- [ ] Crear `UpdateInterviewRequiredRolesCommand` para actualizar roles requeridos
- [ ] Actualizar `InviteInterviewerCommand`:
  - Validar que el usuario tenga al menos uno de los roles requeridos de la entrevista

### 3.3. DTOs

- [ ] Actualizar `InterviewDto` con nuevos campos:
  - `required_roles: List[str]`
  - `process_type: Optional[str]`
  - `deadline_date: Optional[datetime]`
- [ ] Actualizar método `from_entity()` en `InterviewDto`

---

## Fase 4: Presentation Layer (Backend)

### 4.1. Schemas

- [ ] Actualizar `InterviewCreateRequest` con nuevos campos:
  - `required_roles: List[str]` (obligatorio)
  - `process_type: Optional[str]`
  - `deadline_date: Optional[str]` (datetime)
- [ ] Actualizar `InterviewUpdateRequest` con nuevos campos editables
- [ ] Actualizar `InterviewManagementResponse` con nuevos campos
- [ ] Agregar validaciones en schemas (required_roles no vacío)

### 4.2. Endpoints

- [ ] Actualizar endpoint `POST /api/company/interviews` para aceptar nuevos campos
- [ ] Actualizar endpoint `PUT /api/company/interviews/{id}` para aceptar nuevos campos
- [ ] Crear endpoint `GET /api/company/interviews/statistics` - Para métricas de cabecera
- [ ] Crear endpoint `GET /api/company/interviews/calendar` - Para calendario
- [ ] Crear endpoint `GET /api/company/interviews/overdue` - Para entrevistas pasadas fecha límite
- [ ] Actualizar endpoint `GET /api/company/interviews` con nuevos filtros

### 4.3. Controllers

- [ ] Actualizar `InterviewController.create()` para manejar nuevos campos
- [ ] Actualizar `InterviewController.update()` para manejar nuevos campos
- [ ] Crear método `InterviewController.get_statistics()`
- [ ] Crear método `InterviewController.get_calendar()`
- [ ] Crear método `InterviewController.get_overdue()`

---

## Fase 5: Frontend (UI)

### 5.1. Rediseño de Listado (CompanyInterviewsPage.tsx)

- [ ] Implementar nueva cabecera con métricas (izquierda):
  - Pendientes de planificar (sin fecha o sin entrevistador asignado) con link a filtro
  - Planificadas (con fecha y entrevistador) con link a filtro
  - En proceso (fecha = hoy) con link a filtro
  - Finalizadas recientes (últimos 30 días) con link a filtro
  - Pasadas fecha límite con link a filtro
  - Pendiente de feedback o scoring con link a filtro
- [ ] Implementar calendario en cabecera (derecha):
  - Mostrar calendario
  - Indicar número de entrevistas por día
  - Link para filtrar por día
- [ ] Implementar filtros avanzados:
  - Búsqueda por nombre de persona
  - Filtro por `InterviewProcessTypeEnum`
  - Filtro por `InterviewTypeEnum`
  - Filtro por `InterviewStatusEnum`
  - Filtro por fecha o rango de fechas
  - Filtro por JobPosition
  - Filtro por Entrevistador
  - Filtro por CompanyRole
- [ ] Mejorar columnas del listado:
  - Fusionar columnas "Entrevista" y "Tipo" en una sola
  - Mostrar tipo en tamaño más pequeño (9-10pt) debajo del nombre
  - Mostrar persona asignada (entrevistador) o role si no hay
  - Click para asignar entrevistador
  - Click en fecha N/A para mostrar calendario
  - Click en fecha existente para editar

### 5.2. Modificaciones en Pantallas de Crear/Editar

#### 5.2.1. CreateInterviewPage.tsx

- [ ] Agregar selector múltiple para `required_roles` (obligatorio, lista de CompanyRole)
- [ ] Agregar campo `deadline_date` (opcional, datetime-local)
- [ ] Agregar selector para `process_type` (InterviewProcessTypeEnum)
- [ ] Actualizar selector de `interview_type`:
  - Agregar nuevos valores: `KNOWLEDGE_CHECK`, `EXPERIENCE_CHECK`
  - Eliminar valores deprecated: `EXTENDED_PROFILE`, `POSITION_INTERVIEW`
- [ ] Reemplazar `interviewers` (nombres como strings) por selector de usuarios de la compañía (CompanyUserId)
- [ ] Validar que `required_roles` no esté vacío antes de enviar
- [ ] Validar que usuarios seleccionados tengan al menos uno de los roles requeridos

#### 5.2.2. EditInterviewPage.tsx

- [ ] Agregar campo editable `required_roles` (selector múltiple de CompanyRole)
- [ ] Agregar campo editable `deadline_date` (datetime-local)
- [ ] Agregar campo editable `process_type` (selector)
- [ ] Reemplazar `interviewers` (nombres) por selector de usuarios de la compañía
- [ ] Mostrar valores actuales de todos los campos nuevos
- [ ] Validar que usuarios seleccionados tengan al menos uno de los roles requeridos

### 5.3. Componentes Reutilizables

- [ ] Crear componente `CompanyRoleSelector`:
  - Selección múltiple de CompanyRole
  - Búsqueda/filtro mientras se escribe
  - Usar shadcn/ui components
- [ ] Crear componente `CompanyUserSelector`:
  - Selección múltiple de usuarios de la compañía
  - Búsqueda/filtro mientras se escribe
  - Botón "Asignar a mi" (asignar usuario actual)
  - Usar shadcn/ui components
- [ ] Crear componente `InterviewerAssignmentDialog`:
  - Popup para asignar entrevistadores
  - Múltiples usuarios, al menos uno por role
  - Mostrar todos los empleados
  - Input para filtrar mientras se escribe
  - Botón "Asignar a mi"
  - Usar componente `CompanyUserSelector`
- [ ] Crear componente `InterviewCalendar`:
  - Calendario con indicador de número de entrevistas por día
  - Click en día para filtrar
  - Usar shadcn/ui components
- [ ] Crear componente `InterviewFilters`:
  - Panel de filtros avanzados
  - Todos los filtros mencionados en requerimientos
  - Usar shadcn/ui components

### 5.4. Funcionalidades de Fecha

- [ ] Mejorar selector de fecha y hora:
  - Permitir especificar hora además de fecha
  - Usar componente datetime-local mejorado
- [ ] Implementar click en fecha N/A para mostrar calendario
- [ ] Implementar click en fecha existente para editar

### 5.5. Servicios Frontend

- [ ] Actualizar `companyInterviewService.ts`:
  - Agregar método `getInterviewStatistics()`
  - Agregar método `getInterviewCalendar()`
  - Agregar método `getOverdueInterviews()`
  - Actualizar `createInterview()` para incluir nuevos campos
  - Actualizar `updateInterview()` para incluir nuevos campos
  - Actualizar tipos TypeScript con nuevos campos

---

## Fase 6: Testing

### 6.1. Tests Unitarios (Backend)

- [ ] Tests para `InterviewProcessTypeEnum`
- [ ] Tests para `InterviewTypeEnum` (nuevos valores)
- [ ] Tests para validación de `required_roles` (obligatorio, no vacío)
- [ ] Tests para validación de `CompanyRoleId` existentes
- [ ] Tests para validación de usuarios con roles requeridos
- [ ] Tests para métodos de dominio nuevos

### 6.2. Tests de Integración (Backend)

- [ ] Tests para `CreateInterviewCommand` con nuevos campos
- [ ] Tests para `ListInterviewsQuery` con nuevos filtros
- [ ] Tests para `GetInterviewStatisticsQuery`
- [ ] Tests para endpoints nuevos
- [ ] Tests para validaciones de roles requeridos

### 6.3. Tests E2E (Frontend)

- [ ] Test de creación de entrevista con `required_roles`
- [ ] Test de edición de entrevista con nuevos campos
- [ ] Test de listado con filtros avanzados
- [ ] Test de asignación de entrevistadores
- [ ] Test de validaciones en formularios

---

## Fase 7: Documentación

- [ ] Actualizar documentación de API con nuevos endpoints
- [ ] Actualizar documentación de schemas con nuevos campos
- [ ] Documentar cambios en enums
- [ ] Actualizar README si es necesario
- [ ] Documentar componentes nuevos de frontend

---

## Checklist de Verificación Final

### Backend

- [ ] Todos los enums creados/actualizados
- [ ] Entidad `Interview` actualizada con todos los campos
- [ ] Modelo `InterviewModel` actualizado
- [ ] Repositorio actualizado con mapeos
- [ ] Migraciones creadas y ejecutadas
- [ ] Commands actualizados/creados
- [ ] Queries actualizadas/creadas
- [ ] DTOs actualizados
- [ ] Schemas actualizados
- [ ] Endpoints actualizados/creados
- [ ] Controllers actualizados
- [ ] Container actualizado con nuevos handlers

### Frontend

- [ ] Listado rediseñado con cabecera y calendario
- [ ] Filtros avanzados implementados
- [ ] Pantalla de crear actualizada
- [ ] Pantalla de editar actualizada
- [ ] Componentes reutilizables creados
- [ ] Servicios actualizados
- [ ] Tipos TypeScript actualizados
- [ ] Validaciones implementadas

### Testing

- [ ] Tests unitarios escritos
- [ ] Tests de integración escritos
- [ ] Tests E2E escritos
- [ ] Todos los tests pasando

### Documentación

- [ ] Documentación actualizada
- [ ] README actualizado si es necesario

---

## Notas Importantes

1. **Orden de Implementación**: Seguir estrictamente el orden de fases (Domain → Infrastructure → Application → Presentation → Frontend)
2. **Validaciones**: Todas las validaciones deben estar en domain layer
3. **Tipado**: Usar Value Objects directamente en Commands/Queries, NO strings
4. **JSON vs Tabla**: Usar JSON para `required_roles` según análisis realizado
5. **Fase de Desarrollo**: No preocuparse por compatibilidad hacia atrás, eliminar datos antes de comenzar

---

**Última Actualización**: Enero 2025

