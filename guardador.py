import pandas as pd

class GuardadorCSV:
    def __init__(self, archivo='humedad_datos.csv'):
        self.datos = []
        self.archivo = archivo

    def agregar(self, tiempo, humedad):
        self.datos.append({'tiempo': tiempo, 'humedad': humedad})

    def guardar(self):
        df = pd.DataFrame(self.datos)
        df.to_csv(self.archivo, index=False)
        print(f"\n✅ Datos guardados en '{self.archivo}'")
