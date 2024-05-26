# Versión 3. Añadimos los métodos heredados y los nuevos métodos que necesitaremos implementar en cada clase.

from abc import ABC, abstractmethod


class Subscriptor(ABC):

    @abstractmethod
    def actualizar_estado(self, estado):
        pass
    

class Publicador(ABC):

    @abstractmethod
    def añadir_subscriptor(self, subscriptor: Subscriptor):
        pass

    @abstractmethod
    def eliminar_subscriptor(self, subscriptor: Subscriptor):
        pass

    @abstractmethod
    def notificar_evento(self):
        pass


# SensorTemperatrura que va a ser un Publicador.

class SensorTemperatura(Publicador):

    # Métodos heredados de Publicador relacionados con los subscriptores.
    def añadir_subscriptor(self, subscriptor: Subscriptor):
        pass

    def eliminar_subscriptor(self, subscriptor: Subscriptor):
        pass

    def notificar_evento(self, estado):
        pass
    
    # Métodos propios de SensorTemperatura.
    def modificar_estado(self, estado):
        pass

    def iniciar_sensor(self, tiempo):
        pass


class Manejador(ABC):
    def siguiente_manejador(self, manejador):
        pass

    @abstractmethod
    def manejar(self, temperaturas_60, temperaturas_30):
        pass


# Sistema como un Subscriptor y además un patrón de Singleton en él mismo porque sólo puede haber una instancia.

class Sistema(Subscriptor):
    def __init__(self):
        pass

    def __str__(self):
        pass
    
    @classmethod 
    def obtener_instancia(cls):
        pass

    def actualizar_estado(self, estado):
        pass


# Tenemos 3 manejadores.
# Todos los manejadores concretos manejan una solicitud o la pasan al siguiente manejador en la cadena.

# SuperaUmbral como Manejador.

class SuperaUmbral(Manejador):
    def manejar(self, temperaturas_60, temperaturas_30):
        pass


# CambioDrastico como Manejador.

class CambioDrastico(Manejador):
    def cambio_drastico(self, valores, umbral):
        pass
    
    def manejar(self, temperaturas_60, temperaturas_30):
        pass

    

# Interfaz de Estrategia para el patrón de Strategy.

class Estrategia(ABC):

    @abstractmethod
    def hacer_calculo(self, valores):
        pass


# Estrategia para calcular la Media.

class Media(Estrategia):

    def hacer_calculo(self, valores):
        pass

# Estrategia para calcular los Cuantiles.

class Cuantiles(Estrategia):
    
    def hacer_calculo(self, valores):
        pass

# Estrategia para calcular la DesviacionTipica.

class DesviacionTipica(Estrategia):
    
    def calculo(self, valores):
        pass
    
    def hacer_calculo(self, valores: list):
        pass


# Estrategia para calcular los MaximoMinimo.

class MaximoMinimo(Estrategia):
    
    def hacer_calculo(self, valores):
        pass



# Manejador de Estadisticos.

class Estadisticos(Manejador):
    def __init__(self, estrategia: Estrategia):
        pass

    def manejar(self, temperaturas_60, temperaturas_30):
        pass