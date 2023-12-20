import socket
import sys
import json
import threading
from mensaje import codificacion_rapida, decodificar_rapido, recibir_mensaje, mandar_mensaje
from server_utils import (
    puntajes_altos, pretty_print, usuario_permitido, modificar_registro, encontrar_nivel, 
    arreglar_registros
)


class Servidor:
    id_clientes = 0

    def __init__(self, port: int, host: str, path_baneados: str, path_puntajes: str):
        self.host = host
        self.port = port
        self.path_baneados = path_baneados
        self.path_puntajes = path_puntajes
        self.abierto = True
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.revisar_leaderboard()
        self.abrir_server()
        self.manejar_server()

    def revisar_leaderboard(self):
        with open(self.path_puntajes, "r", encoding = "utf-8") as puntos:
            arreglar, leaderboard = arreglar_registros(puntos.readlines())
        if arreglar:
            with open(self.path_puntajes, "w", encoding = "utf-8") as puntos:
                puntos.writelines(leaderboard)

    def abrir_server(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        pretty_print((f'Servidor escuchando en {self.host} : {self.port}'))

        self.sockets = {}
        self.accept_connections()

    def accept_connections(self) -> None:
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self) -> None:
        try:
            while self.abierto:
                socket_cliente, address = self.socket_server.accept()
                self.sockets[socket_cliente] = address
                listening_client_thread = threading.Thread(
                    target=self.listen_client_thread,
                    args=(socket_cliente, ),
                    daemon=True)
                listening_client_thread.start()
        except OSError as e:
            # Esta se ejecuta con errores de socket, suele suceder al cerrar el server.
            if e.errno != 10038:
                raise(e)

    def listen_client_thread(self, socket_cliente: socket) -> None:
        try:
            posibles_acciones = {
                "LEADERBOARD": self.leaderboard,
                "CONECTAR": self.usuario_conectado,
                "GANAR": self.ganar
            }
            while self.abierto:
                pedido = decodificar_rapido(recibir_mensaje(socket_cliente))
                accion, _, argumentos = pedido.partition(":")
                # Activar esta excepcion para ver el comportamiento cuando ocurre una
                # Excepcion del lado del servidor.
                # raise Exception("LOLOLOL")
                if accion in posibles_acciones:
                    posibles_acciones[accion](argumentos, socket_cliente)
                else:
                    respuesta = codificacion_rapida(f"ERROR:{accion} no es valida")
                    mandar_mensaje(respuesta, socket_cliente)

        except ConnectionError:
            pretty_print(f"[{self.sockets[socket_cliente]}] Cliente desconectado")
            socket_cliente.close()
            del self.sockets[socket_cliente]

        except OSError as e:
            # Esta se ejecuta con errores de socket, suele suceder al cerrar el server.
            if e.errno != 10038:
                raise e

        #En teoria en este caso no es malo, pues en la experiencia 4 se permitia esto con
        # El fin de que no se caiga el servidor, pero me causo mas problemas de los que arreglaba.
        # Debido a eso, no esta activado, y debe ser descomentado.
        # En caso de querer ver el comportamiento, descomentese esto y el raise exception dentro
        # De try:

        # except Exception as e:
        #     pretty_print(f"[{self.sockets[socket_cliente]}] Cliente desconectado por excepcion\n"
        #                  f"La excepcion ocurrida fue {e}")
        #     socket_cliente.close()
        #     del self.sockets[socket_cliente]
     

    def leaderboard(self, _, socket_cliente):
        with open(self.path_puntajes, "r", encoding = "utf-8") as puntos:
            leaderboard = codificacion_rapida(puntajes_altos(puntos.readlines()))
        # El codigo de mensaje es "PUNTAJES:user1;nivel;puntaje_total,user2..."
        mandar_mensaje(leaderboard, socket_cliente)
        pretty_print(f"{self.sockets[socket_cliente]} Se ha conectado al juego")


    def usuario_conectado(self, usuario, socket_cliente):
        with open(self.path_baneados, "r", encoding = "utf-8") as archivo:
            baneados = json.load(archivo)
        if not usuario_permitido(usuario, baneados):
            respuesta = "ERROR:Usuario Baneado"
            pretty_print(f"\n{self.sockets[socket_cliente]} Trato de iniciar como\n" +
                         f"Usuario no permitido {usuario}\n")
        else:
            with open(self.path_puntajes, "r", encoding = "utf-8") as archivo:
                nivel = encontrar_nivel(archivo.readlines(), usuario)
            respuesta = f"NIVEL:{nivel}"
            pretty_print(f"\n{self.sockets[socket_cliente]} Ha iniciado como {usuario}\n")
        codificado = codificacion_rapida(respuesta)
        mandar_mensaje(codificado, socket_cliente)

    def ganar(self, argumentos, socket_cliente):
        usuario, nivel, puntos = argumentos.split(";")

        with open(self.path_puntajes, "r", encoding = "utf-8") as archivo:
            lista_usuarios = archivo.readlines()

        total_puntos, lista_usuarios = modificar_registro(
            lista_usuarios, usuario, nivel, puntos
        )

        with open(self.path_puntajes, "w", encoding = "utf-8") as archivo:
            archivo.writelines(lista_usuarios)
        if int(nivel) < 3:
            # Puntos totales, nivel
            respuesta = f"AVANZAR:{total_puntos};{int(nivel) + 1}"
            pretty_print(f"\n{usuario} ha terminado el nivel {nivel} con {puntos},\n" +
                         f"acumulando hasta el momento {total_puntos} puntos en total\n" +
                         f"Y por tanto, avanzando al nivel {int(nivel) + 1}\n")
        else:
            respuesta = f"WIN:{total_puntos}"
            pretty_print(f"\n{usuario} termino el nivel 3 con {puntos}, y por tanto,\n" + 
                         "ha ganado el juego con un total a su cuenta de:\n" +
                         f"{total_puntos} puntos\n")
        mandar_mensaje(codificacion_rapida(respuesta), socket_cliente)

    def manejar_server(self):
        menu = """
OPCIONES DE MANEJO DE SERVIDOR:
EXIT: Cerrar servidor.
MENU: Abrir este menu de accion nuevamente

Seleccione opciones usando la consola de comandos.
Las opciones deben ser escritas en mayuscula.
"""
        pretty_print(menu)
        while self.abierto:
            accion = input()
            if accion == "EXIT":
                self.abierto = False
                pretty_print("Cerrando Servidor...")
                self.socket_server.close()
            elif accion == "MENU":
                pretty_print(menu)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError(
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║Debes especificar un puerto numerico despues de 'python main.py'              ║
║                                                                              ║
║Por ejemplo, 'python main.py 9999'                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        )
    puerto = int(sys.argv[1])
    PATH_HOST = "host.json"
    BANEADOS = "baneados.json"
    PUNTAJES = "puntaje.txt"
    with open(PATH_HOST, "rb") as archivo:
        host_json = json.load(archivo)
        host = host_json["host"]
    server = Servidor(puerto, host, path_baneados=BANEADOS, path_puntajes=PUNTAJES)

