# Plan de Tareas: Sistema de Roles y Gestión de Usuarios

Este documento contiene las tareas específicas para implementar el sistema de roles y gestión de usuarios según el análisis en `security.md`.

**IMPORTANTE**: Seguir estrictamente el orden de las fases. No avanzar a la siguiente fase sin confirmación del usuario.

---

## FASE 1: Domain Layer (Entidades y Lógica de Negocio)

### Tarea 1.1: Expandir Enums

#### 1.1.1 Enum de Estado de Invitación
- [x] Crear `src/company/domain/enums/company_user_invitation_status.py`
  - [x] `PENDING`: Invitación pendiente
  - [x] `ACCEPTED`: Invitación aceptada
  - [x] `REJECTED`: Invitación rechazada
  - [x] `EXPIRED`: Invitación expirada
  - [x] `CANCELLED`: Invitación cancelada
  - [x] Documentar cada valor con docstring
- [x] Actualizar `src/company/domain/enums/__init__.py` para exportar el nuevo enum

#### 1.1.2 Expandir Roles (Opcional - verificar si se necesita)
- [x] Revisar si se necesitan nuevos roles además de ADMIN, RECRUITER, VIEWER
- [x] Se mantiene un solo rol principal por ahora (diseño actual)
- [x] Roles secundarios se implementarán más adelante

### Tarea 1.2: Expandir Value Objects

#### 1.2.1 Expandir CompanyUserPermissions
- [x] Actualizar `src/company/domain/value_objects/company_user_permissions.py`
  - [x] Agregar `can_delete_candidates: bool`
  - [x] Agregar `can_view_candidates: bool` (hacer explícito)
  - [x] Agregar `can_change_settings: bool`
  - [x] Agregar `can_change_phase: bool`
  - [x] Actualizar `to_dict()` para incluir nuevos permisos
  - [x] Actualizar `from_dict()` para incluir nuevos permisos
  - [x] Actualizar métodos `default_for_admin()`, `default_for_recruiter()`, `default_for_viewer()` con valores apropiados

#### 1.2.2 Nuevo Value Object: CompanyUserInvitationId
- [x] Crear `src/company/domain/value_objects/company_user_invitation_id.py`
  - [x] Heredar de clase base o seguir patrón similar a `CompanyUserId`
  - [x] Validación de formato si aplica

#### 1.2.3 Nuevo Value Object: InvitationToken
- [x] Crear `src/company/domain/value_objects/invitation_token.py`
  - [x] Inmutable
  - [x] Validación de formato (mínimo 16 caracteres)
  - [x] Método `generate()` estático para generar token seguro

### Tarea 1.3: Nueva Entidad: CompanyUserInvitation

- [x] Crear `src/company/domain/entities/company_user_invitation.py`
  - [x] Constructor con todos los parámetros requeridos (sin valores por defecto)
    - [x] `id: CompanyUserInvitationId`
    - [x] `company_id: CompanyId`
    - [x] `email: str`
    - [x] `invited_by_user_id: CompanyUserId`
    - [x] `token: InvitationToken`
    - [x] `status: CompanyUserInvitationStatus`
    - [x] `expires_at: datetime`
    - [x] `accepted_at: Optional[datetime]`
    - [x] `rejected_at: Optional[datetime]`
    - [x] `created_at: datetime`
    - [x] `updated_at: datetime`
  - [x] Propiedades públicas (NO usar @property para getters/setters)
  - [x] Factory method `create()`:
    - [x] Genera token automáticamente
    - [x] Establece status a PENDING
    - [x] Establece expires_at (7 días desde ahora)
    - [x] Valida email no vacío
    - [x] Valida company_id y invited_by_user_id no vacíos
  - [x] Método `accept()`:
    - [x] Valida que status sea PENDING
    - [x] Valida que no esté expirada (`is_expired()`)
    - [x] Modifica la instancia directamente (mutabilidad)
  - [x] Método `reject()`:
    - [x] Valida que status sea PENDING
    - [x] Modifica la instancia directamente (mutabilidad)
  - [x] Método `expire()`:
    - [x] Modifica la instancia directamente (mutabilidad)
  - [x] Método `cancel()`:
    - [x] Valida que status sea PENDING
    - [x] Modifica la instancia directamente (mutabilidad)
  - [x] Método `is_expired() -> bool`:
    - [x] Verifica si `datetime.utcnow() > expires_at`
  - [x] Método `is_pending() -> bool`:
    - [x] Verifica si status es PENDING

