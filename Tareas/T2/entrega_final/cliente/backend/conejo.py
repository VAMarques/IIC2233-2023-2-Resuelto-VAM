from backend.clases_abstractas import Animado
from backend.clases_laberinto import BombaManzana, BombaCongelar
from backend.backend_utilities import (
    validar_direccion, raycaster, poner_bomba, usar_item, euclid
)
from PyQt6.QtCore import pyqtSignal

class Conejo(Animado):
    sennal_numero_bomba = pyqtSignal(str, int)
    sennal_morir = pyqtSignal()

    velocidad = 10 # valor por defecto.

    def __init__(self, fila, columna, laberinto, entrada, salida):
        super().__init__(fila, columna, laberinto)
        self.definir_sprites()
        self.estacionado = True
        self.ciclo = 0
        # Segun la pauta es necesario que la velocidad aumente con los niveles
        self.velocidad = (
            Conejo.velocidad / self.laberinto.p_1 / self.laberinto.p_2 / self.laberinto.p_3
        )
        self.inventario = self.laberinto.inventario
        self.entrada = entrada
        self.salida = salida
        self.codigo = ["-", "-", "-"]

    def graficar(self):
        super().graficar()
        self.sennal_numero_bomba.emit("manzana", self.inventario.count("manzana"))
        self.sennal_numero_bomba.emit("congelacion", self.inventario.count("congelacion"))

    def definir_sprites(self):
        self.sprite = "conejo"
        self.sprites = {}
        for i in range(1, 4):
            self.sprites[f"U{i}"] = "conejo" + "_" + "arriba" + "_" + str(i)
            self.sprites[f"D{i}"] = "conejo" + "_" + "abajo" + "_" + str(i)
            self.sprites[f"L{i}"] = "conejo" + "_" + "izquierda" + "_" + str(i)
            self.sprites[f"R{i}"] = "conejo" + "_" + "derecha" + "_" + str(i)

    def run(self):
        if not self.estacionado:
            self.mover()
            self.ciclo += 1
            if (self.ciclo % 10) == 0:
                if self.ciclo == 30:
                    self.ciclo = 0
                self.sprite = self.sprites[self.direccion + str(1 + self.ciclo // 10)]
                self.sennal_cambiar.emit(self.id, self.sprite)
        self.colision()

    def colision(self):
        for enemigo in (self.laberinto.lobos + self.laberinto.zanahorias):
            #Es un rango menor a 1, por tanto no se sentira tan injusto
            # colision circular por distancia euclideana
            if not enemigo.destruido:
                if euclid(self.posicion, enemigo.posicion, 0.8):
                    self.morir()
                    break

    def llegar(self):
        self.fila = float(self.destino[0])
        self.columna = float(self.destino[1])
        if self.tab_pos == self.salida:
            self.laberinto.ganar()
        self.estacionado = True
        self.sprite = "conejo"
        self.ciclo = 0
        self.sennal_cambiar.emit(self.id, self.sprite)

    def tecla(self, tecla):
        direcciones = {"w": "U",    "s": "D",    "a": "L",    "d": "R"}
        if tecla in direcciones and self.estacionado:
            direccion = direcciones[tecla]
            if validar_direccion(self.tablero, self.tab_pos, direccion):
                self.estacionado = False
                self.direccion = direccion
                self.destino = raycaster(self.tablero, self.tab_pos, direccion)
                self.sprite = self.sprites[self.direccion + "1"]
                self.sennal_cambiar.emit(self.id, self.sprite)
        elif tecla in direcciones:
            pass
        elif tecla == "g":
            for item in self.laberinto.items:
                if item.posicion == self.tab_pos and not item.destruido:
                    tipo = item.tipo
                    self.inventario.append(tipo)
                    item.destruir()
                    self.sennal_numero_bomba.emit(tipo, self.inventario.count(tipo))
        else:
            self.codigo.pop(0)
            self.codigo.append(tecla)
            print(self.codigo)
            if self.codigo == ["k", "i", "l"]:
                self.laberinto.matar()
                self.laberinto.sennal_status.emit("Lobos eliminados")
            elif self.codigo == ["i", "n", "f"]:
                self.laberinto.infinito()
                self.laberinto.sennal_status.emit("Tiempo y Vidas\nInfinitas")
            elif self.codigo == ["b", "m", "b"]:
                # Gracias a self.inventario + lista, es que el inventario vuelve a la normalidad
                # despues de terminado el nivel, pues es el inventario de nivel el que se mantiene.
                self.inventario = self.inventario + ["manzana"] * 100
                self.inventario = self.inventario + ["congelacion"] * 100
                self.sennal_numero_bomba.emit("manzana", self.inventario.count("manzana"))
                self.sennal_numero_bomba.emit("congelacion", self.inventario.count("congelacion"))
    def colocar_bomba(self, fila, columna, tipo):
        se_tiene, self.inventario = usar_item(tipo, self.inventario)
        clase = {"manzana": BombaManzana, "congelacion": BombaCongelar}[tipo]
        if se_tiene:
            for i, j in poner_bomba(self.tablero, [fila, columna]):
                clase(i, j, self.laberinto)
            self.sennal_numero_bomba.emit(tipo, self.inventario.count(tipo))
            self.laberinto.sennal_status.emit(f"Bomba {tipo} colocada\nen {fila}, {columna}")
        else:
            self.laberinto.sennal_status.emit("No te quedan bombas\nde este tipo")

    def morir(self):
        fila, columna = self.entrada
        self.fila, self.columna = (float(fila), float(columna))
        self.destino = self.posicion
        self.sennal_mover.emit(self.id, [self.fila, self.columna])
        self.laberinto.perder_vida()
        self.laberinto.reset()