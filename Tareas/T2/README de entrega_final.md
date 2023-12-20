# Tarea 2: DCConejoChico 🐇💨

DCConejoChico es un juego ahora disponible en DCCoolProgrammingGames.com.

¡Termina los laberintos para ayudar a Gatochico (quien ha sido transformada en Conejochico) a escapar de las garras de Pacalein!

Despues de varios problemas de infraestructura de ultimo minuto, finalmente el juego esta de vuelta en linea, ¡disfruten!

## Consideraciones generales :octocat:

Fue una tarea muy dificil y muy larga, trabaje en ella casi 80 horas esta semana, y en total superara las 100, pero el esfuerzo lo valio porque la implementacion me dejo orgulloso, a pesar de ser muy desordenada en el backend de los niveles.

(Desordenada para mi, a lo mejor en realidad es un codigo bastante simple, pero no estoy seguro de si lo que hice estara 100% correcto.)

**Recuerden ver la seccion de ejecucion para instrucciones de como abrir esta tarea.**

La mayoria si no es que todos los archivos son obligatorios, incluyendo los Json

Hay mucho contenido como para explicar simplemente, pero hice unos diagramas para que se puedan orientar con la multitud de cosas que hay.

#### Diagrama de clase

- https://drive.google.com/file/d/1fN8wV38Mr_Th2bFB06S_7P6k06KwiQm7/view?usp=sharing

- En flechas rojas se describe herencia

- En flechas verdes se describe Inicializacion, es decir, cuando se hace Clase(Argumentos)

- En flechas magenta punteadas se describe inclusion, es decir, si tengo objeto_1, entonces si hago objeto_2.incluido = objeto_1, eso es inclusion, eso pasa con ciertas clases, especificamente TODAS las entidades contienen el laberinto, y zanahoria, bomba manzana, y bomba congelacion se auto-incluyen en el laberinto

- En cuadros negros esta cada archivo.

- En naranjo esta el nombre del archivo.

#### Diagrama de importacion.

- https://drive.google.com/file/d/1rmlT92nfpMJ84LkwzlVINVrhRmkVPQ20/view?usp=sharing

- Una flecha es que ese archivo se importa en la direccion de la flecha, una flecha con puntos es que se añade a la importacion de la flecha a la cual llega, por tanto, laberinto.py importa todos conejo.py, clases_laberinto.py, clases_abstractas.py, backend_utilities.py

#### Otras consideraciones

No se como ayudar a que se entienda lo que hice, es una cosa **super** desordenada pero funcional, sobre todo las Laberinto y sus Entidades, yo recomiendo revisar todos esos archivos juntos, pues hay que saltar de uno hacia el otro para entender la funcionalidad.

Especificamente el mecanismo de laberinto es desordenado, pues hay muchas funciones siendo intercambiadas entre el laberinto y sus entidades, por lo que es un poco enredado.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Entrega Final: 46 pts (75%)
##### ✅ Ventana Inicio

No es bonita, pero cumple lo que necesita el enunciado.

##### ✅ Ventana Juego

Tienen una caracteristica no pedida en el enunciado, pero que añadi para hacer mas disfrutable la experiencia, puedes arrastrar las bombas para colocarlas

##### ✅ ConejoChico

Se mueve animada y fluidamente, igual que los lobos y zanahorias.

Aumenta su velocidad con cada nivel, ¿Porque?, porque en la rubrica sale que debe pasar eso.

##### ✅ Lobos

Aumentan de velocidad con cada nivel.

##### ✅ Cañón de Zanahorias

Tienen un cooldown para no ser molestos, sin embargo, en ninguna parte se especifica que se velocidad suba por nivel, por tanto su velocidad no sube.

Por otra parte, el cooldown, es decir, el tiempo de respawn de zanahoria, es mayor mientras mas rapidas sean las zanahorias.

##### ✅ Bomba Manzana

Tienen añadidas la capacidad de destruir cañones, ¿Porque?, porque si no, el nivel 3 es imposible sin empezar desde uno anterior, y si no es imposible, entonces es extremadamente dificil, y yo note que convenientemente si se reventaba un cañon, entonces el nivel era facilmente posible.

##### ✅ Bomba Congeladora

Tienen un nuevo parametro en parametros.py para cambiar su nivel de ralentizacion, por defecto deberia ser 0.75, pues quita 25%, pero yo lo cambiaria a 0.25, pues segun el enunciado son muy debiles.

