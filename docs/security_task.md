# Plan de Tareas: Sistema de Roles y Gestión de Usuarios

Este documento contiene las tareas específicas para implementar el sistema de roles y gestión de usuarios según el análisis en `security.md`.

**IMPORTANTE**: Seguir estrictamente el orden de las fases. No avanzar a la siguiente fase sin confirmación del usuario.

---

## FASE 1: Domain Layer (Entidades y Lógica de Negocio)

### Tarea 1.1: Expandir Enums

#### 1.1.1 Enum de Estado de Invitación
- [ ] Crear `src/company/domain/enums/company_user_invitation_status.py`
  - [ ] `PENDING`: Invitación pendiente
  - [ ] `ACCEPTED`: Invitación aceptada
  - [ ] `REJECTED`: Invitación rechazada
  - [ ] `EXPIRED`: Invitación expirada
  - [ ] `CANCELLED`: Invitación cancelada
  - [ ] Documentar cada valor con docstring
- [ ] Actualizar `src/company/domain/enums/__init__.py` para exportar el nuevo enum

#### 1.1.2 Expandir Roles (Opcional - verificar si se necesita)
- [ ] Revisar si se necesitan nuevos roles además de ADMIN, RECRUITER, VIEWER
- [ ] Si se requieren: Actualizar `src/company/domain/enums/company_user_role.py`
  - [ ] `INTERVIEW_MANAGER`
  - [ ] `HIRING_MANAGER`
  - [ ] `EXTERNAL_INTERVIEWER`
  - [ ] `SUPERVISOR`

### Tarea 1.2: Expandir Value Objects

#### 1.2.1 Expandir CompanyUserPermissions
- [ ] Actualizar `src/company/domain/value_objects/company_user_permissions.py`
  - [ ] Agregar `can_delete_candidates: bool`
  - [ ] Agregar `can_view_candidates: bool` (hacer explícito)
  - [ ] Agregar `can_change_settings: bool`
  - [ ] Agregar `can_change_phase: bool`
  - [ ] Actualizar `to_dict()` para incluir nuevos permisos
  - [ ] Actualizar `from_dict()` para incluir nuevos permisos
  - [ ] Actualizar métodos `default_for_admin()`, `default_for_recruiter()`, `default_for_viewer()` con valores apropiados

#### 1.2.2 Nuevo Value Object: CompanyUserInvitationId
- [ ] Crear `src/company/domain/value_objects/company_user_invitation_id.py`
  - [ ] Heredar de clase base o seguir patrón similar a `CompanyUserId`
  - [ ] Validación de formato si aplica

#### 1.2.3 Nuevo Value Object: InvitationToken
- [ ] Crear `src/company/domain/value_objects/invitation_token.py`
  - [ ] Inmutable
  - [ ] Validación de formato (opcional)
  - [ ] Método `generate()` estático para generar token seguro

### Tarea 1.3: Nueva Entidad: CompanyUserInvitation

- [ ] Crear `src/company/domain/entities/company_user_invitation.py`
  - [ ] Constructor con todos los parámetros requeridos (sin valores por defecto)
    - `id: CompanyUserInvitationId`
    - `company_id: CompanyId`
    - `email: str`
    - `invited_by_user_id: CompanyUserId`
    - `token: InvitationToken`
    - `status: CompanyUserInvitationStatus`
    - `expires_at: datetime`
    - `accepted_at: Optional[datetime]`
    - `rejected_at: Optional[datetime]`
    - `created_at: datetime`
    - `updated_at: datetime`
  - [ ] Propiedades públicas (NO usar @property para getters/setters)
  - [ ] Factory method `create()`:
    - Genera token automáticamente
    - Establece status a PENDING
    - Establece expires_at (7 días desde ahora)
    - Valida email no vacío
    - Valida company_id y invited_by_user_id no vacíos
  - [ ] Método `accept()`:
    - Valida que status sea PENDING
    - Valida que no esté expirada (`is_expired()`)
    - Retorna nueva instancia con status ACCEPTED y accepted_at
  - [ ] Método `reject()`:
    - Valida que status sea PENDING
    - Retorna nueva instancia con status REJECTED y rejected_at
  - [ ] Método `expire()`:
    - Retorna nueva instancia con status EXPIRED
  - [ ] Método `cancel()`:
    - Valida que status sea PENDING
    - Retorna nueva instancia con status CANCELLED
  - [ ] Método `is_expired() -> bool`:
    - Verifica si `datetime.utcnow() > expires_at`
  - [ ] Método `is_pending() -> bool`:
    - Verifica si status es PENDING

