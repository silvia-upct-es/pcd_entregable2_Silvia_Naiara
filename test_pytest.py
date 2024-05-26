from entregable_main import *
from generar_datos import *
from statistics import mean, pstdev
import pytest


# Generación de datos.
def test_generador_datos():
    datos = generador_datos()

    # Verificamos que devuelve una tupla.
    assert isinstance(datos, tuple)

    # Verificamos que la tupla tenga dos elementos.
    assert len(datos) == 2

    # Verificamos que el primer elemento sea una cadena de texto con el formato de fecha y hora.
    try:
        datetime.strptime(datos[0], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        assert False, "El primer elemento de la tupla no tiene el formato de fecha y hora esperado"

    # Verificamos que el segundo elemento sea un número (temperatura) dentro del rango esperado (0 a 50 grados Celsius).
    assert isinstance(datos[1], (int, float))
    assert 0 <= datos[1] <= 50


# Comprobacion instancia unica Singleton.
def test_singleton():
    instancia_1 = Sistema.obtener_instancia()
    instancia_2 = Sistema.obtener_instancia()
    assert instancia_1 is instancia_2 # Verifica que ambas instancias son la misma.


# Suscripcion al publicador.
def test_suscribirse_desuscribirse():
    sensor = SensorTemperatura()
    sistema = Sistema.obtener_instancia()

    sensor.añadir_subscriptor(sistema)
    assert sistema in sensor._lista_subscriptores

    sensor.eliminar_subscriptor(sistema)
    assert sistema not in SensorTemperatura._lista_subscriptores


# Estadísticos.

def test_media():
    datos_prueba = [[1, 4, 7], [1, 6,5, 2], [3, 45,23, 1]]
    media = Media()
    for lista in datos_prueba:
        assert mean(lista) == media.hacer_calculo(lista)


def test_desviacion_tipica():
    datos_prueba = [[1, 4, 7], [1, 6,5, 2], [3, 45,23, 1]]
    desviacion = DesviacionTipica()
    for lista in datos_prueba:
        print(pstdev(lista), desviacion.hacer_calculo(lista))
        assert pstdev(lista) == desviacion.hacer_calculo(lista)


def test_cuantiles():
    datos_prueba = [[1, 4, 7], [1, 6, 5, 2], [3, 45, 23, 1]]
    cuantiles = Cuantiles()
    for lista in datos_prueba:
        percentiles = np.percentile(lista, [25, 50, 75])
        resultado = cuantiles.hacer_calculo(lista)
        assert round(percentiles[0], 2) == resultado["25%"]
        assert round(percentiles[1], 2) == resultado["50%"]
        assert round(percentiles[2], 2) == resultado["75%"]


def test_max_min():
    datos_prueba = [[1, 4, 7], [1, 6, 5, 2], [3, 45, 23, 1]]
    max_min = MaximoMinimo()
    for lista in datos_prueba:
        maximo = max(lista)
        minimo = min(lista)
        resultado = max_min.hacer_calculo(lista)
        assert maximo == resultado["max"]
        assert minimo == resultado["min"]


# Recolección de datos.
def test_iniciar_sensor():
    # Crear instancias de los componentes del sistema.
    sensor = SensorTemperatura()
    sistema = Sistema.obtener_instancia()
    sensor.añadir_subscriptor(sistema)

    estrategia_media = Media()
    estadisticos = Estadisticos(estrategia_media)
    umbral = SuperaUmbral()
    cambio_drastico = CambioDrastico()

    estadisticos.siguiente_manejador(umbral).siguiente_manejador(cambio_drastico)
    sistema.manejador = estadisticos

    # Simular la recolección de datos durante 21 segundos.
    sensor.iniciar_sensor(21)

    # Verificar que se han registrado datos en el sistema.
    assert len(sistema._temperaturas) > 0
    assert len(sistema._temperaturas_30) <= 6
    assert len(sistema._temperaturas_60) <= 12


# Configuración de cadena de responsabilidad.
def test_cadena():
    estrategia_media = Media()
    estrategia_cuantiles = Cuantiles()
    estrategia_desviacion = DesviacionTipica()
    estrategia_min_max = MaximoMinimo()

    # Crear instancias de los manejadores.
    estadisticos_m = Estadisticos(estrategia_media)
    estadisticos_c = Estadisticos(estrategia_cuantiles)
    estadisticos_d = Estadisticos(estrategia_desviacion)
    estadisticos_mm = Estadisticos(estrategia_min_max)
    umbral = SuperaUmbral()
    cambio_drastico = CambioDrastico()

    # Configurar la cadena de responsabilidad.
    estadisticos_m.siguiente_manejador(estadisticos_c).siguiente_manejador(estadisticos_d).siguiente_manejador(estadisticos_mm).siguiente_manejador(umbral).siguiente_manejador(cambio_drastico)

    assert estadisticos_m._siguiente_manejador == estadisticos_c
    assert estadisticos_c._siguiente_manejador == estadisticos_d
    assert estadisticos_d._siguiente_manejador == estadisticos_mm
    assert estadisticos_mm._siguiente_manejador == umbral
    assert umbral._siguiente_manejador == cambio_drastico
    assert cambio_drastico._siguiente_manejador == None
