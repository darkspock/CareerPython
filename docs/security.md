# Sistema de Roles y Gestión de Usuarios - Análisis y Plan de Implementación

## Estado Actual del Sistema

### Entidades y Modelos Existentes

El sistema ya cuenta con una base para la gestión de usuarios de empresa:

- **Entidad `CompanyUser`**: Representa usuarios que trabajan para una empresa (reclutadores, HR, managers)
  - Ubicación: `src/company/domain/entities/company_user.py`
  - Campos principales: id, company_id, user_id, role, permissions, status

- **Value Object `CompanyUserPermissions`**: Permisos actuales del usuario
  - Ubicación: `src/company/domain/value_objects/company_user_permissions.py`
  - Permisos actuales:
    - `can_create_candidates`
    - `can_invite_candidates`
    - `can_add_comments`
    - `can_manage_users`
    - `can_view_analytics`

- **Enum `CompanyUserRole`**: Roles actuales del sistema
  - Ubicación: `src/company/domain/enums/company_user_role.py`
  - Roles disponibles:
    - `ADMIN`: Administrador
    - `RECRUITER`: Reclutador
    - `VIEWER`: Visualizador

- **Repositorio y Modelos**: Ya existe infraestructura básica de persistencia
  - Modelo: `src/company/infrastructure/models/company_user_model.py`
  - Repositorio: `src/company/infrastructure/repositories/company_user_repository.py`

## Requerimientos del Sistema

### Fase 1: Gestión de Usuarios

#### 1.1 Interfaz de Usuario
- **Menú de "Usuarios"** en el frontend para gestión de usuarios de la empresa
- Acceso desde el panel de administración de la empresa

#### 1.2 Invitación de Usuarios
Funcionalidades requeridas:
- Opción de **"Invitar Usuarios"**
  - Envío de correo electrónico con link de invitación
  - Mostrar el link por si se quiere compartir por otros medios (manual)
  - Token de invitación único y con expiración
  - Información de la empresa y mensaje personalizado opcional

#### 1.3 Flujo de Registro por Invitación
El usuario invitado puede seguir dos caminos:

**Caso A: Usuario Nuevo**
- Pincha el link de invitación
- Se muestra pantalla de aceptación para unirse a la empresa
- Se solicita: email, nombre y contraseña
- **IMPORTANTE**: No se crea candidato para este usuario (solo User + CompanyUser)

**Caso B: Usuario Existente**
- Pincha el link de invitación
- Se muestra pantalla de aceptación
- Si el usuario ya existe en el sistema, se vincula automáticamente a la empresa
- No requiere registro adicional

#### 1.4 Eliminación de Usuarios
- Se pueden quitar usuarios de la empresa
- **Validaciones críticas**:
  - Al menos un usuario debe ser ADMIN (no se puede eliminar el último admin)
  - No puedes eliminarte a ti mismo

#### 1.5 Asignación de Roles
- Se pueden asignar roles a los usuarios
- Los roles determinan los permisos del usuario

### Fase 2: Gestión de Roles y Permisos

#### 2.1 Sistema de Permisos por Acciones

El documento define una serie de acciones predefinidas en el sistema, y los roles pueden tener o no acceso a cada acción:

**Acciones identificadas**:
- Agregar Candidatos
- Eliminar Candidatos
- Ver Candidatos
- Cambiar Configuración
- Agregar comentarios
- Cambiar de fase

**Nota importante**: En esta primera iteración, **NO vamos a controlar el acceso** en los endpoints, solo haremos la gestión de roles y permisos. La validación de permisos en los endpoints será una fase posterior.

#### 2.2 Comando de Inicialización de Roles

Se necesita un comando que:
- Inicialice los roles del sistema
- Borre los roles actuales
- Cree los roles de nuevo desde cero
- **Manejo de usuarios existentes**: Si hay usuarios con roles asignados, se les borra la asignación y se ponen todos como ADMIN temporalmente

### Fase 3: Definición de Roles

#### 3.1 Roles Sugeridos

El documento propone los siguientes roles (requiere definir nombres técnicos apropiados):

1. **Administrador**
   - Control total del sistema
   - Gestión de usuarios y configuración

2. **Recruiter/Screener** (Reclutador/Filtrador)
   - Persona que se encarga de buscar candidatos y filtrarlos
   - Permisos: ver, agregar candidatos