### Tarea 1.4: Actualizar Entidad CompanyUser

- [ ] Actualizar `src/company/domain/entities/company_user.py`
  - [ ] Agregar método `remove()`:
    - NO retorna nada (void)
    - No elimina físicamente, solo prepara para eliminación
    - Lógica de validación debe estar en el Command Handler, no aquí
  - [ ] Revisar que `update()` soporte actualizar role y permissions
  - [ ] Mantener inmutabilidad: métodos retornan nuevas instancias

### Tarea 1.5: Interface del Repositorio de Invitaciones

- [ ] Crear `src/company/domain/infrastructure/company_user_invitation_repository_interface.py`
  - [ ] `save(invitation: CompanyUserInvitation) -> None`
  - [ ] `get_by_id(invitation_id: CompanyUserInvitationId) -> Optional[CompanyUserInvitation]`
  - [ ] `get_by_token(token: InvitationToken) -> Optional[CompanyUserInvitation]`
  - [ ] `get_by_email_and_company(email: str, company_id: CompanyId) -> Optional[CompanyUserInvitation]`
  - [ ] `find_pending_by_email(email: str) -> List[CompanyUserInvitation]`
  - [ ] `find_expired() -> List[CompanyUserInvitation]`
  - [ ] `delete(invitation_id: CompanyUserInvitationId) -> None`
  - [ ] Todos los métodos abstractos documentados

### Tarea 1.6: Actualizar Interface del Repositorio CompanyUser

- [ ] Actualizar `src/company/domain/infrastructure/company_user_repository_interface.py`
  - [ ] Agregar método `count_admins_by_company(company_id: CompanyId) -> int`
  - [ ] Revisar que todos los métodos necesarios estén presentes

### Tarea 1.7: Tests Unitarios - Domain Layer

- [ ] Crear `tests/unit/company/domain/enums/test_company_user_invitation_status.py`
  - [ ] Test todos los valores del enum

- [ ] Crear `tests/unit/company/domain/value_objects/test_company_user_permissions_expanded.py`
  - [ ] Test nuevos permisos
  - [ ] Test `from_dict()` y `to_dict()` con nuevos permisos
  - [ ] Test valores por defecto de cada rol

- [ ] Crear `tests/unit/company/domain/value_objects/test_invitation_token.py`
  - [ ] Test generación de token
  - [ ] Test validaciones si aplican

- [ ] Crear `tests/unit/company/domain/entities/test_company_user_invitation.py`
  - [ ] Test factory method `create()`
  - [ ] Test método `accept()` - caso exitoso
  - [ ] Test método `accept()` - error si expirada
  - [ ] Test método `accept()` - error si no está PENDING
  - [ ] Test método `reject()`
  - [ ] Test método `expire()`
  - [ ] Test método `cancel()`
  - [ ] Test método `is_expired()`
  - [ ] Test método `is_pending()`
  - [ ] Test validaciones de email
  - [ ] Test inmutabilidad (métodos retornan nuevas instancias)

- [ ] Actualizar `tests/unit/company/domain/entities/test_company_user.py`
  - [ ] Test método `remove()` si se implementa
  - [ ] Test actualización de role y permissions

**🛑 FIN DE FASE 1 - Confirmar con usuario antes de continuar a Fase 2**

---

## FASE 2: Infrastructure Layer (Persistencia)

### Tarea 2.1: Modelo SQLAlchemy para Invitaciones

