# Plan de Trabajo: Sistema de Onboarding de Candidatos

## 📋 Análisis de Estado Actual

### ✅ **Lo que YA existe y funciona:**

1. **Dominio Candidate**: Completamente implementado siguiendo Clean Architecture
   - Entidades: `Candidate`, `CandidateExperience`, `CandidateEducation`, `CandidateProject`
   - Comandos: Create, Update, Delete para todas las entidades
   - Queries: Obtener candidatos, experiencias, educaciones, proyectos
   - Repositorios: Implementados con interfaces y SQLAlchemy
   - DTOs y Mappers: Para transformación de datos

2. **Dominio User**: Estructura básica presente
   - Entidad `User` existe
   - Comandos básicos implementados

3. **Frontend Components**: Múltiples páginas ya creadas
   - `LandingPage.tsx` - Página inicial con upload de CV
   - `CompleteProfilePage.tsx` - Completar perfil del candidato
   - `WorkExperiencePage.tsx` - Gestión de experiencia
   - `EducationPage.tsx` - Gestión de educación
   - `ProjectsPage.tsx` - Gestión de proyectos
   - `ResumePage.tsx` - Vista del CV generado

### ❌ **Lo que NO funciona o falta:**

#### **Backend Critical Issues:**

1. **Dominio Notification**: Completamente ausente
   - No existe `src/notification/`
   - No hay comandos para enviar emails
   - No hay integración con Mailgun

2. **UserAsset Management**: Parcialmente implementado
   - Entidad `UserAsset` existe en `src_bad/` pero no en `src/`
   - No hay procesamiento de PDF
   - No hay extracción de texto con regex
   - No hay almacenamiento en tabla `user_assets`

3. **Landing Endpoint**: No existe
   - No hay endpoint `/api/candidate/landing` o similar
   - No hay controlador para procesar el formulario inicial
   - No hay comando `CreateUserFromLanding`

4. **Email/Password Flow**: No implementado
   - No hay generación de contraseña aleatoria
   - No hay envío de email de reset
   - No hay token management

#### **Frontend Issues:**

1. **Navigation Flow**: Páginas existen pero navegación incompleta
   - No hay flujo delante/atrás entre páginas
   - No hay estado compartido entre steps
   - No hay progress indicator

2. **API Integration**: Endpoints no conectados
   - LandingPage llama a API que no existe
   - Formularios no están conectados con backend real

3. **PDF Processing**: Frontend preparado pero backend ausente
   - Upload funciona pero no hay procesamiento

## 🎯 **Requerimientos del ONBOARDING.md**

### **Página 1: Email + PDF Upload + Job Application**
- ✅ Frontend existe (`LandingPage.tsx`)
- ❌ Backend endpoint falta
- ❌ PDF text extraction falta
- ❌ Regex name extraction falta
- ❌ UserAsset storage falta
- ❌ Email sending falta
- ❌ User creation logic falta
- ❌ **NUEVO**: CandidateApplication domain falta
- ❌ **NUEVO**: JobPositionId handling en URL falta

### **Páginas 2-5: Candidate Data Flow**
- ✅ Frontend components existen
- ✅ Backend candidate domain completo
- ❌ Navigation flow entre páginas
- ❌ State management compartido

### **Página 6: CV Preview**
- ✅ Frontend component existe (`ResumePage.tsx`)
- ❌ CV generation logic

## 🚀 **Plan de Trabajo Propuesto**

### **FASE 1: Backend Foundation (Prioridad Alta)**

#### **1.1 Crear Dominio CandidateApplication**
```
src/candidate_application/
├── domain/
│   ├── entities/candidate_application.py
│   ├── enums/application_status.py
│   ├── value_objects/candidate_application_id.py
│   └── repositories/candidate_application_repository_interface.py
├── application/
│   ├── commands/create_candidate_application.py
│   ├── commands/update_application_status.py
│   └── queries/get_application_by_candidate_and_position.py
└── infrastructure/
    ├── models/candidate_application_model.py
    └── repositories/candidate_application_repository.py
```

**Entidad CandidateApplication:**
```python
@dataclass
class CandidateApplication:
    id: CandidateApplicationId
    candidate_id: CandidateId
    job_position_id: JobPositionId
    application_status: ApplicationStatusEnum  # applied, reviewing, rejected, accepted
    applied_at: datetime
    updated_at: Optional[datetime]
    notes: Optional[str]
```

#### **1.2 Crear Dominio Notification**
```
src/notification/
├── domain/
│   ├── entities/email_notification.py
│   ├── enums/notification_type.py
│   └── exceptions/notification_exceptions.py
├── application/
│   ├── commands/send_email_command.py
│   └── queries/get_notification_status.py
└── infrastructure/
    ├── services/mailgun_service.py
    └── repositories/notification_repository.py
```

**Archivos clave a crear:**
- `SendEmailCommand` - Comando para enviar email
- `MailgunService` - Servicio para integración con Mailgun API
- `EmailNotification` entity - Para tracking de emails enviados

#### **1.2 Migrar y mejorar UserAsset**
**De `src_bad/` a `src/`:**
- Copiar y adaptar `UserAsset` entity desde `src_bad/user/domain/entities/user_asset.py`
- Crear repositorio completo con interface
- Añadir procesamiento de PDF (PyPDF2 o similar)
- Implementar regex para extracción de nombre/apellidos

**Regex patterns a implementar:**
```python
NAME_PATTERNS = [
    r"Name:\s*([A-Za-z\s]+)",
    r"^([A-Z][a-z]+\s+[A-Z][a-z]+)",  # Firstname Lastname al inicio
    # Más patterns según necesidad
]
```