3. **Interview Manager** (Gestor de Entrevistas)
   - Persona que se encarga de gestionar el proceso de entrevistas
   - Permisos: ver candidatos, agregar comentarios, cambiar de fase

4. **Hiring Manager** (Gestor de Contratación)
   - Persona encargada de la fase de contratación y onboarding
   - Permisos: ver candidatos, cambiar de fase, agregar comentarios

5. **External Interviewer** (Entrevistador Externo)
   - Entrevistadores externos a RRHH, como un manager o un ingeniero
   - Permisos limitados: ver candidatos específicos, agregar comentarios

6. **Supervisor**
   - Rol de supervisión con permisos intermedios
   - Ver candidatos y analytics

#### 3.2 Extensión Futura

- Más adelante se implementará también control de permisos por **phase** y **workflow**
- Esta fase inicial se enfoca solo en permisos generales a nivel de empresa

## Gaps Identificados

### 1. Sistema de Invitaciones
- ❌ No existe entidad/modelo para invitaciones de usuarios de empresa
- ❌ No hay token de invitación para `CompanyUser`
- ❌ No hay endpoints para gestionar invitaciones
- ❌ No hay endpoints para aceptar invitaciones
- ❌ No existe servicio de email para invitaciones de usuarios

### 2. Permisos Incompletos
- ✅ `can_create_candidates` (existe como `can_create_candidates`)
- ✅ `can_add_comments` (existe)
- ❌ `can_delete_candidates` (falta)
- ❌ `can_view_candidates` (falta explícito, aunque podría inferirse)
- ❌ `can_change_settings` (falta)
- ❌ `can_change_phase` (falta)

### 3. Validaciones de Negocio
- ❌ No hay validación de "al menos un admin siempre activo"
- ❌ No hay validación de "no auto-eliminación"
- ❌ No hay validación de expiración de invitaciones

### 4. Sistema de Roles
- ⚠️ Roles están hardcodeados (ADMIN, RECRUITER, VIEWER)
- ❌ Falta sistema de roles configurables con permisos asignables dinámicamente
- **Decisión requerida**: ¿Mantenemos roles fijos o implementamos sistema de roles dinámicos?

## Arquitectura Propuesta

Siguiendo las reglas del repositorio, la implementación debe seguir 3 fases estrictas:

### Fase 1: Domain Layer (Entidades y Lógica de Negocio)

#### 1.1 Nuevos Enums
```
src/company/domain/enums/
  - company_user_invitation_status.py
    * PENDING
    * ACCEPTED
    * REJECTED
    * EXPIRED
    * CANCELLED
```

#### 1.2 Expansión de Permisos
```
src/company/domain/value_objects/company_user_permissions.py
  - Agregar nuevos permisos:
    * can_delete_candidates: bool
    * can_view_candidates: bool (explícito)
    * can_change_settings: bool
    * can_change_phase: bool
```

#### 1.3 Nueva Entidad: CompanyUserInvitation
```
src/company/domain/entities/company_user_invitation.py
  - id: CompanyUserInvitationId
  - company_id: CompanyId
  - email: str
  - invited_by_user_id: CompanyUserId
  - token: str (único, seguro)
  - status: InvitationStatus
  - expires_at: datetime
  - accepted_at: Optional[datetime]
  - rejected_at: Optional[datetime]
  - created_at: datetime
  - updated_at: datetime

  Métodos:
  - create(): Factory method
  - accept(): Cambia status a ACCEPTED
  - reject(): Cambia status a REJECTED
  - expire(): Cambia status a EXPIRED
  - cancel(): Cambia status a CANCELLED
  - is_expired(): Validación de expiración
```

#### 1.4 Actualización de Entidad CompanyUser
```
src/company/domain/entities/company_user.py
  - Agregar método: remove()
  - Validaciones:
    * ensure_at_least_one_admin() en métodos de eliminación
    * prevent_self_removal() en métodos de eliminación
```

#### 1.5 Nuevos Value Objects
```
src/company/domain/value_objects/
  - company_user_invitation_id.py
  - invitation_token.py (con validación de formato)
```

**FIN DE FASE 1** - Confirmar con el usuario antes de continuar

---

### Fase 2: Infrastructure Layer (Persistencia)

#### 2.1 Nuevo Modelo SQLAlchemy
```
src/company/infrastructure/models/company_user_invitation_model.py
  - Tabla: company_user_invitations
  - Campos según entidad
  - Índices: email, token, company_id
  - Foreign keys: company_id, invited_by_user_id
```