- [ ] Crear `src/company/infrastructure/models/company_user_invitation_model.py`
  - [ ] Tabla: `company_user_invitations`
  - [ ] Columnas:
    - `id`: String, primary_key, index
    - `company_id`: String, ForeignKey a companies, index
    - `email`: String, index
    - `invited_by_user_id`: String, ForeignKey a company_users
    - `token`: String, unique, index
    - `status`: Enum (CompanyUserInvitationStatus), nullable=False
    - `expires_at`: DateTime, nullable=False
    - `accepted_at`: DateTime, nullable=True
    - `rejected_at`: DateTime, nullable=True
    - `created_at`: DateTime, nullable=False, default=func.now()
    - `updated_at`: DateTime, nullable=False, default=func.now(), onupdate=func.now()
  - [ ] Índice compuesto en (email, company_id) para búsquedas
  - [ ] UniqueConstraint en token
  - [ ] ForeignKey constraints con ondelete apropiado

### Tarea 2.2: Repositorio de Invitaciones

- [ ] Crear `src/company/infrastructure/repositories/company_user_invitation_repository.py`
  - [ ] Implementar `CompanyUserInvitationRepositoryInterface`
  - [ ] Método `_to_domain(model: CompanyUserInvitationModel) -> CompanyUserInvitation`:
    - Convertir modelo SQLAlchemy a entidad de dominio
    - Manejar conversión de enums
    - Manejar valores None
  - [ ] Método `_to_model(invitation: CompanyUserInvitation) -> CompanyUserInvitationModel`:
    - Convertir entidad de dominio a modelo SQLAlchemy
  - [ ] Implementar todos los métodos de la interface:
    - [ ] `save()`
    - [ ] `get_by_id()`
    - [ ] `get_by_token()`
    - [ ] `get_by_email_and_company()`
    - [ ] `find_pending_by_email()`
    - [ ] `find_expired()`
    - [ ] `delete()`
  - [ ] Manejo de errores apropiado
  - [ ] Logging de operaciones críticas

### Tarea 2.3: Actualizar Repositorio CompanyUser

- [ ] Actualizar `src/company/infrastructure/repositories/company_user_repository.py`
  - [ ] Implementar método `count_admins_by_company(company_id: CompanyId) -> int`:
    - Query que cuenta usuarios con role ADMIN y status ACTIVE para una empresa
    - Retornar int
  - [ ] Optimizar queries si es necesario

### Tarea 2.4: Mappers (Entity → DTO)

- [ ] Crear `src/company/application/mappers/company_user_invitation_mapper.py`
  - [ ] Método `to_dto(invitation: CompanyUserInvitation) -> CompanyUserInvitationDto`

- [ ] Actualizar `src/company/application/mappers/company_user_mapper.py` si existe
  - [ ] Asegurar que mapea todos los campos correctamente

### Tarea 2.5: DTOs

- [ ] Crear `src/company/application/dtos/company_user_invitation_dto.py`
  - [ ] Campos: id, company_id, email, invited_by_user_id, token, status, expires_at, accepted_at, rejected_at, created_at, updated_at

- [ ] Actualizar `src/company/application/dtos/company_user_dto.py` si es necesario
  - [ ] Asegurar que incluye todos los campos actualizados

### Tarea 2.6: Migración de Base de Datos

- [ ] Crear migración con Alembic:
  ```bash
  make revision m="add company_user_invitation table"
  ```
- [ ] Revisar migración generada en `alembic/versions/`
  - [ ] Verificar estructura de tabla
  - [ ] Verificar índices
  - [ ] Verificar ForeignKeys
  - [ ] Ajustar si es necesario
- [ ] Aplicar migración:
  ```bash
  make migrate
  ```
- [ ] Verificar que la migración se aplicó correctamente

### Tarea 2.7: Tests de Repositorio

