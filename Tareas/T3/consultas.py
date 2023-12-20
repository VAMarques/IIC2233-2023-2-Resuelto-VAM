
import collections
import datetime
from functools import reduce
import itertools
import math
import utilidades

from typing import Generator


def peliculas_genero(generador_peliculas: Generator, genero: str):
    return (filter(lambda x: x.genero == genero, generador_peliculas))

def personas_mayores(generador_personas: Generator, edad: int):
    return (filter(lambda x: x.edad >= edad, generador_personas))

def funciones_fecha(generador_funciones: Generator, fecha: str):
    fecha_limpia = fecha[:-4] + fecha[-2:]
    return (filter(lambda x: x.fecha == fecha_limpia, generador_funciones))

def titulo_mas_largo(generador_peliculas: Generator) -> str:
    def comparar_titulo(titulo_1, titulo_2):
        # Casos len distinto
        len_1 = len(titulo_1.titulo)
        len_2 = len(titulo_2.titulo)
        if len_1 > len_2:
            return titulo_1
        if len_1 < len_2:
            return titulo_2
        # Casos mismo len, distinto rate
        rate_1 = titulo_1.rating
        rate_2 = titulo_2.rating
        if rate_1 > rate_2:
            return titulo_1
        if rate_1 < rate_2:
            return titulo_2
        # Mismo rate, mismo len, sobrevive la de mayor posicion.
        return titulo_2
    return reduce(comparar_titulo, generador_peliculas).titulo

def normalizar_fechas(generador_funciones: Generator):
    def transformar_fecha(funcion):
        # Extraer los atributos de la funcion de la pelicula
        # Son funciones en sentido cinematografico, no en el sentido matematico o computacional.
        id_funcion = funcion.id
        numero_sala = funcion.numero_sala
        id_pelicula = funcion.id_pelicula
        horario = funcion.horario
        fecha = funcion.fecha

        # Rearmar la fecha
        anno = fecha[-2:]
        mes = fecha[3:5]
        dia = fecha[0:2]

        siglo = ("20" if int(anno) < 24 else "19")
        nueva_fecha = f"{siglo}{anno}-{mes}-{dia}"

        # Hacer return rearmando la funcion con sus atributos
        return utilidades.Funciones(id_funcion, numero_sala, id_pelicula, horario, nueva_fecha)
    return map(transformar_fecha, generador_funciones)


def personas_reservas(generador_reservas: Generator):
    # En vez de usar set(), me acorde que los sets pueden hacerse por comprension.
    return {x.id_persona for x in generador_reservas}

def peliculas_en_base_al_rating(generador_peliculas: Generator, genero: str, rating_min: int, rating_max: int):
    return filter(
        lambda x: (x.genero == genero) and (rating_min <= x.rating <= rating_max),
        generador_peliculas)

def mejores_peliculas(generador_peliculas: Generator):
    # El peor metodo posible para hacer esto, yo hice algo mucho mas elegante con sorted, que mas
    # aun, es lo que de verdad harias si estuvieramos haciendo programacion funcional de verdad,
    # pero ustedes lo prohibieron, pero dejaron permitido el resto de estas cosas.
    ordenado = [x for x in generador_peliculas]
    ordenado.sort(key=lambda x: x.id)
    ordenado.sort(key=lambda x: x.rating, reverse=True)
    return (x for x in ordenado[0:20])

def pelicula_genero_mayor_rating(generador_peliculas: Generator, genero: str) -> str:
    def comparar_rating(titulo_1, titulo_2):
        # Casos mismo len, distinto rate
        if not titulo_1: # el string vacio inicial
            return titulo_2
        rate_1 = titulo_1.rating
        rate_2 = titulo_2.rating
        if rate_1 > rate_2:
            return titulo_1
        if rate_1 < rate_2:
            return titulo_2
        # Mismo rate, mismo len, sobrevive la de menor posicion.
        return titulo_1
    mismo_genero = peliculas_genero(generador_peliculas, genero)
    resultado = reduce(comparar_rating, mismo_genero, "")
    if not resultado:
        return ""
    return resultado.titulo

def fechas_funciones_pelicula(generador_peliculas: Generator, generador_funciones: Generator, titulo: str):
    # Absurdamente obscurado, en el caso de no estar el titulo quedara "", y en ese caso al hacer
    # filter sera un generador vacio, podria haberse hecho haciendo return (), pero las tuplas
    # estan prohibidas.
    pelicula = reduce(lambda x, y: y.id if y.titulo == titulo else x, generador_peliculas, "")
    funciones = filter(lambda x: x.id_pelicula == pelicula, generador_funciones)
    return map(lambda x: x.fecha, funciones)


