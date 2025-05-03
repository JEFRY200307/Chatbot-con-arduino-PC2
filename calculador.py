def calcular_humedad(valor, wet=250, dry=450):
    """
    Convierte un valor crudo del sensor a porcentaje de humedad.
    - wet: valor en suelo totalmente húmedo (100%).
    - dry: valor en suelo totalmente seco (0%).
    """
    # Calculamos la posición relativa dentro del rango [wet, dry]
    porcentaje = (valor - wet) * 100 / (dry - wet)
    # Invertimos la escala: valores altos → baja humedad
    porcentaje = 100 - porcentaje  # inversión
    # Limitamos el resultado entre 0% y 100%, redondeado
    return max(0, min(100, round(porcentaje)))

