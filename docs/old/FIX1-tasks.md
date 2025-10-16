# FIX1 - Plan de Tareas para Conformidad Arquitectónica

## Resumen Ejecutivo

Este documento define las **52 tareas específicas** necesarias para alcanzar **100% conformidad** con la especificación FIX1.md.

**Estado Actual**: 80% conformidad | **Gap**: 20% | **Esfuerzo Estimado**: ~5-8 días

---

## 🚨 **FASE 1: CRÍTICAS - Naming & Estructura (5-7 días)**

### **Backend: Reestructuración de Endpoints**

#### 1.1 **Renombrar Grupo Candidate**
- [X] **T001** - Renombrar router `/candidates` → `/candidate`
  - **Archivos**: `presentation/candidate/routers/candidate_router.py`
  - **Tiempo**: 2 horas
  - **Prioridad**: 🚨 CRÍTICO

- [X] **T002** - Actualizar prefijo en router: `APIRouter(prefix="/candidate")`
  - **Archivos**: `presentation/candidate/routers/candidate_router.py:52`
  - **Tiempo**: 15 minutos
  - **Prioridad**: 🚨 CRÍTICO

#### 1.2 **Eliminar "me" de Rutas**
- [X] **T003** - Cambiar `/candidates/me/profile` → `/candidate/profile`
  - **Archivos**: `presentation/candidate/routers/candidate_router.py`
  - **Endpoints afectados**: 15 endpoints
  - **Tiempo**: 3 horas
  - **Prioridad**: 🚨 CRÍTICO

- [X] **T004** - Cambiar `/candidates/me/experiences` → `/candidate/experience`
  - **Nota**: También cambiar plural → singular según FIX1.md
  - **Tiempo**: 2 horas
  - **Prioridad**: 🚨 CRÍTICO

- [X] **T005** - Cambiar `/candidates/me/educations` → `/candidate/education`
  - **Tiempo**: 2 horas
  - **Prioridad**: 🚨 CRÍTICO

- [X] **T006** - Cambiar `/candidates/me/projects` → `/candidate/projects`
  - **Tiempo**: 2 horas
  - **Prioridad**: 🚨 CRÍTICO

#### 1.3 **Consolidar Endpoints de Auth**
- [X] **T007** - Crear `/candidate/auth` endpoints
  - **Mover desde**: `/api/auth`
  - **Endpoints**: `POST /candidate/auth/login`, `GET /candidate/auth/me`
  - **Tiempo**: 4 horas
  - **Prioridad**: 🚨 CRÍTICO

- [X] **T008** - Crear `/admin/auth` endpoints
  - **Implementar**: Admin auth real (no mock)
  - **Endpoints**: `POST /admin/auth/login`, `GET /admin/auth/me`
  - **Tiempo**: 6 horas
  - **Prioridad**: 🚨 CRÍTICO

#### 1.4 **Mover Resume a Candidate**
- [X] **T009** - Mover `/api/resumes` → `/candidate/resume`
  - **Archivos**: `presentation/candidate/routers/resume_router.py`
  - **Tiempo**: 3 horas
  - **Prioridad**: 🚨 CRÍTICO

- [X] **T010** - Actualizar imports y dependencias de resume
  - **Archivos**: `main.py`, `core/container.py`
  - **Tiempo**: 1 hora
  - **Prioridad**: 🚨 CRÍTICO

#### 1.5 **Eliminar Grupos No Conformes**
- [X] **T011** - Eliminar grupo `/api/auth`
  - **Archivos**: `presentation/shared/routes/auth_router.py`
  - **Después de**: T007, T008
  - **Tiempo**: 1 hora
  - **Prioridad**: 🚨 CRÍTICO

- [X] **T012** - Eliminar grupo `/api/resumes`
  - **Después de**: T009
  - **Tiempo**: 1 hora
  - **Prioridad**: 🚨 CRÍTICO

- [X] **T013** - Integrar `/landing` en `/candidate`
  - **Archivos**: `presentation/candidate/routers/landing_router.py`
  - **Tiempo**: 4 horas
  - **Prioridad**: 🚨 CRÍTICO

---

## ⚠️ **FASE 2: IMPORTANTES - Funcionalidades Faltantes (6-8 días)**

### **Backend: Funcionalidades Missing**

