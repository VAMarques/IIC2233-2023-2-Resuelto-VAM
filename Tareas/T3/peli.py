import api
import requests


class Peliculas:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"

    def saludar(self) -> dict:
        saludo = {}
        getted = requests.get(f"{self.base}/")
        saludo["status-code"] = getted.status_code
        saludo["saludo"] = getted.json()["result"]
        return saludo

    def verificar_informacion(self, pelicula: str) -> bool:
        return pelicula in requests.get(f"{self.base}/peliculas").json()["result"]

    def dar_informacion(self, pelicula: str) -> dict:
        getted = requests.get(f"{self.base}/informacion", params={"pelicula": pelicula})
        informacion = {}
        informacion["status-code"] = getted.status_code
        informacion["mensaje"] = getted.json()["result"]
        return informacion

    def dar_informacion_aleatoria(self) -> dict:
        getted_1 = requests.get(f"{self.base}/aleatorio")
        resultado = {}
        if getted_1.status_code != 200:
            resultado["status-code"] = getted_1.status_code
            resultado["mensaje"] = getted_1.json()["result"]
            return resultado
        nueva_url = getted_1.json()["result"]
        getted_2 = requests.get(nueva_url)
        resultado["status-code"] = getted_2.status_code
        resultado["mensaje"] = getted_2.json()["result"]
        return resultado

    def agregar_informacion(self, pelicula: str, sinopsis: str, access_token: str):
        data = {"pelicula": pelicula, "sinopsis": sinopsis}
        head = {"Authorization": access_token}
        putted = requests.post(f"{self.base}/update", data=data, headers=head)
        if putted.status_code == 401:
            return "Agregar pelicula no autorizado"
        elif putted.status_code == 400:
            return putted.json()["result"]
        else:
            return "La base de la API ha sido actualizada"

    def actualizar_informacion(self, pelicula: str, sinopsis: str, access_token: str):
        data = {"pelicula": pelicula, "sinopsis": sinopsis}
        head = {"Authorization": access_token}
        putted = requests.patch(f"{self.base}/update", data=data, headers=head)
        if putted.status_code == 401:
            return "Editar información no autorizado"
        elif putted.status_code == 200:
            return "La base de la API ha sido actualizada"
        else:
            return putted.json()["result"]

    def eliminar_pelicula(self, pelicula: str, access_token: str):
        data = {"pelicula": pelicula}
        head = {"Authorization": access_token}
        putted = requests.delete(f"{self.base}/remove", data=data, headers=head)
        if putted.status_code == 401:
            return "Eliminar pelicula no autorizado"
        elif putted.status_code == 200:
            return "La base de la API ha sido actualizada"
        else:
            return putted.json()["result"]

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "Mamma Mia": "Mamma Mia es una Comedia musical con ABBA",
        "Monsters Inc": "Monsters Inc trata sobre monstruos que asustan, niños y risas",
        "Incredibles": "Incredibles trata de una familia de superhéroes que salva el mundo",
        "Avengers": "Avengers trata de superhéroes que luchan contra villanos poderosos",
        "Titanic": "Titanic es sobre amor trágico en el hundimiento del Titanic",
        "Akira": "Akira es una película de ciencia ficción japonesa con poderes psíquicos",
        "High School Musical": "High School Musical es un drama musical adolescente en East High",
        "The Princess Diaries": "The Princess Diaries es sobre Mia, una joven que descubre que es" 
        "princesa de Genovia",
        "Iron Man": "Iron Man trata sobre un hombre construye traje de alta tecnología "
        "para salvar al mundo",
        "Tarzan": "Tarzan es sobre un hombre criado por simios en la jungla",
        "The Pianist": "The Pianist es sobre un músico judío que sobrevive en Varsovia"
        " durante el Holocausto",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    Peliculas = Peliculas(HOST, PORT)
    print(Peliculas.saludar())
    print(Peliculas.dar_informacion_aleatoria())
    print(Peliculas.actualizar_informacion("Titanic", "Titanic es sobre amor trágico inspitado"
                                          " en el historico hundimiento del Titanic","tereiic2233"))
    print(Peliculas.verificar_informacion("Tarzan"))
    print(Peliculas.dar_informacion("The Princess Diaries"))
    print(Peliculas.dar_informacion("Monsters Inc"))
    print(Peliculas.agregar_informacion("Matilda", "Matilda es sobre una niña con poderes"
                                     "telequinéticos que enfrenta a su malvada directora", 
                                      "tereiic2233"))
    print(Peliculas.dar_informacion("Matilda"))