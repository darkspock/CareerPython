# Plan de Implementación: Dashboard del Candidato

## Resumen Ejecutivo

Implementar un dashboard completo para candidatos en `/candidate/profile` que permita:
1. **Modificar perfil completo** - Reutilizando componentes del onboarding
2. **Gestión de CVs** - Acceso a generación y listado de currículos
3. **Seguimiento de candidaturas** - Lista de aplicaciones activas
4. **Gestión de entrevistas** - Próximas entrevistas y historial
5. **Configuración de cuenta** - Email, contraseña, privacidad, logout

## Análisis del Estado Actual

### ✅ **Backend - Completamente Implementado**
- **API de Candidatos**: Controller con CRUD completo (candidate.py:42-213)
- **Gestión de Experiencias**: Crear, editar, eliminar experiencias laborales
- **Gestión de Educación**: Crear, editar, eliminar formación académica
- **Gestión de Proyectos**: Crear, editar, eliminar proyectos
- **Sistema de CVs**: API completa para generar y gestionar currículos
- **Autenticación JWT**: Sistema completo con tokens Bearer

### ✅ **Frontend - Componentes Existentes**
- **OnboardingLayout**: Layout reutilizable con navegación (OnboardingLayout.tsx:21-158)
- **CompleteProfilePage**: Formulario completo de perfil (CompleteProfilePage.tsx:61-596)
- **useOnboarding**: Hook con gestión de estado del candidato
- **API Client**: Cliente completo para todas las operaciones backend

### ❌ **Por Implementar**
- **Dashboard principal** del candidato
- **Páginas de edición** reutilizando componentes del onboarding
- **Integración con sistema de CVs** desde el dashboard
- **Lista de candidaturas** y entrevistas
- **Página de configuración** de cuenta

---

## FASE 1: Dashboard Principal y Navegación

### **Tarea 1.1: Crear Dashboard Layout Base**
**Prioridad**: 🔴 CRÍTICA
**Tiempo estimado**: 3-4 horas

#### **Archivos a crear:**
```
/client-vite/src/components/candidate-profile/
├── CandidateProfileLayout.tsx        # Layout principal del dashboard
├── ProfileSidebar.tsx               # Navegación lateral
├── ProfileHeader.tsx                # Header con info del candidato
└── index.ts                         # Exports
```

#### **CandidateProfileLayout.tsx**:
```typescript
interface CandidateProfileLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  currentSection?: string;
}

const CandidateProfileLayout: React.FC<CandidateProfileLayoutProps> = ({
  children,
  title,
  subtitle,
  currentSection
}) => {
  const [candidate, setCandidate] = useState<CandidateData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCandidateData();
  }, []);

  const loadCandidateData = async () => {
    try {
      const profileSummary = await api.getMyProfileSummary();
      setCandidate(profileSummary.candidate);
    } catch (error) {
      console.error('Error loading candidate:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <ProfileHeader candidate={candidate} />

      <div className="flex">
        {/* Sidebar */}
        <ProfileSidebar currentSection={currentSection} />

        {/* Main Content */}
        <main className="flex-1 p-6">
          {title && (
            <div className="mb-6">
              <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
              {subtitle && <p className="text-gray-600 mt-1">{subtitle}</p>}
            </div>
          )}

          <div className="bg-white rounded-lg shadow-sm border">
            {loading ? (
              <div className="p-8 text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-2 text-gray-600">Cargando...</p>
              </div>
            ) : (
              children
            )}
          </div>
        </main>
      </div>
    </div>
  );
};
```