#### 2.2 Nuevo Repositorio
```
src/company/infrastructure/repositories/company_user_invitation_repository.py
  - Interface en: src/company/domain/infrastructure/company_user_invitation_repository_interface.py
  - Métodos:
    * save()
    * find_by_id()
    * find_by_token()
    * find_by_email_and_company()
    * find_pending_by_email()
    * find_expired()
```

#### 2.3 Migraciones
- Migración para tabla `company_user_invitations`
- Migración para expandir permisos en `company_users` (si necesario)
- Índices para performance

#### 2.4 Actualización de Repositorio CompanyUser
```
src/company/infrastructure/repositories/company_user_repository.py
  - Agregar validaciones:
    * count_admins_by_company()
    * ensure_at_least_one_admin_remains()
```

**FIN DE FASE 2** - Confirmar con el usuario antes de continuar

---

### Fase 3: Application & Presentation Layer (API)

#### 3.1 Commands (Operaciones de Escritura)
```
src/company/application/commands/
  - invite_company_user_command.py
    * InviteCompanyUserCommand
    * InviteCompanyUserCommandHandler
    * Genera token, crea invitación, envía email

  - accept_user_invitation_command.py
    * AcceptUserInvitationCommand
    * AcceptUserInvitationCommandHandler
    * Valida token, crea/vincula User, crea CompanyUser

  - remove_company_user_command.py
    * RemoveCompanyUserCommand
    * RemoveCompanyUserCommandHandler
    * Valida al menos un admin, no auto-eliminación

  - assign_role_to_user_command.py
    * AssignRoleToUserCommand
    * AssignRoleToUserCommandHandler

  - initialize_roles_command.py
    * InitializeRolesCommand
    * InitializeRolesCommandHandler
    * Borra roles actuales, crea nuevos, asigna admin temporal a usuarios existentes
```

#### 3.2 Queries (Operaciones de Lectura)
```
src/company/application/queries/
  - get_user_invitation_query.py
    * GetUserInvitationQuery
    * GetUserInvitationQueryHandler
    * Por token o por email

  - list_company_users_query.py
    * ListCompanyUsersQuery
    * ListCompanyUsersQueryHandler

  - list_user_permissions_query.py
    * ListUserPermissionsQuery
    * ListUserPermissionsQueryHandler
```

#### 3.3 DTOs
```
src/company/application/dtos/
  - company_user_invitation_dto.py
  - user_permissions_dto.py (expandido)
```

#### 3.4 Request Schemas
```
presentation/schemas/ o adapters/http/company/schemas/
  - InviteCompanyUserRequest
  - AcceptInvitationRequest
  - RemoveCompanyUserRequest
  - AssignRoleRequest
```

#### 3.5 Response Schemas
```
presentation/schemas/ o adapters/http/company/schemas/
  - CompanyUserInvitationResponse
  - UserInvitationLinkResponse (con link para compartir)
  - CompanyUserListResponse
```

#### 3.6 Controllers
```
presentation/controllers/ o adapters/http/company/controllers/
  - CompanyUserInvitationController
  - CompanyUserManagementController
```

#### 3.7 Routers
```
adapters/http/company/routers/
  - Endpoints:
    * POST /companies/{company_id}/users/invite
    * POST /invitations/accept
    * GET /invitations/{token}
    * DELETE /companies/{company_id}/users/{user_id}
    * PUT /companies/{company_id}/users/{user_id}/role
    * GET /companies/{company_id}/users
    * POST /admin/roles/initialize (comando de inicialización)
```

#### 3.8 Servicio de Email
```
src/notification/infrastructure/services/
  - Agregar método en EmailServiceInterface:
    * send_user_invitation()
  - Implementar en SMTPEmailService y MailgunService
  - Template HTML: user_invitation.html
```

**FIN DE FASE 3** - Feature completamente implementada

---

## Plan de Implementación Detallado

### Priorización

1. **Fase 1 Prioritaria**: Gestión básica de usuarios
   - Invitación de usuarios
   - Aceptación de invitaciones
   - Eliminación con validaciones

2. **Fase 2 Prioritaria**: Expansión de permisos
   - Agregar permisos faltantes
   - Actualizar value objects y entidades

3. **Fase 3**: Sistema de roles
   - Definir nombres técnicos de roles
   - Comando de inicialización
   - Asignación de roles

### Nombres de Roles Propuestos

Mapeo sugerido de roles:

| Nombre Técnico | Nombre en Español | Descripción |
|---------------|-------------------|-------------|
| `ADMIN` | Administrador | Control total |
| `RECRUITER` | Reclutador | Buscar y filtrar candidatos |
| `INTERVIEW_MANAGER` | Gestor de Entrevistas | Gestionar proceso de entrevistas |
| `HIRING_MANAGER` | Gestor de Contratación | Contratación y onboarding |
| `EXTERNAL_INTERVIEWER` | Entrevistador Externo | Entrevistadores externos (limitado) |
| `SUPERVISOR` | Supervisor | Supervisión y analytics |
| `VIEWER` | Visualizador | Solo lectura (mantener para retrocompatibilidad) |

### Validaciones Críticas a Implementar

1. **Validación de Al Menos Un Admin**
   ```python
   def remove(self, user_id: UserId, company_id: CompanyId) -> None:
       # Antes de eliminar, validar que no sea el último admin
       admin_count = self.repository.count_admins_by_company(company_id)
       user_to_remove = self.repository.find_by_user_and_company(user_id, company_id)
       
       if user_to_remove.role == CompanyUserRole.ADMIN and admin_count <= 1:
           raise CompanyValidationError("Cannot remove last admin user")
   ```

2. **Validación de No Auto-Eliminación**
   ```python
   def remove(self, user_id: UserId, current_user_id: UserId) -> None:
       if user_id == current_user_id:
           raise CompanyValidationError("Cannot remove yourself")
   ```

3. **Validación de Expiración de Invitaciones**
   ```python
   def is_expired(self) -> bool:
       return datetime.utcnow() > self.expires_at
   
   def accept(self) -> "CompanyUserInvitation":
       if self.is_expired():
           raise CompanyValidationError("Invitation has expired")
       if self.status != InvitationStatus.PENDING:
           raise CompanyValidationError("Invitation is not pending")
   ```

### Integración con Sistema Existente

1. **Servicio de Email**
   - Reutilizar `EmailServiceInterface`
   - Nuevo método: `send_user_invitation(email, invitation_token, company_name)`
   - Template HTML similar a `password_reset.html`

2. **Sistema de Usuarios**
   - Integrar con entidad `User` existente
   - Usar `UserId` para vinculación
   - No crear `Candidate` para usuarios invitados (solo `User` + `CompanyUser`)

3. **Autenticación**
   - Reutilizar sistema de autenticación actual
   - El link de invitación puede llevar a página de registro/login
   - Si el usuario ya está autenticado, aceptar automáticamente

### Consideraciones de Seguridad

1. **Tokens de Invitación**
   - Generar con `secrets.token_urlsafe(32)` (similar a password reset)
   - Expiración: 7-30 días (configurable)
   - Único por invitación
   - No reutilizable (cambiar status después de uso)

2. **Validación de Email**
   - Verificar que el email no esté ya vinculado a la empresa
   - Un email solo puede tener una invitación pendiente por empresa
   - Validar formato de email

3. **Auditoría**
   - Registrar quién invitó a quién
   - Timestamp de creación y aceptación
   - Logs de eliminación de usuarios

## Preguntas y Decisiones Pendientes

1. **¿Sistema de roles dinámicos o fijos?**
   - Opción A: Roles fijos predefinidos (más simple, actual)
   - Opción B: Roles configurables dinámicamente (más flexible, más complejo)
   - **Recomendación**: Empezar con roles fijos, migrar a dinámicos después

2. **Duración de expiración de invitaciones**
   - Propuesta: 7 días (similar a password reset: 24 horas)
   - Configurable vía settings

3. **¿Permisos a nivel de workflow/phase en esta fase?**
   - **Decisión**: NO, solo permisos generales a nivel de empresa
   - Workflow/phase será fase futura

4. **Nombres finales de roles**
   - Requiere aprobación del equipo
   - Los 6 roles propuestos vs. mantener solo los 3 actuales más algunos nuevos

## Próximos Pasos

1. ✅ Análisis completado
2. ⏳ **Confirmación del usuario para iniciar Fase 1**
3. ⏳ Implementar Domain Layer (Fase 1)
4. ⏳ Implementar Infrastructure Layer (Fase 2)
5. ⏳ Implementar Application & Presentation Layer (Fase 3)
6. ⏳ Tests unitarios e integración
7. ⏳ Documentación de API

---

**Última actualización**: Análisis inicial completado
**Estado**: Listo para implementación siguiendo el workflow de 3 fases del repositorio