##### ✅ Fin del nivel

Hay un mensaje que te indica el puntaje acumulado hasta el momento

##### ✅ Fin del Juego

Sale un mensaje indicando el fin del juego con el sonido correspondiente

##### ✅ Recoger (G)

Recoge correctamente las bombas.

Pero el inventario no funciona en torno a Clases, si no que respecto a strings, Uno no debe complicar lo que deberia ser simple, por otra parte, los items y bombas si son clases.

##### ✅ Cheatcodes (Pausa, K+I+L, I+N+F)

En consola se muestra la combinacion actual de botones en formato ["-", "-", "-"]

Ambos codigos fueron implementados, proceder con precausion pues ["K", "I", "L"] añadira los lobos destruidos al contador de lobos eliminados, y estos mismos lobos reaparecen una vez Conejo muere.

Ademas, se añade un nuevo cheatcode, ["B", "M", "B"], que añade 100 bombas de ambos tipos.

Una vez se avanza al siguiente nivel los codigos no se mantienen activos, incluso BMB, pues Conejo deja de usar el inventario de nivel y crea una copia de la lista, cuidado, Una vez activas BMB las bombas que recoges en el nivel no se guardan.

##### ✅ Networking

Tras tener varios errores, el servidor presenta un funcionamiento correcto, con 5 mensajes distintos del lado del servidor, para una conexion, desconeccion, pedido de tablero, Avanzar o Ganar, o un usuario baneado que trato de entrar.

Tienen un estilo de caja los mensajes en consola, al menos por parte del servidor.

En la distribucion de puntajes, se habla de locks, estos no me acuerdo que hayan aparecido en las guias de contenido, y por tanto no supe que tenia que hacer para que eso sea correcto.

El sistema de Networking que hice me gusto mucho, porque uno tiene que mandar mensajes del tipo "CODIGO:argumento", y en base al codigo, el otro lado sabra que es lo que tiene que hacer, por ejemplo:

- cliente puede hacer "LEADERBOARD:" para pedir los puntajes, "CONECTAR:usuario" para iniciar sesion, "GANAR:usuario;nivel;puntos" para guardar su puntaje en el servidor.

- servidor puede devolver tambien codigos de errores, aunque no son muy usados, los normales son: "PUNTAJES:user1;nivel;puntaje_total,user2..." para mandar la lista de puntajes historicos, "NIVEL:nivel" para indicar cual nivel tiene que empezar cierto usuario, "AVANZAR:puntos;nivel" para que el cliente avanze de nivel y "WIN:puntos" para indicar que el usuario gano DCConejoChico.

Si resulta alguna excepcion en el server, el Cliente puede quedarse pegado, en teoria, parece que si pasa esto, entonces el server debe botar al cliente, para que no se mantenga pegado, esto se hace con except Exception, el codigo esta comentado, porque como ha sido mencionado, es mala practica, y cuando tenia errores no sabia porque eran, En caso de ver como funciona esto solo descomenten el codigo, de hecho, junto con un raise exception para ver el comportamiento, el Cliente recibe el mensaje "No se pudo decodificar :c"

##### ✅ Decodificación

Implementado en mensaje.py

##### ✅ Desencriptación

Implementado en mensaje.py

##### ✅ Archivos

Con esto creo que se refiere a parametros y assets, segun la pauta, y si, se implemento todo, todos los parametros tienen funcionalidad, y cambian el sentido de juego, aunque no los he probado completamente, pero por ejemplo cambiar ancho y largo cambia el tamaño del laberinto, pero el layout de la ventana de inicio no esta diseñado para esta funcion.

Por otra parte todos los assets son usados, excepto los sonidos WAV, si tu sistema no puede usar sonido wav podrias ir a main_utilities y cambiar entre wav y mp3, yo elegi mp3 porque es un formato mas reconocible, pero solo fue gusto personal.

El resto de archivos se describe en la seccion de modulos
##### ✅ Funciones

La mayoria de funciones de la entrega intermedia han sido usadas, excepto algunas en cliente, como riesgo_mortal, y encontrar conejo, que fue una que habia creado yo, sin embargo, raycaster es una de las funciones mas importantes y esa fue mi implementacion original de riesgo mortal.

- Contenidos.

1. backend_utilities.py

- - usar_item

- - validar_direccion

- - riesgo_mortal, Indirectamente mediante raycaster, pues yo no la encontre util.

- - validacion_formato

- - calcular_puntaje

