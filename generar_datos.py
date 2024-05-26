import random
from datetime import datetime

def generador_datos():
    # Generamos una temperatura aleatoria entre 0 y 50 grados Celsius.
    temperature = round(random.uniform(0, 50), 2)
    
    # Registramos el tiempo en el que se ha obtenido la temperatura.
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Formato de año-mes-dia hora-minuto-segundo.
    
    # Devolvemos los datos de temperatura y el momento en el que fue registrada en una tupla.
    return(timestamp, temperature)