### Tarea 1.4: Actualizar Entidad CompanyUser

- [x] Actualizar `src/company/domain/entities/company_user.py`
  - [x] Agregar método `remove()`:
    - [x] NO retorna nada (void)
    - [x] No elimina físicamente, solo prepara para eliminación (deactiva)
    - [x] Lógica de validación debe estar en el Command Handler, no aquí
  - [x] Revisar que `update()` soporte actualizar role y permissions
  - [x] Actualizar `update()`, `activate()`, `deactivate()` para que sean mutables (modifican la instancia directamente)

### Tarea 1.5: Interface del Repositorio de Invitaciones

- [x] Crear `src/company/domain/infrastructure/company_user_invitation_repository_interface.py`
  - [x] `save(invitation: CompanyUserInvitation) -> None`
  - [x] `get_by_id(invitation_id: CompanyUserInvitationId) -> Optional[CompanyUserInvitation]`
  - [x] `get_by_token(token: InvitationToken) -> Optional[CompanyUserInvitation]`
  - [x] `get_by_email_and_company(email: str, company_id: CompanyId) -> Optional[CompanyUserInvitation]`
  - [x] `find_pending_by_email(email: str) -> List[CompanyUserInvitation]`
  - [x] `find_expired() -> List[CompanyUserInvitation]`
  - [x] `delete(invitation_id: CompanyUserInvitationId) -> None`
  - [x] Todos los métodos abstractos documentados

### Tarea 1.6: Actualizar Interface del Repositorio CompanyUser

- [x] Actualizar `src/company/domain/infrastructure/company_user_repository_interface.py`
  - [x] Agregar método `count_admins_by_company(company_id: CompanyId) -> int`
  - [x] Revisar que todos los métodos necesarios estén presentes

### Tarea 1.7: Tests Unitarios - Domain Layer

- [x] Crear `tests/unit/company/domain/enums/test_company_user_invitation_status.py`
  - [x] Test todos los valores del enum

- [x] Crear `tests/unit/company/domain/value_objects/test_company_user_permissions_expanded.py`
  - [x] Test nuevos permisos
  - [x] Test `from_dict()` y `to_dict()` con nuevos permisos
  - [x] Test valores por defecto de cada rol

- [x] Crear `tests/unit/company/domain/value_objects/test_invitation_token.py`
  - [x] Test generación de token
  - [x] Test validaciones si aplican

- [x] Crear `tests/unit/company/domain/entities/test_company_user_invitation.py`
  - [x] Test factory method `create()`
  - [x] Test método `accept()` - caso exitoso
  - [x] Test método `accept()` - error si expirada
  - [x] Test método `accept()` - error si no está PENDING
  - [x] Test método `reject()`
  - [x] Test método `expire()`
  - [x] Test método `cancel()`
  - [x] Test método `is_expired()`
  - [x] Test método `is_pending()`
  - [x] Test validaciones de email
  - [x] Test mutabilidad (métodos modifican la instancia directamente)

- [x] Crear `tests/unit/company/domain/entities/test_company_user.py`
  - [x] Test método `remove()` si se implementa
  - [x] Test actualización de role y permissions
  - [x] Test mutabilidad de métodos (`update()`, `activate()`, `deactivate()`, `remove()`)
  - [x] Test preservación de campos no modificados
  - [x] Test actualización de timestamps

**✅ FIN DE FASE 1 - Fase 1 completada exitosamente**

---

## FASE 2: Infrastructure Layer (Persistencia)

### Tarea 2.1: Modelo SQLAlchemy para Invitaciones

- [x] Crear `src/company/infrastructure/models/company_user_invitation_model.py`
  - [x] Tabla: `company_user_invitations`
  - [x] Columnas:
    - [x] `id`: String, primary_key, index
    - [x] `company_id`: String, ForeignKey a companies, index
    - [x] `email`: String, index
    - [x] `invited_by_user_id`: String, ForeignKey a company_users
    - [x] `token`: String, unique, index
    - [x] `status`: String (CompanyUserInvitationStatus), nullable=False
    - [x] `expires_at`: DateTime, nullable=False
    - [x] `accepted_at`: DateTime, nullable=True
    - [x] `rejected_at`: DateTime, nullable=True
    - [x] `created_at`: DateTime, nullable=False, default=func.now()
    - [x] `updated_at`: DateTime, nullable=False, default=func.now(), onupdate=func.now()
  - [x] Índice compuesto en (email, company_id) para búsquedas
  - [x] UniqueConstraint en token
  - [x] ForeignKey constraints con ondelete apropiado

