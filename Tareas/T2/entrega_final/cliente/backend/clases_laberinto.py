from backend.clases_abstractas import Animado, Estatico, Bomba
from backend.backend_utilities import raycaster, chebyshev


class Item(Estatico):

    def __init__(self, argumento, fila, columna, laberinto):
        super().__init__(fila, columna, laberinto)
        self.destruido = False
        self.tipo = {"M": "manzana", "C": "congelacion"}[argumento]
        self.definir_sprites()

    def definir_sprites(self):
        self.sprite = self.tipo + "_" + "burbuja"

    def destruir(self):
        self.destruido = True
        self.laberinto.sennal_esconder.emit(self.id)

    def reset(self):
        self.destruido = False


class Lobo(Animado):
    velocidad = 5

    def __init__(self, argumento, fila, columna, laberinto):
        super().__init__(fila, columna, laberinto)
        self.eje = ("vertical" if argumento == "V" else "horizontal")
        self.ciclo = 0
        self.destruido = False
        self.congelado = False
        self.velocidad = (
            Lobo.velocidad / self.laberinto.p_1 / self.laberinto.p_2 / self.laberinto.p_3
        )
        self.definir_sprites()
        self.encontrar_camino()

    def definir_sprites(self):
        direccion_1, direccion_2 = {
            "vertical": ("arriba", "abajo"),
            "horizontal": ("izquierda", "derecha")
        }[self.eje]
        self.sprites = {}
        for i in range(1, 4):
            self.sprites[i]   = "lobo" + "_" + self.eje + "_" + direccion_1 + "_" + str(i)
            self.sprites[- i] = "lobo" + "_" + self.eje + "_" + direccion_2 + "_" + str(i)
        self.sprite = self.sprites[1] # sprite base del lobo

    def encontrar_camino(self):
        direcciones = {
            "vertical": ["U", "D"],
            "horizontal": ["L", "R"]
        }[self.eje]
        self.direccion_1, self.direccion_2 = direcciones
        self.fin = raycaster(self.tablero, self.tab_pos, self.direccion_1)
        self.inicio = raycaster(self.tablero, self.tab_pos, self.direccion_2)
        self.destino = self.fin
        self.direccion = self.direccion_1

    def run(self):
        if not self.destruido:
            self.mover()
            self.ciclo += 1
            if (self.ciclo % 10) == 0:
                if self.ciclo == 30:
                    self.ciclo = 0
                signo = {"U": 1, "L": 1, "D": -1, "R": -1}[self.direccion]
                self.sprite = self.sprites[signo * (1 + self.ciclo // 10)]
                self.sennal_cambiar.emit(self.id, self.sprite)

    def llegar(self):
        self.fila = float(self.destino[0])
        self.columna = float(self.destino[1])

        if self.destino == self.fin:
            self.destino = self.inicio
        else:
            self.destino = self.fin

        if self.direccion == self.direccion_1:
            self.direccion = self.direccion_2
        else:
            self.direccion = self.direccion_1

        signo = {"U": 1, "L": 1, "D": -1, "R": -1}[self.direccion]
        self.sprite = self.sprites[signo]
        self.ciclo = 0
        self.sennal_cambiar.emit(self.id, self.sprite)
    def lento(self, coeficiente):
        if not self.congelado:
            self.velocidad = self.velocidad * coeficiente
            self.congelado = True

    def destruir(self):
        self.destruido = True
        self.laberinto.lobos_destruidos += 1
        self.laberinto.sennal_esconder.emit(self.id)

    def reset(self):
        self.fila, self.columna = self.posicion_original
        self.destruido = False
        self.congelado = False
        self.laberinto.sennal_reaparecer.emit(self.id)
        self.velocidad = (
            Lobo.velocidad / self.laberinto.p_1 / self.laberinto.p_2 / self.laberinto.p_3
        )

class Zanahoria(Animado):
    velocidad = 8

    def __init__(self, argumento, fila, columna, laberinto):
        super().__init__(fila, columna, laberinto)
        vector = {"U":[-1, 0, "arriba"],
                 "D":[1, 0, "abajo"],
                 "L":[0, -1, "izquierda"],
                 "R":[0, 1, "derecha"]}[argumento]
        self.inicio = [self.fila, self.columna]
        boca_de_cannon = [fila + vector[0], columna + vector[1]]
        self.destino = raycaster(self.tablero, boca_de_cannon, argumento)

        self.direccion = vector[2]
        self.definir_sprites()
        # tarda la mitad de su velocidad en segundos en reaparecer
        self.desaparecer = 60 * Zanahoria.velocidad // 2
        self.destruido = False
        self.respawn = True
        self.ciclo = 0

    def run(self):
        if not self.destruido:
            self.mover()
        elif self.respawn: # Si su cañon esta destruido no queremos que reaparezca
            self.ciclo += 1
            if self.ciclo == self.desaparecer:
                self.ciclo = 0
                self.destruido = False
                self.laberinto.sennal_reaparecer.emit(self.id)

    def llegar(self):
        self.fila, self.columna = self.inicio
        self.destruido = True
        self.laberinto.sennal_esconder.emit(self.id)

    def definir_sprites(self):
        self.sprite = "zanahoria" + "_" + self.direccion

    def destruir(self):
        self.ciclo = 0
        self.llegar()

    def reset(self):
        self.respawn = True

class Cannon(Estatico):

    def __init__(self, argumento, fila, columna, laberinto):
        super().__init__(fila, columna, laberinto)
        self.direccion = {"U": "arriba", "D": "abajo", "L": "izquierda", "R": "derecha"}[argumento]
        self.definir_sprites()
        self.destruido = False
        self.zanahoria = Zanahoria(argumento, self.fila, self.columna, self.laberinto)
        self.laberinto.zanahorias.append(self.zanahoria)
    def definir_sprites(self):
        self.sprite = "canon" + "_" + self.direccion

    def destruir(self):
        self.destruido = True
        self.zanahoria.respawn = False
        self.tablero[self.fila][self.columna] = "-"
        self.laberinto.sennal_esconder.emit(self.id)
    def reset(self):
        self.destruido = False
        self.zanahoria.respawn = True
        self.tablero[self.fila][self.columna] = "CN"
        self.laberinto.sennal_reaparecer.emit(self.id)

class BombaManzana(Bomba):

    def __init__(self, fila, columna, laberinto):
        super().__init__(fila, columna, laberinto)
        # Destruye cañones
        for cannon in self.laberinto.cannones:
            if self.posicion == cannon.posicion:
                cannon.destruir()
    def definir_sprites(self):
        self.sprite = "explosion"
    def efecto(self):
        for enemigo in self.laberinto.lobos + self.laberinto.zanahorias:
            if chebyshev(self.posicion, enemigo.posicion, 0.99):
                enemigo.destruir()

class BombaCongelar(Bomba):
    coeficiente = 0.75

    def __init__(self, fila, columna, laberinto):
        super().__init__(fila, columna, laberinto)
    def definir_sprites(self):
        self.sprite = "congelacion"
    def efecto(self):
        for lobo in self.laberinto.lobos:
            if chebyshev(self.posicion, lobo.posicion, 0.99):
                lobo.lento(BombaCongelar.coeficiente)