# Plan de Implementación: Dashboard del Candidato - Dividido en Dos Fases

## FASE A: MVP BÁSICO - Login, CVs y Perfil ✅
**Objetivo**: Dashboard funcional con las características principales
**Tiempo estimado**: 15-20 horas
**Backend necesario**: ✅ **CERO cambios** (todo ya implementado)

### **Funcionalidades Incluidas en MVP**
1. **✅ Login/Autenticación** - Ya funciona completamente
2. **✅ Dashboard principal** - Información básica del candidato
3. **✅ Edición de perfil personal** - Reutiliza CompleteProfilePage
4. **✅ Gestión de experiencias** - CRUD completo ya implementado
5. **✅ Gestión de educación** - CRUD completo ya implementado
6. **✅ Gestión de proyectos** - CRUD completo ya implementado
7. **✅ Sistema de CVs** - Listar, crear, editar, preview
8. **✅ Navegación y layout** - Sidebar y header del dashboard

---

## FASE A: IMPLEMENTACIÓN MVP

### **Backend: ✅ TODO YA IMPLEMENTADO**
- **Autenticación JWT**: Sistema completo funcionando
- **API de Candidatos**: Controller con CRUD completo
- **API de CVs**: Sistema completo de generación y gestión
- **API de Experiencias**: CRUD completo
- **API de Educación**: CRUD completo
- **API de Proyectos**: CRUD completo

**🎉 NO HAY QUE TOCAR EL BACKEND PARA EL MVP**

### **Frontend MVP: Tareas Específicas**

#### **Tarea A1: Layout Base del Dashboard**
**Tiempo**: 4-5 horas
**Archivos a crear**:
```
/client-vite/src/components/candidate-profile/
├── CandidateProfileLayout.tsx        # Layout principal
├── ProfileSidebar.tsx               # Navegación lateral
├── ProfileHeader.tsx                # Header con info candidato
└── index.ts
```

#### **Tarea A2: Dashboard Principal**
**Tiempo**: 3-4 horas
**Archivos a crear**:
```
/client-vite/src/pages/CandidateProfilePage.tsx
/client-vite/src/components/candidate-profile/
├── StatCard.tsx                     # Cards de estadísticas
├── QuickActionCard.tsx              # Acciones rápidas
└── RecentActivitySection.tsx        # Actividad reciente
```

#### **Tarea A3: Reutilizar Formularios de Perfil**
**Tiempo**: 4-5 horas
**Archivos a crear**:
```
/client-vite/src/components/candidate-profile/forms/
├── ProfileBasicInfoForm.tsx         # Extraído de CompleteProfilePage
├── ProfileExperienceForm.tsx        # Formulario experiencias
├── ProfileEducationForm.tsx         # Formulario educación
├── ProfileProjectsForm.tsx          # Formulario proyectos
└── index.ts
```

#### **Tarea A4: Páginas de Edición**
**Tiempo**: 3-4 horas
**Archivos a crear**:
```
/client-vite/src/pages/candidate-profile/
├── EditBasicInfoPage.tsx
├── EditExperiencePage.tsx
├── EditEducationPage.tsx
└── EditProjectsPage.tsx
```

#### **Tarea A5: Integración con Sistema de CVs**
**Tiempo**: 2-3 horas
**Archivos a crear**:
```
/client-vite/src/pages/candidate-profile/
├── ResumesPage.tsx                  # Lista de CVs
└── CreateResumePage.tsx             # Crear nuevo CV
```

#### **Tarea A6: Rutas y Navegación**
**Tiempo**: 1-2 horas
**Archivos a modificar**:
```
/client-vite/src/App.tsx             # Configurar rutas React Router
```