### Tarea 2.2: Repositorio de Invitaciones

- [x] Crear `src/company/infrastructure/repositories/company_user_invitation_repository.py`
  - [x] Implementar `CompanyUserInvitationRepositoryInterface`
  - [x] Método `_to_domain(model: CompanyUserInvitationModel) -> CompanyUserInvitation`:
    - [x] Convertir modelo SQLAlchemy a entidad de dominio
    - [x] Manejar conversión de enums
    - [x] Manejar valores None
  - [x] Método `_to_model(invitation: CompanyUserInvitation) -> CompanyUserInvitationModel`:
    - [x] Convertir entidad de dominio a modelo SQLAlchemy
  - [x] Implementar todos los métodos de la interface:
    - [x] `save()`
    - [x] `get_by_id()`
    - [x] `get_by_token()`
    - [x] `get_by_email_and_company()`
    - [x] `find_pending_by_email()`
    - [x] `find_expired()`
    - [x] `delete()`
  - [x] Manejo de errores apropiado (try/except con logging)
  - [x] Logging de operaciones críticas (save, delete, get_by_token)

### Tarea 2.3: Actualizar Repositorio CompanyUser

- [x] Actualizar `src/company/infrastructure/repositories/company_user_repository.py`
  - [x] Implementar método `count_admins_by_company(company_id: CompanyId) -> int`:
    - [x] Query que cuenta usuarios con role ADMIN y status ACTIVE para una empresa
    - [x] Retornar int
  - [x] Optimizar queries si es necesario

### Tarea 2.4: Mappers (Entity → DTO)

- [x] Crear `src/company/application/mappers/company_user_invitation_mapper.py`
  - [x] Método `entity_to_dto(invitation: CompanyUserInvitation) -> CompanyUserInvitationDto`

- [x] Actualizar `src/company/application/mappers/company_user_mapper.py` si existe
  - [x] Asegurar que mapea todos los campos correctamente

### Tarea 2.5: DTOs

- [x] Crear `src/company/application/dtos/company_user_invitation_dto.py`
  - [x] Campos: id, company_id, email, invited_by_user_id, token, status, expires_at, accepted_at, rejected_at, created_at, updated_at

- [x] Actualizar `src/company/application/dtos/company_user_dto.py` si es necesario
  - [x] Asegurar que incluye todos los campos actualizados

### Tarea 2.6: Migración de Base de Datos

- [x] Crear migración con Alembic:
  ```bash
  make revision m="add company_user_invitation table"
  ```
- [x] Revisar migración generada en `alembic/versions/`
  - [x] Verificar estructura de tabla
  - [x] Verificar índices
  - [x] Verificar ForeignKeys
  - [x] Ajustar si es necesario
- [x] Aplicar migración:
  ```bash
  make migrate
  ```
- [x] Verificar que la migración se aplicó correctamente

### Tarea 2.7: Tests de Repositorio

- [x] Crear `tests/integration/company/infrastructure/repositories/test_company_user_invitation_repository.py`
  - [x] Test `save()` y `get_by_id()`
  - [x] Test `get_by_token()`
  - [x] Test `get_by_email_and_company()`
  - [x] Test `find_pending_by_email()`
  - [x] Test `find_expired()`
  - [x] Test `delete()`
  - [x] Test conversión domain ↔ model
  - [x] Test manejo de errores (not found, etc.)

- [x] Actualizar `tests/integration/company/infrastructure/repositories/test_company_user_repository.py`
  - [x] Test método `count_admins_by_company()`
  - [x] Test casos edge (0 admins, 1 admin, múltiples admins)

**✅ FIN DE FASE 2 - Fase 2 completada exitosamente**

---

## FASE 3: Application & Presentation Layer (API)

### Tarea 3.1: Commands (Operaciones de Escritura)

