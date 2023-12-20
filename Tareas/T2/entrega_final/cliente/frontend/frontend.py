from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from frontend.frontend_classes import DraggableLabel



class Titulo(QWidget):
    assets = {}

    def __init__(self):
        super().__init__()
        self.init_gui()
    def init_gui(self):
        # Tamaño maximo: (768, 512)
        self.titulo = QLabel(self)
        self.titulo.setPixmap(QPixmap(Titulo.assets["logo"]))
        self.titulo.setGeometry(144, 80, 480, 80)
        self.titulo.setScaledContents(True)

        self.subtitulo = QLabel("¿Una Partida?", self)
        self.subtitulo.setGeometry(234, 144, 300, 80)
        self.subtitulo.setFont(QFont(self.font().family(), 29))

        self.editar = QLineEdit(self)
        self.editar.setPlaceholderText("Ingrese su Usuario")
        self.editar.setGeometry(192, 224, 384, 40)

        self.ingresar = QPushButton("Ingresar", self)
#        self.ingresar.resize(self.ingresar.sizeHint())
        self.ingresar.setGeometry(192, 288, 120, 40)

        self.salir = QPushButton("Salir", self)
#        self.salir.resize(self.salir.sizeHint())
        self.salir.setGeometry(456, 288, 120, 40)

        self.salon_de_fama = QLabel("Salon de la Fama", self)
        self.salon_de_fama.setGeometry(192, 350, 300, 40)
        self.salon_de_fama.setFont(QFont(self.font().family(), 20))
        self.salon_de_fama.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.usuarios = {}
        self.puntajes = {}
        for i in range(5):
            self.usuarios[i] = QLabel(str(i + 1) + ". SIN PUNTAJE", self)
            self.usuarios[i].setGeometry(192, 400 + (i * 17), 384, 15)
            self.usuarios[i].setFont(QFont(self.font().family(), 10))

            self.puntajes[i] = QLabel("0 Puntos", self)
            self.puntajes[i].setGeometry(192, 400 + (i * 17), 384, 15)
            self.puntajes[i].setFont(QFont(self.font().family(), 10))
            self.puntajes[i].setAlignment(Qt.AlignmentFlag.AlignRight)

    def construir_leaderboard(self, leaderboard: dict):
        num_usuario = 0
        for key, value in leaderboard.items():
            self.usuarios[num_usuario].setText(str(num_usuario + 1) + ". " + key)
            self.puntajes[num_usuario].setText(str(value) + " Puntos")
            num_usuario += 1




class Nivel(QWidget):
    sennal_pausar = pyqtSignal()
    sennal_tecla = pyqtSignal(str)
    sennal_colocar_bomba = pyqtSignal(list, str)
    
    assets = {}

    def __init__(self, base):
        super().__init__()
        self.entidades = {}
        self.tablero = [["" for x in range(len(base[0]))] for x in range(len(base))]
        self.graficar_laberinto(base)
        self.init_gui()

    def init_gui(self):
        self.tiempo = QLabel("Tiempo: NaN segundos", self)
        self.tiempo.setFont(QFont(self.font().family(), 15))
        self.tiempo.setGeometry(16, 32, 320, 40)

        self.vidas = QLabel("Vidas restantes: NaN", self)
        self.vidas.setFont(QFont(self.font().family(), 15))
        self.vidas.setGeometry(16, 72, 320, 40)

        self.salir = QPushButton("Salir", self)
        self.salir.setGeometry(16, 112, 96, 40)

        self.pausa = QPushButton("Pausa", self)
        self.pausa.setGeometry(144, 112, 96, 40)
        self.pausa.clicked.connect(self.pausar)

        self.manzana = DraggableLabel("manzana", 20, 192, 88, 88, self)
        self.manzana.setPixmap(QPixmap(Nivel.assets["manzana"]))
        self.manzana.setScaledContents(True)
        self.manzana.drop.connect(self.colocar_bomba)

        self.congelar = DraggableLabel("congelacion", 148, 192, 88, 88, self)
        self.congelar.setPixmap(QPixmap(Nivel.assets["congelacion"]))
        self.congelar.setScaledContents(True)
        self.congelar.drop.connect(self.colocar_bomba)

        self.cantidad_manzanas = QLabel("Bombas\nManzanas:\nNaN", self)
        self.cantidad_manzanas.setGeometry(0, 288, 128, 60)
        self.cantidad_manzanas.setFont(QFont(self.font().family(), 13))
        self.cantidad_manzanas.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cantidad_congelar = QLabel("Bombas\nCongelacion:\nNaN", self)
        self.cantidad_congelar.setGeometry(128, 288, 128, 60)
        self.cantidad_congelar.setFont(QFont(self.font().family(), 13))
        self.cantidad_congelar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status= QLabel("Tip: Puedes arrastrar\n" +
                            "las bombas usando\n" +
                            "el mouse", self)
        self.status.setGeometry(0, 384, 256, 128)
        self.status.setFont(QFont(self.font().family(), 13))
        self.status.setAlignment(Qt.AlignmentFlag.AlignHCenter)


    def actualizar_vidas(self, vidas_nuevas):
        self.vidas.setText(f"Vidas restantes: {vidas_nuevas}")

    def cambiar_status(self, nuevo_status):
        self.status.setText(nuevo_status)

    def actualizar_tiempo(self, nuevo_tiempo):
        self.tiempo.setText(f"Tiempo: {nuevo_tiempo} segundos")
        
    def colocar_bomba(self, tipo, x_pos, y_pos):
        fila = y_pos // 32
        columna = (x_pos - 256) // 32
        self.sennal_colocar_bomba.emit([fila, columna], tipo)

    def pausar(self):
        self.sennal_pausar.emit()
        
    def keyPressEvent(self, event):
        tecla = event.text().lower()
        if tecla == "P":
            self.pausar()
        else:
            self.sennal_tecla.emit(tecla)

    def graficar_laberinto(self, base):
        # Tileset del laberinto.
        # Cañon es solido pero transparente
        fondo = QPixmap(Nivel.assets["bloque_fondo"])
        pared = QPixmap(Nivel.assets["bloque_pared"])
        tileset = {"-": fondo,    "CN": fondo,    "P": pared}
        for i in range(len(base)):
            for j in range(len(base[0])):
                celda = base[i][j]
                label = QLabel(self)
                label.setPixmap(tileset[celda])
                label.setScaledContents(True)
                label.setGeometry(256 + (32 * j), (32 * i), 32, 32)
                label.show()
                self.tablero[i][j] = label

    def graficar_entidad(self, entity_id, posicion, sprite):
        y_pos = int(posicion[0] * 32)
        x_pos = int(posicion[1] * 32)
        label = QLabel(self)
        label.setPixmap(QPixmap(Nivel.assets[sprite]))
        label.setScaledContents(True)
        label.setGeometry(256 + x_pos, y_pos, 32, 32)
        self.entidades[entity_id] = label
        if sprite in ["explosion", "congelacion"]:
            label.stackUnder(self.entidades[0])
        label.show()

    def mover_entidad(self, entity_id, posicion):
        # posicion = [fila, columna] = [y, x]
        y_pos = int(posicion[0] * 32)
        x_pos = int(posicion[1] * 32)
        self.entidades[entity_id].move(256 + x_pos, y_pos)

    def cambiar_sprite(self, entity_id, sprite):
        self.entidades[entity_id].setPixmap(QPixmap(Nivel.assets[sprite]))

    def esconder_entidad(self, entity_id: int):
        self.entidades[entity_id].hide()

    def mostrar_entidad(self, entity_id: int):
        self.entidades[entity_id].show()

    def eliminar_sprite(self, entity_id: int):
        self.entidades[entity_id].hide()
        self.entidades[entity_id].deleteLater()
        del self.entidades[entity_id]
    
    def reaparecer_entidad(self, entity_id: int):
        self.entidades[entity_id].show()

    def numero_bomba(self, tipo: str, numero: int):
        if tipo == "congelacion":
            self.cantidad_congelar.setText(f"Bombas\nCongelacion:\n{numero}")
        elif tipo == "manzana":
            self.cantidad_manzanas.setText(f"Bombas\nManzanas:\n{numero}")