#### **ProfileSidebar.tsx**:
```typescript
interface ProfileSidebarProps {
  currentSection?: string;
}

const ProfileSidebar: React.FC<ProfileSidebarProps> = ({ currentSection }) => {
  const navigate = useNavigate();

  const menuItems = [
    {
      id: 'profile',
      label: 'Mi Perfil',
      icon: User,
      path: '/candidate/profile',
      description: 'Información personal y profesional'
    },
    {
      id: 'experience',
      label: 'Experiencia',
      icon: Briefcase,
      path: '/candidate/profile/experience',
      description: 'Experiencia laboral'
    },
    {
      id: 'education',
      label: 'Educación',
      icon: GraduationCap,
      path: '/candidate/profile/education',
      description: 'Formación académica'
    },
    {
      id: 'projects',
      label: 'Proyectos',
      icon: FolderOpen,
      path: '/candidate/profile/projects',
      description: 'Proyectos realizados'
    },
    {
      id: 'resumes',
      label: 'Mis CVs',
      icon: FileText,
      path: '/candidate/profile/resumes',
      description: 'Generar y gestionar currículos'
    },
    {
      id: 'applications',
      label: 'Candidaturas',
      icon: Send,
      path: '/candidate/profile/applications',
      description: 'Seguimiento de aplicaciones'
    },
    {
      id: 'interviews',
      label: 'Entrevistas',
      icon: Calendar,
      path: '/candidate/profile/interviews',
      description: 'Próximas entrevistas'
    },
    {
      id: 'settings',
      label: 'Configuración',
      icon: Settings,
      path: '/candidate/profile/settings',
      description: 'Cuenta y privacidad'
    }
  ];

  return (
    <aside className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
      <nav className="p-4">
        <div className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentSection === item.id;

            return (
              <button
                key={item.id}
                onClick={() => navigate(item.path)}
                className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg text-left transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-blue-600' : 'text-gray-500'}`} />
                <div>
                  <div className="font-medium">{item.label}</div>
                  <div className="text-xs text-gray-500">{item.description}</div>
                </div>
              </button>
            );
          })}
        </div>
      </nav>
    </aside>
  );
};
```

### **Tarea 1.2: Página Principal del Dashboard**
**Prioridad**: 🔴 CRÍTICA
**Tiempo estimado**: 2-3 horas

#### **Archivo a crear:**
```
/client-vite/src/pages/CandidateProfilePage.tsx
```

#### **CandidateProfilePage.tsx**:
```typescript
const CandidateProfilePage: React.FC = () => {
  return (
    <CandidateProfileLayout
      title="Dashboard"
      subtitle="Resumen de tu perfil profesional"
      currentSection="profile"
    >
      <div className="p-6 space-y-6">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard
            title="CVs Creados"
            value="3"
            icon={FileText}
            color="blue"
          />
          <StatCard
            title="Candidaturas Activas"
            value="5"
            icon={Send}
            color="green"
          />
          <StatCard
            title="Entrevistas Pendientes"
            value="2"
            icon={Calendar}
            color="orange"
          />
          <StatCard
            title="Perfil Completado"
            value="85%"
            icon={User}
            color="purple"
          />
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <QuickActionCard
            title="Generar Nuevo CV"
            description="Crea un curriculum personalizado"
            icon={FileText}
            action={() => navigate('/candidate/profile/resumes/create')}
            buttonText="Crear CV"
          />
          <QuickActionCard
            title="Completar Perfil"
            description="Añade más información a tu perfil"
            icon={User}
            action={() => navigate('/candidate/profile/edit')}
            buttonText="Editar Perfil"
          />
        </div>

        {/* Recent Activity */}
        <RecentActivitySection />
      </div>
    </CandidateProfileLayout>
  );
};
```

---

## FASE 2: Páginas de Edición del Perfil

### **Tarea 2.1: Reutilizar Componentes del Onboarding**
**Prioridad**: 🟡 ALTA
**Tiempo estimado**: 4-5 horas

#### **Estrategia de Reutilización:**
El `CompleteProfilePage.tsx` existente ya contiene toda la lógica necesaria. Vamos a:
1. **Extraer componentes reutilizables** del formulario actual
2. **Crear versiones adaptadas** para el dashboard
3. **Mantener la lógica de API** existente

#### **Archivos a crear:**
```
/client-vite/src/components/candidate-profile/forms/
├── ProfileBasicInfoForm.tsx         # Extraído de CompleteProfilePage
├── ProfileExperienceForm.tsx        # Nuevo para experiencias
├── ProfileEducationForm.tsx         # Nuevo para educación
├── ProfileProjectsForm.tsx          # Nuevo para proyectos
└── index.ts
```

#### **ProfileBasicInfoForm.tsx** (Extraído de CompleteProfilePage):
```typescript
interface ProfileBasicInfoFormProps {
  initialData?: CandidateData;
  onSave: (data: CandidateData) => Promise<void>;
  onCancel: () => void;
}

