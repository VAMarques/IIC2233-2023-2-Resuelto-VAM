def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    return not nombre in usuarios_no_permitidos

def puntajes_altos(puntajes: list):
    """Transforma el archivo de puntajes a un string de los 5 mas altos"""
    puntajes = puntajes.copy()
    data = "PUNTAJES:"
    for index, line in enumerate(puntajes):
        puntajes[index] = line.strip().split(",")
        puntajes[index][2] = float(puntajes[index][2])
    puntajes_altos = sorted(puntajes, key=lambda x: x[2], reverse=True)
    for registro in puntajes_altos[0:5]: # Solo los 5 mas altos
        data += registro[0] + ";" + str(registro[2]) + ","
    return data[0:-1] # Remueve el ultimo coma

def arreglar_registros(leaderboard: list):
    """Arregla el leaderboard si falta un salto de linea"""
    leaderboard = leaderboard.copy()
    arreglar = False
    if leaderboard[-1][-1] != "\n":
        leaderboard[-1] += "\n"
        arreglar = True
    return (arreglar, leaderboard)

def modificar_registro(leaderboard: list, usuario: str, nivel: str, puntos: str):
    leaderboard = arreglar_registros(leaderboard)[1]
    for index, line in enumerate(leaderboard):
        partido = line.strip().split(",")
        if usuario == partido[0]:
            old_puntos = float(partido[2])
            new_puntos = str(round(old_puntos + float(puntos), 2))
            leaderboard[index] = usuario + "," + nivel + "," + new_puntos + "\n"
            break
    else: # No Break
        new_puntos = puntos
        leaderboard.append((usuario + "," + nivel + "," + puntos + "\n"))
    return [new_puntos, leaderboard]

def encontrar_nivel(leaderboard: list, usuario: str):
    leaderboard = leaderboard.copy()
    for line in leaderboard:
        partido = line.strip().split(",")
        if usuario == partido[0]:
            nivel = int(partido[1])
            if nivel < 3:
                return nivel
    return 0


def pretty_print(texto: str):
    mejoradas = "╔══════════════════════════════════════════════════════════════════════════════╗"
    for line in texto.split("\n"):
        mejoradas += ("\n" "║"+ line.ljust(78)+"║")
    mejoradas += "\n"
    mejoradas += "╚══════════════════════════════════════════════════════════════════════════════╝"
    print(mejoradas)

if __name__ == "__main__":
    pretty_print("12345\n" + "Salto de linea\n" + "otro ejemplo mas")
