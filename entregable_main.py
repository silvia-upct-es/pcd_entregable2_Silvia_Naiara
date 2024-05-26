# Versión 1. Esqueleto muy esquelético para empezar.

from abc import ABC


class Subscriptor(ABC):
    pass
    

class Publicador(ABC):
    pass


# SensorTemperatrura que va a ser un Publicador.

class SensorTemperatura(Publicador):
    pass


class Manejador(ABC):
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
    pass