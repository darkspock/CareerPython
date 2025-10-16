# Generación de Curriculum Vitae (Resume)

## Visión General

El sistema de generación de CVs es una solución diseñada para facilitar a los candidatos la creación de currículums
personalizados, optimizados y adaptados a sus necesidades profesionales. Desde la perspectiva de Recursos Humanos (RRHH)
y reclutamiento, este sistema agiliza el proceso de creación de CVs, mejora la calidad del contenido presentado a los
empleadores y permite a los candidatos destacar en procesos de selección mediante personalización y asistencia de
inteligencia artificial (IA). El sistema es flexible, escalable y está diseñado para integrarse con datos de perfiles de
candidatos y ofertas de trabajo, ofreciendo una experiencia eficiente tanto para los usuarios como para los
reclutadores.

## Arquitectura y Diseño

### Estructura del Dominio (DDD)

#### Entidades Principales

- **Resume**: Entidad principal que representa un CV
- **ResumeContent**: Value Object con el contenido básico
- **AIGeneratedContent**: Value Object con contenido generado por IA
- **ResumeFormattingPreferences**: Value Object con preferencias de formato

#### Enums

- **ResumeType**: `GENERAL`, `POSITION`, `ROLE`
- **ResumeStatus**: `DRAFT`, `GENERATING`, `COMPLETED`, `ERROR`
- **AIEnhancementStatus**: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`, `NOT_REQUESTED`

### Patrones de Arquitectura

- **CQRS**: Separación entre comandos (escritura) y queries (lectura)
- **Repository Pattern**: Abstracción de acceso a datos
- **Factory Methods**: Creación de resumenes específicos
- **Value Objects**: Para contenido, preferencias y datos complejos

## Funcionalidades Implementadas

### 1. Creación de CVs

#### Tipos de CV Disponibles

- **CV General**: Para uso multipropósito
- **CV Específico para Posición**: Personalizado para una oferta
- **CV por Rol/Área**: Enfocado en un área profesional específica


### 2. Contenido del CV
Un CV tiene varias secciones. Hay secciones fijas y secciones variables.
#### Secciones Fijas
* Datos Generales: titulo de CV, email, teléfono, nombre
* Necesito un value object para los datos generales

#### Secciones Variables
Un CV puede tener varias secciones variables. Cada sección variable tiene:
* key
* title
* content
* el contenido de las secciones variables puede ser htnml.

#### Secciones Implementadas
- **Summary**: Por defecto vacio.
- **Experiencia Profesional** : Listado de experiencias profesionales de la tabla candidate_experience
- **Educación**: Listado de formaciones académicas de la tabla candidate_education
- **Proyectos**: Listado de proyectos de la tabla candidate_project (si existe alguno)
- **Habilidades** (`skills`): De candidate.skills


## Editor de CV
El editor de CV es wysiwyg.
Se pueden agregar secciones y contenido.
Se puede eliminar una sección.