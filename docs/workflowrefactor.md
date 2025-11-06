Anteriormente teniamos varios sistema de workflow y nos hemos quedado en medio de un refactoring.

Vamos a hacer algo mejor, un unico motor de workflow que sirve para:
* Job Position Openings
* Candidate Applications
* Candidate Onboarding
  (Enum WorkflowTypeEnum)

Entonces vamos a hacer lo siguiente.

Primero arreglar el Workflow.
Por ahora nos olvidamos de lo que habia antiguo, despues lo eliminaremos.
Solo quiero arreglar la carpeta /src/workflow.


Entidades:
* Workflow
* WorkflowStage

El objetivo de src/workflow es permitir gestionar cualquier tipo de workflow.

Asi que, arregla workflow.