- [ ] Crear `tests/integration/company/infrastructure/repositories/test_company_user_invitation_repository.py`
  - [ ] Test `save()` y `get_by_id()`
  - [ ] Test `get_by_token()`
  - [ ] Test `get_by_email_and_company()`
  - [ ] Test `find_pending_by_email()`
  - [ ] Test `find_expired()`
  - [ ] Test `delete()`
  - [ ] Test conversión domain ↔ model
  - [ ] Test manejo de errores (not found, etc.)

- [ ] Actualizar `tests/integration/company/infrastructure/repositories/test_company_user_repository.py`
  - [ ] Test método `count_admins_by_company()`
  - [ ] Test casos edge (0 admins, 1 admin, múltiples admins)

**🛑 FIN DE FASE 2 - Confirmar con usuario antes de continuar a Fase 3**

---

## FASE 3: Application & Presentation Layer (API)

### Tarea 3.1: Commands (Operaciones de Escritura)

#### 3.1.1 Command: Invitar Usuario
- [ ] Crear `src/company/application/commands/invite_company_user_command.py`
  - [ ] `InviteCompanyUserCommand` (dataclass):
    - `company_id: str`
    - `email: str`
    - `invited_by_user_id: str`
    - `role: Optional[str] = None` (default a RECRUITER o según lógica)
  - [ ] `InviteCompanyUserCommandHandler`:
    - Valida que el usuario invitador existe y tiene permisos
    - Valida que el email no está ya vinculado a la empresa
    - Genera token único
    - Crea `CompanyUserInvitation` con factory method
    - Guarda en repositorio
    - Envía email de invitación (ver Tarea 3.8)
    - NO retorna valor (void)

#### 3.1.2 Command: Aceptar Invitación
- [ ] Crear `src/company/application/commands/accept_user_invitation_command.py`
  - [ ] `AcceptUserInvitationCommand` (dataclass):
    - `token: str`
    - `email: Optional[str] = None` (si usuario nuevo)
    - `name: Optional[str] = None` (si usuario nuevo)
    - `password: Optional[str] = None` (si usuario nuevo)
  - [ ] `AcceptUserInvitationCommandHandler`:
    - Busca invitación por token
    - Valida que no esté expirada
    - Valida que status sea PENDING
    - **Caso A: Usuario nuevo**:
      - Crea `User` (usar repositorio de usuarios existente)
      - NO crea `Candidate`
    - **Caso B: Usuario existente**:
      - Busca `User` por email
      - Valida que existe
    - Crea `CompanyUser` vinculando User a Company
    - Actualiza invitación a ACCEPTED
    - Guarda CompanyUser y actualiza invitación
    - NO retorna valor (void)

#### 3.1.3 Command: Eliminar Usuario de Empresa
- [ ] Crear `src/company/application/commands/remove_company_user_command.py`
  - [ ] `RemoveCompanyUserCommand` (dataclass):
    - `company_id: str`
    - `user_id_to_remove: str`
    - `current_user_id: str` (para validación de no auto-eliminación)
  - [ ] `RemoveCompanyUserCommandHandler`:
    - Valida que current_user_id != user_id_to_remove
    - Busca CompanyUser a eliminar
    - Valida que no es el último admin (usar `count_admins_by_company()`)
    - Si es admin y es el último, lanza excepción
    - Elimina CompanyUser del repositorio
    - NO retorna valor (void)

#### 3.1.4 Command: Asignar Rol a Usuario
- [ ] Crear `src/company/application/commands/assign_role_to_user_command.py`
  - [ ] `AssignRoleToUserCommand` (dataclass):
    - `company_id: str`
    - `user_id: str`
    - `role: str`
    - `permissions: Optional[Dict[str, bool]] = None`
  - [ ] `AssignRoleToUserCommandHandler`:
    - Busca CompanyUser
    - Valida que el rol existe
    - Usa método `update()` de la entidad con nuevo role
    - Si permissions no se proporciona, usa defaults del role
    - Guarda actualización
    - NO retorna valor (void)

