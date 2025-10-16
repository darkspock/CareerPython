# Integración Mejorada de Procesamiento XAI

## Introducción

El sistema actual marca los PDFs como "completed" inmediatamente después de la subida, pero antes de que XAI termine de procesar y extraer los datos. Esto causa que la pantalla intermedia de procesamiento no espere a que XAI termine realmente, mostrando datos vacíos al usuario cuando debería mostrar los datos extraídos por la IA.

## Requisitos

### Requisito 1: Estados de Procesamiento Precisos

**User Story:** Como usuario que sube un PDF, quiero que el sistema espere a que la IA termine de procesar completamente mi currículum antes de mostrarme los datos extraídos, para que pueda revisar información precisa y completa.

#### Acceptance Criteria

1. WHEN un PDF es subido THEN el sistema SHALL marcar el estado como "processing" hasta que XAI termine completamente
2. WHEN XAI está procesando el PDF THEN el sistema SHALL mantener el estado como "processing" 
3. WHEN XAI termina exitosamente THEN el sistema SHALL actualizar el estado a "completed" y los datos extraídos SHALL estar disponibles
4. WHEN XAI falla en el procesamiento THEN el sistema SHALL actualizar el estado a "failed" con detalles del error
5. WHEN el procesamiento toma más de 60 segundos THEN el sistema SHALL marcar como "timeout" pero continuar procesando en segundo plano

### Requisito 2: Procesamiento Asíncrono Mejorado

**User Story:** Como usuario, quiero que el procesamiento de mi PDF sea completamente asíncrono para que no tenga que esperar en una página bloqueada, pero que reciba feedback preciso del progreso real.

#### Acceptance Criteria

1. WHEN un PDF es subido THEN el procesamiento SHALL ejecutarse de forma asíncrona usando background tasks
2. WHEN el procesamiento está en curso THEN el sistema SHALL proporcionar actualizaciones de estado precisas
3. WHEN el procesamiento se completa THEN los datos extraídos SHALL estar inmediatamente disponibles para el usuario
4. WHEN hay un error en el procesamiento THEN el sistema SHALL proporcionar información específica del error
5. WHEN el usuario consulta el estado THEN el sistema SHALL devolver el estado real del procesamiento XAI

### Requisito 3: Manejo de Errores de XAI

**User Story:** Como usuario, quiero recibir información clara cuando hay problemas con el procesamiento de mi PDF, para que pueda entender qué pasó y qué opciones tengo.

#### Acceptance Criteria

1. WHEN XAI no está disponible THEN el sistema SHALL marcar el estado como "failed" con mensaje "Servicio de IA temporalmente no disponible"
2. WHEN XAI devuelve un error THEN el sistema SHALL capturar el error específico y mostrarlo al usuario
3. WHEN XAI timeout ocurre THEN el sistema SHALL reintentar hasta 3 veces antes de marcar como "failed"
4. WHEN el procesamiento falla THEN el usuario SHALL poder continuar manualmente con el formulario
5. WHEN hay errores de parsing THEN el sistema SHALL proporcionar detalles específicos del problema

### Requisito 4: Sincronización Frontend-Backend

**User Story:** Como usuario, quiero que la pantalla de procesamiento refleje exactamente lo que está pasando en el backend, para que tenga confianza en el sistema y sepa cuándo mis datos estarán listos.

#### Acceptance Criteria

1. WHEN la pantalla de procesamiento consulta el estado THEN SHALL recibir el estado real del procesamiento XAI
2. WHEN XAI está procesando THEN la pantalla SHALL mostrar "Analizando con IA..." con indicador de progreso
3. WHEN XAI termina THEN la pantalla SHALL redirigir inmediatamente al formulario con datos pre-llenados
4. WHEN hay un error THEN la pantalla SHALL mostrar el mensaje específico del error
5. WHEN el timeout ocurre THEN la pantalla SHALL explicar que el procesamiento continúa en segundo plano

### Requisito 5: Datos Extraídos Disponibles

**User Story:** Como usuario, quiero que cuando el procesamiento se complete, todos mis datos extraídos estén inmediatamente disponibles en el formulario, para que pueda revisarlos y corregirlos si es necesario.

#### Acceptance Criteria

1. WHEN XAI completa el procesamiento THEN todos los datos extraídos SHALL estar guardados en la base de datos
2. WHEN el usuario accede al formulario de revisión THEN los datos SHALL estar pre-llenados automáticamente
3. WHEN hay datos parciales extraídos THEN el sistema SHALL mostrar lo que pudo extraer y permitir completar manualmente
4. WHEN no se pudieron extraer datos THEN el sistema SHALL explicar el problema y ofrecer entrada manual
5. WHEN los datos están disponibles THEN el sistema SHALL indicar claramente qué información fue extraída automáticamente

### Requisito 6: Background Task Management

**User Story:** Como administrador del sistema, quiero que el procesamiento de PDFs sea robusto y maneje correctamente los fallos, para que los usuarios tengan una experiencia confiable.

#### Acceptance Criteria

1. WHEN un PDF es subido THEN SHALL crearse un background task para el procesamiento XAI
2. WHEN el task está ejecutándose THEN el estado del asset SHALL reflejar "processing"
3. WHEN el task se completa exitosamente THEN SHALL actualizar el estado a "completed" y guardar los datos
4. WHEN el task falla THEN SHALL actualizar el estado a "failed" y registrar el error
5. WHEN el task toma demasiado tiempo THEN SHALL implementar timeout y cleanup apropiado

### Requisito 7: Logging y Monitoreo

**User Story:** Como desarrollador, quiero tener visibilidad completa del procesamiento XAI para poder diagnosticar problemas y mejorar el sistema.

#### Acceptance Criteria

1. WHEN el procesamiento inicia THEN SHALL registrar el inicio con timestamp y user_id
2. WHEN XAI es llamado THEN SHALL registrar la request y response (sin datos sensibles)
3. WHEN hay errores THEN SHALL registrar detalles completos del error para debugging
4. WHEN el procesamiento se completa THEN SHALL registrar métricas de tiempo y éxito
5. WHEN hay timeouts THEN SHALL registrar la duración y razón del timeout