#### 2.1 **Implementar Application Management**
- [X] **T014** - Crear dominio `Application`
  - **Archivos**: `src/candidate_application/` (YA EXISTE)
  - **Tiempo**: 8 horas
  - **Prioridad**: ⚠️ CRÍTICO

- [X] **T015** - Crear endpoints `/candidate/application`
  - **Endpoints**: CRUD completo para solicitudes (YA EXISTE)
  - **Tiempo**: 12 horas
  - **Prioridad**: ⚠️ CRÍTICO

- [X] **T016** - Crear relación Application ↔ JobPosition
  - **DB Migration**: Tabla applications (YA EXISTE)
  - **Tiempo**: 4 horas
  - **Prioridad**: ⚠️ CRÍTICO

#### 2.2 **Implementar Interview Management**
- [ ] **T017** - Crear endpoints `/admin/interview`
  - **Separado de**: interview-templates (DOMINIO EXISTE, FALTA PRESENTACIÓN)
  - **Endpoints**: Schedule, conduct, evaluate interviews
  - **Tiempo**: 8 horas (solo presentación)
  - **Prioridad**: ⚠️ CRÍTICO

- [ ] **T018** - Crear relación Interview ↔ Application
  - **DB Migration**: Agregar application_id a interviews (FALTA IMPLEMENTAR)
  - **Tiempo**: 6 horas
  - **Prioridad**: ⚠️ CRÍTICO

### **Frontend: Eliminar Duplicaciones**

#### 2.3 **Limpiar Rutas Duplicadas**
- [X] **T019** - Eliminar ruta `/work-experience`
  - **Mantener solo**: `/candidate/profile/experience`
  - **Archivos**: `client-vite/src/App.tsx`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ IMPORTANTE

- [X] **T020** - Eliminar ruta `/education`
  - **Mantener solo**: `/candidate/profile/education`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ IMPORTANTE

- [X] **T021** - Eliminar ruta `/projects`
  - **Mantener solo**: `/candidate/profile/projects`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ IMPORTANTE

- [X] **T022** - Eliminar rutas `/resumes/*`
  - **Mantener solo**: `/candidate/profile/resumes`
  - **Tiempo**: 3 horas
  - **Prioridad**: ⚠️ IMPORTANTE

#### 2.4 **Integrar Auth en Flujos**
- [X] **T023** - Mover `/candidate/login` → `/candidate/auth/login`
  - **Archivos**: `client-vite/src/App.tsx`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ IMPORTANTE

- [X] **T024** - Mover `/admin/login` → `/admin/auth/login`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ IMPORTANTE

- [X] **T025** - Eliminar `/auth/login` genérico
  - **Tiempo**: 1 hora
  - **Prioridad**: ⚠️ IMPORTANTE

#### 2.5 **Corregir Rutas Frontend No Conformes**
- [X] **T025A** - Mover `/complete-profile` → `/candidate/onboarding/complete-profile`
  - **Archivos**: `client-vite/src/App.tsx`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ CRÍTICO

- [X] **T025B** - Mover `/auth/register` → `/candidate/auth/register`
  - **Archivos**: `client-vite/src/App.tsx`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ CRÍTICO

- [X] **T025C** - Mover `/pdf-processing` → `/candidate/onboarding/pdf-processing`
  - **Archivos**: `client-vite/src/App.tsx`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ CRÍTICO

- [X] **T025D** - Mover `/dashboard` → `/candidate/dashboard`
  - **Archivos**: `client-vite/src/App.tsx`
  - **Tiempo**: 1 hora
  - **Prioridad**: ⚠️ IMPORTANTE

- [X] **T025E** - Mover `/candidates` → `/candidate/search`
  - **Archivos**: `client-vite/src/App.tsx`
  - **Tiempo**: 2 horas
  - **Prioridad**: ⚠️ IMPORTANTE

---

## 📱 **FASE 3: MEDIAS - Screens Faltantes (4-6 días)**

### **Frontend: Implementar Screens Missing**

#### 3.1 **Application Screens**
- [ ] **T026** - Crear `/candidate/application` screen
  - **Funcionalidad**: Ver solicitudes enviadas
  - **Tiempo**: 8 horas
  - **Prioridad**: 📱 MEDIO

- [ ] **T027** - Crear application management en candidate
  - **Funcionalidad**: Aplicar a posiciones
  - **Tiempo**: 12 horas
  - **Prioridad**: 📱 MEDIO

