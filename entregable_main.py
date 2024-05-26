# Versión 4. Especificamos que queremos que haga cada método de las clases y les atribuimos roles descriptivos junto con el método innit de las que lo necesitan.
# Tag 1: importnate especificaciones del esquema más concretas, la implementación coge la idea que pretendemos seguir y sólo queda meter el código dentro.

from abc import ABC, abstractmethod
from generar_datos import generador_datos # Tenemos en cuenta el formato de tupla en el que vienen los datos.

# Interfaces de Subscriptor y Publicador para el patrón Observer.
# Heredan de abstract methods para que no se puedan llamar directamente.

class Subscriptor(ABC):
    """
    Interfaz que declara el método abstracto actualizar para el sujeto. 
    """

    @abstractmethod
    def actualizar_estado(self, estado):
        """ 
        Recibe una actualización del sujeto. 

        Parámetros:
        - estado: tuple
        """
        pass
    

class Publicador(ABC):
    """
    Interfaz que declara un métodos abstractos para gestionar los observadores (subscriptores a las publicaciones).
    """

    @abstractmethod
    def añadir_subscriptor(self, subscriptor: Subscriptor):
        """ 
        Añade un subscriptor de un publicador. 

        Parámetros:
        - subscriptor: Instancia de la clase Subscriptor.
        """
        pass

    @abstractmethod
    def eliminar_subscriptor(self, subscriptor: Subscriptor):
        """ 
        Elimina un subscriptor de un publicador. 

        Parámetros:
        - subscriptor: Instancia de la clase Subscriptor.
        """
        pass

    @abstractmethod
    def notificar_evento(self):
        """ 
        Notifica a los subscriptores de un cambio o acontecimiento. 
        """
        pass


# SensorTemperatrura que va a ser un Publicador.

class SensorTemperatura(Publicador):
    # Definimos estas dos variables como protegidas, es decir, no son accesibles fuera de la clase si no es a través de getters o setters.
    _estado = None # Inicializamos la tupla del estado como None porque aún no lo hemos recibido.
    _lista_subscriptores: list[Subscriptor] = [] # La lista está formada por instancioas de Subscriptor.

    # Métodos heredados de Publicador relacionados con los subscriptores.
    # Su especificación va dada por los métodos de la clase de la que los heredan.
    def añadir_subscriptor(self, subscriptor: Subscriptor):
        pass

    def eliminar_subscriptor(self, subscriptor: Subscriptor):
        pass

    def notificar_evento(self, estado):
        pass
    
    # Métodos propios de SensorTemperatura.
    def modificar_estado(self, estado):
        """
        Modifica el estado.

        Parámetros:
        - estado: tuple
        """
        pass

    def iniciar_sensor(self, tiempo):
        """
        Pone en marcha el sensor.

        Parámetros:
        - tiempo: int
        """
        pass


#  Interfaz de Manejador para el patrón Chain of Responsibility.

class Manejador(ABC):
    """
    Interfaz que declara métodos para manejadores que utilizarán el sistema gestor de datos con cada notificación.
    """

    def siguiente_manejador(self, manejador):
        """
        Método que permite establecer el siguiente manejador en la cadena.

        Parámetros:
        - manejador: Instancia de la clase Manejador.
        """
        pass

    @abstractmethod
    def manejar(self, temperaturas_60, temperaturas_30):
        """
        Maneja las temperaturas registradas.
        Debe ser implementado por cada manejador concreto para realizar alguna acción basada en los datos de temperatura.
        Si el manejador actual no puede manejar la solicitud, pasa la responsabilidad al siguiente manejador en la cadena.

        Parámetros:
        - temperaturas_60: list
        - temperaturas_30: list
        """
        pass


# Sistema como un Subscriptor y además un patrón de Singleton en él mismo porque sólo puede haber una instancia.

class Sistema(Subscriptor):
    _instancia_sistema = None

    def __init__(self):
        self._nombre = "SuperSistema" # Super nombre!!!!
        self._temperaturas = []
        self._temperaturas_30 = []
        self._temperaturas_60 = []
        self._manejador = None # Inicializamos la cadena de manejadores como None para atribuirle valores más tarde.

    def __str__(self): # Para que cuando se subscriba al sensor aparezca su nombre.
        pass
    
    @classmethod # Método de clase del esquema Singleton para generar una única instancia si no existe ya.
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
    
# Antes de definir el Manejador de estadísticos, debemos implementar cada una de sus estrategias utilizando programación funcional.

# Interfaz de Estrategia para el patrón de Strategy.

class Estrategia(ABC):
    """
    Interfaz que declara un método para realizar el cálculo pedido.
    """

    @abstractmethod
    def hacer_calculo(self, valores):
        pass


# Estrategia para calcular la Media.

class Media(Estrategia):
    """
    Calcula la media.
    """

    def hacer_calculo(self, valores):
        pass


# Estrategia para calcular los Cuantiles.

class Cuantiles(Estrategia):
    """
    Calcula los cuantiles.
    """
    
    def hacer_calculo(self, valores):
        pass


# Estrategia para calcular la DesviacionTipica.

class DesviacionTipica(Estrategia):
    """
    Calcula la desviación típica.
    """
    
    def calculo(self, valores): # Programación funcional para hallar la desviación típica.
        pass
    
    def hacer_calculo(self, valores: list):
        pass


# Estrategia para calcular los MaximoMinimo.

class MaximoMinimo(Estrategia):
    """
    Calcula los máximos y los mínimos.
    """
    
    def hacer_calculo(self, valores):
        pass



# Manejador de Estadisticos.

class Estadisticos(Manejador):
    def __init__(self, estrategia: Estrategia):
        self._estrategia = estrategia

    def manejar(self, temperaturas_60, temperaturas_30):
        pass