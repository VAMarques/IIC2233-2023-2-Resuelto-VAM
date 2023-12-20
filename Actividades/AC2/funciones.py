from copy import copy
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Generator

from parametros import RUTA_PELICULAS, RUTA_GENEROS
from utilidades import (
    Pelicula, Genero, obtener_unicos, imprimir_peliculas,
    imprimir_generos, imprimir_peliculas_genero
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_peliculas(ruta: str) -> Generator:
    with open(ruta, "r") as archivo:
        data = archivo.readlines()
    for linea in data[1:]:
        id_pelicula, titulo, director, anno, rating = linea.strip("\n").split(",")
        id_pelicula = int(id_pelicula)
        anno = int(anno)
        rating = float(rating)
        linea = Pelicula(id_pelicula, titulo, director, anno, rating)
        yield linea
    


def cargar_generos(ruta: str) -> Generator:
    with open(ruta, "r") as archivo:
        data = archivo.readlines()
    for linea in data[1:]:
        genero, id_pelicula = linea.strip("\n").split(",")
        id_pelicula = int(id_pelicula)
        linea = Genero(genero, id_pelicula)
        yield linea


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_directores(generador_peliculas: Generator) -> set:
    directores = obtener_unicos(map(lambda x: x.director, generador_peliculas))
    return directores



def obtener_str_titulos(generador_peliculas: Generator) -> str:
    peliculas = map(lambda x: x.titulo, generador_peliculas)
    reducido = reduce(lambda peli_1, peli_2: f"{peli_1}, {peli_2}", peliculas, "")
    reducido = reducido[2:]
    return reducido


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None
) -> filter:
    filtrado = filter(lambda x: x == x, generador_peliculas)
    if (director is not None):
        filtrado = filter(lambda x: x.director == director, filtrado)
    if (rating_min is not None):
        filtrado = filter(lambda x: x.rating >= rating_min, filtrado)
    if (rating_max is not None):
        filtrado = filter(lambda x: x.rating <= rating_max, filtrado)
    return filtrado


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None
) -> Generator:
    if (genero is not None):
        filtrado_generos = filter(lambda x: x.genero == genero, generador_generos)
    else:
        filtrado_generos = filter(lambda x: x == x, generador_generos)
    producto = product(generador_peliculas, filtrado_generos)
    filtrado = filter(lambda x: x[0].id_pelicula == x[1].id_pelicula, producto)
    return filtrado


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class DCCMax:
    def __init__(self, peliculas: list) -> None:
        self.peliculas = peliculas

    def __iter__(self):
        return IteradorDCCMax(self.peliculas)


class IteradorDCCMax:
    def __init__(self, iterable_peliculas: list) -> None:
        self.peliculas = copy(iterable_peliculas)
        self.peliculas.sort(reverse=True, key=lambda x: x.rating)
        self.peliculas.sort(reverse=False, key=lambda x: x.estreno)

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        if not self.peliculas:
            raise StopIteration()
        else:
            valor = self.peliculas.pop(0)
            return valor



if __name__ == '__main__':
    print('> Cargar películas:')
    imprimir_peliculas(cargar_peliculas(RUTA_PELICULAS))
    print()

    print('> Cargar géneros')
    imprimir_generos(cargar_generos(RUTA_GENEROS), 5)
    print()

    print('> Obtener directores:')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(list(obtener_directores(generador_peliculas)))
    print()

    print('> Obtener string títulos')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(obtener_str_titulos(generador_peliculas))
    print()

    print('> Filtrar películas (por director):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(
        generador_peliculas, director='Christopher Nolan'
    ))
    print('\n> Filtrar películas (rating min):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_min=9.1))
    print('\n> Filtrar películas (rating max):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_max=8.7))
    print()

    print('> Filtrar películas por género')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    generador_generos = cargar_generos(RUTA_GENEROS)
    imprimir_peliculas_genero(filtrar_peliculas_por_genero(
        generador_peliculas, generador_generos, 'Biography'
    ))
    print()

    print('> DCC Max')
    for (estreno, pelis) in DCCMax(list(cargar_peliculas(RUTA_PELICULAS))):
        print(f'\n{estreno:^80}\n')
        imprimir_peliculas(pelis)
