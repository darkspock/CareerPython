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

Reglas de negocio:
* Cada stage tiene uno o varios roles asignados.
* Cada stage puede tener reglas de validaciones. Estas validaciones las tendremos en JsonLogic. Necesitamos un campo para esto.
* Cada stage puede tener reglas recomendadas. Es como las validaciones, pero no impide el cambio de estado. También usaremos JsonLogic. 


Vamos a ir por partes:
1. Domain Entities. Confirmar que están bien, y que no tienen ninguna dependencia con otras entidades que impida que sea generico.
2. Reglas de negocio.
3. Repositorio. Usa tablas nuevas, olvida por ahora lo que habia antes.
4. Repasa las excepciones, que estén bien.
5. Comandos y Queries
5. Rutas y Controladores