class Juego(QStackedWidget):
    sennal_obtener_nivel = pyqtSignal(str)
    assets = {}
    ancho = 16
    largo = 16

    def __init__(self, titulo: Titulo):
        super().__init__()

        self.setWindowIcon((QIcon(Nivel.assets["conejo"])))
        self.setWindowTitle("DCConejoChico")
        
        self.titulo = titulo

        size = (max(768, 256 + (Juego.largo * 32)), max(512, (Juego.ancho * 32)))
        self.setMaximumSize(* size)
        self.setMinimumSize(* size)
        
        self.addWidget(self.titulo)
        self.titulo.ingresar.clicked.connect(self.entrar_nivel)
        self.titulo.salir.clicked.connect(self.close)

    def entrar_nivel(self):
        self.sennal_obtener_nivel.emit(self.titulo.editar.text())

    def error(self, error):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Critical)
        box.setWindowTitle("ERROR!")
        box.setText(error)
        box.exec()
    def warning(self, error):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle("Error.")
        box.setText(error)
        box.exec()
    def avanzar(self, nivel, total, puntos):
        box = QMessageBox(self)
        box.setIconPixmap(QPixmap(Juego.assets["conejo"]))
        box.setWindowTitle("Avanzar nivel.")
        box.setText(f"Avance hacia Nivel {nivel}.\n" +
                    f"Puntaje de nivel: {puntos}\n" +
                    f"Puntaje Acumulado hasta ahora: {total}")
        box.exec()
    def perder(self):
        file_url = QUrl.fromLocalFile(Juego.assets["derrota"])
        media_player = QMediaPlayer(self)
        media_player.setAudioOutput(QAudioOutput(self))
        media_player.setSource(file_url)
        media_player.play()
        box = QMessageBox(self)
        box.setIconPixmap(QPixmap(Juego.assets["conejo"]))
        box.setWindowTitle("PERDISTE!")
        box.setText("Perdiste el juego y Gatochico quedo\n" +
                    "condenada por la eternidad a vivir\n" +
                    "dentro del mundo virtual como un conejo.")
        box.exec()
        self.close()
    def win(self, total, puntos):
        file_url = QUrl.fromLocalFile(Juego.assets["victoria"])
        media_player = QMediaPlayer(self)
        media_player.setAudioOutput(QAudioOutput(self))
        media_player.setSource(file_url)
        media_player.play()
        box = QMessageBox(self)
        box.setIconPixmap(QPixmap(Juego.assets["conejo"]))
        box.setWindowTitle("GANASTE!")
        box.setText("Ganaste el juego y escapaste del mundo\n" +
                    "virtual, Tu puntaje en el ultimo nivel fue\n" +
                    f"{puntos} Puntos.\n" +
                    f"Y tu puntaje total acumulado es {total}")
        box.exec()
        self.close()