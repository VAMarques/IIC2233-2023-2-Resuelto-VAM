class PiezaExplosiva:
    def __init__(self, alcance: int, tipo: str, posicion: list) -> None:
        self.alcance = alcance
        self.tipo = tipo
        self.posicion = posicion

    def __str__(self) -> str:
        fila, columna = self.posicion
        texto = f"Soy la pieza {self.tipo}{self.alcance}\n"
        texto += f"\tEstoy en la fila {fila} y columna {columna}\n"
        return texto

    # Listo
    def verificar_alcance(self, fila: int, columna: int) -> bool:
        pieza_fila, pieza_columna = self.posicion

        vertical = columna == pieza_columna
        horizontal = fila == pieza_fila

        if (self.tipo == "V"):
            return vertical
        if (self.tipo == "H"):
            return horizontal
        if (self.tipo == "R"):
            if (vertical or horizontal):
                return True
            diagonal = abs(fila - pieza_fila) == abs(columna - pieza_columna)
            return diagonal


if __name__ == "__main__":
    """
    Ejemplos:

    Dado el siguiente tablero
    [
        ["--", "V2", "PP", "--", "H2"],
        ["H3", "--", "--", "PP", "R11"]
    ]

    """
    # Ejemplo 1 - Pieza R11
    pieza_1 = PiezaExplosiva(11, "R", [1, 4])
    print(str(pieza_1))

    # Ejemplo 2 - Pieza V2
    pieza_2 = PiezaExplosiva(2, "V", [0, 1])
    print(str(pieza_2))
