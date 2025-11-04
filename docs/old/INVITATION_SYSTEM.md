# Sistema de Invitaciones y Gestión de Usuarios

## 📋 Resumen

Este documento describe el sistema de invitaciones y gestión de usuarios implementado para la plataforma CareerPython. El sistema permite a las empresas invitar usuarios, gestionar roles y permisos, y controlar el acceso a las funcionalidades del sistema.

## 🎯 Funcionalidades Principales

### 1. Invitación de Usuarios

Las empresas pueden invitar nuevos usuarios mediante un sistema de invitaciones por email:

- **Endpoint**: `POST /company/{company_id}/users/invite`
- **Proceso**:
  1. Un administrador o usuario con permisos invita a un nuevo usuario por email
  2. Se genera un token único de invitación con expiración (7 días por defecto)
  3. Se envía un email con un link de invitación
  4. El link puede ser compartido manualmente si es necesario

### 2. Aceptación de Invitaciones

Los usuarios pueden aceptar invitaciones de dos formas:

#### Caso A: Usuario Nuevo
- El usuario hace clic en el link de invitación
- Se muestra una pantalla de aceptación
- Se solicita: email, nombre y contraseña
- Se crea el usuario y se vincula a la empresa

#### Caso B: Usuario Existente
- El usuario hace clic en el link de invitación
- Si el usuario ya existe en el sistema, se vincula automáticamente a la empresa
- No requiere registro adicional

**Endpoints**:
- `GET /invitations/{token}` - Obtener detalles de la invitación
- `POST /invitations/accept` - Aceptar una invitación

### 3. Gestión de Usuarios

#### Eliminación de Usuarios
- **Endpoint**: `DELETE /company/{company_id}/users/{user_id}`
- **Validaciones**:
  - No se puede eliminar el último administrador de la empresa
  - No puedes eliminarte a ti mismo

#### Asignación de Roles
- **Endpoint**: `PUT /company/{company_id}/users/{user_id}/role`
- Permite asignar roles a usuarios (ADMIN, RECRUITER, VIEWER)
- Los roles determinan los permisos del usuario

#### Listado de Usuarios
- **Endpoint**: `GET /company/{company_id}/users`
- Lista todos los usuarios de una empresa
- Soporta filtro `active_only` para mostrar solo usuarios activos

## 🔐 Roles y Permisos

### Roles Disponibles

1. **ADMIN** - Administrador
   - Control total del sistema
   - Gestión de usuarios y configuración
   - Todos los permisos habilitados

2. **RECRUITER** - Reclutador
   - Buscar y filtrar candidatos
   - Agregar candidatos
   - Gestionar el proceso de selección

3. **VIEWER** - Visualizador
   - Solo lectura
   - Ver candidatos y analytics
   - Permisos limitados

### Permisos Disponibles

Los permisos se pueden configurar por usuario:

- `can_create_candidates` - Crear candidatos
- `can_delete_candidates` - Eliminar candidatos
- `can_view_candidates` - Ver candidatos
- `can_invite_candidates` - Invitar candidatos
- `can_add_comments` - Agregar comentarios
- `can_manage_users` - Gestionar usuarios
- `can_change_settings` - Cambiar configuración
- `can_change_phase` - Cambiar fase de candidatos
- `can_view_analytics` - Ver analytics

## 📧 Email de Invitación

El sistema envía emails automáticos cuando se invita a un usuario:

- **Template**: `src/shared/infrastructure/services/email_templates/user_invitation.html`
- **Proveedores soportados**:
  - SMTP (configuración por variables de entorno)
  - Mailgun (configuración por API key)

**Contenido del email**:
- Nombre de la empresa
- Link de invitación con token
- Nombre del usuario que invita
- Mensaje personalizado opcional
- Fecha de expiración de la invitación

## 🗄️ Modelo de Datos

### CompanyUserInvitation

Entidad que representa una invitación de usuario:

```python
CompanyUserInvitation:
  - id: CompanyUserInvitationId
  - company_id: CompanyId
  - email: str
  - invited_by_user_id: CompanyUserId
  - token: InvitationToken
  - status: CompanyUserInvitationStatus (PENDING, ACCEPTED, REJECTED, EXPIRED, CANCELLED)
  - expires_at: datetime
  - accepted_at: Optional[datetime]
  - rejected_at: Optional[datetime]
  - created_at: datetime
  - updated_at: datetime
```

