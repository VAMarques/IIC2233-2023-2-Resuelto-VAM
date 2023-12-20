import sys
import os
from funciones_menu import abrir_tablero, imprimir_menu
from imprimir_tablero import imprimir_tablero
from tablero import Tablero


LONG_BAR = "═══════════════════════════════════════════════════════════════════════════════"
# Resulta que tambien es convencion asignar constantes en UPPER_CASE, como LONG_BAR no va a
# cambiar a travez del codigo, me parece que tiene sentido asignarlo de esta manera
# Hace que resalte mas.

# TODO: Completar

if __name__ != "__main__":
    print(LONG_BAR)
    print("Parece que estas abriendo DCChexxploding incorrectamente")
    print("Tienes que abrir main.py directamente desde la consola")
    print("No mediante otro archivo python")
    print(LONG_BAR)
    exit(0)  # Esto es meramente una curiosidad
            # si no abres abrir_incorrecto.py, no deberia aparecer.
# exit(0) significa que el programa termino sin errores, el significado de "sin errores" esta a la
# interpretacion.


if __name__ == "__main__":
    # Intente hacer "python3 main.py hola mundo"
    argumentos_por_consola = sys.argv
    if ("tableros.txt" not in os.listdir(".")):
        print(LONG_BAR)
        print("Debes abrir este archivo desde la carpeta T1, y no desde otro directorio")
        print("Si lo abriste desde T1, asegurate de que exista tableros.txt")
        print(LONG_BAR)
        exit(0)
    
    if (len(argumentos_por_consola) != 3):
        print(LONG_BAR)
        print("Al abrir este archivo, tienes que darle dos argumentos extra.")
        print("1. - Un nombre con solo caracteres alfabeticos, por ejemplo, VAMarques")
        print("2. - El nombre de un tablero incluido dentro de tableros.txt, por ejemplo")
        print("Si por alguna razon diste mas de 2 argumentos, estos no seran tomados en cuenta")
        print(LONG_BAR)
        exit(0)
    
    nombre = argumentos_por_consola[1]
    nombre_tablero = argumentos_por_consola[2]
    tablero_abierto = abrir_tablero(nombre_tablero)
    if (not nombre.isalpha()) or (len(nombre) < 4) or (not tablero_abierto):
        print(LONG_BAR)
        if not nombre.isalpha() or (len(nombre) < 4):
            print("-Tu nombre no es alfabetico o tiene menos de 4 caracteres,",
                  "y por tanto es invalido.")
            print(" Elimina los numeros y otros simbolos, o hazlo mas largo, e intentalo de nuevo")
        if (not nombre.isalpha() or (len(nombre) < 4)) and (not tablero_abierto):
            print() # Añade un salto de linea en caso de que ambos esten incorrectos
        if not tablero_abierto:
            print("-Tu tablero no se encuentra dentro del archivo tableros.txt")
            print(" Busca dentro del archivo ver los tableros incluidos.") 
        print(LONG_BAR)
        exit(0)
    # Si se llego a esta parte del codigo entonces el programa se inicializo correctamente.
    tablero_juego = Tablero(tablero_abierto)
    print(LONG_BAR)
    print(f"¡Buenos dias {nombre}! Accediendo a DCChexxploding...")
    print(LONG_BAR)

    play = True
    while play:
        print(f"Tablero Actual: {nombre_tablero}")
        print(f"Nombre de Usuario: {nombre}")
        imprimir_menu()
        opcion = input("Seleccione una opcion...  -> ")
        if (opcion == "1"):
            print(LONG_BAR)
            imprimir_tablero(tablero_juego.tablero)
            input("Presione ENTER para volver al menu...")
            print(LONG_BAR)
        elif (opcion == "2"):
            print(LONG_BAR)
            print("¿Quieres eliminar los peones del tablero? No podras deshacer esta opcion.")
            print(LONG_BAR)
            print("Si la respuesta es si, ingrese Y.")
            print("Si quiere volver al menu, ingrese cualquier otro caracter")
            opcion = input("Seleccione una opcion...  -> ").lower()
            if (opcion == "y"):
                print(LONG_BAR)
                tablero_juego.limpiar()
                print("Se eliminaron los peones del tablero")
                imprimir_tablero(tablero_juego.tablero)
                input("Presione ENTER para volver al menu...")
            print(LONG_BAR)
        elif (opcion == "3"):
            print(LONG_BAR)
            print("ADVERTENCIA: Si cargaste un tablero muy grande, esta herramienta puede tomarse")
            print("varios minutos en funcionar, si se tarda mucho en cargar, use CTRL+C para")
            print("volver al menu, ¿estas seguro de que quieres intentar solucionar el tablero?")
            print(LONG_BAR)
            print("Si la respuesta es si, ingrese Y.")
            print("Si quiere volver al menu, ingrese cualquier otro caracter")
            opcion = input("Seleccione una opcion...  -> ").lower()
            if (opcion == "y"):
                try:
                    print(LONG_BAR)
                    tablero_solucionado = tablero_juego.solucionar()
                    if (not tablero_solucionado):
                        print("No tiene solucion :(")
                        input("Presione ENTER para volver al menu...")
                    else:
                        imprimir_tablero(tablero_solucionado)
                        print("¿Volver este el tablero de juego?")
                        print("Si la respuesta es si, ingrese Y.")
                        print("En otro caso ingrese cualquier otro caracter")
                        opcion = input("Seleccione una opcion...  -> ").lower()
                        if (opcion == "y"):
                            tablero_juego = Tablero(tablero_solucionado)
                except KeyboardInterrupt:
                    print()
                    input("Presione ENTER para volver al menu...")
            print(LONG_BAR)
        elif (opcion == "4"):
            print(LONG_BAR)
            print("¡Gracias por jugar Chexxploding!")
            print("Nos vemos la proxima vez.")
            print(LONG_BAR)
            play = False
        else:
            print(LONG_BAR)
            print("Debes seleccionar una opcion valida")
            print("Puedes escoger entre 1, 2, 3, y 4")
            input("Presione ENTER para volver al menu...")
            print(LONG_BAR)