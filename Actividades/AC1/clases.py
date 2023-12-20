from abc import ABC, abstractmethod
import random

class Vehiculo(ABC):

    identificador = 0

    def __init__(self, rendimiento, marca, energia = 120, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rendimiento = int(rendimiento)
        self.marca = str(marca)
        self._energia = int(energia)
        self.identificador = Vehiculo.identificador
        Vehiculo.identificador += 1
        
    @abstractmethod
    def recorrer(self, kilometros) -> None:
        pass
    
    @property
    def autonomia(self) -> float:
        return self._energia * self.rendimiento

    @property
    def energia(self) -> int:
        return self._energia
    
    @energia.setter
    def energia(self, nueva_energia) -> None:
        if (nueva_energia >= 0):
            self._energia = nueva_energia
        else:
            self._energia = 0
        

class AutoBencina(Vehiculo):
    
    def __init__(self, bencina_favorita, *args, **kwargs) -> None:
        self.bencina_favorita = bencina_favorita
        super().__init__(*args, **kwargs)
    
    # Problema entre floats y ints
    # si algo no funciona remover la division entera presente aca.
    def recorrer(self, kilometros) -> str:
        if (self.autonomia > kilometros):
            gasto = kilometros // self.rendimiento
            self.energia -= gasto
            return f"Anduve por {kilometros}Km y gasté {gasto}L de bencina"
        else:
            kilometros_maximos = self.autonomia
            gasto = self.energia
            self.energia = 0
            return f"Anduve por {kilometros_maximos}Km y gasté {gasto}L de bencina"


class AutoElectrico(Vehiculo):

    def __init__(self, vida_util_bateria, *args, **kwargs) -> None:
        self.vida_util_bateria = vida_util_bateria
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros) -> str:
        if (self.autonomia > kilometros):
            gasto = kilometros // self.rendimiento
            self.energia -= gasto
            return f"Anduve por {kilometros}Km y gasté {gasto}W de energía eléctrica"
        else:
            kilometros_maximos = self.autonomia
            gasto = self.energia
            self.energia = 0
            return f"Anduve por {kilometros_maximos}Km y gasté {gasto}W de energía eléctrica"


class Camioneta(AutoBencina):

    def __init__(self, capacidad_maleta, *args, **kwargs) -> None:
        self.capacidad_maleta = capacidad_maleta
        super().__init__(*args, **kwargs)


class Telsa(AutoElectrico):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros) -> str:
        return AutoElectrico.recorrer(kilometros)+"de forma inteligente"


class FaitHibrido(AutoBencina, AutoElectrico):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(vida_util_bateria = 5, *args, **kwargs)
    
    def recorrer(self, kilometros) -> str:
        if (self.autonomia > kilometros):
            recorrido_bencina = AutoBencina.recorrer(self, kilometros/2)
            recorrido_electrico = AutoElectrico.recorrer(self, kilometros/2)
            return recorrido_bencina + recorrido_electrico
        else:
            kilometros = self.autonomia
            recorrido_bencina = AutoBencina.recorrer(self, kilometros/2)
            recorrido_electrico = AutoElectrico.recorrer(self, kilometros/2)
            return recorrido_bencina + recorrido_electrico