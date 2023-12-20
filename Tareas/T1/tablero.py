from pieza_explosiva import PiezaExplosiva
import copy

class Tablero:
    def __init__(self, tablero: list) -> None:
        # filas         #columnas
        self.dimensiones = [len(tablero), len(tablero[0])]
        self.tablero = tablero

    @property
    def desglose(self) -> list:
        explosivas = 0
        peones = 0
        vacios = 0
        n_filas, n_columnas = self.dimensiones
        for fil in range(n_filas):
            for col in range(n_columnas):
                tipo = self.tablero[fil][col]
                if (tipo[0] in ["V", "H", "R"]):
                    explosivas += 1
                elif (tipo == "PP"):
                    peones += 1
                elif (tipo == "--"):
                    vacios += 1
        return [explosivas, peones, vacios]

    def peones_vecinos(self, fila, columna) -> int:
        n_filas, n_columnas = self.dimensiones
        vecinos = 0
        if (fila + 1 < n_filas):  # abajo
            if (self.tablero[fila + 1][columna] == "PP"):
                vecinos += 1
        if (fila - 1 >= 0):  # arriba
            if (self.tablero[fila - 1][columna] == "PP"):
                vecinos += 1
        if (columna + 1 < n_columnas):  # derecha
            if (self.tablero[fila][columna + 1] == "PP"):
                vecinos += 1
        if (columna - 1 >= 0):  # izquierda
            if (self.tablero[fila][columna - 1] == "PP"):
                vecinos += 1
        return vecinos

    @property
    def peones_invalidos(self) -> int:
        n_filas, n_columnas = self.dimensiones
        invalidos = 0
        for fil in range(n_filas):
            for col in range(n_columnas):
                if (self.tablero[fil][col] == "PP"):
                    if (self.peones_vecinos(fil, col) > 1):
                        invalidos += 1
        return invalidos

    @property
    def piezas_explosivas_invalidas(self) -> int:
        n_filas, n_columnas = self.dimensiones
        invalidos = 0
        # Too many nested blocks, pero necesito estas 4 for loops.
        for pos_fil in range(n_filas):
            for pos_col in range(n_columnas):
                pieza = self.tablero[pos_fil][pos_col]
                tipo = pieza[0]
                if tipo in ["V", "H", "R"]:
                    rango = int(pieza[1:])
                if ((tipo == "V") and (rango > n_filas)):
                    invalidos += 1
                if ((tipo == "H") and (rango > n_columnas)):
                    invalidos += 1
                if (tipo == "R"):
                    alcance = n_filas + n_columnas - 1
                    for target_fil in range(n_filas):
                        for target_col in range(n_columnas):
                            not_centro = (pos_fil != target_fil) and (pos_col != target_col)
                            diagonal = abs(pos_fil - target_fil) == abs(pos_col - target_col)
                            if (not_centro and diagonal):
                                alcance += 1
                    if (rango > alcance):
                        invalidos += 1
        return invalidos

    @property
    def tablero_transformado(self) -> list:
        n_filas, n_columnas = self.dimensiones
        tablero_nuevo = self.tablero
        # fil es abreviatura de filas y col es abreviatura de columnas
        for fil in range(n_filas):
            for col in range(n_columnas):
                if (self.tablero[fil][col][0] in ["V", "H", "R"]):
                    alcance = int(self.tablero[fil][col][1:])  # desde 1 estan los numeros de pieza
                    tipo = self.tablero[fil][col][0]
                    posicion = [fil, col]
                    tablero_nuevo[fil][col] = PiezaExplosiva(alcance, tipo, posicion)
        return tablero_nuevo

    def explosiva_raycaster(self, posicion: list, direccion: list) -> int:
        # Funcion manda un rayo que devuelve la cantidad de celdas afectadas antes de chocar
        # con un peon.
        fila, columna = posicion
        vertical, horizontal = direccion
        n_filas, n_columnas = self.dimensiones
        afectadas = 0  # en el inicio no hay celdas afectadas por el rayo.
        pasos = 1  # se empieza en uno para no contar el origen del rayo
        abierto = True
        fila_bounded = ((fila + (pasos * vertical) >= 0) and
                        (fila + (pasos * vertical) < n_filas))
        columna_bounded = ((columna + (pasos * horizontal) >= 0) and
                           (columna + (pasos * horizontal) < n_columnas))
        while abierto and fila_bounded and columna_bounded:
            if (self.tablero[fila + (pasos * vertical)][columna + (pasos * horizontal)] != "PP"):
                afectadas += 1
                pasos += 1
                fila_bounded = ((fila + (pasos * vertical) >= 0) and
                                (fila + (pasos * vertical) < n_filas))
                columna_bounded = ((columna + (pasos * horizontal) >= 0) and
                                   (columna + (pasos * horizontal) < n_columnas))
            else:
                abierto = False
        return afectadas

    def celdas_afectadas(self, fila: int, columna: int) -> int:
        afectadas = 1
        pieza = self.tablero[fila][columna]
        if (pieza[0] == "V"):
            afectadas += self.explosiva_raycaster([fila, columna], [1, 0])
            afectadas += self.explosiva_raycaster([fila, columna], [-1, 0])
            return afectadas
        elif (pieza[0] == "H"):
            afectadas += self.explosiva_raycaster([fila, columna], [0, 1])
            afectadas += self.explosiva_raycaster([fila, columna], [0, -1])
            return afectadas
        elif (pieza[0] == "R"):
            afectadas += self.explosiva_raycaster([fila, columna], [1, 0])
            afectadas += self.explosiva_raycaster([fila, columna], [-1, 0])
            afectadas += self.explosiva_raycaster([fila, columna], [0, 1])
            afectadas += self.explosiva_raycaster([fila, columna], [0, -1])
            afectadas += self.explosiva_raycaster([fila, columna], [1, 1])
            afectadas += self.explosiva_raycaster([fila, columna], [1, -1])
            afectadas += self.explosiva_raycaster([fila, columna], [-1, 1])
            afectadas += self.explosiva_raycaster([fila, columna], [-1, -1])
            return afectadas
        else:
            return -1

    def limpiar(self) -> None:
        filas, columnas = self.dimensiones
        for i in range(filas):
            for j in range(columnas):
                if (self.tablero[i][j] == "PP"):
                    self.tablero[i][j] = "--"

    def reemplazar(self, nombre_nuevo_tablero: str) -> bool:
        # El encoding es debido a caracteres como la ñ, é. etc, me lo recomendo un ayudante.
        with open("tableros.txt", "r", encoding = "utf-8") as archivo:
            data = archivo.readlines()
        tablero_encontrado = False
        for linea in data:
            linea = linea.strip("\n").split(",")
            if (linea[0] == nombre_nuevo_tablero):
                tablero_encontrado = True
                n_filas = int(linea[1])
                n_columnas = int(linea[2])
                tablero_buscado = linea[3:]
        if (tablero_encontrado is False):
            return False
        nuevo_tablero = []
        for fila in range(n_filas):
            nuevo_tablero.append(
                tablero_buscado[(fila * n_columnas):((fila + 1) * n_columnas)]
            )
        self.dimensiones = [n_filas, n_columnas]
        self.tablero = nuevo_tablero
        return True

    #Todos las siguientes properties y todos los siguentes metodos son parte de solucionar.
    @property
    def es_solucion(self) -> bool:
        # Verifica las reglas del tablero.
        n_filas, n_columnas = self.dimensiones
        if (self.peones_invalidos > 0) or (self.piezas_explosivas_invalidas > 0):
            return False
        for fil in range(n_filas):
            for col in range(n_columnas):
                pieza = self.tablero[fil][col]
                if (pieza[0] in ["V", "H", "R"]):
                    alcance = int(pieza[1:])
                    if (self.celdas_afectadas(fil, col) != alcance):
                        return False
        return True

    @property
    def inviable(self) -> bool:
        # Caso mas extremo de no ser solucion, no hay peones que puedan solucionar el tablero
        n_filas, n_columnas = self.dimensiones
        for fil in range(n_filas):
            for col in range(n_columnas):
                pieza = self.tablero[fil][col]
                if (pieza[0] in ["V", "H", "R"]):
                    alcance = int(pieza[1:])
                    if (self.celdas_afectadas(fil, col) < alcance):
                        return True
        return False

    def peon_redundante(self, target_fil, target_col) -> bool:
        # Retorna True si un peon no esta en el rango de ninguna pieza explosiva
        # False en caso contrario
        # Ayuda a que en el tablero no se posicionen peones donde no es necesario
        n_filas, n_columnas = self.dimensiones
        for pos_fil in range(n_filas):
            for pos_col in range(n_columnas):
                pieza = self.tablero[pos_fil][pos_col]
                tipo = pieza[0]
                if (tipo == "V") and (pos_col == target_col):
                    return False
                if (tipo == "H") and (pos_fil == target_fil):
                    return False
                if (
                    tipo == "R" and (
                        (pos_col == target_col) or
                        (pos_fil == target_fil) or
                        (abs(pos_fil - target_fil) == abs(pos_col - target_col))
                    )
                ):
                    return False
        return True

    @property
    def es_valido(self) -> bool:
        # revisa si el tablero se puede solucionar
        if ((self.peones_invalidos > 0) or
            (self.piezas_explosivas_invalidas > 0) or
            (self.inviable)):
            return False
        return True

    def sanitizar(self, tablero):  # limpia un tablero, cambiando "~~" a "--"
        n_filas = len(tablero)
        n_columnas = len(tablero[0])
        for fil in range(n_filas):
            for col in range(n_columnas):
                if tablero[fil][col] == "~~":
                    tablero[fil][col] = "--"
        return tablero
    
    def peon_en_alcance(self, explosiva, peon):
        #explosiva = list["tipo", fila, col]
        tipo, i, j = explosiva
        fila, col = peon

        vertical = col == j
        horizontal = fila == i

        if (tipo == "V"):
            return vertical
        if (tipo == "H"):
            return horizontal
        if (tipo == "R"):
            if (vertical or horizontal):
                return True
            diagonal = abs(fila - i) == abs(col - j)
            return diagonal

    def peon_raycaster(self, posicion, direccion):
        # Retorna True si hay una pieza explosiva viable que se beneficie de añadir un peon
        i, j = posicion
        v, h = direccion
        n, m = self.dimensiones
        k = 1
        k_fil = i + (k * v)
        k_col = j + (k * h)
        bounded = ((k_fil >= 0) and (k_fil < n) and (k_col >= 0) and (k_col < m))
        while bounded:
            pieza = self.tablero[k_fil][k_col]
            if (pieza == "PP"):
                return False
            elif (pieza[0] in ["V", "H", "R"]):
                tipo = pieza[0]
                alcance = int(pieza[1:])
                if (self.peon_en_alcance([tipo, k_fil, k_col], [i, j])):
                    if (self.celdas_afectadas(k_fil, k_col) > alcance):
                        return True
            k += 1
            k_fil = i + (k * v)
            k_col = j + (k * h)
            bounded = ((k_fil >= 0) and (k_fil < n) and (k_col >= 0) and (k_col < m))
        return False
    
    def peon_util(self, posicion):
        i, j = posicion
        if (self.peon_raycaster([i, j], [1, 0]) or
            self.peon_raycaster([i, j], [-1, 0]) or
            self.peon_raycaster([i, j], [0, 1]) or
            self.peon_raycaster([i, j], [0, -1]) or
            self.peon_raycaster([i, j], [1, 1]) or
            self.peon_raycaster([i, j], [1, -1]) or
            self.peon_raycaster([i, j], [-1, 1]) or
            self.peon_raycaster([i, j], [-1, -1])):
            return True
        else:
            return -1


    def solucionar(self) -> list:
        nuevo = copy.deepcopy(self)
        if not nuevo.es_valido:
            return []
        if nuevo.es_solucion:
            return self.sanitizar(nuevo.tablero)  # Limpia las casillas marcadas
        n_filas, n_columnas = self.dimensiones
        for fil in range(n_filas):
            for col in range(n_columnas):
                if nuevo.tablero[fil][col] == "--":
                    if (nuevo.peon_redundante(fil, col)):  # Es este peon redundante?
                        # Esto marca la casilla para no volver a pasar por ella
                        nuevo.tablero[fil][col] = "~~"
                    elif not (nuevo.peon_util([fil, col])):  # Es este peon util?
                        nuevo.tablero[fil][col] = "~~"
                    else:
                        nuevo.tablero[fil][col] = "PP"
                        if (not nuevo.es_valido):  # Sigue siendo valido el tablero?
                            nuevo.tablero[fil][col] = "~~"
                        elif (not nuevo.solucionar()):  # Alguno de los futuros tableros sera solucion?
                            nuevo.tablero[fil][col] = "~~"
                        return nuevo.solucionar()
        return []