from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from backend.clases_abstractas import Entidad, Bomba
from backend.clases_laberinto import Lobo, Zanahoria, Cannon, Item, BombaCongelar
from backend.conejo import Conejo
from backend.backend_utilities import chebyshev, calcular_puntaje

class Laberinto(QObject):
    # Valores por defecto en parametros.py
    duracion = 120
    ancho = 16
    largo = 16
    vidas = 3
    ponderar_1 = 1
    ponderar_2 = 0.9
    ponderar_3 = 0.8
    inf_puntos = 350
    sennal_graficar = pyqtSignal(int, list, str) # id, [fila, columna], sprite
    sennal_mover = pyqtSignal(int, list) # id, [fila, columna]
    sennal_cambiar = pyqtSignal(int, str) # id, nuevo sprite
    sennal_tiempo = pyqtSignal(int) # nuevo tiempo
    sennal_esconder = pyqtSignal(int) # id
    sennal_reaparecer = pyqtSignal(int) # id
    sennal_status = pyqtSignal(str) # texto cualquiera
    sennal_eliminar = pyqtSignal(int) # id
    sennal_vidas = pyqtSignal(int)
    sennal_perder = pyqtSignal()
    sennal_ganar = pyqtSignal(int, float, list, int) # Nivel, puntos, inventario, vidas

    def __init__(self, laberinto_base: list[list], nivel, vidas_anteriores, inventario):
        super().__init__()
        Laberinto.clear_entity_ids()
        # Tomar en cuenta que todos los laberintos son 16x16
        self.tablero = [
            ["-" for _ in range(Laberinto.largo)] for _ in range(Laberinto.ancho)
        ]
        self.nivel = nivel
        # Obteniendo ponderadores dependiendo del nivel del laberinto.
        self.p_1, self.p_2, self.p_3 = Laberinto.administrar_ponderador(nivel)
        self.tiempo = int(Laberinto.duracion * self.p_1 * self.p_2 * self.p_3)
        self.vidas = Laberinto.obtener_vidas(vidas_anteriores, self.nivel)
        self.inventario = ([] if not inventario else inventario)
        self.lobos = []
        self.cannones = []
        self.items = []
        self.bombas = []
        self.zanahorias = []
        self.entidades = []
        self.lobos_destruidos = 0
        self.pausa = False
        self.infinity = False

        self.transformar(laberinto_base)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 16 ms == 1 frame, 60 frames aprox 1 segundo
        self.timer.timeout.connect(self.run)
        self.tick = QTimer(self)
        self.tick.setInterval(16)  # 16 ms == 1 frame, 60 frames aprox 1 segundo
        self.tick.timeout.connect(self.run_entities)

# ╔══════════════════════════════════
# ║ Seccion transformacion nivel
# ╚══════════════════════════════════
    def transformar(self, laberinto_base):
        entidades = []
        for i in range(Laberinto.ancho):
            for j in range(Laberinto.largo):
                elemento = laberinto_base[i][j]
                if elemento in ["P", "-"]:
                    self.tablero[i][j] = elemento
                    continue
                elif elemento in ["CU", "CD", "CL", "CR"]:
                    self.tablero[i][j] = "CN"
                entidades.append((elemento, i, j))
        self.implementar(entidades)

    def implementar(self, entidades: list):
        for entidad, i, j in entidades:
            if entidad in ["CU", "CD", "CL", "CR"]:
                self.cannones.append(Cannon(entidad[1], i, j, self))
            elif entidad in ["LV", "LH"]:
                self.lobos.append(Lobo(entidad[1], i, j, self))
            elif entidad in ["BM", "BC"]:
                self.items.append(Item(entidad[1], i, j, self))
            elif entidad == "C":
                conejo = [i, j]
            elif entidad == "E":
                entrada = [i, j]
            elif entidad == "S":
                salida = [i, j]
            else:
                raise ValueError(f"No se puede implementar '{entidad}' en {[i, j]}")
        # Definimos conejo de ultimo para añadirle la entrada y salida
        self.conejo = Conejo(conejo[0], conejo[1], self, entrada, salida)