**Rutas MVP**:
```typescript
<Route path="/candidate/profile" element={<CandidateProfilePage />} />
<Route path="/candidate/profile/edit" element={<EditBasicInfoPage />} />
<Route path="/candidate/profile/experience" element={<EditExperiencePage />} />
<Route path="/candidate/profile/education" element={<EditEducationPage />} />
<Route path="/candidate/profile/projects" element={<EditProjectsPage />} />
<Route path="/candidate/profile/resumes" element={<ResumesPage />} />
<Route path="/candidate/profile/resumes/create" element={<CreateResumePage />} />
```

---

## FASE B: CARACTERÍSTICAS AVANZADAS
**Objetivo**: Candidaturas, entrevistas y configuración avanzada
**Tiempo estimado**: 25-35 horas
**Backend necesario**: ❌ **SÍ requiere cambios** (5-8 horas backend)

### **Funcionalidades Fase B**
1. **❌ Lista de candidaturas** - Requiere backend
2. **❌ Seguimiento de aplicaciones** - Requiere backend
3. **❌ Sistema de entrevistas** - Requiere backend
4. **❌ Configuración de cuenta** - Cambio password, privacy
5. **❌ Notificaciones** - Sistema de alerts
6. **❌ Analytics avanzados** - Gráficos y estadísticas

---

## FASE B: IMPLEMENTACIÓN AVANZADA

### **Backend B: Cambios Necesarios (5-8 horas)**

#### **B1: Sistema de Candidaturas**
**Tiempo**: 4-5 horas
```python
# Nuevos archivos necesarios:
src/candidate_application/application/queries/get_applications_by_candidate_id.py
src/candidate_application/application/handlers/get_applications_by_candidate_id_query_handler.py
presentation/candidate/controllers/candidate_application_controller.py

# Endpoints nuevos en candidate_router.py:
GET /api/candidates/me/applications
GET /api/candidates/me/applications/stats
```

#### **B2: Sistema de Entrevistas**
**Tiempo**: 6-8 horas
```python
# Sistema completo de entrevistas (si no existe):
src/interview/domain/entities/interview.py
src/interview/application/queries/get_interviews_by_candidate_id.py
presentation/candidate/controllers/interview_controller.py

# Endpoints nuevos:
GET /api/candidates/me/interviews
GET /api/candidates/me/interviews/upcoming
```

#### **B3: Configuración de Cuenta**
**Tiempo**: 2-3 horas
```python
# Endpoints adicionales en candidate_router.py:
PUT /api/candidates/me/settings/password
PUT /api/candidates/me/settings/privacy
PUT /api/candidates/me/settings/notifications
```

### **Frontend B: Características Avanzadas (20-27 horas)**

#### **B4: Sistema de Candidaturas**
**Tiempo**: 6-8 horas
```
/client-vite/src/pages/candidate-profile/
├── ApplicationsPage.tsx
├── ApplicationDetailPage.tsx
└── ApplicationsStatsPage.tsx
```

#### **B5: Sistema de Entrevistas**
**Tiempo**: 6-8 horas
```
/client-vite/src/pages/candidate-profile/
├── InterviewsPage.tsx
├── InterviewDetailPage.tsx
└── InterviewCalendarPage.tsx
```

#### **B6: Configuración Avanzada**
**Tiempo**: 4-5 horas
```
/client-vite/src/pages/candidate-profile/
├── SettingsPage.tsx
├── PasswordChangePage.tsx
├── PrivacySettingsPage.tsx
└── NotificationSettingsPage.tsx
```

#### **B7: Analytics y Dashboards Avanzados**
**Tiempo**: 4-6 horas
```
/client-vite/src/components/candidate-profile/
├── AdvancedStatsCard.tsx
├── ApplicationTrendsChart.tsx
├── InterviewSuccessChart.tsx
└── ProfileCompletenessChart.tsx
```

---

## CRONOGRAMA DE DOS FASES

### **🚀 FASE A - MVP (15-20 horas)**
**Semana 1-2: Solo Frontend, Backend ya listo**