def genero_mas_transmitido(generador_peliculas: Generator, generador_funciones: Generator, fecha: str) -> str:
    nueva_fecha = fecha[0:6] + fecha[8:]
    funciones_filtradas = filter(lambda x: x.fecha == nueva_fecha, generador_funciones)
    dict_pelis = {x.id: x.genero for x in generador_peliculas}
    transformado = map(lambda x: dict_pelis[x.id_pelicula], funciones_filtradas)

    # Counter ya soporta iterables, no es necesario hacer nada por comprension.
    # Aun asi hare x for x in por precausion, pues tambien uno haria list(generador)
    genero_count = collections.Counter(x for x in transformado)
    if genero_count:
        return max(genero_count, key=lambda x: genero_count[x])
    return ""

def id_funciones_genero(generador_peliculas: Generator, generador_funciones: Generator, genero: str):
    genero_filtrado = filter(lambda x: x.genero == genero, generador_peliculas)
    transformado_peliculas = {x.id: x.genero for x in genero_filtrado}
    transformado_funciones = filter(
        lambda x: transformado_peliculas.get(x.id_pelicula), generador_funciones
    )
    return map(lambda x: x.id, transformado_funciones)


def butacas_por_funcion(generador_reservas: Generator, generador_funciones: Generator, id_funcion: int) -> int:
    funcion = reduce(lambda x, y: y if y.id == id_funcion else x, generador_funciones, "")
    reservas = filter(lambda x: x.id_funcion == funcion.id, generador_reservas)
    return reduce(lambda x, y: x+1, reservas, 0)

def salas_de_pelicula(generador_peliculas: Generator, generador_funciones: Generator, nombre_pelicula: str):
    pelicula = reduce(
        lambda x, y: y.id if y.titulo == nombre_pelicula else x, generador_peliculas, ""
    )
    funciones_validas = filter(lambda x: x.id_pelicula == pelicula, generador_funciones)
    return map(lambda x: x.numero_sala, funciones_validas)

def nombres_butacas_altas(generador_personas: Generator, generador_peliculas: Generator, generador_reservas: Generator,
                          generador_funciones: Generator, titulo: str, horario: int):
    pelicula = reduce(lambda x, y: y if y.titulo == titulo else x, generador_peliculas, "")
    funciones_filtradas = filter(
        lambda x: (x.id_pelicula == pelicula.id) and (x.horario == horario),
        generador_funciones
    )
    ids_funciones = [x for x in map(lambda x: x.id, funciones_filtradas)]
    reservas = filter(lambda x: x.id_funcion in ids_funciones, generador_reservas)
    ids_personas = [x.id_persona for x in reservas]
    personas = filter(lambda x: x.id in ids_personas, generador_personas)
    return {x.nombre for x in personas}

def nombres_persona_genero_mayores(generador_personas: Generator, generador_peliculas: Generator,
                                   generador_reservas: Generator, generador_funciones: Generator, nombre_pelicula: str,
                                   genero: str, edad: int):
    pelicula = reduce(
        lambda x, y: y if y.titulo == nombre_pelicula else x, generador_peliculas, ""
    )
    funciones_filtradas = filter(lambda x: (x.id_pelicula == pelicula.id), generador_funciones)
    ids_funciones = [x for x in map(lambda x: x.id, funciones_filtradas)]
    reservas = filter(lambda x: x.id_funcion in ids_funciones, generador_reservas)
    ids_personas = [x.id_persona for x in reservas]
    personas = filter(
        lambda x: (x.id in ids_personas) and (x.genero == genero) and (x.edad >= edad),
        generador_personas
    )
    return {x.nombre for x in personas}

