import api
import requests


class Yolanda:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"
        dupla = "\d{1,2}"
        space = "\s"
        alpha = "[a-zA-Z]"
        fecha_digitos = "(19|20)[0-9]{1,2}"
        fecha_siglos = "[0-9]{1,2}"
        self.regex_validador_fechas = (f"^{dupla}{space}de{space}{alpha}+{space}de{space}" +
                                       f"({fecha_digitos}|{fecha_siglos})$")
        self.regex_extractor_signo = "^(?:Las|Los)\s+(.+([aAoO][sS]))\s+pueden\s+.+\."

    def saludar(self) -> dict:
        saludo = {}
        getted = requests.get(f"{self.base}/")
        saludo["status-code"] = getted.status_code
        saludo["saludo"] = getted.json()["result"]
        return saludo

    def verificar_horoscopo(self, signo: str) -> bool:
        return signo in requests.get(f"{self.base}/signos").json()["result"]

    def dar_horoscopo(self, signo: str) -> dict:
        getted = requests.get(f"{self.base}/horoscopo", params={"signo": signo})
        horoscopo = {}
        horoscopo["status-code"] = getted.status_code
        horoscopo["mensaje"] = getted.json()["result"]
        return horoscopo

    def dar_horoscopo_aleatorio(self) -> dict:
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

    def agregar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        data = {"signo": signo, "mensaje": mensaje}
        head = {"Authorization": access_token}
        putted = requests.post(f"{self.base}/update", data=data, headers=head)
        if putted.status_code == 400:
            return putted.json()["result"]
        elif putted.status_code == 401:
            return "Agregar horóscopo no autorizado"
        else:
            return "La base de YolandAPI ha sido actualizada"


    def actualizar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        data = {"signo": signo, "mensaje": mensaje}
        head = {"Authorization": access_token}
        putted = requests.put(f"{self.base}/update", data=data, headers=head)
        if putted.status_code == 400:
            return putted.json()["result"]
        elif putted.status_code == 401:
            return "Editar horóscopo no autorizado"
        else:
            return "La base de YolandAPI ha sido actualizada"

    def eliminar_signo(self, signo: str, access_token: str) -> str:
        data = {"signo": signo}
        head = {"Authorization": access_token}
        putted = requests.delete(f"{self.base}/remove", data=data, headers=head)
        if putted.status_code == 400:
            return putted.json()["result"]
        elif putted.status_code == 401:
            return "Eliminar signo no autorizado"
        else:
            return "La base de YolandAPI ha sido actualizada"


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "acuario": "Hoy será un hermoso día",
        "leo": "No salgas de casa.... te lo recomiendo",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    yolanda = Yolanda(HOST, PORT)
    # print(yolanda.saludar())
    # print(yolanda.dar_horoscopo_aleatorio())
    # print(yolanda.verificar_horoscopo("acuario"))
    # print(yolanda.verificar_horoscopo("pokemon"))
    # print(yolanda.dar_horoscopo("acuario"))
    # print(yolanda.dar_horoscopo("pokemon"))
    print(yolanda.agregar_horoscopo("a", "aaaaa", "pepaiic2233"))
    # print(yolanda.dar_horoscopo("a"))
