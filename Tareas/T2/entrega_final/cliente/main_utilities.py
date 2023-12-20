"""
Importa los archivos de assets en un unico diccionario para su facil acceso, Tenia pensado en
hacerlo con una diccionario gigante de join's, pero la idea me parecio ineficiente.

Tambien contiene open_laberinto, su funcion es abrir uno de los archivos tableros usando su path.
"""

from os import listdir
from os.path import join


ASSETS = {}
for carpeta in listdir("assets"):
    for archivo in listdir(join("assets", carpeta)):
        if archivo in ["derrota.wav", "victoria.wav"]: # Solo quiero los mp3, no los wav.
            continue
        ASSETS[archivo.partition(".")[0]] = join("assets", carpeta, archivo)

def open_laberinto(path_laberinto, ancho, largo):
    """"Usando un path, un ancho, y un largo, abre el archivo del laberinto y devuelve una lista
    de listas.
    """
    laberinto = []
    with open(path_laberinto, "r", encoding="ascii") as archivo:
        # Extrae solo una cantidad "ancho" de lineas del archivo
        for _ in range(ancho):
            # Extrae una linea, Quita saltos de linea, Elimina comas extras, Divide por coma
            # Selecciona solo una cantidad "largo" de caracteres
            # Y lo añade al laberinto.
            laberinto.append(archivo.readline().strip("\n").strip(",").split(",")[0:largo])
    # Devuelve una lista de listas de (ancho) filas X (largo) columnas.
    return laberinto