const ProfileBasicInfoForm: React.FC<ProfileBasicInfoFormProps> = ({
  initialData,
  onSave,
  onCancel
}) => {
  // Reutilizar la lógica exacta de CompleteProfilePage
  const [formData, setFormData] = useState<FormData>({
    name: initialData?.name || "",
    dateOfBirth: initialData?.date_of_birth || "1990-01-01",
    city: initialData?.city || "",
    country: initialData?.country || "",
    phone: initialData?.phone || "",
    email: initialData?.email || "",
    jobCategory: initialData?.job_category || "OTHER",
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const profileData = {
        name: formData.name,
        date_of_birth: formData.dateOfBirth,
        city: formData.city,
        country: formData.country,
        phone: formData.phone,
        email: formData.email,
        job_category: JobCategoryMapping[formData.jobCategory] || formData.jobCategory,
      };

      await api.updateMyProfile(profileData);
      await onSave(profileData);
    } catch (error) {
      setError("Error al actualizar el perfil");
    } finally {
      setIsLoading(false);
    }
  };

  // Reutilizar exactamente el mismo JSX del formulario de CompleteProfilePage
  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      {/* Mismo formulario que CompleteProfilePage pero sin OnboardingLayout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Todos los campos del formulario */}
      </div>

      <div className="flex justify-end gap-3">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? 'Guardando...' : 'Guardar Cambios'}
        </button>
      </div>
    </form>
  );
};
```

### **Tarea 2.2: Páginas de Edición Individual**
**Prioridad**: 🟡 ALTA
**Tiempo estimado**: 3-4 horas

#### **Archivos a crear:**
```
/client-vite/src/pages/candidate-profile/
├── EditBasicInfoPage.tsx
├── EditExperiencePage.tsx
├── EditEducationPage.tsx
└── EditProjectsPage.tsx
```

#### **EditBasicInfoPage.tsx**:
```typescript
const EditBasicInfoPage: React.FC = () => {
  const navigate = useNavigate();
  const [candidate, setCandidate] = useState<CandidateData | null>(null);

  const handleSave = async (data: CandidateData) => {
    // Recargar datos y volver al dashboard
    navigate('/candidate/profile', {
      state: {
        showSuccessMessage: true,
        successMessage: 'Perfil actualizado correctamente'
      }
    });
  };

  const handleCancel = () => {
    navigate('/candidate/profile');
  };

  return (
    <CandidateProfileLayout
      title="Editar Información Personal"
      subtitle="Actualiza tus datos personales y profesionales"
      currentSection="profile"
    >
      <div className="p-6">
        <ProfileBasicInfoForm
          initialData={candidate}
          onSave={handleSave}
          onCancel={handleCancel}
        />
      </div>
    </CandidateProfileLayout>
  );
};
```

---

## FASE 3: Integración con Sistema de CVs

### **Tarea 3.1: Lista de CVs en el Dashboard**
**Prioridad**: 🟡 ALTA
**Tiempo estimado**: 3-4 horas

#### **Archivo a crear:**
```
/client-vite/src/pages/candidate-profile/ResumesPage.tsx
```

#### **ResumesPage.tsx**:
```typescript
const ResumesPage: React.FC = () => {
  const [resumes, setResumes] = useState<ResumeData[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      const data = await api.getResumes();
      setResumes(data);
    } catch (error) {
      console.error('Error loading resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateResume = () => {
    navigate('/candidate/profile/resumes/create');
  };

  const handleViewResume = (resumeId: string) => {
    navigate(`/resumes/${resumeId}/preview`);
  };

  const handleEditResume = (resumeId: string) => {
    navigate(`/resumes/${resumeId}/edit`);
  };

  return (
    <CandidateProfileLayout
      title="Mis Currículos"
      subtitle="Gestiona y crea nuevos CVs personalizados"
      currentSection="resumes"
    >
      <div className="p-6">
        {/* Create Button */}
        <div className="mb-6">
          <button
            onClick={handleCreateResume}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <Plus className="w-4 h-4" />
            Crear Nuevo CV
          </button>
        </div>

        {/* Resumes Grid */}
        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {resumes.map((resume) => (
              <ResumeCard
                key={resume.id}
                resume={resume}
                onView={() => handleViewResume(resume.id)}
                onEdit={() => handleEditResume(resume.id)}
              />
            ))}
          </div>
        )}
      </div>
    </CandidateProfileLayout>
  );
};
```

### **Tarea 3.2: Formulario de Creación de CVs**
**Prioridad**: 🟡 ALTA
**Tiempo estimado**: 2-3 horas

#### **Archivo a crear:**
```
/client-vite/src/pages/candidate-profile/CreateResumePage.tsx
```

Reutilizar la lógica existente del sistema de CVs pero integrarla en el dashboard del candidato.

---

## FASE 4: Candidaturas y Entrevistas

### **Tarea 4.1: Lista de Candidaturas**
**Prioridad**: 🟠 MEDIA
**Tiempo estimado**: 3-4 horas

#### **Nuevos endpoints backend necesarios:**
```python
# En candidate controller
def get_applications_by_candidate_id(self, candidate_id: str) -> List[CandidateApplicationResponse]:
    # Implementar query para obtener candidaturas del candidato
    pass