- - Otras cosas, como 3 medidas de distancia distintas, un convertidor de string a diccionario que es usado por el Backend, y funciones para las bombas.

2. mensaje.py

- - Todas las funciones de servidor de entrega intermedia excepto usuario_permitido.

- - Funciones inversas de esas funciones.

- - Versiones compactas de estas mismas funciones.

3. server_utils.py

- - usuario_permitido

Hay muchas otras funciones, para abrir archivos, etc, estas suelen encontrarse en los archivos utilities.

## Ejecución :computer:
Para abrir la tarea:

1. mover estos archivos:

- - Assets -> Carpeta Cliente en entrega_final

- - Parametros.py No es necesario moverlo, ya se incluye en la entrega, ademas, con un parametro nuevo.

2. Tienen que estar presentes:

- - host.json, tanto cliente como servidor

- - baneados.json, solo servidor

- - puntaje.txt, servidor

Estos archivos estan presentes desde antes, para que se entienda su formato.

3. Abrir servidor\\main.py con un puerto de argumento.

4. Abrir cliente\\main.py con un puerto de argumento.


## Librerías :books:
### Librerías externas utilizadas
Solo fueron usadas librerias que se se permiten, todas o builtin, o PyQt6, :

1. ```math```: ```copysign```
2. ```socket```: ```varias```
3. ```json```: ```json.load```
4. ```sys```: ```sys.exit, sys.argv, sys.excepthook```
5. ```os```: ```join, listdir```
6. ```abc```: ```ABC, abcmeta```
7. ```PyQt6```: ```varias, demasiadas, incluso.```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### En cliente y servidor:

1. ```mensaje.py```: Contiene los metodos de envio y recibo de mensajes, desencriptar, encriptar, etc...
2. ```host.json```: Contiene el host al cual se conectan o el cual usan cliente y servidor, el juego puede romperse si no se incluye.

#### En cliente\\backend:

1. ```clases_abstractas.py```: en cliente\\backend, Contiene a las clases abstractas para clases_laberinto.py y conejo.py
2. ```clases_laberinto.py```: Las distintas clases que habitan el Laberinto de juego, los lobos, zanahorias, cañones (Escrito dentro de codigo como cannones respetando la idea de que la ñ es una doble n, ademas de que asi es en ingles), bombas...
3. ```conejo.py```: Contiene exclusivamente la clase Conejo, y su logica.
4. ```laberinto.py```: El VERDADERO backend, a pesar de que es desechado cada vez que se termine un nivel, maneja toda la logica correspondiente a los niveles, junto con los 3 archivos anteriores, es la parte mas compleja
5. ```backend.py```: El falso backend, ni siquiera queria crearlo, pero algo tenia que manejar las comunicaciones entre cliente/servidor
6. ```backend_utilities.py```: Distintas funciones para los archivos del Backend.

Mensaje.py tambien esta aca.

#### En cliente\\frontend:

1. ```frontend_classes.py```: Contiene una DraggableLabel, para implementar Labels que se mueven con el mouse y emiten una señal al ser botadas.
2. ```frontend.py```: Contiene las ventanas visuales, Juego es un stacked widget que cambia el widget activo.

#### En cliente:

1. ```main_utilities.py```: Añade un diccionario llamado ASSETS que contiene todos los paths, ademas de una funcion para abrir los laberintos.

2. ```main.py```: Abre DCConejoChico.

#### En server:

1. ```server_utilities.py```: Distintas funciones para la funcionalidad del server que no tienen que ver con el encriptado y desencriptado de mensajes.

2. ```main.py```: Abre el servidor.

3. ```baneados.json```: Es una lista que contiene usuarios que no tienen permitido acceso al servidor, servidor puede romperse si no existe el archivo.