### CompanyUser

Entidad que representa un usuario dentro de una empresa:

```python
CompanyUser:
  - id: CompanyUserId
  - company_id: CompanyId
  - user_id: UserId
  - role: CompanyUserRole (ADMIN, RECRUITER, VIEWER)
  - permissions: CompanyUserPermissions
  - status: CompanyUserStatus (ACTIVE, INACTIVE)
  - created_at: datetime
  - updated_at: datetime
```

## 🔄 Flujos Principales

### Flujo de Invitación

```
1. Admin invita usuario
   ↓
2. Se crea CompanyUserInvitation
   ↓
3. Se genera token único
   ↓
4. Se envía email con link
   ↓
5. Usuario hace clic en link
   ↓
6. Se muestra pantalla de aceptación
   ↓
7. Usuario acepta (nuevo o existente)
   ↓
8. Se crea/vincula CompanyUser
   ↓
9. Invitación se marca como ACCEPTED
```

### Flujo de Eliminación

```
1. Admin intenta eliminar usuario
   ↓
2. Validación: ¿Es último admin?
   → Sí: Error - No se puede eliminar
   → No: Continuar
   ↓
3. Validación: ¿Se está eliminando a sí mismo?
   → Sí: Error - No puedes eliminarte
   → No: Continuar
   ↓
4. Se desactiva CompanyUser (status = INACTIVE)
```

## 🧪 Testing

El sistema cuenta con tests completos:

### Tests Unitarios (Domain Layer)
- Tests de entidades (`CompanyUser`, `CompanyUserInvitation`)
- Tests de value objects (`CompanyUserPermissions`, `InvitationToken`)
- Tests de enums y validaciones

### Tests de Integración (Infrastructure Layer)
- Tests de repositorios
- Tests de persistencia
- Tests de conversión Entity ↔ Model

### Tests de Integración (Presentation Layer)
- **15 tests de endpoints**:
  - 9 tests para endpoints de invitaciones
  - 6 tests para endpoints de gestión de usuarios
- Casos de éxito y error
- Validaciones de negocio

## 📚 Referencias

- **Análisis completo**: `docs/security.md`
- **Plan de tareas**: `docs/security_task.md`
- **API Documentation**: http://localhost:8000/docs (cuando el servidor está corriendo)

## 🔒 Validaciones de Seguridad

1. **Token de Invitación**:
   - Mínimo 16 caracteres
   - Generación segura con `secrets.token_urlsafe()`
   - Expiración configurable (7 días por defecto)

2. **Validaciones de Negocio**:
   - No se puede eliminar el último admin
   - No puedes eliminarte a ti mismo
   - Invitaciones expiran después del tiempo configurado
   - Email único por empresa (no se puede invitar dos veces al mismo email)

3. **Validaciones de Datos**:
   - Validación de formato de email
   - Validación de permisos en value objects
   - Validación de roles en enums

## 🚀 Uso

### Invitar un Usuario

```bash
POST /company/{company_id}/users/invite
Content-Type: application/json

{
  "email": "nuevo.usuario@example.com",
  "role": "recruiter"
}
```

### Aceptar Invitación (Usuario Nuevo)

```bash
POST /invitations/accept
Content-Type: application/json

{
  "token": "token_de_invitacion",
  "email": "nuevo.usuario@example.com",
  "name": "Nuevo Usuario",
  "password": "password_seguro"
}
```

### Aceptar Invitación (Usuario Existente)

```bash
POST /invitations/accept
Content-Type: application/json

{
  "token": "token_de_invitacion",
  "user_id": "user-id-existente"
}
```

## 🔮 Mejoras Futuras

- [ ] Sistema de roles dinámicos (en lugar de enums fijos)
- [ ] Permisos a nivel de workflow/phase
- [ ] Historial de cambios de roles
- [ ] Notificaciones cuando se asigna/elimina usuario
- [ ] Rate limiting en endpoints de invitación
- [ ] Validación de dominio de email (si empresa requiere dominio específico)
- [ ] Logs de auditoría para invitaciones y cambios de roles

