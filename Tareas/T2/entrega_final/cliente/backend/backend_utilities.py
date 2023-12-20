def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    if item in inventario:
        inventario.remove(item)
        return (True, inventario)
    return (False, inventario)

def validar_direccion(laberinto: list[list], posicion: list, key: str) -> bool:
    direccion = {"U":[-1, 0],
                 "D":[1, 0],
                 "L":[0, -1],
                 "R":[0, 1],}[key]
    obstaculos = {"CN", "P"}
    row, col = map(sum, zip(posicion, direccion))
    n_rows, n_cols = len(laberinto), len(laberinto[0])
    if (0 <= row < n_rows) and (0 <= col < n_cols):
        return laberinto[row][col] not in obstaculos
    return False

def raycaster(laberinto: list[list], posicion: list, key: str) -> bool:
    """
    Manda un rayo en una direccion 'key' desde "posicion" en un laberinto.
    
    Se detiene cuando encuentra una pared.
    """
    # Parte 1: Definir Variables
    row, col = posicion
    n_rows, n_cols = len(laberinto), len(laberinto[0])
    vertical, horizontal = {
        "U":[-1, 0],
        "D":[1, 0],
        "L":[0, -1],
        "R":[0, 1]
    }[key] # Direccion a partir de 'key'
    obstaculos = {"CN", "P"}
    # Parte 2: while loop
    while (0 <= row < n_rows) and (0 <= col < n_cols):
        objeto = laberinto[row][col]
        if objeto in obstaculos: # Choco con algo, Retroceder
            row -= vertical
            col -= horizontal
            return [row, col]
        row += vertical # Despejado, avanzar
        col += horizontal
    row -= vertical # Llego al borde del mapa, Retroceder
    col -= horizontal
    return [row, col]

def dictify_puntajes(puntajes: str):
    diccionario = {}
    for dupla in puntajes.split(","):
        jugador, puntos = dupla.split(";")
        diccionario[jugador] = float(puntos)
    return diccionario

def validacion_formato(nombre:str) -> bool:
    tiene_numero = any(map(lambda char: char.isdigit(), nombre))
    tiene_mayus = any(map(lambda char: char.isupper(), nombre))
    es_alnum = nombre.isalnum()
    es_acotado = (len(nombre) >= 3) and (len(nombre) <= 16)
    condiciones = (tiene_numero, tiene_mayus, es_alnum, es_acotado)
    return all(condiciones)

# 3 Metodos de distancia distintos.
# euclid es colision circular
# manhattan es colision rombica
# chebyshev es colision cuadrada.
def euclid(posicion_1: list, posicion_2: list, maximo: float):
    """Distancia de Euclid, colision circular"""
    y_1, x_1 = posicion_1
    y_2, x_2 = posicion_2
    return (y_1 - y_2)**2 + (x_1 - x_2)**2 <= maximo**2
def manhattan(posicion_1: list, posicion_2: list, maximo: float):
    """Distancia de Manhattan, colision rombica"""
    y_1, x_1 = posicion_1
    y_2, x_2 = posicion_2
    return abs(y_1 - y_2) + abs(x_1 - x_2) <= maximo
def chebyshev(posicion_1: list, posicion_2: list, maximo: float):
    """Distancia de Chebyshev, colision cuadrada"""
    y_1, x_1 = posicion_1
    y_2, x_2 = posicion_2
    return (- maximo <= (y_1 - y_2) <= maximo) and (- maximo <= (x_1 - x_2) <= maximo)

# Bombcaster, raycaster para bombas que devuelve las posiciones que alcanza.
# Asume que inicia en una zona despejada que no es una pared.
def bombcaster(laberinto, posicion, key):
    row, col = posicion
    n_rows, n_cols = len(laberinto), len(laberinto[0])
    vertical, horizontal = {
        "U":[-1, 0],
        "D":[1, 0],
        "L":[0, -1],
        "R":[0, 1]
    }[key] # Direccion a partir de 'key'
    # Parte 2: while loop
    # Avanzar por uno para no contar la de inicio
    row += vertical
    col += horizontal
    superficie = []
    while (0 <= row < n_rows) and (0 <= col < n_cols):
        objeto = laberinto[row][col]
        if objeto == "P": # Choco con una pared, Retroceder
            return superficie
        superficie.append([row, col])
        row += vertical # Despejado, avanzar
        col += horizontal
    return superficie

def poner_bomba(tablero: list[list], posicion: list):
    superficie = [posicion]
    superficie += bombcaster(tablero, posicion, "U")
    superficie += bombcaster(tablero, posicion, "D")
    superficie += bombcaster(tablero, posicion, "L")
    superficie += bombcaster(tablero, posicion, "R")
    return superficie

def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:
    if cantidad_lobos > 0:
        puntaje_raw = (tiempo * vidas) / (cantidad_lobos * PUNTAJE_LOBO)
        return round(puntaje_raw, 2)
    return 0.0