# Plan de Implementación - Integración XAI Mejorada

## Tareas de Backend

- [x] 1. Crear sistema de background tasks para procesamiento XAI
  - Implementar `XAIProcessingTask` que ejecute el procesamiento de forma asíncrona
  - Configurar task queue (usando asyncio o similar)
  - Añadir manejo de timeouts y reintentos
  - _Requirements: 1.1, 1.3, 6.1, 6.2_

- [x] 2. Modificar handler de upload para usar background tasks
  - Actualizar `UploadResumeHandler` para no marcar como "completed" inmediatamente
  - Cambiar estado inicial a "processing" cuando se inicia el background task
  - Remover procesamiento XAI síncrono del handler
  - _Requirements: 1.1, 1.2, 2.1_

- [x] 3. Implementar actualización de estados durante procesamiento XAI
  - Modificar `ResumeUploadedHandler` para actualizar estado del asset
  - Añadir actualización a "completed" cuando XAI termina exitosamente
  - Implementar actualización a "failed" con detalles de error
  - _Requirements: 1.3, 1.4, 3.1, 3.2_

- [x] 4. Mejorar endpoint de processing status
  - Actualizar `/api/files/processing-status` para devolver estados precisos
  - Añadir información detallada de errores XAI
  - Incluir timestamp de última actualización
  - _Requirements: 2.2, 4.1, 5.4_

- [ ] 5. Implementar manejo robusto de errores XAI
  - Añadir captura específica de errores de XAI service
  - Implementar reintentos automáticos (máximo 3 intentos)
  - Crear mensajes de error user-friendly
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 6. Añadir logging y monitoreo mejorado
  - Implementar logging detallado del procesamiento XAI
  - Añadir métricas de tiempo de procesamiento
  - Crear alertas para fallos frecuentes
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

## Tareas de Frontend

- [x] 7. Actualizar PDFProcessingPage para estados precisos
  - Modificar polling para interpretar estados reales de XAI
  - Añadir manejo específico para estado "processing" vs "completed"
  - Mejorar mensajes de estado para reflejar procesamiento real
  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 8. Implementar timeout inteligente
  - Cambiar timeout de 30 a 60 segundos para dar más tiempo a XAI
  - Añadir mensaje explicando que procesamiento continúa en segundo plano
  - Permitir continuar manualmente después del timeout
  - _Requirements: 1.5, 4.4, 4.5_

- [ ] 9. Mejorar indicadores visuales de procesamiento
  - Añadir indicador específico "Analizando con IA..."
  - Mostrar tiempo transcurrido durante procesamiento XAI
  - Añadir animaciones para indicar procesamiento activo
  - _Requirements: 4.2, 5.5_

- [ ] 10. Actualizar manejo de errores en frontend
  - Mostrar mensajes específicos de errores XAI
  - Añadir opciones de reintento para errores temporales
  - Mejorar UX para diferentes tipos de error
  - _Requirements: 3.4, 4.4_

## Tareas de Integración

- [ ] 11. Actualizar CompleteProfilePage para datos XAI
  - Verificar que datos extraídos por XAI estén disponibles
  - Mejorar carga de datos del endpoint de profile summary
  - Añadir indicadores de qué datos fueron extraídos automáticamente
  - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [ ] 12. Implementar sincronización frontend-backend
  - Asegurar que estados del frontend reflejen backend exactamente
  - Añadir manejo de desconexiones de red durante polling
  - Implementar cache local para reducir requests
  - _Requirements: 4.1, 4.5_

## Tareas de Testing

- [ ] 13. Crear tests para background task system
  - Test de procesamiento XAI exitoso
  - Test de manejo de errores XAI
  - Test de timeouts y reintentos
  - _Requirements: 6.3, 6.4, 6.5_

- [ ] 14. Crear tests de integración frontend-backend
  - Test de flujo completo de procesamiento
  - Test de polling y actualización de estados
  - Test de manejo de errores end-to-end
  - _Requirements: 2.3, 4.1, 4.5_

- [ ] 15. Crear tests de performance y reliability
  - Test de carga con múltiples PDFs simultáneos
  - Test de recuperación de fallos XAI
  - Test de cleanup de tasks huérfanos
  - _Requirements: 6.5, 7.4_