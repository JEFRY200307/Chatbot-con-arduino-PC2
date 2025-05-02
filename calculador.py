def calcular_humedad(valor, wet=250, dry=450):
    porcentaje = (valor - wet) * 100 / (dry - wet)
    porcentaje = 100 - porcentaje  # inversión
    return max(0, min(100, round(porcentaje)))
