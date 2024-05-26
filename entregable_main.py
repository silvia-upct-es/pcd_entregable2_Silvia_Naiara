# Versión 7. Código añadiendo control de errores con try, except, raise.
# Tag 2: importante adicion de control de errores.

from abc import ABC, abstractmethod
import time
from generar_datos import generador_datos
from functools import reduce, partial
import numpy as np



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
    def añadir_subscriptor(self, subscriptor: Subscriptor):
        self._lista_subscriptores.append(subscriptor)
        print(f"{subscriptor} subscrito al sensor de temperatura.")

    def eliminar_subscriptor(self, subscriptor: Subscriptor):
        if subscriptor in self._lista_subscriptores:
            self._lista_subscriptores.remove(subscriptor)
            print(f"{subscriptor} desubscrito del sensor de temperatura.")
        else:
            raise ValueError(f"Error: {subscriptor} no estaba suscrito.")

    def notificar_evento(self, estado):
        print("Notificando a los subscriptores...")
        for subscriptor in self._lista_subscriptores:
            subscriptor.actualizar_estado(estado)
    
    # Métodos propios de SensorTemperatura.
    def modificar_estado(self, estado):
        """
        Modifica el estado.

        Parámetros:
        - estado: tuple
        """
        print("\n¡La temperatura ha cambiado!")
        self._estado = estado
        self.notificar_evento(estado)

    def iniciar_sensor(self, tiempo):
        """
        Pone en marcha el sensor.

        Parámetros:
        - tiempo: int
        """
        print("\nTomando datos...")
        final = time.time() + tiempo # Calcula el tiempo final de la toma de datos.
        while final > time.time(): # Mientras el tiempo actual sea menor que el tiempo final...
            dato = generador_datos()
            self.modificar_estado(dato)
            time.sleep(5)
            print("\n") # Esperamos 5 segundos antes de tomar el siguiente dato.


#  Interfaz de Manejador para el patrón Chain of Responsibility.

class Manejador(ABC):
    """
    Interfaz que declara métodos para manejadores que utilizarán el sistema gestor de datos con cada notificación.
    """
    _siguiente_manejador = None

    def siguiente_manejador(self, manejador):
        """
        Método que permite establecer el siguiente manejador en la cadena.

        Parámetros:
        - manejador: Instancia de la clase Manejador.
        """
        self._siguiente_manejador = manejador
        return manejador

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
        if self._siguiente_manejador:
            return self._siguiente_manejador.manejar(temperaturas_60, temperaturas_30)
        return None


# Sistema como un Subscriptor y además un patrón de Singleton en él mismo porque sólo puede haber una instancia.

class Sistema(Subscriptor):
    _instancia_sistema = None

    def __init__(self):
        self._nombre = "SuperSistema"
        self._temperaturas = []
        self._temperaturas_30 = []
        self._temperaturas_60 = []
        self._manejador = None # Inicializamos la cadena de manejadores como None para atribuirle valores más tarde.

    def __str__(self): # Para que cuando se subscriba al sensor aparezca su nombre.
        return self._nombre 
    
    @classmethod # Método de clase del esquema Singleton para generar una única instancia si no existe ya.
    def obtener_instancia(cls):
        if not cls._instancia_sistema:
            cls._instancia_sistema = cls()
        return cls._instancia_sistema

    @property
    def manejador(self):
        return self._manejador

    @manejador.setter # Pasar una cadena de manejadores al gestor antes de inicializar el sensor.
    def manejador(self, manejador: Manejador):
        self._manejador = manejador

    def actualizar_estado(self, estado):
        # Añadimos las temperaturas (el primer elemento de la tupla de estado) a las listas correspondientes.
        _temperatura = estado[1]
        _fecha = estado[0]
        self._temperaturas.append(_temperatura)
        self._temperaturas_60.append(_temperatura)
        self._temperaturas_30.append(_temperatura)

        # Como cada 5 segundos se recoge un valor, en 30 segundos se deberían recoger 6 valores y en 60 segundos 12 valores.
        if len(self._temperaturas_60) > 6: # Verifica si se han registrado más de 6 temperaturas (más de 30 segundos de datos).
            # Actualiza la lista de temperaturas de los últimos 30 segundos con las últimas 6 temperaturas.
            self._temperaturas_30 = self._temperaturas_60[-6:]

        if len(self._temperaturas_60) > 12: # Verifica si se han registrado más de 12 temperaturas (más de 60 segundos de datos).
            # Actualiza la lista de temperaturas de los últimos 60 segundos con las últimas 12 temperaturas.
            self._temperaturas_60 = self._temperaturas_60[-12:]
        
        print(f"El sensor marca {_temperatura}º a las {_fecha}.")
        print(f"Temperaturas hasta ahora: {self._temperaturas}")
        print(f"Temperaturas en los últimos 30 segundos: {self._temperaturas_30}")
        print(f"Temperaturas en los últimos 60 segundos: {self._temperaturas_60}")

        # Pasamos las listas de temperaturas al primer manejador de la cadena para que realice la acción correspondiente o pase la responsabilidad al siguiente.
        self._manejador.manejar(self._temperaturas_60, self._temperaturas_30)


# Tenemos 3 manejadores.
# Todos los manejadores concretos manejan una solicitud o la pasan al siguiente manejador en la cadena.

# SuperaUmbral como Manejador.