4. ```puntaje.txt```: Guarda el usuario, su nivel, y su puntaje acumulado a travez de todas las partidas que ha jugado de DCConejoChico.


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se usa un QTimer global para la clase Laberinto la cual actualiza todas las subclases, en ese sentido, si QTimer no cuenta como Threading, entonces la Tarea no tiene ningun thread, trate de implementarlos, sin embargo, causaron mas problemas de los que arreglaban, y segun me acuerdo incluso causaban lentitud en el programa, debido a eso no los use, este metodo obviamente tiene sus problemas, pero los pude solucionar con ingenio, por ejemplo, si necesitaba saltarme 1 segundo del ciclo en una entidad, es decir, 60 ticks de juego, solo tenia que hacer un ciclo que subiera por uno hasta llegar a 60.
2. La MegaClase DCConejoChico parece hacer demasiadas cosas, a mi no me parece que haya hecho algo malo, si lo piensan, Entre el Backend, Frontend, y Laberinto, no saben que les pasa el uno al otro, solo es una super-clase mediadora entre estas 3, con la unica funcion extra de cargar el tablero del laberinto, que TAL VEZ podria considerarse funcion del Backend, pero para mi es simple manejo de archivo
3. El laberinto y sus entidades un poco acoplados, diria yo, pues uno tiene que entender lo que hace laberinto para entender lo que hacen las entidades, y viceversa, aun asi esta no es la clase de acoplamiento que quieren evaluar, si no que el acoplamiento frontend-backend, el cual es nulo.

PD: **El frontend y laberinto no saben lo que le pasa al otro, no estan acoplados, pues DCConejoChico solo se encarga de mediar las distintas conexiones entre clases.**

PD2: **Esta tarea se desarollo en Windows 11 con PyQt6, si hay algun error inesperado, que hasta donde yo se ya arregle todos los bugs, entonces podria tener que ver con la version de sistema, me acuedo que PyQt6 tenia problemas con hacerlo en Ubuntu, asi que por eso creo que esto es valido.**

PD3: **LOS PUNTAJES EN EL SERVIDOR ESTAN EN DECIMAL CON 2 NUMEROS, esto debido a que en una de las funciones de la entrega intermedia, y en el enunciado, deben quedar 2 decimales, aunque en varias partes parece que los puntajes deberian ser enteros, pero yo decidi que lo mejor seria hacer que los puntajes fueran decimal de todas formas.**

PD4: **Habia entregado esta tarea con un cupon y estaba perfecta, pero por culpa de usar Github Desktop se me borro la ultima linea de puntaje.txt, y esto causaba que el servidor se cayera, ahora es a prueba de tontos, y es una de las referencias en el inicio, respecto a como hubo un problema de infraestructura, ahora Estoy usando Vscode, pues este no borra saltos de linea, Talvez en algun futuro me parezca buena idea usar git, pero no me gusta mucho tener que hacer tantas cosas por consola**

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. \<https://www.pythonguis.com/tutorials/pyqt6-dialogs/>: Fue usado para implementar las cajas de dialogo al avanzar, ganar, perder, usar un usuario baneado, etc.
2. \<https://stackoverflow.com/questions/55842776/how-to-change-ui-in-same-window-using-pyqt5>: Me dio la idea de usar QStackedWidget en el frontend.
3. \<https://stackoverflow.com/questions/46837947/how-to-create-an-abstract-base-class-in-python-which-derived-from-qobject>: Fue la razon de porque creé la metaclase QAbstract
4. \<https://www.w3resource.com/python-exercises/pyqt/python-pyqt-event-handling-exercise-6.php>, \<https://stackoverflow.com/questions/64516089/draggable-qlabels-in-pyqt5>, \<https://stackoverflow.com/questions/66988388/resize-widget-from-center-when-animating-the-size-property> Para poder implementar las DraggableLabel en frontend_classes.py, tambien use mucho el comando help() en distintos objetos de pyqt para poder lograr que el primer codigo se arregle, porque estaba hecho para PyQt5 y me tarde 3 horas en actualizarlo y arreglarlo, y entonces aplicar mis necesidades para la tarea, como hacer que cambie de tamaño y que emita una señal al botarlo.
5. \<https://stackoverflow.com/questions/35179317/python-user-defined-exceptions-to-handle-specific-oserror-codes>: Para hacer except de ciertos OSError en el networking cliente servidor.
6. \<https://stackoverflow.com/questions/20309255/how-to-pad-a-string-to-a-fixed-length-with-spaces> Para hacer el pretty print del servidor.
7. \<https://stackoverflow.com/questions/37201338/how-to-place-custom-image-onto-qmessagebox> Icono personalizado en los dialogos de texto.
8. Las distintas ayudantias, experiencias, contenidos pasados, etc... Mi tarea en ciertos lugares es un frankenstein de estos contenidos, especialmente la experiencia 4 de servidores.
9. Podria poner mas cosas, pero si siguiera tendria mas de 100 fuentes en total o algo asi, algunas otras cosas eran de sintasis regular de python, o cosas que ya me sabia de memoria, o simplemente creacion propia.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).