#### 3.1.1 Command: Invitar Usuario
- [x] Crear `src/company/application/commands/invite_company_user_command.py`
  - [x] `InviteCompanyUserCommand` (dataclass):
    - [x] `company_id: CompanyId` (Value Object)
    - [x] `email: str`
    - [x] `invited_by_user_id: CompanyUserId` (Value Object)
    - [x] `role: Optional[CompanyUserRole] = None` (default a RECRUITER o según lógica)
  - [x] `InviteCompanyUserCommandHandler`:
    - [x] Valida que el usuario invitador existe y tiene permisos
    - [x] Valida que el email no está ya vinculado a la empresa
    - [x] Genera token único
    - [x] Crea `CompanyUserInvitation` con factory method
    - [x] Guarda en repositorio
    - [x] Envía email de invitación (ver Tarea 3.8)
    - [x] NO retorna valor (void)

#### 3.1.2 Command: Aceptar Invitación
- [x] Crear `src/company/application/commands/accept_user_invitation_command.py`
  - [x] `AcceptUserInvitationCommand` (dataclass):
    - [x] `token: InvitationToken` (Value Object)
    - [x] `email: Optional[str] = None` (si usuario nuevo)
    - [x] `name: Optional[str] = None` (si usuario nuevo)
    - [x] `password: Optional[str] = None` (si usuario nuevo)
    - [x] `user_id: Optional[UserId] = None` (si usuario existente)
  - [x] `AcceptUserInvitationCommandHandler`:
    - [x] Busca invitación por token
    - [x] Valida que no esté expirada
    - [x] Valida que status sea PENDING
    - [x] **Caso A: Usuario nuevo**:
      - [x] Crea `User` (usar repositorio de usuarios existente)
      - [x] NO crea `Candidate`
    - [x] **Caso B: Usuario existente**:
      - [x] Busca `User` por email
      - [x] Valida que existe
    - [x] Crea `CompanyUser` vinculando User a Company
    - [x] Actualiza invitación a ACCEPTED
    - [x] Guarda CompanyUser y actualiza invitación
    - [x] NO retorna valor (void)

#### 3.1.3 Command: Eliminar Usuario de Empresa
- [x] Crear `src/company/application/commands/remove_company_user_command.py`
  - [x] `RemoveCompanyUserCommand` (dataclass):
    - [x] `company_id: CompanyId` (Value Object)
    - [x] `user_id_to_remove: UserId` (Value Object)
    - [x] `current_user_id: UserId` (Value Object, para validación de no auto-eliminación)
  - [x] `RemoveCompanyUserCommandHandler`:
    - [x] Valida que current_user_id != user_id_to_remove
    - [x] Busca CompanyUser a eliminar
    - [x] Valida que no es el último admin (usar `count_admins_by_company()`)
    - [x] Si es admin y es el último, lanza excepción
    - [x] Elimina CompanyUser del repositorio
    - [x] NO retorna valor (void)

#### 3.1.4 Command: Asignar Rol a Usuario
- [x] Crear `src/company/application/commands/assign_role_to_user_command.py`
  - [x] `AssignRoleToUserCommand` (dataclass):
    - [x] `company_id: CompanyId` (Value Object)
    - [x] `user_id: UserId` (Value Object)
    - [x] `role: CompanyUserRole` (Enum)
    - [x] `permissions: Optional[Dict[str, bool]] = None`
  - [x] `AssignRoleToUserCommandHandler`:
    - [x] Busca CompanyUser
    - [x] Valida que el rol existe
    - [x] Usa método `update()` de la entidad con nuevo role
    - [x] Si permissions no se proporciona, usa defaults del role
    - [x] Guarda actualización
    - [x] NO retorna valor (void)

#### 3.1.5 Command: Inicializar Roles
- [ ] Crear `src/company/application/commands/initialize_roles_command.py` ⚠️ **OPCIONAL**
  - [ ] `InitializeRolesCommand` (dataclass):
    - Sin parámetros (comando de sistema)
  - [ ] `InitializeRolesCommandHandler`:
    - Lista todos los CompanyUser del sistema
    - Para cada uno con role asignado:
      - Cambia temporalmente a ADMIN
      - Guarda
    - **Nota**: Este comando borra y recrea roles. En esta implementación, como los roles son enums fijos, solo se asigna ADMIN a usuarios existentes.
    - NO retorna valor (void)
  - **Estado**: No implementado - los roles son enums fijos, no se requiere inicialización dinámica

### Tarea 3.2: Queries (Operaciones de Lectura)

#### 3.2.1 Query: Obtener Invitación por Token
- [x] Crear `src/company/application/queries/get_user_invitation_query.py`
  - [x] `GetUserInvitationQuery` (dataclass):
    - [x] `token: InvitationToken` (Value Object)
  - [x] `GetUserInvitationQueryHandler`:
    - [x] Busca invitación por token
    - [x] Retorna `CompanyUserInvitationDto` o None
    - [x] NO incluye información sensible si no aplica

