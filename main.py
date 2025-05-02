from datetime import datetime
import time

from lector_serial import iniciar_arduino, leer_valor_crudo
from graficador import Graficador
from guardador import GuardadorCSV
from calculador import calcular_humedad

arduino = iniciar_arduino('COM7', 9600)
graf = Graficador()
guarda = GuardadorCSV()

print("⏳ Leyendo datos crudos... Ctrl+C para detener.")

try:
    while True:
        valor = leer_valor_crudo(arduino)
        if valor is not None:
            humedad = calcular_humedad(valor, wet=250, dry=450)
            hora = datetime.now().strftime("%H:%M:%S")
            print(f"{hora} - Valor: {valor} - Humedad: {humedad}%")
            graf.actualizar(hora, humedad)
            guarda.agregar(hora, humedad)
        time.sleep(1)

except KeyboardInterrupt:
    guarda.guardar()
    arduino.close()
    print("🔚 Finalizado.")
