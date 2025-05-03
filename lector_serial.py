import serial
import time

def iniciar_arduino(puerto='COM7', baudios=9600):
    arduino = serial.Serial(puerto, baudios)
    """
    Abre el puerto serie hacia Arduino y espera unos segundos
    para asegurar que el dispositivo esté listo.
    """
    # Pausa para que Arduino reinicie y comience a enviar datos
    time.sleep(2)
    return arduino
    
def leer_valor_crudo(arduino):
    """
    Lee una línea del puerto serie, decodifica a string,
    remueve espacios y convierte a entero.
    Devuelve None si la conversión falla.
    """
    try:
        linea = arduino.readline().decode('utf-8').strip()
        return int(linea)
    except:
        return None
