from datetime import datetime
import time, sys

from lector_serial import iniciar_puerto, leer_datos
from guardador      import init_csv, append_csv
from graficador     import Graficador

def main():
    ser = iniciar_puerto()
    if ser is None:
        sys.exit(1)

    init_csv()
    graf = Graficador()
    print("⏳ Leyendo datos… Ctrl+C para detener.")

    try:
        while True:
            datos = leer_datos(ser)
            if datos:
                raw, pct = datos
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"{ts} → raw:{raw}  pct:{pct}%")
                append_csv(ts, raw, pct)
                graf.actualizar(ts, pct)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n🔌 Detenido por usuario.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
