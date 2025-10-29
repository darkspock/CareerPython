## Candidate Application
Cada empresa define una serie de fases por las que pasa el candidato.
Estas fases son personalizables por la empresa:
* Nombre de la fase
* sort_order
* Vista por defecto: Kanban/listado
* Objetivo de la fase: Texto explicativo que usará la IA para ayudar.
Dentro de cada fase, el candidato tendrá un workflow (ya tenemos eso hecho).

De forma que un candidate_application tiene:
* phase id
* workflow id
* stage id

Dentro de candidate application, tendremos un json Data con información que vamos a ir recopilando durante el proceso.

Los workflow por defecto están en status draft, y pueden estar activos o archivados. Cambia WorkflowStatusEnum, 
ahora mismo tiene otros valores.
Cuando creas un workflow está en draft hasta que le das a activar.

Repetimos, una empresa pueda configurar:
* Fases
* Workflows (que debe elegir a que fase pertenece)
* Stages. Dentro de stages, que ya está hecho, en StageType, hay que quitar custom y poner fail, y cambiar final, por success.

## OpenPosition
Cuando creamos una posición, tenemos que indicar que flujo va a seguir. 
Así que mostraremos todas las fases para que eliga que flujo seguir en cada fase.
Para simplificar la usabilidad, si sólo hay un workflow activo para esa fase, se selecciona automáticamente y no permite elegir.
En el caso de que sólo hubiera en workflow activo en cada una de las fases, no se muestra configuración. Se almacena, pero no se muestra.

## CANDIDATE STAGES
Para gestionar las fases, vamos a tener una tabla candidate_stages.
* tendremos las fechas de inicio, fin, deadline, coste de la fase (optional) y automático obtenido de la configuración del workflow.
* Tendremos un campo de comentarios
* Y tendremos DATA, json con información que se captura en esta fase. Esta información al terminar la fase, se guarda tambien en candidate_application

* Cuando se llega a un stage de tipo success, el usuario se pasa a la siguiente fase.
* En cualquier momento el usuario, desde el estado lost, puede mover a otra fase. 

## Company Onboarding
Cuando activamos una empresa, (o se hace un reset de configuración en sus ajustes), se crea por defecto una serie fases predefinidas.

## Sourcing.
Proceso de screening y descarte. Por defecto agregaremos las siguientes fases.
* Pending
* Screening
* Cualificado
* No apto
* On Hold

## Evaluation
Flujo por defecto configurado a:
* Entrevista Recursos Humanos
* Entrevista Manager
* Prueba
* Entrevista Directivo
* Seleccionado
* Descartado

## Offer and Pre-Onboarding
Flujo por defecto a:
* Offer Proposal
* Negotiation
* Document Submission
* Document Verification
* Lost

## Talent Pool
* Welcome
* Recovered
* Lost

# EMAIL
En cada fase, podemos enviar emails, por lo que necesitamos:
* option to define email templates, we will embed unlayer
* in each stage, define the template for automated email
* Also, predefined message to include in the template

## DATA
each workflow has custom fields
* text
  * fixed
  * text area
* fixed answer:
  * dropdown
  * checkbox
  * radio
* date & time
  * date time
  * time
* file
* number
  * currency
  * integer
  * float
  * percentage

At stage level, we can configure how fields will work
* each fields can be hidden, mandatory, recommended, or optional
That ensures that the workflow is flexible enough to be used in different scenarios.
And we have the correct outcome for the process.


