from PyQt6.QtCore import QObject, pyqtSignal
from backend.mensaje import (
    codificacion_rapida, decodificar_rapido, recibir_mensaje, mandar_mensaje
)
from backend.backend_utilities import dictify_puntajes, validacion_formato
import socket


class Backend(QObject):
    sennal_sin_server = pyqtSignal()
    sennal_desconexion = pyqtSignal()
    sennal_puntajes = pyqtSignal(dict)
    sennal_win = pyqtSignal(int)
    sennal_avanzar = pyqtSignal(int, int)
    sennal_nivel = pyqtSignal(int)
    sennal_error = pyqtSignal(str)
    sennal_warning = pyqtSignal(str)

    def __init__(self, host, puerto):

        super().__init__()
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket_cliente.connect((host, puerto))
            self.conectado = True
        except ConnectionError:
            self.socket_cliente.close()
            self.conectado = False

    def obtener_nivel(self, usuario):
        if validacion_formato(usuario):
            return self.comunicar(f"CONECTAR:{usuario}")
        else:
            return (
                "WARNING", "ERROR: nombre de usuario invalido:\n" +
                "Debe tener al menos un numero, una mayuscula\n" +
                "ser compuesto de solo letras y numeros,\n" +
                "y tener entre 3 y 16 caracteres"
            )
    def avanzar_nivel(self, usuario, nivel, puntos):
        # El servidor lo diseñe pensando que puntos era int, resulta que eran float?
        # No se explico muy bien eso.
        # Solo me acorde por las funciones.
        return self.comunicar(f"GANAR:{usuario};{nivel};{puntos}")

    def comunicar(self, mensaje: str) -> str:
        if self.conectado:
            try:
                codificado = codificacion_rapida(mensaje)
                mandar_mensaje(codificado, self.socket_cliente)
                recibido = decodificar_rapido(recibir_mensaje(self.socket_cliente))
                return self.procesar_mensaje(recibido)
            except ConnectionError:
                self.sennal_desconexion.emit()
                self.socket_cliente.close()
                self.conectado = False
            except OSError as e:
                # OSError es un error peculiar, en este caso este especifico numero es uno que
                # resulta cuando se desconecta el socket antes de tiempo.
                if e.errno != 10038:
                    raise(e)
                self.sennal_desconexion.emit()
                self.socket_cliente.close()
                self.conectado = False
        else:
            self.sennal_sin_server.emit()

    def procesar_mensaje(self, mensaje: str):
        codigo, _, argumento = mensaje.partition(":")
        if codigo == "PUNTAJES":
            resultado = dictify_puntajes(argumento)
        elif codigo == "NIVEL":
            resultado = int(argumento)
        elif codigo == "WIN":
            resultado = float(argumento)
        elif codigo == "AVANZAR":
            puntos_actual, proximo_nivel = argumento.split(";")
            resultado = (float(puntos_actual), int(proximo_nivel))
        elif codigo in ["ERROR", "WARNING"]:
            resultado = (argumento)
        else:
            # Error de codificacion, solo para consola
            print(f"ERROR DE CODIFICACION {codigo}:{argumento}")
        return (codigo, resultado)