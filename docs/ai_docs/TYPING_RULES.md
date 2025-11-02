# Reglas de Tipado - Commands y Queries

## ⚠️ REGLA CRÍTICA: Tipado de Commands y Queries

**Los Commands y Queries DEBEN usar Value Objects directamente, NO strings.**

### ✅ CORRECTO

```python
from dataclasses import dataclass
from src.company.domain.value_objects import CompanyId, CompanyUserId
from src.company.domain.enums import CompanyUserRole
from src.user.domain.value_objects.UserId import UserId
from src.company.domain.value_objects.invitation_token import InvitationToken
from src.shared.application.command_bus import Command, CommandHandler

@dataclass
class InviteCompanyUserCommand(Command):
    """Command to invite a user to a company"""
    company_id: CompanyId  # ✅ Value Object
    email: str
    invited_by_user_id: CompanyUserId  # ✅ Value Object
    role: Optional[CompanyUserRole] = None  # ✅ Enum


@dataclass
class AcceptUserInvitationCommand(Command):
    """Command to accept a user invitation"""
    token: InvitationToken  # ✅ Value Object
    user_id: Optional[UserId] = None  # ✅ Value Object


@dataclass
class AssignRoleToUserCommand(Command):
    """Command to assign a role to a company user"""
    company_id: CompanyId  # ✅ Value Object
    user_id: UserId  # ✅ Value Object
    role: CompanyUserRole  # ✅ Enum


@dataclass
class GetUserInvitationQuery(Query):
    """Query to get a user invitation by token"""
    token: InvitationToken  # ✅ Value Object
```

### ❌ INCORRECTO

```python
# ❌ NUNCA usar strings para IDs o value objects
@dataclass
class InviteCompanyUserCommand(Command):
    company_id: str  # ❌ INCORRECTO
    user_id: str  # ❌ INCORRECTO
    role: str  # ❌ INCORRECTO
    token: str  # ❌ INCORRECTO
```

## 📍 Dónde hacer la conversión

### ✅ CORRECTO: Conversión en Controller/Router

```python
class CompanyUserController:
    def invite_company_user(
        self,
        company_id: str,  # Recibe string del HTTP request
        request: InviteCompanyUserRequest,
        current_user_id: str
    ):
        # ✅ Conversión aquí, en el Controller
        command = InviteCompanyUserCommand(
            company_id=CompanyId.from_string(company_id),
            email=request.email,
            invited_by_user_id=CompanyUserId.from_string(current_user_id),
            role=CompanyUserRole(request.role) if request.role else None
        )
        self.command_bus.dispatch(command)
```

### ❌ INCORRECTO: Conversión en Handler

```python
class InviteCompanyUserCommandHandler(CommandHandler):
    def execute(self, command: InviteCompanyUserCommand) -> None:
        # ❌ NUNCA hacer conversión aquí
        company_id = CompanyId.from_string(command.company_id)  # ❌ INCORRECTO
        # El handler debe recibir value objects directamente
```

## 📋 Checklist de Tipado

Al crear un nuevo Command o Query:

- [ ] ¿Todos los IDs usan Value Objects? (`CompanyId`, `UserId`, `CompanyUserId`, etc.)
- [ ] ¿Todos los tokens usan Value Objects? (`InvitationToken`, etc.)
- [ ] ¿Todos los enums están tipados correctamente? (`CompanyUserRole`, etc.)
- [ ] ¿Las conversiones de string → value object están en el Controller/Router?
- [ ] ¿El Handler NO hace conversiones, solo trabaja con value objects?

## 🔍 Ejemplos de Value Objects comunes

```python
# IDs
from src.company.domain.value_objects import CompanyId, CompanyUserId
from src.user.domain.value_objects.UserId import UserId

# Tokens
from src.company.domain.value_objects.invitation_token import InvitationToken

# Enums (NO son value objects, pero se importan del dominio)
from src.company.domain.enums import CompanyUserRole
```

## 💡 Razones

1. **Type Safety**: Los value objects garantizan que solo valores válidos pasen al handler
2. **Validación temprana**: Las validaciones ocurren al crear el value object en el controller
3. **Consistencia**: Todos los handlers trabajan con los mismos tipos del dominio
4. **Mantenibilidad**: Si cambia la estructura del ID, solo se cambia el value object
5. **Separación de responsabilidades**: El controller se encarga de la conversión HTTP → dominio, el handler trabaja solo con el dominio

## 📝 Nota sobre Queries

Las Queries siguen las mismas reglas que los Commands:

```python
@dataclass
class GetUserInvitationQuery(Query):
    """Query to get a user invitation by token"""
    token: InvitationToken  # ✅ Value Object, NO str
```

```python
# En el router/controller:
token_vo = InvitationToken.from_string(token_str)  # ✅ Conversión aquí
query = GetUserInvitationQuery(token=token_vo)
dto = query_bus.query(query)
```

---

**Recuerda**: Si el campo representa un concepto del dominio (ID, token, etc.), debe ser un Value Object, NO un string.

