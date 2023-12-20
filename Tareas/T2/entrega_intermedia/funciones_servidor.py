def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    return not nombre in usuarios_no_permitidos


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