#### 3.1.5 Command: Inicializar Roles
- [ ] Crear `src/company/application/commands/initialize_roles_command.py`
  - [ ] `InitializeRolesCommand` (dataclass):
    - Sin parámetros (comando de sistema)
  - [ ] `InitializeRolesCommandHandler`:
    - Lista todos los CompanyUser del sistema
    - Para cada uno con role asignado:
      - Cambia temporalmente a ADMIN
      - Guarda
    - **Nota**: Este comando borra y recrea roles. En esta implementación, como los roles son enums fijos, solo se asigna ADMIN a usuarios existentes.
    - NO retorna valor (void)

### Tarea 3.2: Queries (Operaciones de Lectura)

#### 3.2.1 Query: Obtener Invitación por Token
- [ ] Crear `src/company/application/queries/get_user_invitation_query.py`
  - [ ] `GetUserInvitationQuery` (dataclass):
    - `token: str`
  - [ ] `GetUserInvitationQueryHandler`:
    - Busca invitación por token
    - Retorna `CompanyUserInvitationDto` o None
    - NO incluye información sensible si no aplica

#### 3.2.2 Query: Listar Usuarios de Empresa
- [ ] Crear `src/company/application/queries/list_company_users_query.py`
  - [ ] `ListCompanyUsersQuery` (dataclass):
    - `company_id: str`
    - `include_inactive: bool = False`
  - [ ] `ListCompanyUsersQueryHandler`:
    - Lista usuarios de la empresa
    - Filtra por activos si `include_inactive=False`
    - Retorna `List[CompanyUserDto]`

#### 3.2.3 Query: Obtener Permisos de Usuario
- [ ] Crear `src/company/application/queries/get_user_permissions_query.py`
  - [ ] `GetUserPermissionsQuery` (dataclass):
    - `company_id: str`
    - `user_id: str`
  - [ ] `GetUserPermissionsQueryHandler`:
    - Busca CompanyUser
    - Retorna `CompanyUserPermissionsDto` o dict con permisos
    - Incluye role y todos los permisos

### Tarea 3.3: Request Schemas

- [ ] Crear `adapters/http/company/schemas/company_user_invitation_request.py`
  - [ ] `InviteCompanyUserRequest` (Pydantic):
    - `email: str` (EmailStr)
    - `role: Optional[str] = None`
    - Validaciones de email

- [ ] Crear `adapters/http/company/schemas/accept_invitation_request.py`
  - [ ] `AcceptInvitationRequest` (Pydantic):
    - `token: str`
    - `email: Optional[str] = None` (requerido si usuario nuevo)
    - `name: Optional[str] = None` (requerido si usuario nuevo)
    - `password: Optional[str] = None` (requerido si usuario nuevo)
    - Validación: si token corresponde a usuario nuevo, email/name/password requeridos

- [ ] Crear `adapters/http/company/schemas/assign_role_request.py`
  - [ ] `AssignRoleRequest` (Pydantic):
    - `role: str`
    - `permissions: Optional[Dict[str, bool]] = None`
    - Validación de role válido

- [ ] Actualizar `adapters/http/company/schemas/company_user_request.py` si es necesario

### Tarea 3.4: Response Schemas

- [ ] Crear `adapters/http/company/schemas/company_user_invitation_response.py`
  - [ ] `CompanyUserInvitationResponse` (Pydantic):
    - Todos los campos del DTO
    - `invitation_link: str` (URL completa con token)

- [ ] Crear `adapters/http/company/schemas/user_invitation_link_response.py`
  - [ ] `UserInvitationLinkResponse` (Pydantic):
    - `invitation_id: str`
    - `invitation_link: str` (para compartir manualmente)
    - `expires_at: datetime`
    - `email: str`

- [ ] Actualizar `adapters/http/company/schemas/company_user_response.py` si es necesario

### Tarea 3.5: Controllers