# ╔══════════════════════════════════════════════
# ║ Seccion eventos, graficos, timers... etc.
# ╚══════════════════════════════════════════════

    def iniciar(self):
        self.graficar()
        self.sennal_tiempo.emit(self.tiempo)
        self.sennal_vidas.emit(self.vidas)
        self.timer.start()
        self.tick.start()

    def graficar(self):
        for item in self.items:
            item.graficar()
        for enemigo in (self.lobos + self.zanahorias):
            enemigo.graficar()
        for cannon in self.cannones:
            cannon.graficar()
        self.conejo.graficar()

    def run(self):
        if not self.pausa:
            self.tiempo -= 1
            self.sennal_tiempo.emit(self.tiempo)
            if self.tiempo == 0:
                self.perder()

    def run_entities(self):
        if not self.pausa:
            self.conejo.run()
            for lobo in self.lobos:
                lobo.run()
            for zanahoria in self.zanahorias:
                zanahoria.run()
            for bomba in self.bombas:
                bomba.run()

    def pausar(self):
        self.pausa = not self.pausa
    
    def colocar_bomba(self, posicion: list, tipo: str):
        fila, columna = posicion
        if ((0 <= fila <= Laberinto.ancho) and (0 <= columna <= Laberinto.largo)):
            caminable = self.tablero[fila][columna] not in ["P", "CN"]
            despejado = True
            for entity in self.lobos + self.zanahorias + self.items:
                if entity.destruido is False:
                    despejado = despejado and not chebyshev(posicion, entity.posicion, 0.99)
            if caminable and despejado:
                self.conejo.colocar_bomba(fila, columna, tipo)
            elif caminable:
                self.sennal_status.emit("No puedes colocar\nbombas sobre enemigos.")
            else:
                self.sennal_status.emit("No puedes colocar\nbombas sobre obstaculos.")

    def infinito(self):
        self.timer.stop()
        self.infinity = True
        self.sennal_tiempo.emit("infinitas")
        self.sennal_vidas.emit(999999)

    def matar(self):
        for lobo in self.lobos:
            lobo.destruir()
        for zanahoria in self.zanahorias:
            # Las zanahorias no van a respawnear
            zanahoria.destruir()
            zanahoria.respawn = False

    def perder_vida(self):
        if not self.infinity:
            self.vidas -= 1
            self.sennal_vidas.emit(self.vidas)
        if self.vidas == 0:
            self.perder()

    def reset(self):
        for objeto in self.lobos + self.cannones:
            objeto.reset()
# ╔══════════════════════════════════════════════
# ║ Seccion fin de nivel.
# ╚══════════════════════════════════════════════
    def perder(self):
        self.timer.stop()
        self.tick.stop()
        self.sennal_perder.emit()

    def ganar(self):
        puntos = self.calcular_puntos()
        self.sennal_ganar.emit(self.nivel, puntos, self.inventario, self.vidas)

    def calcular_puntos(self):
        if self.infinity is False:
            return calcular_puntaje(
                self.tiempo, self.vidas, self.lobos_destruidos, Laberinto.puntos_lobo
                )
        else:
            return float(Laberinto.inf_puntos)
        
    def autodestruir(self):
        # Destruye todas las entidades para poder optimizar la aplicacion
        self.timer.stop()
        self.tick.stop()
        del self.timer
        del self.tick
        del self.conejo
        entidades = (self.lobos + self.items + self.bombas + self.zanahorias)
        for entidad in entidades:
            del entidad

# ╔══════════════════════════════════════════════
# ║ Seccion metodos estaticos.
# ╚══════════════════════════════════════════════
    @staticmethod
    def definir_parametros(
        ancho, largo, velocidad_conejo, velocidad_lobo, velocidad_zanahoria, tiempo_bomba,
        duracion_inicial, ponderar_1, ponderar_2, ponderar_3, puntos_lobo, vidas_inicial,
        puntaje_inf, coeficiente_congelar,
        ):
        Laberinto.ancho = ancho
        Laberinto.largo = largo
        Laberinto.vidas = vidas_inicial
        Laberinto.duracion = duracion_inicial
        Laberinto.ponderar_1 = ponderar_1
        Laberinto.ponderar_2 = ponderar_2
        Laberinto.ponderar_3 = ponderar_3
        Laberinto.puntos_lobo = puntos_lobo
        Laberinto.inf_puntos = puntaje_inf
        Conejo.velocidad = velocidad_conejo
        Lobo.velocidad = velocidad_lobo
        Zanahoria.velocidad = velocidad_zanahoria
        Bomba.tiempo_defusion = tiempo_bomba
        BombaCongelar.coeficiente = coeficiente_congelar

    @staticmethod
    def clear_entity_ids():
        Entidad.entity_id = 0

    @staticmethod
    def obtener_vidas(vidas, nivel):
        if vidas is False:
            return max(1, Laberinto.vidas - nivel + 1)
        else:
            return vidas
        
    @staticmethod
    def administrar_ponderador(nivel):
        if nivel == 1:
            return [Laberinto.ponderar_1, 1, 1]
        elif nivel == 2:
            return [Laberinto.ponderar_1, Laberinto.ponderar_2, 1]
        elif nivel == 3:
            return [Laberinto.ponderar_1, Laberinto.ponderar_2, Laberinto.ponderar_3]