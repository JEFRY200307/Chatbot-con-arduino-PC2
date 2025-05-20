import io
import base64
from django.http import HttpResponse
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models.functions import TruncDate
import seaborn as sns
from django.conf import settings
import pytz
import os
from django.shortcuts import render
from django.http import JsonResponse
from .models import RegistroHumedad
from django.db.models import Avg, Max, Min
from django.utils.timezone import now, timedelta


def generar_grafico_humedad_en_memoria():
    # Obtener todos los registros de la base de datos
    queryset = RegistroHumedad.objects.all()
    
    # Crear un DataFrame con los datos
    data = list(queryset.values('humedad'))
    df = pd.DataFrame(data)
    
    if df.empty:
        return None  # o lanzar excepción o un gráfico vacío
    
    # Convertir a numérico (por si acaso) y filtrar valores positivos
    df['humedad'] = pd.to_numeric(df['humedad'], errors='coerce')
    valores_validos = df[df['humedad'] > 0]['humedad']
    
    plt.figure(figsize=(8,6))
    sns.boxplot(y=valores_validos, color="skyblue")
    plt.title("Gráfico de Cajas de Humedad (%)")
    plt.ylabel("Humedad (%)")
    plt.grid(True)
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def grafico_humedad(request):
    buffer = generar_grafico_humedad_en_memoria()
    return HttpResponse(buffer.getvalue(), content_type='image/png')

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


#----------------------------------------------------------------------
def estadisticas_humedad(request):
    datos = RegistroHumedad.objects.all()
    estadisticas = datos.aggregate(
        promedio=Avg('humedad'),
        minimo=Min('humedad'),
        maximo=Max('humedad'),
    )
    return JsonResponse(estadisticas)

def pagina_estadisticas(request):
    return render(request, 'dashboard/estadisticas.html')
#------------------------------------------------------


def indicador_riesgo_humedad(request):
    try:
        ultimo_registro = RegistroHumedad.objects.latest('timestamp')
        humedad = ultimo_registro.humedad
    except RegistroHumedad.DoesNotExist:
        humedad = None

    # Definir nivel riesgo
    if humedad is None:
        nivel = 'No hay datos'
        color = 'gray'
    elif humedad <= 60:
        nivel = 'Normal'
        color = 'green'
    elif 60 < humedad <= 80:
        nivel = 'Moderado'
        color = 'yellow'
    else:
        nivel = 'Alto'
        color = 'red'

    context = {
        'humedad': humedad,
        'nivel': nivel,
        'color': color,
    }
    return render(request, 'dashboard/indicador_riesgo.html', context)

#--------------------------------------------------------------------

def generar_grafico_humedad_diaria(fecha_obj):
    registros = RegistroHumedad.objects.filter(timestamp__date=fecha_obj).order_by('timestamp')

    if not registros.exists():
        return None

    zona_peru = pytz.timezone(settings.TIME_ZONE)
    horas = [r.timestamp.astimezone(zona_peru).strftime('%H:%M:%S') for r in registros]
    humedades = [r.humedad for r in registros]

    plt.figure(figsize=(10, 5))
    plt.plot(horas, humedades, marker='o', linestyle='-', color='blue')
    plt.title(f'Humedad durante el {fecha_obj}')
    plt.xlabel('Hora')
    plt.ylabel('Humedad (%)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    image_png = buffer.getvalue()
    buffer.close()
    grafico_base64 = base64.b64encode(image_png).decode('utf-8')

    return grafico_base64


def historial_por_dia(request):
    # Agrupar registros por día y obtener el promedio de humedad de cada día
    datos_diarios = (
        RegistroHumedad.objects
        .annotate(dia=TruncDate('timestamp'))
        .values('dia')
        .order_by('-dia')
        .distinct()
    )
    return render(request, 'dashboard/historial.html', {'datos_diarios': datos_diarios})

def historial_detalle(request, fecha):
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    registros = RegistroHumedad.objects.filter(timestamp__date=fecha_obj).order_by('timestamp')
    grafico= generar_grafico_humedad_diaria(fecha_obj)

    return render(request, 'dashboard/historial_detalle.html', {
        'registros': registros,
        'fecha': fecha_obj,
        'grafico': grafico
    })