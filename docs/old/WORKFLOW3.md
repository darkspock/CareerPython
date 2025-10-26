## Candidate Applicatoin

Un candidato puede tener varios workflows. Estos workflows son por ahora fijos y hay 3:
De forma que un candidate_application, tiene un workflow_id y stage_id y un workflow_type. Pues dentro de un type puede haber varios según el tipo de posición.
Dentro de candidate application, tendremos un json Data con información que vamos a ir recopilando durante el proceso.

## Sourcing.
Proceso de screening y descarte. Este flujo no será personalizable por ahora, tendremos las siguientes fase.
* Pending
* Screening
* Descartado
* On Hold
* To talent Pool. Este caso en concreto, vamos a tener una tabla company_talent_pool con el candidate Id y comentarios,

* Una vez aceptado el candidato pasa a evaluación.

## Evaluation
Este es el flujo que ya hemos definido con fases que se pueden personalizar.

## Offer and Pre-Onboarding
Este flujo tambien es personalizable, inicialmente:
* Offer Proposal
* Negotiation
* Document Submission
* Document Verification

## STAGES
Para gestionar las fases, vamos a tener una tabla workflow_stages.
* tendremos las fechas de inicio, fin, deadline, coste de la fase (optional) y automático obtenido de la configuración del workflow.
* Tendremos un campo de comentarios
* Y tendremos DATA, json con información que se captura en esta fase. Esta información al terminar la fase, se guarda tambien en candidate_application

## EMAIL
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


