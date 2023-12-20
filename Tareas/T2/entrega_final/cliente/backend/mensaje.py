# Serializar -> (Separar ->) Encriptar -> Codificar
def serializar_mensaje(mensaje: str) -> bytearray:
    encoded = bytearray(mensaje, encoding="utf-8")
    return encoded

def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    a, b, c = [bytearray(), bytearray(), bytearray()]
    for index, byte in enumerate(mensaje):
        modulo = index % 6
        parte = {
            0: a,
            1: b,
            2: c,
            3: c,
            4: b,
            5: a
        }[modulo]
        parte.append(byte)
    return [a, b, c]

def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    a, b, c = separar_mensaje(mensaje)
    n = (a[0] + b[-1]+ c[0] + 1) % 2 # si la suma de bytes correspondientes es par = 1, impar = 0
    encriptado = bytearray([n])
    if n == 1:
        encriptado += a + c + b
    else:
        encriptado += b + a + c
    return encriptado

def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    separado = []
    longitud = bytearray(len(mensaje).to_bytes(4, byteorder="big"))
    separado.append(longitud)
    secciones = len(mensaje) // 36
    for s in range(secciones):
        bloque = bytearray((s + 1).to_bytes(4, byteorder="big"))
        seccion = mensaje[36 * s:36 * (s + 1)]
        separado.append(bloque)
        separado.append(seccion)
    bloque = bytearray((secciones + 1).to_bytes(4, byteorder="big"))
    seccion = mensaje[36 * secciones:] + bytearray(b"\x00") * 36
    seccion = seccion[0:36]
    separado.append(bloque)
    separado.append(seccion)
    return separado





# Decodificar -> Desencriptar -> (Recombinar ->) Deserializar
def deserializar_mensaje(encoded: bytearray) -> str:
    return encoded.decode(encoding="utf-8", errors="replace")

def recombinar_mensaje(separado: list[bytearray]) -> bytearray:
    a, b, c = separado
    serial = bytearray()
    for i in range(len(a) + (len(b) + len(c))):
        modulo = i % 6
        parte = {
            0: a,
            1: b,
            2: c,
            3: c,
            4: b,
            5: a
        }[modulo]
        serial.append(parte.pop(0))
    return serial

def desencriptar_mensaje(mensaje: bytearray) -> bytearray:
    mensaje = mensaje.copy()
    n = mensaje.pop(0)
    n_bytes = len(mensaje)
    # Metodo numerico, para hacerlo revise con un cuaderno los valores, y pense en lo ciclico del
    # patron subyacente.
    len_a = 1 + ((n_bytes - 1) // 6) + (n_bytes // 6)
    len_b = (n_bytes + 1) // 3
    len_c = ((n_bytes + 3) // 6) + ((n_bytes + 2) // 6)
    if n == 1:
        a = mensaje[0:len_a]
        c = mensaje[len_a:len_a + len_c]
        b = mensaje[len_a + len_c:len_a + len_c + len_b]
    if n == 0:
        b = mensaje[0:len_b]
        a = mensaje[len_b:len_b + len_a]
        c = mensaje[len_b + len_a:len_b + len_a + len_c]
    return recombinar_mensaje([a, b, c])

def decodificar_mensaje(mensaje: list[bytearray]) -> bytearray:
    mensaje = mensaje.copy()
    longitud = int.from_bytes(mensaje.pop(0), "big")
    decodificado = bytearray()
    bloque = 1
    for index, array in enumerate(mensaje):
        if (index % 2) == 1:
            if longitud >= 36:
                decodificado.extend(array)
                longitud -= 36
            else:
                decodificado.extend(array[0:longitud])
        else:
            if (int.from_bytes(array, "big")) != bloque:
                return False # Mensaje cortado, corrompido, modificado...
            else:
                bloque += 1
    return decodificado





# Versiones comprimidas:
def codificacion_rapida(mensaje: str) -> list[bytearray]:
    return codificar_mensaje(encriptar_mensaje(serializar_mensaje(mensaje)))

def decodificar_rapido(mensaje: list[bytearray]) -> str:
    decodificado = decodificar_mensaje(mensaje)
    if decodificado:
        return deserializar_mensaje(desencriptar_mensaje(decodificado))
    else:
        return "No se pudo decodificar :c"




def recibir_mensaje(sock):
    datos = [sock.recv(4)]
    largo = int.from_bytes(datos[0], byteorder='big')
    for _ in range((largo + 36) // 36): # cantidad de chunks de 36 bytes
        datos.append(sock.recv(4))
        datos.append(sock.recv(36))
    return datos

def mandar_mensaje(codificado: list[bytearray], sock):
    sock.sendall(codificado.pop(0))
    for array in codificado:
        sock.sendall(array)