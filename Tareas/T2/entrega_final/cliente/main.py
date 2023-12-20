from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QFont

import sys
import json

from frontend.frontend import Titulo, Nivel, Juego
from backend.laberinto import Laberinto
from backend.backend import Backend

from main_utilities import ASSETS, open_laberinto
import parametros as p


class DCConejoChico(QObject):
    # Parametros de init
    def __init__(self,
        host: str,
        puerto: int,
        assets: dict,
        ancho: int,
        largo: int,
        velocidad_conejo: int,
        velocidad_lobo: int,
        velocidad_zanahoria: int,
        duracion_inicial: int,
        ponderar_1: float,
        ponderar_2: float,
        ponderar_3: float,
        puntos_lobo: int,
        vidas_inicial: int,
        puntaje_inf: int,
        tiempo_bomba: int,
        coeficiente_congelar: float
        ):
        super().__init__()
        # Definir parametros de Clase
        self.assets = assets
        self.ancho = ancho
        self.largo = largo
        Titulo.assets = self.assets
        Nivel.assets = self.assets
        Juego.assets = self.assets
        Juego.ancho = ancho
        Juego.largo = largo
        Laberinto.definir_parametros(
            ancho = ancho,
            largo = largo,
            velocidad_conejo = velocidad_conejo,
            velocidad_lobo = velocidad_lobo,
            velocidad_zanahoria = velocidad_zanahoria,
            duracion_inicial = duracion_inicial,
            ponderar_1 = ponderar_1,
            ponderar_2 = ponderar_2,
            ponderar_3 = ponderar_3,
            puntos_lobo = puntos_lobo,
            vidas_inicial = vidas_inicial,
            puntaje_inf = puntaje_inf,
            tiempo_bomba = tiempo_bomba,
            coeficiente_congelar = coeficiente_congelar
        )
        # Iniciar clases permanentes
        self.titulo = Titulo()
        self.frontend = Juego(self.titulo)
        self.backend = Backend(host, puerto)
        self.backend.sennal_sin_server.connect(self.error_conectar_server)
        self.backend.sennal_desconexion.connect(self.error_desconectado)
        self.frontend.sennal_obtener_nivel.connect(self.obtener_nivel)
        puntajes = self.backend.comunicar("LEADERBOARD:")[1] # Solo el resultado, no el codigo
        self.titulo.construir_leaderboard(puntajes)
        self.iniciar()

    def error_conectar_server(self):
        print("No se pudo conectar al server")
        exit()
    def error_desconectado(self):
        self.frontend.error("ERROR: Se perdio la conexion al server")
        exit()

    def obtener_nivel(self, usuario):
        self.usuario = usuario
        codigo, resultado = self.backend.obtener_nivel(usuario)
        if codigo == "NIVEL":
            self.iniciar_juego(resultado)
        elif codigo == "WARNING":
            self.frontend.warning(resultado)
        elif codigo == "ERROR":
            self.frontend.error(resultado)

    def iniciar_juego(self, nivel):
        # nivel = ultimo nivel registrado, 0 si no ha jugado antes o si ya es nivel 3
        self.nivel_actual = nivel + 1
        self.empezar_laberinto(False, False)

    def ganar(self, nivel, puntos, inventario, vidas):
        # Borrar el nivel anterior
        self.laberinto.autodestruir()
        self.frontend.setCurrentWidget(self.titulo)
        self.frontend.removeWidget(self.nivel)
        del self.nivel
        del self.laberinto

        codigo, resultado = self.backend.avanzar_nivel(self.usuario, nivel, puntos)
        if codigo == "AVANZAR":
            total = resultado[0]
            self.nivel_actual = resultado[1]
            self.frontend.avanzar(self.nivel_actual, total, puntos)
            self.empezar_laberinto(vidas, inventario)
        elif codigo == "WIN":
            self.frontend.win(resultado, puntos)

    def empezar_laberinto(self, vidas: int, inventario: list):
        # self.laberinto y self.nivel son ambos clases esporadicas que se borran al final
        tablero = open_laberinto(
            self.assets[f"tablero_{self.nivel_actual}"],
            self.ancho,
            self.largo)
        self.laberinto = Laberinto(tablero, self.nivel_actual, vidas, inventario)
        self.nivel = Nivel(self.laberinto.tablero.copy())
        self.conectar_laberinto()

    def conectar_laberinto(self):
        self.frontend.addWidget(self.nivel)
        self.frontend.setCurrentWidget(self.nivel)
        self.nivel.sennal_tecla.connect(self.laberinto.conejo.tecla)
        self.nivel.sennal_colocar_bomba.connect(self.laberinto.colocar_bomba)
        self.nivel.sennal_pausar.connect(self.laberinto.pausar)
        self.laberinto.conejo.sennal_numero_bomba.connect(self.nivel.numero_bomba)
        self.laberinto.sennal_graficar.connect(self.nivel.graficar_entidad)
        self.laberinto.sennal_mover.connect(self.nivel.mover_entidad)
        self.laberinto.sennal_cambiar.connect(self.nivel.cambiar_sprite)
        self.laberinto.sennal_tiempo.connect(self.nivel.actualizar_tiempo)
        self.laberinto.sennal_esconder.connect(self.nivel.esconder_entidad)
        self.laberinto.sennal_reaparecer.connect(self.nivel.reaparecer_entidad)
        self.laberinto.sennal_status.connect(self.nivel.cambiar_status)
        self.laberinto.sennal_perder.connect(self.frontend.perder)
        self.laberinto.sennal_ganar.connect(self.ganar)
        self.laberinto.sennal_vidas.connect(self.nivel.actualizar_vidas)
        self.laberinto.sennal_eliminar.connect(self.nivel.eliminar_sprite)
        self.nivel.salir.clicked.connect(self.frontend.close)
        self.laberinto.iniciar()

    def iniciar(self):
        self.frontend.show()

if __name__ == "__main__":
    if len(sys.argv) < 2 or not sys.argv[1].isnumeric():
        raise ValueError(
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║Debes especificar un puerto numerico despues de 'python main.py'              ║
║                                                                              ║
║Por ejemplo, 'python main.py 9999'                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    )
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook

    puerto_cliente = int(sys.argv[1])
    with open("host.json", "rb") as archivo:
        host_cliente = json.load(archivo)["host"]

    app = QApplication([])
    app.setFont(QFont("Courier New"))
    game = DCConejoChico(
        host = host_cliente,
        puerto = puerto_cliente,
        assets = ASSETS,
        ancho = p.ANCHO_LABERINTO,
        largo = p.LARGO_LABERINTO,
        velocidad_conejo = p.VELOCIDAD_CONEJO,
        velocidad_lobo = p.VELOCIDAD_LOBO,
        velocidad_zanahoria = p.VELOCIDAD_ZANAHORIA,
        duracion_inicial = p.DURACION_NIVEL_INICIAL,
        ponderar_1 = p.PONDERADOR_LABERINTO_1,
        ponderar_2 = p.PONDERADOR_LABERINTO_2,
        ponderar_3 = p.PONDERADOR_LABERINTO_3,
        puntos_lobo = p.PUNTAJE_LOBO,
        vidas_inicial = p.CANTIDAD_VIDAS,
        puntaje_inf = p.PUNTAJE_INF,
        tiempo_bomba = p.TIEMPO_BOMBA,
        coeficiente_congelar = p.COEFICIENTE_LENTO
    )
    sys.exit(app.exec())