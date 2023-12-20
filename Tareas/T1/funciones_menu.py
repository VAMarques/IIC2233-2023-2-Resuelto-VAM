def abrir_tablero(nombre: str) -> bool:
    with open("tableros.txt", "r", encoding = "utf-8") as archivo:
        data = archivo.readlines()
    tablero = []
    for linea in data:
        linea = linea.strip("\n").split(",")
        if (linea[0] == nombre):
            n_filas = int(linea[1])
            n_columnas = int(linea[2])
            tablero_buscado = linea[3:]
            for fila in range(n_filas):
                tablero.append(tablero_buscado[(fila * n_columnas):((fila + 1) * n_columnas)])
    return tablero

def imprimir_menu() -> None:
    print("╔════════════════════════¡Bienvenido a DCChexxploding!════════════════════════╗")
    print("║         Menu de Acciones                                                    ║")
    print("╠═════════════════════════════════════════════╦═══════════════════════════════╣")
    print("║      1) Mostrar Tablero                     ║ Implementacion por:           ║")
    print("║      2) Limpiar Tablero                     ║    Victor Alonso Marques      ║")
    print("║      3) Solucionar Tablero                  ║ Github: VAMarques             ║")
    print("║      4) Salir de DCChexxploding             ║ Correo: va.marques@uc.cl      ║")
    print("╚═════════════════════════════════════════════╩═══════════════════════════════╝")