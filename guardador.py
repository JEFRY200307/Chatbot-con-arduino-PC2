import pandas as pd

class GuardadorCSV:
    """
    Acumula lecturas de humedad con timestamp
    y las guarda en un archivo CSV al finalizar.
    """    
    def __init__(self, archivo='humedad_datos.csv'):
        self.datos = []
        self.archivo = archivo

    def agregar(self, tiempo, humedad):
        #Añade un registro con la hora y humedad al buffer.
        self.datos.append({'tiempo': tiempo, 'humedad': humedad})

    def guardar(self):
        #Convierte la lista de registros a DataFrame y exporta a CSV.
        df = pd.DataFrame(self.datos)
        df.to_csv(self.archivo, index=False)
        print(f"\n✅ Datos guardados en '{self.archivo}'")
