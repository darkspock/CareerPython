Se le está enviando un link a los candidatos como este:

http://localhost:5173/candidate/registration/verify/V4QfoZHTztg66-DDZ8f3VoStsEXsTl4Gx9wPClFWJoI

hemos revisado el proceso como 10 veces y falla constantemente.

Cuando algo falla tanto, es por que está mal diseñado o estamos mirando donde no es:

# Estrategía
Analizar que le ocurre a este enlace.
¿Se ha generado mal? ¿Le falta un registro en la bbdd?¿no cumple con las condiciones?

Establecer una politica de idempotencia y consistencia eventual para el link. Da igual si recibo un
link para crear una cuenta o para continuar el proceso. El link debe funcionar si o si. 
Si la cuenta existe, me da acceso y se impersona al usuario (login por link)
Si la cuenta no existe, se crea y se hace login.
Pero teniendo un link en el correo, NUNCA debe fallar.