def genero_comun(generador_personas: Generator, generador_peliculas: Generator, generador_reservas: Generator,
                 generador_funciones: Generator, id_funcion: int) -> str:
    funcion = reduce(
        lambda x, y: y if y.id == id_funcion else x, generador_funciones, ""
    )
    pelicula = reduce(
        lambda x, y: y if y.id == funcion.id_pelicula else x, generador_peliculas, ""
    )
    titulo = pelicula.titulo
    reservas = filter(lambda x: x.id_funcion == funcion.id, generador_reservas)
    ids_personas = [x.id_persona for x in reservas]
    personas = filter(lambda x: x.id in ids_personas, generador_personas)
    generos = (collections.Counter(x for x in map(lambda x: x.genero, personas)))
    genero_1 = max(generos, key=lambda x: generos[x])
    genero_2 = max(generos, key=lambda x: generos[x] if x is not genero_1 else 0)
    counts_1 = generos[genero_1]
    counts_2 = generos[genero_2]
    todos_igual = all(map(lambda x: generos[x] == counts_1, generos))

    inicio = f"En la función {id_funcion} de la película {titulo} "
    if genero_1 == genero_2 or (counts_1 > counts_2):
        fin = f"la mayor parte del público es {genero_1}."
    elif todos_igual:
        fin = "se obtiene que la cantidad de personas es igual para todos los géneros."
    else: # (counts_1 == counts_2)
        fin = (f"se obtiene que la mayor parte del público es de {genero_1} y {genero_2} " +
               "con la misma cantidad de personas.")
    return inicio + fin

def edad_promedio(generador_personas: Generator, generador_peliculas: Generator, generador_reservas: Generator,
                  generador_funciones: Generator, id_funcion: int) -> str:
    funcion = reduce(
        lambda x, y: y if y.id == id_funcion else x, generador_funciones, ""
    )
    if not funcion:
        return ""
    pelicula = reduce(
        lambda x, y: y if y.id == funcion.id_pelicula else x, generador_peliculas, ""
    )
    titulo = pelicula.titulo
    reservas = filter(lambda x: x.id_funcion == funcion.id, generador_reservas)
    ids_personas = [x.id_persona for x in reservas]
    personas = [x for x in filter(lambda x: x.id in ids_personas, generador_personas)]
    edades = map(lambda x: x.edad, personas)
    promedio = math.ceil(sum(edades)/len(personas))
    return (f"En la función {id_funcion} de la película {titulo} " +
            f"la edad promedio del público es {promedio}.")

def obtener_horarios_disponibles(generador_peliculas: Generator, generador_reservas: Generator,
                                 generador_funciones: Generator, fecha_funcion: str, reservas_maximas: int):
    funciones_filtradas = filter(lambda x: x.fecha == fecha_funcion, generador_funciones)
    funciones_guardado = [x for x in funciones_filtradas]
    ids_peliculas = {x.id_pelicula for x in funciones_guardado}
    mejor_pelicula = max(
        filter(lambda x: x.id in ids_peliculas, generador_peliculas),
        key=lambda x: x.rating
    )
    funciones_max = filter(
        lambda x: (x.id_pelicula == mejor_pelicula.id),
        funciones_guardado)
    dict_funciones = {x.id: x.horario for x in funciones_max}
    reservas = filter(lambda x: x.id_funcion in dict_funciones, generador_reservas)
    funcion_count = collections.Counter({x: 0 for x in dict_funciones})
    funcion_count.update((x.id_funcion for x in reservas))
    funcion_disponible = filter(lambda x: funcion_count[x] < reservas_maximas, funcion_count)
    horario_disponible = map(lambda x: dict_funciones[x], funcion_disponible)

    return {x for x in horario_disponible}

def personas_no_asisten(generador_personas: Generator, generador_reservas: Generator,
                        generador_funciones: Generator, fecha_inicio: str, fecha_termino: str):
    def fecha_transformada(fecha):
        return datetime.date(int(fecha[6:]), int(fecha[3:5]), int(fecha[0:2]))
    def fecha_funcion(fecha):
        anno = int(fecha[6:])
        siglo = (2000 if anno < 24 else 1900)
        return datetime.date(siglo + anno, int(fecha[3:5]), int(fecha[0:2]))
    fecha_inicio = fecha_transformada(fecha_inicio)
    fecha_termino = fecha_transformada(fecha_termino)
    filtro_funciones = filter(
        lambda x: fecha_inicio <= fecha_funcion(x.fecha) <= fecha_termino,
        generador_funciones
    )
    ids_funciones = {x.id for x in filtro_funciones}
    reservas_en_rango = filter(lambda x: x.id_funcion in ids_funciones, generador_reservas)
    ids_personas_con_reserva = {x.id_persona for x in reservas_en_rango}
    personas_sin_reserva = filter(
        lambda x: x.id not in ids_personas_con_reserva, generador_personas
    )

    return personas_sin_reserva