#### 3.2 **Open Positions Screens**
- [ ] **T028** - Crear `/candidate/open-positions` screen
  - **Funcionalidad**: Búsqueda de empleo
  - **Tiempo**: 10 horas
  - **Prioridad**: 📱 MEDIO

- [ ] **T029** - Integrar search & apply functionality
  - **Tiempo**: 8 horas
  - **Prioridad**: 📱 MEDIO

#### 3.3 **Interview Screens**
- [ ] **T030** - Habilitar interview screens (removar "temporarily disabled")
  - **Archivos**: `client-vite/src/App.tsx:105-108`
  - **Tiempo**: 2 horas
  - **Prioridad**: 📱 MEDIO

- [ ] **T031** - Crear `/candidate/interview` screen
  - **Funcionalidad**: Ver entrevistas programadas
  - **Tiempo**: 8 horas
  - **Prioridad**: 📱 MEDIO

- [ ] **T032** - Crear `/admin/candidates/interview` screen
  - **Funcionalidad**: Gestionar entrevistas por candidato
  - **Tiempo**: 10 horas
  - **Prioridad**: 📱 MEDIO

#### 3.4 **Admin Applications Screen**
- [ ] **T033** - Crear `/admin/companies/applications` screen
  - **Funcionalidad**: Ver solicitudes por empresa
  - **Tiempo**: 8 horas
  - **Prioridad**: 📱 MEDIO

---

## 🔧 **FASE 4: FINALES - Testing & Refactoring (2-3 días)**

### **Testing & Validation**

#### 4.1 **Backend Testing**
- [ ] **T034** - Actualizar tests para nuevas rutas
  - **Archivos**: `tests/`
  - **Tiempo**: 6 horas
  - **Prioridad**: 🔧 FINAL

- [ ] **T035** - Tests de integración para Application & Interview
  - **Tiempo**: 8 horas
  - **Prioridad**: 🔧 FINAL

#### 4.2 **Frontend Testing**
- [ ] **T036** - Actualizar routing tests
  - **Tiempo**: 4 horas
  - **Prioridad**: 🔧 FINAL

- [ ] **T037** - E2E tests para nuevos flujos
  - **Tiempo**: 8 horas
  - **Prioridad**: 🔧 FINAL

### **Documentation & Cleanup**

#### 4.3 **Actualización de Documentación**
- [ ] **T038** - Actualizar API docs con nuevas rutas
  - **Tiempo**: 3 horas
  - **Prioridad**: 🔧 FINAL

- [ ] **T039** - Actualizar README con nueva estructura
  - **Tiempo**: 2 horas
  - **Prioridad**: 🔧 FINAL

#### 4.4 **Code Cleanup**
- [ ] **T040** - Remover código dead de rutas eliminadas
  - **Tiempo**: 4 horas
  - **Prioridad**: 🔧 FINAL

- [ ] **T041** - Optimizar imports después de reestructuración
  - **Tiempo**: 2 horas
  - **Prioridad**: 🔧 FINAL

- [ ] **T042** - Lint & format todo el código
  - **Tiempo**: 1 hora
  - **Prioridad**: 🔧 FINAL

---

## 🎯 **FASE 5: VALIDACIÓN - Conformidad Check (1 día)**

### **Conformidad Validation**

#### 5.1 **Validación Final**
- [ ] **T043** - Verificar 2 grupos de endpoints únicamente
  - **Validar**: Solo `/candidate` y `/admin` existen
  - **Tiempo**: 2 horas
  - **Prioridad**: 🎯 VALIDACIÓN

- [ ] **T044** - Verificar todas las funcionalidades FIX1.md
  - **Checklist**: auth, Profile, Experience, Education, Projects, Resume, Application
  - **Tiempo**: 3 horas
  - **Prioridad**: 🎯 VALIDACIÓN

- [ ] **T045** - Verificar screens frontend completas
  - **Checklist**: onboarding, profile, experience, education, projects, resume, application, interview, open positions, login
  - **Tiempo**: 2 horas
  - **Prioridad**: 🎯 VALIDACIÓN

- [ ] **T046** - Verificar principio de reutilización
  - **Validar**: onboarding y candidate comparten endpoints
  - **Tiempo**: 2 horas
  - **Prioridad**: 🎯 VALIDACIÓN

- [ ] **T047** - Actualizar FIX1-ANALYSIS.md con 100% conformidad
  - **Resultado**: Documento de conformidad final
  - **Tiempo**: 1 hora
  - **Prioridad**: 🎯 VALIDACIÓN