#### 3.2.2 Query: Listar Usuarios de Empresa
- [x] Ya existe `src/company/application/queries/list_company_users_by_company.py` (implementación previa)
  - [x] `ListCompanyUsersByCompanyQuery` (dataclass):
    - [x] `company_id: CompanyId` (Value Object)
    - [x] `active_only: bool = False`
  - [x] `ListCompanyUsersByCompanyQueryHandler`:
    - [x] Lista usuarios de la empresa
    - [x] Filtra por activos si `active_only=True`
    - [x] Retorna `List[CompanyUserDto]`

#### 3.2.3 Query: Obtener Permisos de Usuario
- [x] Crear `src/company/application/queries/get_user_permissions_query.py`
  - [x] `GetUserPermissionsQuery` (dataclass):
    - [x] `company_id: CompanyId` (Value Object) ✅ Corregido para usar Value Objects
    - [x] `user_id: UserId` (Value Object) ✅ Corregido para usar Value Objects
  - [x] `GetUserPermissionsQueryHandler`:
    - [x] Busca CompanyUser
    - [x] Retorna `CompanyUserPermissionsDto` o dict con permisos
    - [x] Incluye role y todos los permisos

### Tarea 3.3: Request Schemas

- [x] Crear `adapters/http/company/schemas/company_user_invitation_request.py`
  - [x] `InviteCompanyUserRequest` (Pydantic):
    - [x] `email: str` (EmailStr)
    - [x] `role: Optional[str] = None`
    - [x] Validaciones de email

- [x] Crear `AcceptInvitationRequest` en `company_user_invitation_request.py`
  - [x] `AcceptInvitationRequest` (Pydantic):
    - [x] `token: str`
    - [x] `email: Optional[str] = None` (requerido si usuario nuevo)
    - [x] `name: Optional[str] = None` (requerido si usuario nuevo)
    - [x] `password: Optional[str] = None` (requerido si usuario nuevo)
    - [x] `user_id: Optional[str] = None` (si usuario existente)
    - [x] Validación: user_id XOR (email, name, password) requeridos

- [x] Crear `AssignRoleRequest` en `company_user_invitation_request.py`
  - [x] `AssignRoleRequest` (Pydantic):
    - [x] `role: str`
    - [x] `permissions: Optional[Dict[str, bool]] = None`
    - [x] Validación de role válido

- [x] Actualizar `adapters/http/company/schemas/company_user_request.py` si es necesario

### Tarea 3.4: Response Schemas

- [x] Crear `adapters/http/company/schemas/company_user_invitation_response.py`
  - [x] `CompanyUserInvitationResponse` (Pydantic):
    - [x] Todos los campos del DTO
    - [x] `invitation_link: str` (URL completa con token)

- [x] Crear `adapters/http/company/schemas/company_user_invitation_response.py` (UserInvitationLinkResponse)
  - [x] `UserInvitationLinkResponse` (Pydantic):
    - [x] `invitation_id: str`
    - [x] `invitation_link: str` (para compartir manualmente)
    - [x] `expires_at: datetime`
    - [x] `email: str`

- [x] Actualizar `adapters/http/company/schemas/company_user_response.py` si es necesario
  - [x] Revisado: `CompanyUserResponse` ya tiene todos los campos necesarios (id, company_id, user_id, role, permissions, status, created_at, updated_at)

### Tarea 3.5: Controllers

- [x] Los métodos de invitación están implementados:
  - [x] `InvitationController` creado en `adapters/http/invitations/controllers/invitation_controller.py`:
    - [x] Método `get_invitation_by_token()`:
      - [x] Recibe token
      - [x] Llama a `GetUserInvitationQuery`
      - [x] Retorna `CompanyUserInvitationResponse`
    - [x] Método `accept_invitation()`:
      - [x] Recibe `AcceptInvitationRequest`
      - [x] Llama a `AcceptUserInvitationCommand`
      - [x] Retorna respuesta de éxito
  - [x] `CompanyUserController` actualizado en `adapters/http/company/controllers/company_user_controller.py`:
    - [x] Método `invite_company_user()`:
      - [x] Recibe `InviteCompanyUserRequest`
      - [x] Llama a `InviteCompanyUserCommand`
      - [x] Retorna `UserInvitationLinkResponse` con link para compartir
    - [x] Método `remove_company_user()`:
      - [x] Recibe company_id y user_id
      - [x] Llama a `RemoveCompanyUserCommand`
      - [x] Retorna respuesta de éxito
    - [x] Método `assign_role_to_user()`:
      - [x] Recibe `AssignRoleRequest`
      - [x] Llama a `AssignRoleToUserCommand`
      - [x] Retorna `CompanyUserResponse`
    - [x] Método `list_company_users()`:
      - [x] Llama a `ListCompanyUsersByCompanyQuery`
      - [x] Retorna lista de usuarios

