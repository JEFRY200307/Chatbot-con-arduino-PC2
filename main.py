from datetime import datetime
import time


# Importamos módulos personalizados
from lector_serial import iniciar_arduino, leer_valor_crudo
from graficador import Graficador
from guardador import GuardadorCSV
from calculador import calcular_humedad

# Inicialización de la conexión con Arduino
arduino = iniciar_arduino('COM7', 9600)
# Inicialización de graficador en tiempo real
graf = Graficador()
# Inicialización del guardador de datos CSV
guarda = GuardadorCSV()

print("⏳ Leyendo datos crudos... Ctrl+C para detener.")

try:
    # Bucle infinito para lectura continua
    while True:
        # Leemos un valor crudo desde Arduino
        valor = leer_valor_crudo(arduino)
        if valor is not None:
             # Calculamos humedad (%) usando valores de calibración wet y dry
            humedad = calcular_humedad(valor, wet=250, dry=450)
            # Obtenemos la hora actual (HH:MM:SS)
            hora = datetime.now().strftime("%H:%M:%S")
            # Mostramos en consola
            print(f"{hora} - Valor: {valor} - Humedad: {humedad}%")
            # Actualizamos la gráfica con el nuevo punto
            graf.actualizar(hora, humedad)
            # Esperamos 1 segundo antes de la siguiente lectura
            guarda.agregar(hora, humedad)
        time.sleep(1)

except KeyboardInterrupt:
    # Al interrumpir, guardamos todos los datos en CSV
    guarda.guardar()
    # Cerramos la conexión con Arduino
    arduino.close()
    print("🔚 Finalizado.")
