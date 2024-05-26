# Versión 2. Rellenamos parcialmente el esqueleto con el esquema de las clases que van a actuar como interfaces.

from abc import ABC, abstractmethod


class Subscriptor(ABC):

    @abstractmethod
    def actualizar_estado(self, estado):
        pass
    

class Publicador(ABC):

    @abstractmethod
    def añadir_subscriptor(self, subscriptor: Subscriptor): # Anotaciones que hacen que la variable tenga que ser un objeto e específico, las usaremos para restringir y controlar los errores.
        pass

    @abstractmethod
    def eliminar_subscriptor(self, subscriptor: Subscriptor):
        pass

    @abstractmethod
    def notificar_evento(self):
        pass


# SensorTemperatrura que va a ser un Publicador.

class SensorTemperatura(Publicador):
    pass


class Manejador(ABC):

    def siguiente_manejador(self, manejador):
        pass

    @abstractmethod
    def manejar(self, temperaturas_60, temperaturas_30):
        pass


# Sistema como un Subscriptor.

class Sistema(Subscriptor):
    pass


# Tenemos 3 manejadores.

# SuperaUmbral como Manejador.

class SuperaUmbral(Manejador):
    pass


# CambioDrastico como Manejador.

class CambioDrastico(Manejador):
    pass

    

# Interfaz de Estrategia para el patrón de Strategy.

class Estrategia(ABC):

    @abstractmethod
    def hacer_calculo(self, valores):
        pass


# Estrategia para calcular la Media.

class Media(Estrategia):
    pass

# Estrategia para calcular los Cuantiles.

class Cuantiles(Estrategia):
    pass

# Estrategia para calcular la DesviacionTipica.

class DesviacionTipica(Estrategia):
    pass


# Estrategia para calcular los MaximoMinimo.

class MaximoMinimo(Estrategia):
    pass



# Manejador de Estadisticos.

class Estadisticos(Manejador):

    def __init__(self, estrategia: Estrategia):
        pass

    def manejar(self, temperaturas_60, temperaturas_30):
        pass