class SuperaUmbral(Manejador):
    def manejar(self, temperaturas_60, temperaturas_30):
        try:
            umbral = 15
            resultado = temperaturas_60[-1] > umbral 
            if resultado:
                print(f"La temperatura {temperaturas_60[-1]}º excede del umbral de {umbral}º")
            else:
                print(f"La temperatura {temperaturas_60[-1]}º no excede del umbral de {umbral}º.")

            # Pasamos las listas de temperaturas al siguiente manejador en la cadena para que continúe.
            return super().manejar(temperaturas_60, temperaturas_30)
        
        except IndexError:
            raise IndexError("Error: no hay suficientes datos para procesar.")


# CambioDrastico como Manejador.

class CambioDrastico(Manejador):
    def cambio_drastico(self, valores, umbral):
        diferencia = max(valores) - min(valores)
        return diferencia > umbral
    
    def manejar(self, temperaturas_60, temperaturas_30):
        try:
            resultado = self.cambio_drastico(temperaturas_30, 15)
            if resultado:
                print(f"¡Cambio drástico! \nEn los últimos 30 segundos la temperatura ha aumentado en más de 15º")
            else:
                print(f"No ha habido cambios drásticos registrados en los últimos 30 segundos.")

            # Pasamos las listas de temperaturas al siguiente manejador en la cadena para que continúe.            
            return super().manejar(temperaturas_60, temperaturas_30)

        except ValueError:
            raise ValueError("Error: no se pueden calcular los cambios drásticos.")

    
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
        try:
            suma = reduce(lambda x, y : x + y, valores)
            return round(suma / len(valores), 2)
        
        except ZeroDivisionError:
            raise ValueError("Error: no se pueden calcular la media de una lista vacía.")


# Estrategia para calcular los Cuantiles.

class Cuantiles(Estrategia):
    """
    Calcula los cuantiles.
    """
    
    def hacer_calculo(self, valores):
        try:
            if not valores:
                raise ValueError("Error: no se pueden calcular los cuantiles de una lista vacía.")
            calcular_percentiles = partial(np.percentile, q=[25, 50, 75])
            percentiles = calcular_percentiles(valores)
            return dict(zip(["25%", "50%", "75%"], map(lambda x: round(x, 2), percentiles)))
        
        except ValueError as e:
            raise ValueError("Error: no se pueden calcular los cuantiles.")


# Estrategia para calcular la DesviacionTipica.

class DesviacionTipica(Estrategia):
    """
    Calcula la desviación típica.
    """
    
    def calculo(self, valores): # Programación funcional para hallar la desviación típica.
        valor_medio = Media().hacer_calculo(valores)
        def f(n):
            return (n - valor_medio) ** 2
        return f
    
    def hacer_calculo(self, valores: list):
        if not valores:
            raise ValueError("Error: no se puede calcular la desviación típica de una lista vacía.")
        
        try:
            elementos_cuadrado = list(map(self.calculo(valores), valores))
            result = Media().hacer_calculo(elementos_cuadrado) ** (1 / 2)
            return result
        
        except (TypeError, ZeroDivisionError):
            raise ValueError("Error: no se pueden calcular la desviación típica de una lista con elementos no numéricos.")


# Estrategia para calcular los MaximoMinimo.

class MaximoMinimo(Estrategia):
    """
    Calcula los máximos y los mínimos.
    """
    
    def hacer_calculo(self, valores):
        if not valores:
            raise ValueError("Error: no se pueden calcular el máximo y el mínimo de una lista vacía.")
        
        try:
            maximo = max(valores)
            minimo = min(valores)
            return {"max": maximo, "min": minimo}
        
        except ValueError:
            raise ValueError("Error: no se pueden calcular el máximo y el mínimo de una lista con elementos no numéricos.")



# Manejador de Estadisticos.

class Estadisticos(Manejador):
    def __init__(self, estrategia: Estrategia):
        self._estrategia = estrategia

    @property
    def estrategia(self):
        return self._estrategia

    @estrategia.setter
    def estrategia(self, estrategia: Estrategia):
        self._estrategia = estrategia 

    def manejar(self, temperaturas_60, temperaturas_30):
        resultado = self._estrategia.hacer_calculo(temperaturas_60)
        if isinstance(self._estrategia, Media):
            print(f"Cálculo de la media: {resultado}º")
        elif isinstance(self._estrategia, Cuantiles):
            print(f"Cuantiles: {resultado}")
        elif isinstance(self._estrategia, DesviacionTipica):
            print(f"Cálculo de la desviación típica: {resultado}")
        elif isinstance(self._estrategia, MaximoMinimo):
            print(f"Máximo: {resultado['max']}º, Mínimo: {resultado['min']}º")

        # Pasamos las listas de temperaturas al siguiente manejador en la cadena para que continúe.
        return super().manejar(temperaturas_60, temperaturas_30)





# Código de prueba.

if __name__=="__main__":
    sensor = SensorTemperatura()
    sistema = Sistema.obtener_instancia()
    sensor.añadir_subscriptor(sistema)

    # Creamos los manejadores.
    supera_umbral = SuperaUmbral()
    cambio_drastico = CambioDrastico()
    estadisticos_media = Estadisticos(Media())
    estadisticos_cuantiles = Estadisticos(Cuantiles())
    estadisticos_desviacion = Estadisticos(DesviacionTipica())
    estadisticos_max_min = Estadisticos(MaximoMinimo())

    # Configuramos la cadena de responsabilidad.
    supera_umbral.siguiente_manejador(cambio_drastico).siguiente_manejador(estadisticos_media).siguiente_manejador(estadisticos_cuantiles).siguiente_manejador(estadisticos_desviacion).siguiente_manejador(estadisticos_max_min)

    # Establecemos el manejador principal del sistema.
    sistema.manejador = supera_umbral

    # Iniciar el sensor de datos (hemos puesto 60 segundos para probar).
    (sensor.iniciar_sensor(60))