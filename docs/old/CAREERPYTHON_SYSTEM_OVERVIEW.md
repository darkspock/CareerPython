# CareerPython - Resumen del Sistema Completo

**Fecha**: 2025-01-25  
**Versión**: 1.0  
**Propósito**: Documento de referencia para el asistente de IA sobre la funcionalidad completa del sistema CareerPython

---

## Tabla de Contenidos

1. [Visión General del Sistema](#visión-general-del-sistema)
2. [Arquitectura Técnica](#arquitectura-técnica)
3. [Módulos Principales](#módulos-principales)
4. [Sistema de Empresas (Company)](#sistema-de-empresas-company)
5. [Sistema de Flujos de Trabajo (Workflow)](#sistema-de-flujos-de-trabajo-workflow)
6. [Sistema de Candidatos y Aplicaciones](#sistema-de-candidatos-y-aplicaciones)
7. [Sistema de Almacenamiento](#sistema-de-almacenamiento)
8. [Sistema de Comunicación](#sistema-de-comunicación)
9. [Estado de Implementación](#estado-de-implementación)
10. [Próximos Pasos](#próximos-pasos)

---

## Visión General del Sistema

CareerPython es una plataforma de gestión de talento (ATS - Applicant Tracking System) que conecta candidatos con empresas a través de un sistema de flujos de trabajo personalizables. El sistema está diseñado con arquitectura hexagonal/clean architecture y sigue patrones CQRS.

### Principios Fundamentales

1. **Los datos son del candidato**: El candidato es el propietario absoluto de su información
2. **Privacidad por defecto**: Los datos del perfil del candidato son PRIVADOS, la empresa NO puede verlos
3. **CRM Desacoplado**: CompanyCandidate es un "Lead" independiente, NO es una relación con Candidate
4. **Autorización explícita**: Solo cuando el candidato aplica formalmente autoriza qué datos compartir
5. **Contexto de candidatura**: Los datos se comparten POR candidatura, no globalmente

### Flujos de Negocio Principales

1. **Sourcing (Prospección)**: Gestión de leads y candidatos que aún no han aplicado
2. **Evaluation (Selección)**: Proceso formal de selección para posiciones específicas
3. **Offer and Pre-Onboarding**: Formalización de ofertas y preparación para onboarding

---

## Arquitectura Técnica

### Patrón de Arquitectura

```
Presentation Layer (Controllers, Routers, Schemas)
    ↓
Application Layer (Commands, Queries, Handlers, DTOs)
    ↓
Domain Layer (Entities, Value Objects, Events)
    ↓
Infrastructure Layer (Repositories, Models, External Services)
```

### Tecnologías

- **Backend**: Python + FastAPI
- **Frontend**: React + TypeScript + Vite
- **Base de Datos**: PostgreSQL + Alembic (migraciones)
- **Almacenamiento**: Local (desarrollo) / AWS S3 (producción)
- **Autenticación**: JWT con contexto de empresa
- **Arquitectura**: Clean Architecture + CQRS

### Estructura del Proyecto

```
src/
├── company/                    # Módulo de empresas
├── company_candidate/          # Relación empresa-candidato
├── company_workflow/          # Flujos de trabajo
├── candidate/                 # Módulo de candidatos
├── candidate_application/     # Aplicaciones de candidatos
├── shared/                    # Utilidades compartidas
└── [otros módulos...]

client-vite/                   # Frontend React
├── src/
│   ├── pages/company/         # Páginas de empresa
│   ├── components/            # Componentes reutilizables
│   ├── services/              # Servicios API
│   └── types/                 # Tipos TypeScript
```

---

## Módulos Principales

### 1. Company (Empresas) ✅ COMPLETADO

**Funcionalidad**: Gestión de empresas y usuarios de empresa

**Entidades Principales**:
- `Company`: Información de la empresa
- `CompanyUser`: Usuarios que trabajan para la empresa

**Estados**:
- ✅ Domain Layer: Entidades, Value Objects, Enums
- ✅ Infrastructure: Repositorios, Modelos, Migraciones
- ✅ Application: Commands, Queries, Handlers
- ✅ Presentation: Controllers, Routers, Schemas
- ✅ Endpoints: 7 endpoints operativos

### 2. CompanyCandidate (Relación Empresa-Candidato) ✅ COMPLETADO

**Funcionalidad**: Gestión de leads/candidatos en el CRM de la empresa

**Entidades Principales**:
- `CompanyCandidate`: Lead independiente (no es relación directa con Candidate)
- `CandidateInvitation`: Invitaciones para que leads se registren
- `CandidateComment`: Comentarios de la empresa sobre candidatos

**Características**:
- Dos flujos: candidato aplica (con candidate_id) vs empresa agrega lead (sin candidate_id)
- Datos básicos copiados: nombre, email, teléfono, país, linkedin
- Datos privados del Candidate NO son visibles para la empresa
- Sistema de ownership: company_owned vs user_owned

### 3. CompanyWorkflow (Flujos de Trabajo) ✅ COMPLETADO

**Funcionalidad**: Flujos de trabajo personalizables para procesos de selección

**Entidades Principales**:
- `CompanyWorkflow`: Plantilla de flujo de trabajo
- `WorkflowStage`: Etapas individuales dentro del flujo

**Tipos de Workflow**:
- **Prospecting**: Gestión de leads (etapas fijas)
- **Selection**: Proceso de selección (personalizable)
- **Offer and Pre-Onboarding**: Formalización de ofertas

**Configuración Avanzada**:
- Roles predeterminados por etapa
- Usuarios asignados por defecto
- Plantillas de email automáticas
- Fechas límite y costos estimados
- Campos personalizados

### 4. CandidateApplication (Aplicaciones Formales) ⏳ PENDIENTE

**Funcionalidad**: Candidaturas formales a posiciones específicas

**Características Planificadas**:
- Vinculación a posición específica
- Autorización de datos a compartir (shared_data)
- Generación de PDF de CV
- Versionado de CV con actualizaciones
- Workflow específico por posición

---

## Sistema de Empresas (Company)

### Modelo de Datos

```python
# Company
{
    "id": "UUID",
    "name": "Nombre de la empresa",
    "domain": "dominio.com",
    "logo_url": "URL del logo",
    "settings": "JSON configuración",
    "status": "active|suspended|deleted",
    "created_at": "datetime",
    "updated_at": "datetime"
}

# CompanyUser
{
    "id": "UUID",
    "company_id": "UUID",
    "user_id": "UUID",
    "role": "admin|recruiter|viewer",
    "permissions": "JSON permisos",
    "status": "active|inactive",
    "roles": "['HR Manager', 'Tech Lead']"  # Nuevo campo
}
```

### Endpoints Implementados

```
POST   /api/company/{company_id}           # Crear empresa
GET    /api/company/{company_id}           # Obtener empresa
PUT    /api/company/{company_id}           # Actualizar empresa
DELETE /api/company/{company_id}           # Eliminar empresa
POST   /api/company/{company_id}/suspend   # Suspender empresa
POST   /api/company/{company_id}/activate  # Activar empresa
GET    /api/companies                      # Listar empresas
```

---

## Sistema de Flujos de Trabajo (Workflow)

### Arquitectura del Workflow

El sistema permite crear flujos de trabajo completamente personalizables con:

1. **Etapas Configurables**:
   - Nombre y descripción
   - Tipo: inicial, intermedia, final, personalizada
   - Orden secuencial
   - Duración estimada y fecha límite
   - Costo estimado

2. **Asignación de Usuarios**:
   - Roles predeterminados por etapa
   - Usuarios específicos asignados
   - Sistema de permisos granular

3. **Comunicación Automática**:
   - Plantillas de email por etapa
   - Texto personalizado adicional
   - Variables dinámicas (nombre, posición, empresa, etc.)

4. **Campos Personalizados**:
   - Tipos: texto, dropdown, checkbox, fecha, archivo, moneda, etc.
   - Configuración por etapa: oculto, obligatorio, recomendado, opcional
   - Validaciones dinámicas

### Modelo de Datos

```python
# CompanyWorkflow
{
    "id": "UUID",
    "company_id": "UUID",
    "name": "Proceso Técnico",
    "description": "Flujo para desarrolladores",
    "workflow_type": "prospecting|selection",
    "status": "active|inactive|archived",
    "is_default": "boolean"
}

# WorkflowStage
{
    "id": "UUID",
    "workflow_id": "UUID",
    "name": "Entrevista Técnica",
    "stage_type": "initial|intermediate|final|custom",
    "order": "integer",
    "estimated_duration_days": "integer",
    "deadline_days": "integer",
    "estimated_cost": "decimal",
    "default_roles": "['Tech Lead', 'HR Manager']",
    "default_assigned_users": "['user_id_1', 'user_id_2']",
    "email_template_id": "UUID",
    "custom_email_text": "string"
}
```

### Sistema de Tareas

**Priorización Inteligente**:
```
Prioridad Total = 100 (base) + peso_fecha_límite + peso_posición + peso_candidato

Peso por fecha límite:
- Vencida: +50
- Vence hoy: +30
- Vence en 1-2 días: +20
- Vence en 3-5 días: +10
- Vence en 6+ días: 0

Peso por posición: prioridad_posición * 10 (0-50)
Peso por candidato: prioridad_candidato * 5 (0-25)
```

**Tipos de Tareas**:
1. **Asignadas Directamente**: Usuario específicamente asignado a la etapa
2. **Disponibles por Rol**: Etapas que coinciden con roles del usuario

---

## Sistema de Candidatos y Aplicaciones

### CompanyCandidate (Lead Management)

**Dos Flujos de Creación**:

1. **Candidato Aplica** (candidate_id presente):
   - Candidato aplica a posición/empresa
   - Se crea CompanyCandidate con candidate_id
   - Se COPIAN solo datos básicos autorizados
   - La empresa NO puede ver perfil completo

2. **Empresa Agrega Lead** (candidate_id = null):
   - Empresa agrega lead manualmente
   - Se crea CompanyCandidate sin candidate_id
   - Empresa rellena datos que tiene
   - Se puede enviar invitación para vincular

### CandidateApplication (Aplicación Formal)

**Características Planificadas**:
- Vinculación a posición específica
- Autorización granular de datos (shared_data)
- Generación y versionado de CV en PDF
- Política de actualización controlada por empresa
- Historial de versiones con changelog

**Estructura de Datos**:
```python
# SharedData (lo que autoriza compartir el candidato)
{
    "include_education": "boolean",
    "include_experience": "boolean", 
    "include_projects": "boolean",
    "include_skills": "boolean",
    "include_languages": "boolean",
    "resume_ids": "['resume_1', 'resume_2']",
    "portfolio_url": "string"
}

# ApplicationData (datos capturados durante el proceso)
{
    "salary_expectation": "120000",
    "available_start_date": "2025-02-01",
    "technical_test_score": "85",
    "interview_notes": "Excellent communication skills",
    "stage_history": "[...]"
}
```

---

## Sistema de Almacenamiento

### Abstracción de Storage

El sistema implementa una abstracción que permite cambiar entre almacenamiento local (desarrollo) y S3 (producción) sin modificar código.

**Implementaciones**:
- `LocalStorageService`: Almacena en filesystem local
- `S3StorageService`: Almacena en AWS S3

**Tipos de Archivos**:
- `CANDIDATE_RESUME`: CVs de candidatos
- `APPLICATION_RESUME`: CVs específicos por aplicación
- `COMPANY_LOGO`: Logos de empresas
- `ATTACHMENT`: Archivos adjuntos

**Estructura de Paths**:
```
company/{company_id}/
├── candidates/{candidate_id}/resume.pdf
├── applications/{application_id}/
│   ├── resume_v1.pdf
│   ├── resume_v2.pdf
│   └── resume_v3.pdf
└── logos/logo.png
```

### Configuración

```bash
# Variables de entorno
STORAGE_TYPE=local  # o 's3'
LOCAL_STORAGE_PATH=uploads
LOCAL_STORAGE_URL=http://localhost:8000/uploads
AWS_S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

---

## Sistema de Comunicación

### Pseudo-Chat con Email

**Flujo de Comunicación**:
1. Empresa envía mensaje → Se guarda en DB + Email al candidato
2. Candidato recibe email → Clic en "Ver Conversación"
3. Candidato responde en-app → Se guarda en DB (NO email a empresa)
4. Empresa ve respuesta en dashboard

**Ventajas**:
- Evita saturación de emails
- Mantiene conversación organizada
- Historial completo y trazable

### Plantillas de Email

**Variables Soportadas**:
- `{{candidate_name}}`: Nombre completo
- `{{candidate_first_name}}`: Primer nombre
- `{{position_title}}`: Título de la posición
- `{{company_name}}`: Nombre de la empresa
- `{{stage_name}}`: Nombre de la etapa
- `{{custom_text}}`: Texto personalizado

**Configuración por Etapa**:
- Plantilla de email predeterminada
- Texto personalizado adicional
- Envío automático al cambiar de etapa

---

## Estado de Implementación

### ✅ Módulos Completados

1. **Company**: CRUD completo, autenticación, gestión de usuarios
2. **CompanyUser**: Roles, permisos, login con JWT
3. **CompanyCandidate**: Gestión de leads, ownership, visibilidad
4. **CompanyWorkflow**: Flujos personalizables, etapas configurables
5. **WorkflowStage**: Configuración avanzada, roles, emails, costos

### ⏳ Módulos Pendientes

1. **CandidateInvitation**: Sistema de invitaciones (ALTA prioridad)
2. **CandidateComment**: Comentarios privados/compartidos (ALTA prioridad)
3. **CandidateAccessLog**: Auditoría y GDPR compliance (MEDIA prioridad)
4. **CandidateApplication**: Aplicaciones formales con versionado de CV
5. **Position**: Gestión de posiciones vacantes
6. **PositionStageAssignment**: Asignación de usuarios a etapas
7. **EmailTemplate**: Sistema de plantillas de email
8. **WorkflowCustomField**: Campos personalizados por workflow

### 📊 Estadísticas

- **Tablas Creadas**: 4/7 (57%)
- **Endpoints Implementados**: ~46 endpoints
- **Arquitectura**: 100% Clean Architecture + CQRS
- **Testing**: Pendiente (unit + integration + E2E)

---

## Próximos Pasos

### Inmediato (1-2 semanas)

1. **Implementar CandidateInvitation**:
   - Sistema de invitaciones para leads
   - Tokens únicos con expiración
   - Emails de invitación
   - Vinculación automática al registrarse

2. **Implementar CandidateComment**:
   - Comentarios privados vs compartidos
   - Soft delete
   - Contexto (interview, screening, review)

### Corto Plazo (1 mes)

3. **Implementar CandidateApplication**:
   - Aplicaciones formales a posiciones
   - Sistema de autorización de datos
   - Generación y versionado de CV
   - Política de actualización controlada

4. **Implementar Position**:
   - Gestión de posiciones vacantes
   - Vinculación con workflows
   - Asignación de usuarios a etapas

### Mediano Plazo (2-3 meses)

5. **Sistema de Campos Personalizados**
6. **Sistema de Plantillas de Email**
7. **Dashboard de Analytics**
8. **Sistema de Notificaciones**

---

## Reglas de Desarrollo

### Orden de Implementación

Seguir estrictamente el flujo de 3 fases:

1. **Fase 1**: Domain Layer (Entidades, Value Objects, Enums) → STOP ✋
2. **Fase 2**: Infrastructure (Repositorios, Mappers, Modelos, Migraciones) → STOP ✋  
3. **Fase 3**: Application & Presentation (Endpoints, Commands, Queries) → DONE ✅

### Convenciones de Naming

- **Entities**: `Company`, `CompanyWorkflow`
- **Models**: `CompanyModel`, `CompanyWorkflowModel`
- **Commands**: `CreateCompanyCommand`, `UpdateCompanyCommand`
- **Queries**: `GetCompanyByIdQuery`, `ListCompaniesQuery`
- **DTOs**: `CompanyDto`, `CompanyWorkflowDto`
- **Requests**: `CreateCompanyRequest`, `UpdateCompanyRequest`
- **Responses**: `CompanyResponse`, `CompanyListResponse`

### Testing

Cada fase debe tener tests:
- **Fase 1**: Tests unitarios de entidades
- **Fase 2**: Tests de repositorios (con DB de test)
- **Fase 3**: Tests de endpoints (integration tests)

---

## Consideraciones Técnicas

### Performance

- **Índices de BD**: Optimizados para queries frecuentes
- **Caching**: Workflows y permisos de usuario
- **Lazy Loading**: PDFs generados bajo demanda

### Seguridad

- **Autorización**: Verificación de permisos en cada operación
- **Privacidad**: Solo datos autorizados por candidato
- **Auditoría**: Log de todas las acciones sensibles

### Escalabilidad

- **Arquitectura Modular**: Fácil agregar nuevos módulos
- **CQRS**: Separación clara de lectura/escritura
- **Event Sourcing**: Preparado para eventos de dominio

---

## Conclusión

CareerPython es un sistema ATS completo y moderno que implementa las mejores prácticas de arquitectura de software. El sistema está diseñado para ser:

- **Flexible**: Flujos de trabajo completamente personalizables
- **Escalable**: Arquitectura modular y clean
- **Seguro**: Control granular de permisos y privacidad
- **Mantenible**: Código bien estructurado y testeable
- **User-Friendly**: Interfaces intuitivas y experiencia fluida

El estado actual muestra una base sólida con los módulos core implementados, listo para continuar con las funcionalidades avanzadas que completarán el ecosistema de gestión de talento.

---

**Documento generado automáticamente el 2025-01-25**  
**Basado en análisis de toda la documentación del proyecto**
