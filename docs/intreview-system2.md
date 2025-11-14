Casas a cambiar:
InterviewTypeEnum:
No tiene sentido lo que hemos hecho, una cosa es en que proceso se hace, otra es en que tipo de entrevista es.
Asi que deberiamos tener algo como:
InterviewPhaseTypeEnum:
* CANDIDATE_SIGN_UP
* CANDIDATE_APPLICATION
* SCREENING
* INTERVIEW
* FEEDBACK (Final)
InterviewTypeEnum:
* CUSTOM
* TECHNICAL
* BEHAVIORAL
* CULTURAL_FIT
* KNOWLEDGE_CHECK
* EXPERIENCE_CHECK

A la entrevista es obligatorio:
* CandidateId
* Lista de Roles
Opcional
* Lista de CompanyUserId

# Listado
Debe usar shadcn
Las entrevistas tienen tiene una fecha de calendario y una fecha límita opcional.
En el listado http://localhost:5174/company/interviews
en la cabecera, te propongo un rediseño.

Dividir la cabecera, mostrastando la información más importante a la izquierda:
* Pendientes de planificar. (sin fecha o sin entrevistador asignado) Con un link a que se filtre automáticamente.
* Planificadas. (Con fecha y entrevistador) Con link a filtro
* En proceso (fecha=hoy). Con link a filtro
* Finalizadas recientes. Con link a filtro a las realizadas en los ultimos 30 días.
* Las que han pasado fecha límite: Con link. Cursor=>Busca un nombre para esto.
* Pendiente de feedback o scoring. Con link.
* En la parte derecha:
* mostrar un calendario. 
* Indicando en los dias que hay entrevistas  el número de ellas. 
* Se puede hacer link para filtar por ese día.

Filtros:
* Búsqueda: Permite buscar por el nombre de la persona.
* Filtro por InterviewPhaseTypeEnum, InterviewTypeEnum y InterviewStatusEnum
* Filtro por fecha o rango de fechas.
* Filtro por JobPosition. Mostrando los que estén activos y los que han terminado en los últimos 30 días.
* Filtro por Entrevistador.

En el listado, cuando una entrevista no tenga fecha programada. Ahora mismo aparece N/A. permitir hacer click y que muestre el calendario
En el caso que tenga fecha, también.
Se tiene que poder especificar hora también.

En las columnas Entrevista y Tipo, fusionar en una. Poniendo Tipo en tamaño mas pequeño (9 o 10pt) debajo del nombre de la entrevista.
Necesitamos que aparezca la persona asignada (entrevistador) y si no hay ninguna, mostrar el role. Se puede hacer click para asignar.
Se muestra un popup para asignar (Se pueden asignar mas de uno, al menos uno por role). mostrando todos los empleados, un inputbox para filtrar mientras se escribe, y un botón que sea "Asignar a mi". Haz un componente para esto, que lo vamos a usar más vees.