- [ ] Crear `adapters/http/admin/controllers/role_management_controller.py` (opcional - requiere InitializeRolesCommand)
  - [ ] `RoleManagementController`:
    - [ ] Método `initialize_roles()`:
      - [ ] Llama a `InitializeRolesCommandHandler`
      - [ ] Retorna respuesta de éxito
  - [ ] **Nota**: Depende de Tarea 3.1.5 (InitializeRolesCommand)

### Tarea 3.6: Routers

- [x] Actualizar `adapters/http/company/routers/company_user_router.py`
  - [x] `POST /companies/{company_id}/users/invite`
    - [x] Body: `InviteCompanyUserRequest`
    - [x] Response: `UserInvitationLinkResponse`
    - [x] Tags: ["Company Users"]
  - [x] `GET /companies/{company_id}/users` (ya existe)
    - [x] Query params: `active_only: bool = False`
    - [x] Response: `List[CompanyUserResponse]`
  - [x] `DELETE /companies/{company_id}/users/{user_id}`
    - [x] Response: mensaje de éxito
  - [x] `PUT /companies/{company_id}/users/{user_id}/role`
    - [x] Body: `AssignRoleRequest`
    - [x] Response: `CompanyUserResponse`

- [x] Crear `adapters/http/invitations/routers/invitation_router.py`
  - [x] `POST /invitations/accept`
    - [x] Body: `AcceptInvitationRequest`
    - [x] Response: mensaje de éxito
    - [x] **Endpoint público** (no requiere autenticación)
    - [x] Lógica movida a `InvitationController`
  - [x] `GET /invitations/{token}`
    - [x] Response: `CompanyUserInvitationResponse`
    - [x] **Endpoint público** (no requiere autenticación)
    - [x] Lógica movida a `InvitationController`

- [ ] Crear `adapters/http/admin/routers/role_router.py` (si es necesario)
  - [ ] `POST /admin/roles/initialize`
    - Response: mensaje de éxito
    - **Solo para administradores del sistema**

- [x] Registrar routers en `main.py` (ya estaba registrado `invitation_router`)

### Tarea 3.7: Registro en Container

- [x] Actualizar `core/container.py`
  - [x] Registrar `CompanyUserInvitationRepository` (implementación)
  - [x] Registrar todos los CommandHandlers:
    - [x] `InviteCompanyUserCommandHandler`
    - [x] `AcceptUserInvitationCommandHandler`
    - [x] `RemoveCompanyUserCommandHandler`
    - [x] `AssignRoleToUserCommandHandler`
  - [x] Registrar todos los QueryHandlers:
    - [x] `GetUserInvitationQueryHandler`
    - [x] `ListCompanyUsersByCompanyQueryHandler` (ya existía)
    - [x] `GetUserPermissionsQueryHandler`
    - [x] `GetInvitationByEmailAndCompanyQueryHandler`
  - [x] Registrar Controllers:
    - [x] `InvitationController`
    - [x] `CompanyUserController` (ya existía, actualizado)

### Tarea 3.8: Servicio de Email

- [x] Actualizar `src/shared/domain/interfaces/email_service.py`
  - [x] Agregar método `send_user_invitation()`:
    ```python
    async def send_user_invitation(
        self,
        email: str,
        company_name: str,
        invitation_link: str,
        inviter_name: Optional[str] = None,
        custom_message: Optional[str] = None
    ) -> bool:
    ```

- [x] Actualizar `src/notification/infrastructure/services/smtp_email_service.py`
  - [x] Implementar `send_user_invitation()`
  - [x] Cargar template HTML `user_invitation.html`
  - [x] Generar URL: `{FRONTEND_URL}/invitations/accept?token={token}`
  - [x] Incluir información de la empresa
  - [x] Incluir link de invitación
  - [x] Incluir mensaje personalizado opcional

