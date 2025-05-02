import serial
import time

def iniciar_arduino(puerto='COM7', baudios=9600):
    arduino = serial.Serial(puerto, baudios)
    time.sleep(2)
    return arduino

def leer_valor_crudo(arduino):
    try:
        linea = arduino.readline().decode('utf-8').strip()
        return int(linea)
    except:
        return None
