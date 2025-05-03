import matplotlib.pyplot as plt
from collections import deque

class Graficador:
    #Muestra una gráfica en tiempo real de los últimos max_puntos valores de humedad.
    def __init__(self, max_puntos=60):
        # Estructuras circulares para datos recientes
        self.humedades = deque(maxlen=max_puntos)
        self.tiempos = deque(maxlen=max_puntos)
        # Activar modo interactivo de matplotlib
        plt.ion()
        self.fig, self.ax = plt.subplots()

    def actualizar(self, tiempo, humedad):

        #Añade nuevo dato y refresca la gráfica.
        
        # Insertamos nuevos valores al final de los deques
        self.tiempos.append(tiempo)
        self.humedades.append(humedad)


        # Limpiamos y volvemos a dibujar
        self.ax.clear()
        self.ax.plot(self.tiempos, self.humedades, marker='o')
        self.ax.set_title("Humedad en tiempo real")
        self.ax.set_ylabel("Humedad (%)")
        self.ax.set_xlabel("Hora")
        self.ax.set_ylim(0, 100)
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Pequeña pausa para actualizar la ventana
        plt.pause(0.01)