- [x] Actualizar `src/notification/infrastructure/services/mailgun_service.py`
  - [x] Implementar `send_user_invitation()` (similar a SMTP)

- [x] Crear template de email `src/shared/infrastructure/services/email_templates/user_invitation.html`
  - [x] Template HTML profesional
  - [x] Variables: `invitation_link`, `company_name`, `inviter_name`, `expires_at`, `custom_message`
  - [x] Botón CTA para aceptar invitación
  - [x] Información de expiración (7 días)
  - [x] Responsive design

### Tarea 3.9: Tests de Integración - API

- [x] Crear `tests/integration/company/presentation/test_company_user_invitation_endpoints.py`
  - [x] Test `POST /companies/{company_id}/users/invite` - éxito
  - [x] Test `POST /companies/{company_id}/users/invite` - email duplicado
  - [x] Test `GET /invitations/{token}` - éxito
  - [x] Test `GET /invitations/{token}` - token inválido
  - [x] Test `GET /invitations/{token}` - token expirado
  - [x] Test `POST /invitations/accept` - usuario nuevo
  - [x] Test `POST /invitations/accept` - usuario existente
  - [x] Test `POST /invitations/accept` - token inválido
  - [x] Test `POST /invitations/accept` - token expirado
  - [ ] Test `POST /companies/{company_id}/users/invite` - sin permisos (requiere autenticación real) ⚠️ **REQUIERE SETUP DE AUTH**
  - **Nota**: Este test requiere configuración de autenticación real, fuera del scope de tests con mocks

- [x] Crear `tests/integration/company/presentation/test_company_user_management_endpoints.py`
  - [x] Test `DELETE /companies/{company_id}/users/{user_id}` - éxito
  - [x] Test `DELETE /companies/{company_id}/users/{user_id}` - último admin
  - [x] Test `DELETE /companies/{company_id}/users/{user_id}` - auto-eliminación
  - [x] Test `PUT /companies/{company_id}/users/{user_id}/role` - éxito
  - [x] Test `GET /companies/{company_id}/users` - listado
  - [x] Test `GET /companies/{company_id}/users` - con active_only filter

- [ ] Crear `tests/integration/admin/presentation/test_role_management_endpoints.py` (opcional - depende de InitializeRolesCommand)
  - [ ] Test `POST /admin/roles/initialize` (opcional - depende de InitializeRolesCommand)

### Tarea 3.10: Actualizar Excepciones

- [x] Revisar `src/company/domain/exceptions/company_exceptions.py`
  - [x] Revisado: `CompanyValidationError` y `CompanyNotFoundError` cubren todos los casos necesarios
  - [x] No se requieren excepciones adicionales específicas

**📋 RESUMEN FASE 3:**
- ✅ Commands: 4/5 completados (InitializeRolesCommand pendiente/opcional)
- ✅ Queries: 3/3 completados (con tipado correcto usando Value Objects)
- ✅ Request Schemas: Completados
- ✅ Response Schemas: Completados
- ✅ Controllers: Completados (RoleManagementController depende de InitializeRolesCommand)
- ✅ Routers: Completados (excepto admin/roles/initialize que depende de InitializeRolesCommand)
- ✅ Container: Completado
- ✅ Email Service: Completado (SMTP y Mailgun implementados)
- ✅ Tests de Integración: Completados (15 tests pasando)
  - ✅ 9 tests para endpoints de invitaciones
  - ✅ 6 tests para endpoints de gestión de usuarios
- ✅ Excepciones: Revisadas y completas

**Nota**: La tarea 3.1.5 (InitializeRolesCommand) y su controller/router asociado están marcados como opcionales porque los roles son enums fijos en esta implementación.

**✅ FIN DE FASE 3 - Feature completamente implementada**

### Resumen de Tests de Integración Creados:
- ✅ `test_company_user_invitation_endpoints.py`: 9 tests pasando
  - Tests para invitar usuarios (éxito, email duplicado)
  - Tests para obtener invitación por token (éxito, inválido, expirado)
  - Tests para aceptar invitación (usuario nuevo, existente, errores)
- ✅ `test_company_user_management_endpoints.py`: 6 tests pasando
  - Tests para eliminar usuario (éxito, último admin, auto-eliminación)
  - Tests para asignar rol
  - Tests para listar usuarios (con y sin filtro active_only)

