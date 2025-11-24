Necesitamos algunas reglas que nos permitan mover de forma automática un candidato de una etapa a la siguiente.
Como ejemplo, en el flujo de Source, todos los candidatos entran en el primer stage. Antes de pasar por el proceso de screening,
se pueden agregar filtros de rechazo automático. Si un candidato no incumple nada, se pasa de forma automatica a la siguiente fase.
En HR no se suelen utilizar reglas en real-time, cuando un candidato se apunta a una oferta, se espera un tiempo hasta que se le notifica el siguiente paso o si está descalificado (desconozo los motivos).

A nivel de stage, vamos a poner una propiedad que indica si automáticamente se mueven al siguiente paso si se cumplen con todos los requisitos.

Teniamos pendiente de implementar JsonValidator basado en los custom fields.
Pero ademas vamos a meter más validaciones.
1. Con los campos que ya tenemos del candidato de work_modality, languages, expected_annual_salary, current_annual_salary, city, country.
2. Con el número de veces que ha aplicado a la misma oferta en un periodo de tiempo.
3. Con el número de veces que ha aplicado a cualquier oferta en un periodo de tiempo. 
4. Detector de Spam

