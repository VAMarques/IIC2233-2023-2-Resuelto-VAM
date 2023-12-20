# Tarea 2 Entrega Intermedia: DCConejoChico 🐇💨

DCConejoChico es un juego proximamente disponible en DCCoolProgrammingGames.com.

¡Termina los laberintos para ayudar a Gatochico (quien ha sido transformada en Conejochico) a escapar de las garras de Pacalein!

## Consideraciones generales :octocat:

Esta implementado todas las funciones pedidas para la entrega intermedia, con dos funciones extras, raycaster() y encontrar_conejo(), las cuales son usadas para generalizar y modularizar otras funciones de funciones_cliente.py

Para las funciones fui un poco creativo, hay mucho uso de la programacion funcional y de las estructuras de datos, como las funciones lambda, map, any, all, uso de sets, uso de diccionarios en vez de if's... Queria hacer algo elegante, sobre todo mejorar mi metodo raycaster, del cual tome cierta inspiracion de lo que hice en la Tarea 1, pero obviamente lo adapte a lo requerido para la entrega intermedia.

La programacion es un poco interlingual, hay ingles y español mezclado, a mi personalmente me parece mas natural pues domino el ingles desde hace muchos años, no si es mala practica..

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Entrega Intermedia: ?? pts (25%)
##### ✅ funciones_servidor.py
##### ✅ funciones_cliente.py

Todas las funciones cumplen todos los testcases tanto dentro de Linux como en Windows.

## Librerías :books:
No fue hecho import de ninguna libreria, ni se creo ningun modulo externo a los principales archivos.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Consideracion 1: Se asume que el uso de U, D, L, R y otros caracteres singulares, seran excepciones a cualquier guia de estilo, pues el uso de estas letras esta explicitamente en el enunciado, otros ejemplos son los enemigos, LV, LH, CU... o las partes de las funciones de servidor, a, b, c, n.

2. Consideracion 2: En una issue se indico que el uso de any() es valido, por tanto, yo tambien lo aplique, y ademas implemente el uso de all(), que es su contraparte en el mismo sentido que ```and``` es contraparte de ```or```

PD: la breve descripcion que le di a la tarea hace una referencia a coolmathgames.com, que aunque yo no creci con ese sitio, era el que tenia mejor juego de palabras con DCC.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. <https://bobbyhadz.com/blog/python-check-if-string-contains-number>: este buscaba si una string tenia un numero y está implementado en el archivo <funciones_cliente.py> en las líneas <1 hasta 7>, yo personalmente lo encontre mas de inspiracion que de copia directa.

2. <https://stackoverflow.com/questions/13628791/determine-whether-integer-is-between-two-other-integers>: Aca yo descubri la sintaxis de (lower_bound <= value <= upper_bound) y esta implementado en 