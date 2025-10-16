## Proceso de onboarding
Los candidatos pueden entrar en la aplicación a través de una página de onboarding.
Crea las páginas que después se puedan entrar para editar, no solo son de creación.
Hay navegación delante/atrás


### Página 1
En la primera página, se pedirá el email y subir un pdf.

El pdf se extrae el texto y se almacena en la tabla user_assets.

Si podemos sacar por expresiones regulares el nombre y apellidos, se almacenan en la tabla users. 
Más tarde lo analizaremos con IA, pero ahora mismo no (segunda fase).

Al hacer submit si el email no existe, se crea un usuario anonimo con password aleatorio.
En la url puede venir de forma opcional un JobPositionId, se apunta al usuario al jobPosition. necesitamos una tabla de CandidateApplication.

Se envia un email con un link para que pueda cambiar la contraseña.

Para enviar emails usaremos el API de mailgun. Tendremos un Comando encargado de eso. Necesitamos src/notification, 
con el codigo para enviar en la parte de Infra.

Si el email ya existe, se redirige a la página de login y después se vuelve a la landing.

Despues continua con la página 2

### Página 2
Aquí se preguntan los datos del candidato, separa los campos requeridos de los opcionales, que se ponen abajo
separando el área con "más información o similar".

### Página 3
Experiencia profesional, permite agregar las experiencias.
Está ordenado por fecha de inicio, haz un modal, en el listado aparece el puesto, empresa y fechas.

### Página 4
Educación, igual que la anterior. Botón de omitir sección.

### Página 5
Proyectos. Botón de omitir y guardar.

### Página 6
Se muestra un CV construido con la información. Un botón para cambiar, que te lleva a la página 2.
Lo dejamos por ahora aquí.