**Total: 15 tests de integración pasando** ✅

## ✅ Estado Final del Proyecto

### Implementación Completa

Todas las fases principales han sido implementadas y probadas:

1. **✅ Fase 1 - Domain Layer**: Completa
   - Enums, Value Objects y Entidades creados
   - Lógica de negocio implementada
   - Validaciones implementadas

2. **✅ Fase 2 - Infrastructure Layer**: Completa
   - Repositorios implementados
   - Modelos SQLAlchemy creados
   - Migraciones aplicadas

3. **✅ Fase 3 - Application & Presentation Layer**: Completa
   - Commands y Queries implementados
   - Controllers y Routers creados
   - Tests de integración pasando
   - Servicio de email implementado

### Documentación Creada

- ✅ `docs/INVITATION_SYSTEM.md` - Documentación completa del sistema
- ✅ `docs/security_task.md` - Plan de tareas actualizado
- ✅ API Documentation (OpenAPI/Swagger) - Generada automáticamente por FastAPI

### Sistema Listo para Producción

El sistema de invitaciones y gestión de usuarios está **funcionalmente completo** y listo para ser utilizado. Los endpoints están disponibles, documentados y probados.

---

## Tareas Adicionales y Mejoras Futuras

### Documentación
- [ ] Actualizar documentación de API (OpenAPI/Swagger)
- [ ] Documentar flujos de invitación en README o docs específicos
- [ ] Documentar permisos y roles disponibles

### Frontend (Fuera del scope de backend, pero mencionar)
- [ ] Página de gestión de usuarios (`/company/users`)
- [ ] Formulario de invitación de usuario
- [ ] Página de aceptación de invitación (`/invitations/accept?token=xxx`)
- [ ] Listado de usuarios con opción de eliminar y cambiar roles

### Validaciones de Seguridad Adicionales
- [ ] Rate limiting en endpoints de invitación
- [ ] Validación de dominio de email (si empresa requiere dominio específico)
- [ ] Logs de auditoría para invitaciones y cambios de roles

### Mejoras Futuras (No en esta fase)
- [ ] Sistema de roles dinámicos (en lugar de enums fijos)
- [ ] Permisos a nivel de workflow/phase
- [ ] Historial de cambios de roles
- [ ] Notificaciones cuando se asigna/elimina usuario

---

## Checklist Final

Antes de considerar la feature completa:

- [x] Todas las tareas de Fase 1 completadas y confirmadas ✅
- [x] Todas las tareas de Fase 2 completadas y confirmadas ✅
- [x] Todas las tareas de Fase 3 completadas ✅
- [x] Todos los tests pasando (unitarios, integración, endpoints)
  - ✅ 50 tests unitarios del Domain Layer pasando
  - ✅ Tests de repositorios pasando
  - ✅ 15 tests de integración de endpoints pasando
- [x] Migraciones aplicadas correctamente
  - ✅ Migración para `company_user_invitations` tabla creada y aplicada
- [x] Documentación de API actualizada (OpenAPI/Swagger se genera automáticamente)
  - ✅ FastAPI genera automáticamente documentación en `/docs` y `/redoc`
  - ✅ Endpoints documentados con tipos Pydantic
  - ✅ Endpoints de invitaciones y gestión de usuarios disponibles en la documentación
  - ℹ️ La documentación se actualiza automáticamente al ejecutar el servidor
- [x] Código revisado y sin errores de linter
  - ✅ Linter sin errores críticos
  - ⚠️ Algunos warnings de deprecación de `datetime.utcnow()` (no bloqueante)
- [x] Validaciones de seguridad implementadas
  - ✅ Validaciones en entidades de dominio
  - ✅ Validaciones en comandos
  - ✅ Validaciones en schemas Pydantic
  - ✅ Validación de último admin al eliminar usuario
- [x] Servicio de email funcionando
  - ✅ Interface `EmailServiceInterface` con `send_user_invitation()`
  - ✅ Implementaciones SMTP y Mailgun
  - ✅ Template HTML creado
- [x] Endpoints probados con tests de integración
  - ✅ 15 tests cubriendo casos de éxito y error

---

**Notas**:
- Este plan sigue estrictamente el workflow de 3 fases del repositorio
- Cada fase debe completarse y confirmarse antes de avanzar
- Los tests son obligatorios en cada fase
- Mantener inmutabilidad y principios DDD en todo momento