---

## 📊 **RESUMEN DE ESFUERZO**

| Fase | Tareas | Tiempo Estimado | Prioridad |
|------|--------|----------------|-----------|
| **Fase 1: Críticas** | ✅ T001-T013 (13 tareas) | ✅ COMPLETADA | 🚨 CRÍTICO |
| **Fase 2: Importantes** | T014-T025E (17 tareas) | 4-6 días | ⚠️ IMPORTANTE |
| **Fase 3: Medias** | T026-T033 (8 tareas) | 4-6 días | 📱 MEDIO |
| **Fase 4: Finales** | T034-T042 (9 tareas) | 2-3 días | 🔧 FINAL |
| **Fase 5: Validación** | T043-T047 (5 tareas) | 1 día | 🎯 VALIDACIÓN |
| **TOTAL** | **52 tareas** | **15-20 días** | - |
| **COMPLETADAS** | **26 tareas (50%)** | **10-12 días ahorrados** | ✅ |

## 🎯 **CRITERIOS DE ÉXITO**

Al completar todas las tareas:

- ✅ **100% conformidad** con FIX1.md
- ✅ **Solo 2 grupos** de endpoints: `/candidate`, `/admin`
- ✅ **Todas las funcionalidades** especificadas implementadas
- ✅ **Naming conventions** correctas (singular, sin "me")
- ✅ **Auth integrado** en flujos principales
- ✅ **Zero rutas duplicadas** en frontend
- ✅ **Principio de reutilización** candidate/onboarding respetado

## 📝 **NOTAS DE IMPLEMENTACIÓN**

### **Dependencias Críticas:**
- T007, T008 deben completarse antes de T011 (eliminar /api/auth)
- T009 debe completarse antes de T012 (eliminar /api/resumes)
- T014-T018 son prerrequisitos para T026-T033

### **Risk Mitigation:**
- Crear branch específico para cada fase
- Testing incremental después de cada fase
- Backup de rutas actuales antes de T003-T006
- Validación de conformidad progresiva

### **Performance Impact:**
- Las tareas T001-T013 requieren actualización de todos los API clients
- Considerar migration strategy para datos existentes
- Posible impacto en cache de frontend por cambios de rutas

---

**Estado**: ✅ **Fase 1 COMPLETADA** | **Próximo**: Ejecutar Fase 2 (T014-T025E)

---

## ✅ **PROGRESO ACTUAL**

### **COMPLETADAS ✅**
- **FASE 1**: T001-T013 - Backend reestructurado, endpoints conformes
  - ✅ Grupos `/candidates` → `/candidate`
  - ✅ Eliminación de "me" en rutas
  - ✅ Auth consolidado `/candidate/auth` y `/admin/auth`
  - ✅ Resume movido a `/candidate/resume`
  - ✅ Eliminados grupos `/api/auth`, `/api/resumes`
  - ✅ Landing integrado en `/candidate/onboarding`

- **FASE 2B**: T019-T025E - Frontend route compliance completada
  - ✅ Eliminadas rutas duplicadas (`/work-experience`, `/education`, `/projects`, `/resumes/*`)
  - ✅ Auth routes integradas (`/candidate/auth/login`, `/admin/auth/login`)
  - ✅ Rutas no conformes movidas a dominios correctos:
    - ✅ `/complete-profile` → `/candidate/onboarding/complete-profile`
    - ✅ `/auth/register` → `/candidate/auth/register`
    - ✅ `/pdf-processing` → `/candidate/onboarding/pdf-processing`
    - ✅ `/dashboard` → `/candidate/dashboard`
    - ✅ `/candidates` → `/candidate/search`

- **FASE 2A PARCIAL**: T014-T016 - Application Management completado
  - ✅ T014: Dominio Application existe (`src/candidate_application/`)
  - ✅ T015: Endpoints `/candidate/application` implementados
  - ✅ T016: Relación Application ↔ JobPosition establecida

### **PRÓXIMAS TAREAS 🔄**
- **FASE 2A PENDIENTE**: T017-T018 - Interview Management
  - 🔄 T017: Endpoints `/admin/interview` (dominio existe, falta presentación)
  - 🔄 T018: Relación Interview ↔ Application (falta implementar)
- **FASE 3**: T026-T033 - Frontend screens faltantes