def validacion_formato(nombre:str) -> bool:
    tiene_numero = any(map(lambda char: char.isdigit(), nombre))
    tiene_mayus = any(map(lambda char: char.isupper(), nombre))
    es_alnum = nombre.isalnum()
    es_acotado = (len(nombre) >= 3) and (len(nombre) <= 16)
    condiciones = (tiene_numero, tiene_mayus, es_alnum, es_acotado)
    return all(condiciones)


def raycaster(laberinto: list[list], conejo: list, key: str) -> bool:
    """
    Manda un rayo en una direccion 'key' desde la posicion 'conejo' en un laberinto.
    
    Se detiene cuando encuentra un peligro o una pared.

    Su proposito es modularizar riesgo_mortal
    """
    # Parte 1: Definir Variables
    row, col = conejo  # Si no se hace esto se vuelve funcion impura.
    n_rows, n_cols = len(laberinto), len(laberinto[0])
    eje = ("V" if key in "UD" else "H")
    anti_key = {"U":"D", "D":"U", "L":"R", "R":"L"}[key]  # La direccion opuesta al rayo 'key'.
    vertical, horizontal = {
        "U":[-1, 0],
        "D":[1, 0],
        "L":[0, -1],
        "R":[0, 1]
    }[key] # Direccion a partir de 'key'
    enemigos = {"L" + eje, "C" + anti_key}
    obstaculos = {"LV", "LH", "CU", "CD", "CL", "CR", "P"} - enemigos
    # Parte 2: while loop
    while (0 <= row < n_rows) and (0 <= col < n_cols):
        objeto = laberinto[row][col]
        if objeto in enemigos:
            return True # Murio
        if objeto in obstaculos:
            return False # Choco con algo
        row += vertical
        col += horizontal
    return False # Llego al borde del mapa

def encontrar_conejo(laberinto: list[list]) -> list:
    """Funcion para riesgo_mortal y validar_direccion, devuelve la posicion de conejo."""
    for row_index, row in enumerate(laberinto):
        if "C" in row:
            col_index = row.index("C")
            return [row_index, col_index]

def riesgo_mortal(laberinto: list[list]) -> bool:
    """
    Encuentra a conejo y luego usa raycaster para detectar peligros.
    """
    conejo = encontrar_conejo(laberinto)
    rayos = (
        raycaster(laberinto, conejo, "U"),  # Up Arriba
        raycaster(laberinto, conejo, "D"),  # Down Abajo
        raycaster(laberinto, conejo, "L"),  # Left Izquierda
        raycaster(laberinto, conejo, "R")   # Right Derecha
    )
    return any(rayos) # Si cualquiera de los rayos encontro un peligro, devuelve True


def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    if item in inventario:
        inventario.remove(item)
        return (True, inventario)
    return (False, inventario)


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:
    if cantidad_lobos > 0:
        puntaje_raw = (tiempo * vidas) / (cantidad_lobos * PUNTAJE_LOBO)
        return round(puntaje_raw, 2)
    return 0.0


def validar_direccion(laberinto: list[list], tecla: str) -> bool:
    conejo = encontrar_conejo(laberinto)
    direccion = {"W":[-1, 0],
                 "S":[1, 0],
                 "A":[0, -1],
                 "D":[0, 1],}[tecla]
    obstaculos = {"CU", "CD", "CL", "CR", "P"}
    row, col = map(sum, zip(conejo, direccion))
    n_rows, n_cols = len(laberinto), len(laberinto[0])
    bounded = (0 <= row < n_rows) and (0 <= col < n_cols)
    abierto = laberinto[row][col] not in obstaculos
    return bounded and abierto