- [ ] Crear `adapters/http/company/controllers/company_user_invitation_controller.py`
  - [ ] `CompanyUserInvitationController`:
    - Método `invite_user()`:
      - Recibe `InviteCompanyUserRequest`
      - Llama a `InviteCompanyUserCommandHandler`
      - Retorna `UserInvitationLinkResponse` con link para compartir
    - Método `accept_invitation()`:
      - Recibe `AcceptInvitationRequest`
      - Llama a `AcceptUserInvitationCommandHandler`
      - Retorna respuesta de éxito

- [ ] Crear o actualizar `adapters/http/company/controllers/company_user_management_controller.py`
  - [ ] `CompanyUserManagementController`:
    - Método `remove_user()`:
      - Recibe company_id y user_id
      - Llama a `RemoveCompanyUserCommandHandler`
      - Retorna respuesta de éxito
    - Método `assign_role()`:
      - Recibe `AssignRoleRequest`
      - Llama a `AssignRoleToUserCommandHandler`
      - Retorna respuesta de éxito
    - Método `list_users()`:
      - Llama a `ListCompanyUsersQueryHandler`
      - Retorna lista de usuarios

- [ ] Crear `adapters/http/admin/controllers/role_management_controller.py` (si es para admin del sistema)
  - [ ] `RoleManagementController`:
    - Método `initialize_roles()`:
      - Llama a `InitializeRolesCommandHandler`
      - Retorna respuesta de éxito

### Tarea 3.6: Routers

- [ ] Actualizar o crear `adapters/http/company/routers/company_user_router.py`
  - [ ] `POST /companies/{company_id}/users/invite`
    - Body: `InviteCompanyUserRequest`
    - Response: `UserInvitationLinkResponse`
    - Tags: ["Company Users"]
  - [ ] `GET /companies/{company_id}/users`
    - Query params: `include_inactive: bool = False`
    - Response: `List[CompanyUserResponse]`
  - [ ] `DELETE /companies/{company_id}/users/{user_id}`
    - Response: mensaje de éxito
  - [ ] `PUT /companies/{company_id}/users/{user_id}/role`
    - Body: `AssignRoleRequest`
    - Response: mensaje de éxito

- [ ] Crear `adapters/http/invitations/routers/invitation_router.py`
  - [ ] `POST /invitations/accept`
    - Body: `AcceptInvitationRequest`
    - Response: mensaje de éxito
    - **Endpoint público** (no requiere autenticación)
  - [ ] `GET /invitations/{token}`
    - Response: `CompanyUserInvitationResponse`
    - **Endpoint público** (no requiere autenticación)

- [ ] Crear `adapters/http/admin/routers/role_router.py` (si es necesario)
  - [ ] `POST /admin/roles/initialize`
    - Response: mensaje de éxito
    - **Solo para administradores del sistema**

- [ ] Registrar routers en `adapters/http/routers.py`

### Tarea 3.7: Registro en Container

- [ ] Actualizar `core/container.py`
  - [ ] Registrar `CompanyUserInvitationRepository` (implementación)
  - [ ] Registrar `CompanyUserInvitationRepositoryInterface` (binding)
  - [ ] Registrar todos los CommandHandlers:
    - [ ] `InviteCompanyUserCommandHandler`
    - [ ] `AcceptUserInvitationCommandHandler`
    - [ ] `RemoveCompanyUserCommandHandler`
    - [ ] `AssignRoleToUserCommandHandler`
    - [ ] `InitializeRolesCommandHandler`
  - [ ] Registrar todos los QueryHandlers:
    - [ ] `GetUserInvitationQueryHandler`
    - [ ] `ListCompanyUsersQueryHandler`
    - [ ] `GetUserPermissionsQueryHandler`
  - [ ] Registrar Controllers:
    - [ ] `CompanyUserInvitationController`
    - [ ] `CompanyUserManagementController`
    - [ ] `RoleManagementController` (si aplica)

### Tarea 3.8: Servicio de Email

- [ ] Actualizar `src/notification/domain/interfaces/email_service_interface.py`
  - [ ] Agregar método `send_user_invitation()`:
    ```python
    async def send_user_invitation(
        self,
        email: str,
        invitation_token: str,
        company_name: str,
        invited_by_name: Optional[str] = None
    ) -> bool:
    ```