#### **1.4 Landing Endpoint y User Creation Flow**
**Crear endpoint `/api/candidate/onboarding/landing`:**
- Recibir: email, PDF file, **job_position_id (opcional)**
- Procesar PDF → extraer texto → buscar nombre
- Crear usuario si no existe con password random
- Almacenar UserAsset
- **NUEVO**: Si job_position_id viene, crear CandidateApplication
- Enviar email con reset password link
- Retornar: token de acceso temporal

**Comando actualizado:**
```python
@dataclass
class CreateUserFromLandingCommand:
    email: str
    pdf_file: Optional[bytes]
    pdf_filename: Optional[str]
    job_position_id: Optional[str]  # NUEVO CAMPO
```

**Flujo de negocio actualizado:**
1. Recibir datos del form + optional job_position_id de URL
2. Crear/buscar User
3. Crear Candidate si no existe
4. Procesar PDF y crear UserAsset
5. **NUEVO**: Si job_position_id → crear CandidateApplication
6. Enviar email de bienvenida
7. Return success response

### **FASE 2: Frontend Navigation Flow (Prioridad Media)**

#### **2.1 Onboarding Context y State Management**
**Crear hook personalizado:**
```typescript
// src/hooks/useOnboarding.ts
export const useOnboarding = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [candidateData, setCandidateData] = useState<CandidateFormData>();
  const [jobPositionId, setJobPositionId] = useState<string | null>(null); // NUEVO
  // Navigation helpers
  const nextStep = () => {...};
  const prevStep = () => {...};
  const goToStep = (step: number) => {...};
}
```

**Actualizar LandingPage para manejar jobPositionId de URL:**
```typescript
// En LandingPage.tsx
const [searchParams] = useSearchParams();
const jobPositionId = searchParams.get('jobPositionId');

// Al hacer submit incluir jobPositionId
const handleSubmit = async (e: React.FormEvent) => {
  const formData = new FormData();
  formData.append('email', email);
  if (selectedFile) formData.append('resume_file', selectedFile);
  if (jobPositionId) formData.append('job_position_id', jobPositionId); // NUEVO

  const data = await api.createAccountFromLanding(formData);
};
```

#### **2.2 Progress Indicator Component**
```typescript
// src/components/onboarding/ProgressIndicator.tsx
const steps = [
  "Email & CV",
  "Perfil Personal",
  "Experiencia",
  "Educación",
  "Proyectos",
  "Revisión CV"
];
```

#### **2.3 Navigation Wrapper**
**Envolver páginas en layout común:**
```typescript
// src/components/onboarding/OnboardingLayout.tsx
- Progress indicator
- Botones Anterior/Siguiente
- Manejo de state compartido
```

### **FASE 3: Integration & Polish (Prioridad Baja)**

#### **3.1 API Integration**
- Conectar todos los forms con endpoints reales
- Implementar error handling
- Añadir loading states

#### **3.2 CV Generation**
- Implementar lógica de generación de CV
- Templates de CV
- Export functionality

#### **3.3 Email Templates**
- Diseñar email templates para Mailgun
- Welcome email template
- Password reset template

## 📁 **Archivos a Reutilizar de src_bad/**

### **Pueden aprovecharse (con adaptaciones):**
1. `src_bad/user/domain/entities/user_asset.py` → Migrar a `src/user/`
2. `src_bad/user/application/commands/create_user_from_landing.py` → Adaptar
3. `src_bad/user/application/commands/create_user_asset.py` → Adaptar
4. Algunos patterns de procesamiento de archivos

### **NO reutilizar:**
- Modelos SQLAlchemy antiguos (usar los actuales)
- Handlers con patrones antiguos
- Anything que no siga CLAUDE.md patterns

## ⚠️ **Cumplimiento de CLAUDE.md**

### **Patrones Mandatorios a Seguir:**

1. **Repository Pattern**:
   - Interface en `domain/repositories/{entity}_repository_interface.py`
   - Implementation en `infrastructure/repositories/{entity}_repository.py`

2. **Data Flow**: `Database Model → Repository → Domain Entity → Query Handler → DTO → Controller → Response Schema`

3. **CQRS**: Commands para writes, Queries para reads

4. **No circular imports**: Usar TYPE_CHECKING y string references

### **Arquitectura para nuevos dominios:**
```
src/notification/
├── domain/
│   ├── entities/           # EmailNotification
│   ├── enums/             # NotificationType, Status
│   ├── exceptions/        # NotificationExceptions
│   └── repositories/     # Repository interfaces
├── application/
│   ├── commands/          # SendEmailCommand
│   ├── queries/           # GetNotificationStatusQuery
│   └── handlers/          # Command/Query handlers
└── infrastructure/
    ├── models/            # SQLAlchemy models
    ├── repositories/      # Repository implementations
    └── services/          # External services (Mailgun)
```

## 🕒 **Estimación de Tiempo**

- **Fase 1 Backend**: 3-4 días
- **Fase 2 Frontend**: 2 días
- **Fase 3 Integration**: 1-2 días
- **Total**: ~1 semana de desarrollo

## 🎯 **Entregables**

1. **Sistema completo de onboarding** funcional
2. **6 páginas** con navegación fluida
3. **PDF processing** con extracción de datos
4. **Email notification** system con Mailgun
5. **CV generation** básico
6. **Cumplimiento 100%** de patrones CLAUDE.md

¿Procedo con la implementación siguiendo esta planificación?