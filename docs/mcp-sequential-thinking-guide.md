# Guía de Uso: MCP Sequential Thinking

## ¿Qué es Sequential Thinking MCP?

El MCP **sequential-thinking** es una herramienta que permite descomponer problemas complejos en pasos secuenciales, facilitando un análisis estructurado y revisable. Es especialmente útil para:

- Planificar tareas complejas
- Descomponer problemas en pasos manejables
- Estructurar el razonamiento de manera clara
- Crear listas de verificación para proyectos

## Configuración

El servidor MCP ya está configurado en tu proyecto. Si necesitas verificar o reinstalar la configuración, agrega esto a tu archivo de configuración MCP (generalmente en `.cursor/mcp.json` o la configuración global de Cursor):

```json
{
  "servers": {
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    }
  }
}
```

## Cómo Usarlo

### 1. Verificar que está disponible

En Cursor, el servidor MCP debería estar disponible automáticamente una vez configurado. Puedes verificar que está activo preguntándome directamente o usando comandos MCP.

### 2. Ejemplos de Uso

#### Ejemplo 1: Planificar una Feature Compleja

Puedes pedirme que use sequential-thinking para planificar una nueva funcionalidad:

```
Usa sequential-thinking para planificar la implementación de un sistema de notificaciones en tiempo real.
Crea una secuencia inicial de 6-8 pasos con entregables medibles para cada uno.
```

#### Ejemplo 2: Descomponer un Problema Técnico

Para problemas técnicos complejos:

```
Usa sequential-thinking para analizar cómo optimizar el rendimiento de las queries de base de datos.
Descompón el problema en pasos secuenciales con análisis y soluciones propuestas.
```

#### Ejemplo 3: Planificar un Refactor

Para refactorizaciones grandes:

```
Usa sequential-thinking para planificar la migración del sistema de autenticación a OAuth2.
Crea una secuencia de pasos con validaciones y puntos de control.
```

### 3. Uso Directo en Conversación

Cuando me pidas usar sequential-thinking, yo automáticamente:

1. **Analizo el problema** y lo descompongo en pensamientos secuenciales
2. **Creo pasos estructurados** con entregables claros
3. **Proporciono una lista de verificación** en formato markdown
4. **Permito revisión y ajuste** de los pasos según sea necesario

### 4. Parámetros del Sequential Thinking

Cuando uso sequential-thinking, puedo ajustar:

- **total_thoughts**: Número inicial de pasos (por defecto se ajusta según la complejidad)
- **thought_number**: Paso actual en el que estamos
- **is_revision**: Si estamos revisando un paso anterior
- **next_thought_needed**: Si necesitamos más análisis

## Ejemplo Práctico: Planificar Nueva Feature

**Tu solicitud:**
```
Usa sequential-thinking para planificar la implementación de un dashboard de analytics para candidatos.
```

**Mi respuesta usando sequential-thinking:**
1. **Análisis inicial**: Definir métricas clave y KPIs
2. **Diseño de datos**: Modelar estructura de datos para analytics
3. **Backend**: Crear endpoints y queries para métricas
4. **Frontend**: Diseñar componentes de visualización
5. **Testing**: Crear tests unitarios e integración
6. **Deployment**: Planificar rollout gradual

Cada paso incluirá:
- Entregables específicos
- Criterios de aceptación
- Dependencias con otros pasos
- Tiempo estimado

## Ventajas del Sequential Thinking

✅ **Estructura clara**: Los problemas complejos se dividen en pasos manejables  
✅ **Revisable**: Puedes revisar y ajustar pasos anteriores  
✅ **Medible**: Cada paso tiene entregables claros  
✅ **Iterativo**: Permite profundizar en pasos específicos según necesidad  

## Cuándo Usarlo

Usa sequential-thinking cuando:

- Necesitas planificar una feature grande
- Tienes un problema complejo que resolver
- Quieres estructurar tu razonamiento
- Necesitas crear una lista de verificación detallada
- Quieres asegurar que no se olviden pasos importantes

## Notas Importantes

- El servidor MCP se ejecuta automáticamente cuando lo uso
- No necesitas instalarlo manualmente (usa `npx` con `-y`)
- Puedo usar sequential-thinking en cualquier momento que lo solicites
- Los pasos pueden revisarse y ajustarse según avanza el proyecto

---

**¿Listo para probarlo?** Solo pídeme que use sequential-thinking para cualquier problema o tarea compleja que tengas.