- [ ] Actualizar `src/notification/infrastructure/services/smtp_email_service.py`
  - [ ] Implementar `send_user_invitation()`
  - [ ] Cargar template HTML `user_invitation.html`
  - [ ] Generar URL: `{FRONTEND_URL}/invitations/accept?token={token}`
  - [ ] Incluir información de la empresa
  - [ ] Incluir link de invitación

- [ ] Actualizar `src/notification/infrastructure/services/mailgun_service.py`
  - [ ] Implementar `send_user_invitation()` (similar a SMTP)

- [ ] Crear template de email `src/shared/infrastructure/services/email_templates/user_invitation.html`
  - [ ] Template HTML profesional
  - [ ] Variables: `invitation_link`, `company_name`, `invited_by_name`, `expires_at`
  - [ ] Botón CTA para aceptar invitación
  - [ ] Información de expiración (7 días)
  - [ ] Responsive design

### Tarea 3.9: Tests de Integración - API

- [ ] Crear `tests/integration/company/presentation/test_company_user_invitation_endpoints.py`
  - [ ] Test `POST /companies/{company_id}/users/invite` - éxito
  - [ ] Test `POST /companies/{company_id}/users/invite` - email duplicado
  - [ ] Test `POST /companies/{company_id}/users/invite` - sin permisos
  - [ ] Test `GET /invitations/{token}` - éxito
  - [ ] Test `GET /invitations/{token}` - token inválido
  - [ ] Test `GET /invitations/{token}` - token expirado
  - [ ] Test `POST /invitations/accept` - usuario nuevo
  - [ ] Test `POST /invitations/accept` - usuario existente
  - [ ] Test `POST /invitations/accept` - token inválido
  - [ ] Test `POST /invitations/accept` - token expirado

- [ ] Crear `tests/integration/company/presentation/test_company_user_management_endpoints.py`
  - [ ] Test `DELETE /companies/{company_id}/users/{user_id}` - éxito
  - [ ] Test `DELETE /companies/{company_id}/users/{user_id}` - último admin
  - [ ] Test `DELETE /companies/{company_id}/users/{user_id}` - auto-eliminación
  - [ ] Test `PUT /companies/{company_id}/users/{user_id}/role` - éxito
  - [ ] Test `GET /companies/{company_id}/users` - listado
  - [ ] Test `GET /companies/{company_id}/users` - con include_inactive

- [ ] Crear `tests/integration/admin/presentation/test_role_management_endpoints.py` (si aplica)
  - [ ] Test `POST /admin/roles/initialize`

### Tarea 3.10: Actualizar Excepciones

- [ ] Revisar `src/company/domain/exceptions/company_exceptions.py`
  - [ ] Agregar `InvitationExpiredError`
  - [ ] Agregar `InvitationAlreadyUsedError`
  - [ ] Agregar `CannotRemoveLastAdminError`
  - [ ] Agregar `CannotRemoveSelfError`
  - [ ] Agregar `UserAlreadyInvitedError`
  - [ ] Agregar `InvalidInvitationTokenError`

**✅ FIN DE FASE 3 - Feature completamente implementada**

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

- [ ] Todas las tareas de Fase 1 completadas y confirmadas
- [ ] Todas las tareas de Fase 2 completadas y confirmadas
- [ ] Todas las tareas de Fase 3 completadas
- [ ] Todos los tests pasando (unitarios, integración, endpoints)
- [ ] Migraciones aplicadas correctamente
- [ ] Documentación de API actualizada
- [ ] Código revisado y sin errores de linter
- [ ] Validaciones de seguridad implementadas
- [ ] Servicio de email funcionando
- [ ] Endpoints probados manualmente

---

**Notas**:
- Este plan sigue estrictamente el workflow de 3 fases del repositorio
- Cada fase debe completarse y confirmarse antes de avanzar
- Los tests son obligatorios en cada fase
- Mantener inmutabilidad y principios DDD en todo momento

