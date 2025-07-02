Documentación de la Arquitectura
1. Visión General
El sistema está diseñado como un sistema experto clásico basado en reglas, utilizando un motor de inferencia de encadenamiento hacia adelante (forward chaining). La arquitectura es modular para permitir la fácil expansión de la base de conocimiento sin modificar la lógica central.

2. Descripción de Componentes (src/core)
Motor de Inferencia (motor_inferencia.py):

Función: Es el componente principal que orquesta el proceso de razonamiento. Su responsabilidad es ejecutar el ciclo Match-Conflict Resolution-Act.

Operación: En cada ciclo, compara los hechos en la Memoria de Trabajo con las reglas de la Base de Conocimiento, utiliza la Agenda para decidir qué regla ejecutar y le pide al Parser que la aplique.

Memoria de Trabajo (memoria_trabajo.py):

Función: Actúa como la memoria a corto plazo del sistema. Almacena los hechos para una consulta específica.

Contenido: Guarda los hechos iniciales (proporcionados por el usuario) y los hechos derivados (generados por el sistema durante la inferencia). Se limpia al inicio de cada nueva consulta.

Agenda (agenda.py):

Función: Gestiona el conjunto de reglas que han sido activadas (cuyas condiciones se cumplen).

Resolución de Conflictos: Cuando múltiples reglas se activan simultáneamente, la Agenda utiliza una estrategia (en nuestro caso, PRIORIDAD_EXPLICITA) para seleccionar cuál ejecutar primero, evitando la indecisión.

3. Descripción de Componentes (src/knowledge)
Base de Conocimiento (base_conocimiento.py):

Función: Contiene el conocimiento experto del dominio (botánica de TDF). Es la memoria a largo plazo del sistema.

Implementación: Está compuesta por una lista de Reglas de Producción. Cada regla es un objeto que define un conjunto de condiciones (SI) y acciones (ENTONCES).

Parser de Reglas (parser_reglas.py):

Función: Actúa como el "intérprete" del sistema. Es el único componente que sabe cómo leer y ejecutar una regla.

Operación: El Motor de Inferencia le entrega una regla, y el Parser se encarga de evaluar sus condiciones contra la Memoria de Trabajo y de ejecutar sus acciones.

4. Flujo de Datos de una Consulta
El usuario envía sus selecciones a través de la Interfaz Web.

La API (api.py) recibe los datos y los pasa al Sistema Experto.

El sistema carga los datos como hechos iniciales en la Memoria de Trabajo.

El Motor de Inferencia inicia su ciclo.

En la fase MATCH, el Parser evalúa las reglas de la Base de Conocimiento contra los hechos. Las reglas válidas se añaden a la Agenda.

En la fase CONFLICT RESOLUTION, la Agenda selecciona la regla de mayor prioridad.

En la fase ACT, el Motor le pide al Parser que ejecute las acciones de la regla seleccionada, lo que puede generar nuevos hechos en la Memoria de Trabajo.

El ciclo se repite hasta que no hay más reglas que ejecutar.

Las conclusiones finales se devuelven a la API y se muestran en la Interfaz Web.