```

#### **Archivo a crear:**
```
/client-vite/src/pages/candidate-profile/ApplicationsPage.tsx
```

### **Tarea 4.2: Lista de Entrevistas**
**Prioridad**: 🟠 MEDIA
**Tiempo estimado**: 3-4 horas

#### **Archivo a crear:**
```
/client-vite/src/pages/candidate-profile/InterviewsPage.tsx
```

---

## FASE 5: Configuración de Cuenta

### **Tarea 5.1: Página de Configuración**
**Prioridad**: 🟠 MEDIA
**Tiempo estimado**: 4-5 horas

#### **Archivo a crear:**
```
/client-vite/src/pages/candidate-profile/SettingsPage.tsx
```

#### **Funcionalidades:**
- **Cambio de contraseña**: Formulario para actualizar password
- **Configuración de privacidad**: Visibilidad del perfil
- **Notificaciones**: Preferencias de email
- **Cerrar sesión**: Logout con limpieza de tokens

---

## FASE 6: Rutas y Navegación

### **Tarea 6.1: Configurar Rutas React Router**
**Prioridad**: 🔴 CRÍTICA
**Tiempo estimado**: 1-2 horas

#### **Archivo a modificar:**
```
/client-vite/src/App.tsx
```

#### **Nuevas rutas:**
```typescript
// Dentro del router existente
<Route path="/candidate/profile" element={<CandidateProfilePage />} />
<Route path="/candidate/profile/edit" element={<EditBasicInfoPage />} />
<Route path="/candidate/profile/experience" element={<EditExperiencePage />} />
<Route path="/candidate/profile/education" element={<EditEducationPage />} />
<Route path="/candidate/profile/projects" element={<EditProjectsPage />} />
<Route path="/candidate/profile/resumes" element={<ResumesPage />} />
<Route path="/candidate/profile/resumes/create" element={<CreateResumePage />} />
<Route path="/candidate/profile/applications" element={<ApplicationsPage />} />
<Route path="/candidate/profile/interviews" element={<InterviewsPage />} />
<Route path="/candidate/profile/settings" element={<SettingsPage />} />
```

### **Tarea 6.2: Integrar con Sistema de Login**
**Prioridad**: 🔴 CRÍTICA
**Tiempo estimado**: 1 hora

#### **Modificar:**
- Añadir enlace en el menú principal para acceder al dashboard
- Redirigir desde `/complete-profile` al dashboard después del onboarding
- Proteger todas las rutas con autenticación JWT

---

## Cronograma de Implementación

### **Sprint 1 (Semana 1): Core Dashboard - 12-15 horas**
- ✅ Tarea 1.1: Dashboard Layout Base (4h)
- ✅ Tarea 1.2: Página Principal del Dashboard (3h)
- ✅ Tarea 6.1: Configurar Rutas (2h)
- ✅ Tarea 6.2: Integración con Login (1h)
- ✅ Testing básico (2-3h)

### **Sprint 2 (Semana 2): Edición de Perfil - 10-12 horas**
- ✅ Tarea 2.1: Reutilizar Componentes (5h)
- ✅ Tarea 2.2: Páginas de Edición (4h)
- ✅ Testing y refinamiento (2-3h)

### **Sprint 3 (Semana 3): Sistema de CVs - 8-10 horas**
- ✅ Tarea 3.1: Lista de CVs (4h)
- ✅ Tarea 3.2: Creación de CVs (3h)
- ✅ Testing integración (2-3h)

### **Sprint 4 (Semana 4): Candidaturas y Configuración - 12-15 horas**
- ✅ Tarea 4.1: Lista de Candidaturas (4h)
- ✅ Tarea 4.2: Lista de Entrevistas (4h)
- ✅ Tarea 5.1: Página de Configuración (5h)
- ✅ Testing final (2-3h)

## **TOTAL ESTIMADO: 42-52 horas**

---

## Criterios de Aceptación

### **Sprint 1 - Dashboard Funcional:**
- ✅ Candidato puede acceder a `/candidate/profile`
- ✅ Navegación lateral funciona correctamente
- ✅ Dashboard muestra información básica del candidato
- ✅ Autenticación JWT protege todas las rutas

### **Sprint 2 - Edición de Perfil:**
- ✅ Candidato puede editar información personal
- ✅ Reutiliza componentes del onboarding sin duplicar código
- ✅ Validaciones y guardado funcionan correctamente

### **Sprint 3 - Sistema de CVs:**
- ✅ Lista de CVs existentes del candidato
- ✅ Creación de nuevos CVs desde el dashboard
- ✅ Navegación fluida al sistema de preview/edición

### **Sprint 4 - Funcionalidades Completas:**
- ✅ Lista de candidaturas activas
- ✅ Próximas entrevistas
- ✅ Configuración de cuenta y logout
- ✅ Experiencia de usuario coherente

---

## Ventajas de este Enfoque

### **1. Máxima Reutilización de Código**
- **CompleteProfilePage**: Lógica de formularios ya implementada
- **OnboardingLayout**: Patrón de layout ya establecido
- **API Client**: Todas las llamadas backend ya disponibles
- **Hooks**: useOnboarding ya maneja estado del candidato

### **2. Consistencia de UX**
- **Mismos componentes**: Formularios idénticos al onboarding
- **Misma lógica**: Validaciones y manejo de errores consistente
- **Mismo estilo**: Tailwind CSS y patrones ya establecidos

### **3. Desarrollo Incremental**
- **Dashboard básico primero**: Funcionalidad mínima viable
- **Edición después**: Reutilizando código existente
- **Características avanzadas al final**: Candidaturas, entrevistas

### **4. Mantenibilidad**
- **Separación clara**: Layout, componentes, páginas
- **Arquitectura escalable**: Fácil añadir nuevas secciones
- **Código reutilizable**: Componentes modulares

---

## Notas Técnicas

### **Reutilización de CompleteProfilePage**
El componente `CompleteProfilePage.tsx` ya implementa:
- ✅ **Formulario completo** con todos los campos necesarios
- ✅ **Validaciones** de datos y manejo de errores
- ✅ **API calls** para actualización de perfil
- ✅ **Estado de carga** y feedback al usuario
- ✅ **Mapeo de categorías** de trabajo

**Estrategia**: Extraer la lógica del formulario a un componente reutilizable `ProfileBasicInfoForm` que pueda usar tanto el onboarding como el dashboard.

### **Integración con Sistema de CVs Existente**
El sistema de CVs ya está implementado:
- ✅ **Backend completo**: API para CRUD de CVs
- ✅ **Frontend de preview**: ResumePreviewPage completamente funcional
- ✅ **Editor**: Sistema de edición (según documentación)

**Estrategia**: Crear páginas de dashboard que redirijan al sistema existente, manteniendo navegación coherente.

### **APIs Backend Disponibles**
```typescript
// Ya implementadas y funcionales
api.getMyProfile()           // Obtener perfil del candidato
api.updateMyProfile()        // Actualizar perfil
api.getResumes()            // Listar CVs del candidato
api.createResume()          // Crear nuevo CV
api.getExperiences()        // Obtener experiencias
api.createExperience()      // Crear experiencia
api.getEducations()         // Obtener educación
api.getProjects()           // Obtener proyectos
```

**Por implementar**:
```typescript
api.getMyApplications()     // Candidaturas del usuario
api.getMyInterviews()       // Entrevistas del usuario
api.updatePassword()        // Cambio de contraseña
```

---

*Este plan aprovecha al máximo el código existente, asegura una implementación rápida y mantiene la consistencia de la experiencia de usuario en toda la aplicación.*