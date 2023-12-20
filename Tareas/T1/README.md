# Tarea 1: DCChexxploding 💥♟️

¡Bienvenido a ```DCChexxploding```! el nuevo juego disponible para DCC-OS

Lee esta guia para aprender sobre las mecanicas de este increible juego.

Esta Tarea fue implementada por Victor Alonso Marques.


## Consideraciones generales :octocat:

Logre implementar todo lo pedido en la tarea, y unas cosas extra que me intereso añadir.

Puede correr todos los test_cases, y el menu cumple con lo pedido.

Tengan en cuenta al revisar que para el menu te va a pedir ```Si la respuesta es si, ingrese Y.```para confimar ciertas cosas, pues ciertas opciones no haran nada si no ingresan y o Y, en una version previa era unicamente Y mayuscula, pero cambie eso porque era muy irritante para usar el menu.

No estoy seguro de si segui por completo el PEP-8, hay algunas cosas de formato que hice segun lo que
me parecia correcto, por ejemplo, abreviar las palabras, como fila &rarr; fil.

Por otra parte hice algunas practicas quiza cuestionables, nada **prohibido** como ex\*c, ev\*l, o un except Except, pero por ejemplo hice un \_\_name\_\_ != \_\_main\_\_ ademas del normal, o por ejemplo, a una constante en main.py la llame LONG_BAR, lo que al parecer es parte de PEP-8, asi que no deberia haber mayor problema.

(ex\*c y ev\*l estan censuradas en caso de haber un filtro automatico, en todo caso mejor ni mencionarlas, son las funciones que no deben ser nombradas.)

La ultima consideracion es que yo use unos caracteres usados para crear cajas, si por algunas razon en la consola que usan para ejecutar main.py hay un vomito de caracteres, esta es la razon, y probablemente haya que instalar un paquete de caracteres, no estoy seguro.

Box-drawing characters.

- https://en.wikipedia.org/wiki/Box-drawing_character

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Menú: 18 pts (30%)
##### ✅ Consola
El menu recibe los argumentos necesarios desde la consola, asi que supongo que estara correcto, da los errores por separado dependiendo de si esta malo el nombre o si no existe el tablero, si se manda una combinacion invalida de argumentos se pide que el usuario intente de nuevo con una valida.
##### ✅ Menú de Acciones
Completo con las 4 acciones pedidas, todas funcionan, ademas, sale del programa en caso de que el usuario inicialize mal el menu.
##### ✅ Modularización
No hay archivo con mas de 400 lineas.
##### ✅ PEP8
Desde mi criterio, yo segui en gran medida el PEP-8, en los if (): especificamente yo los uso con parentesis, lo que al linter automatico no le gusta, pero para mi hace mas facil revisar lo que estan haciendo.

En main.py la constante LONG_BAR esta en UPPER_CASE, segun entiendo esto es correcto para PEP-8

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` en ```T1/```. Ademas de los test_cases que tengan los ayudantes a mano.

Ademas, los siguientes archivos son obligatorios, sin contar a ```main.py```:

1. ```pieza_explosiva.py``` en ```T1/```
2. ```tablero.py``` en ```T1/```
3. ```funciones.menu``` en ```T1/```

Los siguientes archivos son opcionales:

4. ```abrir_incorrecto.py``` en ```T1/```
5. ```tech_demo.txt``` en ```T1/```

Los siguientes archivos se asume que los tienen los que revisaran la tarea, no se incluyen, pero de todos modos son obligatorios:

5. ```imprimir_tablero.py``` en ```T1/```
6. ```tableros.txt``` en ```T1/```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```sys```: ```argv / main.py```
2. ```os```: ```os.listdir() / main.py```
3. ```copy```: ```deepcopy() / tablero.py```

### Librerías propias
Por otro lado, los módulos que fueron creados, los cuales no incluyen aquellos requeridos por el enunciado, fueron los siguientes:

1. ```funciones_menu.py```: Contiene a ```abrir_tablero()```, ```imprimir_menu()```, usado en ```main.py```

2. ```abrir_incorrecto.py```: Hecha para abrir de manera incorrecta ```main.py```, no es obligatoria, pero al hacerlo muestra un mensaje de error indicando que debes abrir ```main.py``` de manera directa.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Abreviacion de filas &rarr; fil y columnas &rarr; col:

La razon es que haciendo esto tienen el mismo largo, y son un poco mas compactas, personalmente me desagradan las variables largas, y si fuera por mi serian i, j en vez de fil, col, pero eso ya iria en contra de PEP-8

2. if, elif, redundante:

Esto aparece en el metodo solucionar, hay 3 if y elif que tienen el mismo efecto, mi razon de porque, es que cuando se ejecuta el primero, no se va a ejecutar el segundo ni tercero, y para este metodo las optimizaciones son importantes, gracias a esto de hecho, algunos tableros de 9x9 se pueden resolver.

3. try, except:

Use una vez un try, except, pero lo use apropiadamente para detectar cuando el usuario quiere abortar el proceso de solucionar el tablero en el menu, si los tableros son muy grandes pueden tomarse minutos en resolver, y por tanto es mejor dar la opcion de arrepentirse en vez de tener que cerrar la consola.

PD: Las siguientes funciones dentro de ```tablero.py``` son dependencias de las otras funciones que si se revisan, se crearon para facilitar el desarollo, y para optimizar el codigo.
### peones_invalidos
- peones_vecinos
### celdas_afectadas
- explosiva_raycaster
### solucionar
- es_solucion
- inviable
- peon_redundante
- es_valido
- sanitizar

PD2: Hay una funcion del menu especial, cuando usas solucionar, te permite cancelar con CTRL-C, la mayoria de tableros se resuelven tan rapido que no se puede probar la eficacia de esta funcion, como manera de probarla, se incluye un archivo tech_demo.txt, el cual incluye un tablero 9x9 que se demora bastante tiempo en procesar, gracias a eso se puede probar esta funcionalidad del menu.

PD3: Hay aun mas errores del menu si lo inicializas mal.
1. Si es que lo abres desde otro archivo.py, como abir_incorrecto.py
2. Si es que no existe tableros.txt, te advierte sobre si estas en la carpeta T1, y si lo estas, que incluyas el archivo.
3. Si no le diste exactamente 2 argumentos para nombre y tablero.
4. Si el nombre o el tablero son incorrectos

PD4: La advertencia 1. utiliza if (\_\_name\_\_ != \_\_main\_\_), esto podria considerarse extraño, pero queria que existiera un error de mensaje si hacias eso y no que no hayan errores.


-------

## Referencias de código externo :book:

Para realizar el solucionador del tablero me inspire bastante en este video:
1. \<https://www.youtube.com/watch?v=G_UYXzGuqvM>:

Obviamente no esta copiado directamente, pero trate de implementar la misma idea, de hecho todavia es posible encontrar similitudes en estructura.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).