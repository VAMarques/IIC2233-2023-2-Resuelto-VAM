from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.sip import wrappertype
import abc
from math import copysign

class QAbstract(abc.ABCMeta, wrappertype):
    pass

class Entidad(abc.ABC, QObject, metaclass=QAbstract):
    entity_id = 0

    def __init__(self, laberinto):
        super().__init__()
        self.laberinto = laberinto
        self.tablero = laberinto.tablero
        self.sprite = ""
        self.sennal_mover = laberinto.sennal_mover
        self.sennal_graficar = laberinto.sennal_graficar
        self.sennal_cambiar = laberinto.sennal_cambiar

        self.id = Entidad.entity_id
        Entidad.entity_id += 1

    def graficar(self):
        self.sennal_graficar.emit(self.id, [self.fila, self.columna], self.sprite)

    @abc.abstractmethod
    def definir_sprites(self):
        pass

class Animado(Entidad):
    """
    Clase Abstracta para Conejo, Lobo, Zanahoria, salen errores para sprite, velocidad, destino.

    Pero eso es porque esos atributos deben definirse en su propia clase en el momento adecuado.

    Ademas, self.velocidad hace referencia a la velocidad de la Clase, NO de la instancia.
    """
    velocidad = 0 # Toda subclase debe tener esto

    def __init__(self, fila, columna, laberinto):
        super().__init__(laberinto)
        self.fila = float(fila)
        self.columna = float(columna)
        self.posicion_original = self.posicion
        self.destino = [0, 0]
        self.velocidad = type(self).velocidad # Por defecto

    def mover(self):
        """Si no esta en el destino, se mueve a self.velocidad hacia el."""

        delta_pos = self.velocidad / 60
        delta_fila = self.fila - self.destino[0]
        delta_col = self.columna - self.destino[1]
        same_fila = -delta_pos < delta_fila < delta_pos
        same_col = -delta_pos < delta_col < delta_pos
        if same_fila and same_col:
            self.llegar()
        elif same_fila:
            self.columna -= copysign(delta_pos, delta_col)
        elif same_col:
            self.fila -= copysign(delta_pos, delta_fila)

        self.sennal_mover.emit(self.id, [self.fila, self.columna])

    @abc.abstractmethod
    def llegar(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    @property
    def posicion(self):
        return [self.fila, self.columna]

    @property
    def tab_pos(self):
        """
        Posicion aproximada en el tablero, pues los animados tienen posicion float,
        Pero el tablero es discreto, solo es int
        """
        return [round(self.fila), round(self.columna)]

class Estatico(Entidad):

    def __init__(self, fila, columna, laberinto):
        super().__init__(laberinto)
        self.fila = fila
        self.columna = columna

    @property
    def posicion(self):
        return [self.fila, self.columna]

class Bomba(Estatico):
    """Debe ser definido su sprite, y su efecto."""
    tiempo_defusion = 5

    def __init__(self, fila, columna, laberinto):
        super().__init__(fila, columna, laberinto)
        self.definir_sprites()
        self.graficar()
        self.ciclo = Bomba.tiempo_defusion * 60
        self.laberinto.bombas.append(self)
    def run(self):
        # Siempre recordar, 60 ticks = 60 frames = 1 segundo.
        # Como las bombas pueden ser pesadas para el rendimiento, no vamos a revisar sus fisicas
        # constantemente, tambien aprovechamos que no se mueven.
        self.ciclo -= 1
        if (self.ciclo % 6) == 0: # diez veces cada segundo
            self.efecto()
        if self.ciclo == 0:
            self.destruir()
    @abc.abstractmethod
    def efecto(self):
        pass
    def destruir(self):
        self.laberinto.sennal_eliminar.emit(self.id)
        self.laberinto.bombas.remove(self)
        del self