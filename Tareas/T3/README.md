# Tarea 3: DCCine 🎬🎥

Despues del gran exito con DCConejoChico (En destrozar las notas de los estudiantes) llega de parte de **IIC2233 TEAM** ¡DCCINE!

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

La verdad no he llegado a comprender exactamente cuanto detalle debo dar, porque a cierto nivel es mejor simplemente hacer comentarios en el codigo que explicar, dare un breve resumen entonces.

####  Programación funcional
##### ✅ Utiliza 1 generador
##### ✅ Utiliza 2 generadores
##### ✅ Utiliza 3 o más generadores

Implementados, corren todos los test_case publicos, hasta donde yo se no hay problemas, hay listas, diccionarios, y sets por comprension, no generados como Objeto(), talvez la implementacion podria ser mejor, pero hice lo mejor que pude en mi consciencia.

####  API
##### ✅ Obtener información
##### ✅ Modificar información

Literalmente casi copiado desde mi actividad 5, lo unico que cambie fue algunas funciones que eran parcialmente distintas.

## Ejecución :computer:

Los unicos archivos que razonablemente deben ser ejecutados son los tests, aun asi, deben estar presentes:

1. ```consultas.py```
2. ```peli.py```
3. ```utilidades.py```
4. ```api.py```

## Librerías :books:
### Librerías externas utilizadas

La lista de librerías externas que utilicé fue la siguiente:

1. ```collections```: ```Counter()```
2. ```itertools```: ```None, no fue usada```
3. ```functools```: ```reduce()```
4. ```math```: ```ceil()```
5. ```requests```: ```get(), post(), put(), patch(), delete()```
6. ```datetime```: ```date()```

### Librerías propias
No se crearon librerias extras, tampoco funciones que no esten definidas dentro de las mismas funciones, aunque si pienso mejorar un poco la legibilidad, o abstraerlo, necesitaria crear un archivo, aunque es posible que no tenga tanto tiempo pensando en otros ramos, por tanto dejo parcialmente la template por si quisiera crear el archivo:

1. ```auxiliares```: ```funciones para consultas```

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Creé funciones dentro de funciones que son espontaneas, para mi son como usar un lambda x mas grande, podria abstraerlas mas poniendolas en un archivo separado, pero prefiero usar ese tiempo en otras cosas.

2. Use slicing de listas en linea 81 de consultas.py, esto puede considerarse que crea una lista, [sin embargo se explicito en una issue que esto es legal.](https://github.com/IIC2233/Syllabus/issues/428)

3. Solo por si acaso, tengo dos .gitignore, uno que es global al repositorio y otro local a esta tarea, que viene incluido en la misma carpeta, uno ignora cosas mas generales como archivos pdf pero el de la tarea ignora las cosas que se piden ignorar, ademas de ignorar redundantemente cosas de python y de otros sistemas.

PD: Cualquier, o casi cualquier cosa hecha la hice pensando en las issues presentes.


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. [collections](https://docs.python.org/3/library/collections.html) : Documentacion de collections, usado para Counter()
2. [datetime](https://docs.python.org/3/library/collections.html) : Documentacion de datetime, usado para date()
3. Mi propia Actividad 5, esto para evadir el tema del autoplagio, tengo que referenciar que es trabajo previo, o al menos eso espero, el codigo es tan similar que pude simplemente hacer copy-paste en la mayoria de las partes

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).