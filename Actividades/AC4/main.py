from typing import List
from clases import Tortuga
import pickle


###################
#### ENCRIPTAR ####
###################
def serializar_tortuga(tortuga: Tortuga) -> bytearray:
    try:
        byte_tortuga = pickle.dumps(tortuga)
        digi_tortuga = bytearray(byte_tortuga)
        return digi_tortuga
    except AttributeError as att_err:
        raise ValueError("No se") from att_err


def verificar_rango(mensaje: bytearray, inicio: int, fin: int) -> None:
    if (inicio < 0) or (fin >= len(mensaje)) or (inicio > fin):
        raise AttributeError("Inicio o fin del mensaje invalidos")
    else:
        return None


def codificar_rango(inicio: int, fin: int) -> bytearray:
    inicio_byte = bytearray(inicio.to_bytes(3, "big"))
    fin_byte = bytearray(fin.to_bytes(3, "big"))
    return (inicio_byte + fin_byte)


def codificar_largo(largo: int) -> bytearray:
    largo_byte = bytearray(largo.to_bytes(3, "big"))
    return largo_byte


def separar_msg(mensaje: bytearray, inicio: int, fin: int) -> List[bytearray]:
    m_extraido = bytearray()
    m_con_mascara = bytearray()
    # Completar
    largo = 1 + fin - inicio
    if (largo % 2 == 0):
        m_extraido += mensaje[inicio:fin+1]
    else:
        m_extraido += mensaje[inicio:fin+1][::-1]

    m_con_mascara += mensaje[0:inicio]
    for i in range(largo):
        m_con_mascara += bytearray(i.to_bytes(1, "big"))
    m_con_mascara += mensaje[fin+1:]
    return [m_extraido, m_con_mascara]


def encriptar(mensaje: bytearray, inicio: int, fin: int) -> bytearray:
    # Se la damos listas
    verificar_rango(mensaje, inicio, fin)

    m_extraido, m_con_mascara = separar_msg(mensaje, inicio, fin)
    rango_codificado = codificar_rango(inicio, fin)
    return (
        codificar_largo(fin - inicio + 1)
        + m_extraido
        + m_con_mascara
        + rango_codificado
    )


######################
#### DESENCRIPTAR ####
######################
def deserializar_tortuga(mensaje_codificado: bytearray) -> Tortuga:
    try:
        mensaje = pickle.loads(mensaje_codificado)
        return mensaje
    except ValueError as val_err:
        raise AttributeError("No se") from val_err


def decodificar_largo(mensaje: bytearray) -> int:
    largo = int.from_bytes(mensaje[0:3], byteorder="big")
    return largo


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_extraido = bytearray()
    m_con_mascara = bytearray()
    rango_codificado = bytearray()
    # Completar
    largo = decodificar_largo(mensaje)
    m_extraido += mensaje[3:3 + largo]
    m_con_mascara += mensaje[3 + largo:-6]
    rango_codificado += mensaje[-6:]
    if (largo % 2 == 1):
        m_extraido.reverse()
    return [m_extraido, m_con_mascara, rango_codificado]


def decodificar_rango(rango_codificado: bytearray) -> List[int]:
    inicio = int.from_bytes(rango_codificado[0:3], byteorder="big")
    fin = int.from_bytes(rango_codificado[3:6], byteorder="big")

    return [inicio, fin]


def desencriptar(mensaje: bytearray) -> bytearray:
    m_extraido, m_con_mascara, rango_codificado = separar_msg_encriptado(mensaje)
    inicio, fin = decodificar_rango(rango_codificado)
    m_con_mascara[inicio:fin+1] = m_extraido
    return m_con_mascara



if __name__ == "__main__":
    # Tortuga
    tama = Tortuga("Tama2")
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
    print(tama.celebrar_anivesario())
    print()

    # Encriptar
    original = serializar_tortuga(tama)
    print("Original: ", original)
    encriptado = encriptar(original, 6, 24)
    print("Encriptado: ", encriptado)
    print()

    # Desencriptar
    mensaje =  bytearray(b'\x00\x00\x13roT\x07\x8c\x94sesalc\x06\x8c\x00\x00\x00\x00\x00\x80\x04\x958\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12tuga\x94\x93\x94)\x81\x94}\x94(\x8c\x06nombre\x94\x8c\x05Tama2\x94\x8c\x04edad\x94K\x01ub.\x00\x00\x06\x00\x00\x18')
    desencriptado = desencriptar(mensaje)
    tama = deserializar_tortuga(desencriptado)

    # Tortuga
    print("Tortuga: ", tama)
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