| Día | Tarea | Horas | Entregable |
|-----|-------|-------|------------|
| 1-2 | A1: Layout Base | 4-5h | Dashboard navegable |
| 3 | A2: Dashboard Principal | 3-4h | Homepage funcional |
| 4-5 | A3: Formularios Perfil | 4-5h | Edición de perfil |
| 6 | A4: Páginas Edición | 3-4h | CRUD completo perfil |
| 7 | A5: Sistema CVs | 2-3h | Gestión de CVs |
| 8 | A6: Rutas | 1-2h | Navegación completa |

**✅ Resultado Fase A**: Dashboard completamente funcional con login, perfil y CVs

### **🎯 FASE B - AVANZADO (25-35 horas)**
**Semana 3-5: Backend + Frontend**

| Semana | Backend | Frontend | Total |
|--------|---------|----------|-------|
| 3 | B1: Candidaturas (4-5h) | B4: UI Candidaturas (6-8h) | 10-13h |
| 4 | B2: Entrevistas (6-8h) | B5: UI Entrevistas (6-8h) | 12-16h |
| 5 | B3: Configuración (2-3h) | B6: UI Config + B7: Analytics (8-11h) | 10-14h |

**✅ Resultado Fase B**: Sistema completo con todas las características

---

## CRITERIOS DE ACEPTACIÓN POR FASE

### **✅ FASE A MVP - Listo para Usuarios**
- Candidato puede hacer login con JWT
- Dashboard muestra información personal y estadísticas básicas
- Puede editar perfil completo (personal, experiencia, educación, proyectos)
- Puede crear, listar y gestionar CVs
- Navegación fluida entre todas las secciones
- UI responsive y consistente con el resto de la app

### **✅ FASE B AVANZADO - Características Premium**
- Lista completa de candidaturas con filtros y búsqueda
- Seguimiento de estado de aplicaciones
- Calendario de entrevistas próximas e historial
- Configuración completa de cuenta y privacidad
- Analytics avanzados con gráficos y tendencias
- Sistema de notificaciones

---

## VENTAJAS DE LA DIVISIÓN EN DOS FASES

### **🎯 Fase A (MVP)**
- **✅ Riesgo CERO**: No hay que tocar backend
- **✅ Rápido de implementar**: Solo frontend, reutilizando código
- **✅ Valor inmediato**: Candidatos pueden usar dashboard básico
- **✅ Feedback temprano**: Validar UX antes de características avanzadas

### **🚀 Fase B (Avanzado)**
- **✅ Características diferenciadas**: Candidaturas y entrevistas
- **✅ Backend robusto**: Implementar APIs específicas
- **✅ Analytics avanzados**: Dashboards con datos reales
- **✅ Experiencia premium**: Funcionalidades avanzadas

### **📊 Comparación de Esfuerzo**

| Aspecto | Fase A (MVP) | Fase B (Avanzado) |
|---------|--------------|-------------------|
| **Backend** | ✅ 0 horas | ❌ 5-8 horas |
| **Frontend** | ✅ 15-20 horas | ❌ 20-27 horas |
| **Riesgo** | 🟢 Muy bajo | 🟡 Medio |
| **Valor** | 🟢 Alto inmediato | 🟢 Muy alto diferenciado |
| **Complejidad** | 🟢 Baja | 🟡 Media-Alta |

---

## RECOMENDACIÓN

**🎯 EMPEZAR CON FASE A (MVP)**

**Razones:**
1. **Sin riesgo backend** - Todo ya implementado
2. **Valor inmediato** - Dashboard funcional en 2 semanas
3. **Reutilización máxima** - Aprovecha CompleteProfilePage y sistema de CVs
4. **Feedback rápido** - Los usuarios pueden probar y dar feedback
5. **Base sólida** - Arquitectura preparada para Fase B

**Después de completar Fase A, evaluar si proceder con Fase B según:**
- Feedback de usuarios
- Prioridades del negocio
- Recursos disponibles

¿Empezamos con la **Fase A (MVP)** implementando el dashboard básico?