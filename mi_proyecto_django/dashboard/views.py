import io
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.conf import settings
import os
from django.shortcuts import render
from django.http import JsonResponse
from .models import RegistroHumedad
from django.db.models import Avg, Max, Min
from django.utils.timezone import now


def generar_grafico_humedad_en_memoria():
    ruta_csv = os.path.join(settings.BASE_DIR, 'humedad_datos.csv')
    df = pd.read_csv(ruta_csv)
    
    df['humidity_pct'] = pd.to_numeric(df['humidity_pct'], errors='coerce')
    valores_validos = df[df['humidity_pct'] > 0]['humidity_pct']
    
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

def generar_grafico_clasificacion_humedad_en_memoria():
    ruta_csv = os.path.join(settings.BASE_DIR, 'humedad_datos.csv')
    df = pd.read_csv(ruta_csv)
    
    # Convertir timestamp a datetime para formato amigable en eje X
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    def clasificar_humedad(h):
        if h <= 60:
            return 'Normal'
        else:
            return 'Alto'

    df['categoria'] = df['humidity_pct'].apply(clasificar_humedad)
    
    colores = {'Normal': 'green', 'Alto': 'red'}
    df['color'] = df['categoria'].map(colores)

    plt.figure(figsize=(14, 6))
    bars = plt.bar(df['timestamp'], df['humidity_pct'], color=df['color'])
    
    import matplotlib.patches as mpatches
    leyenda = [mpatches.Patch(color=color, label=cat) for cat, color in colores.items()]
    plt.legend(handles=leyenda)

    plt.xlabel('Hora')
    plt.ylabel('Humedad (%)')
    plt.title('Clasificación de Humedad por nivel crítico')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer


def grafico_humedad(request):
    buffer = generar_grafico_humedad_en_memoria()
    return HttpResponse(buffer.getvalue(), content_type='image/png')

def grafico_clasificacion_humedad(request):
    buffer = generar_grafico_clasificacion_humedad_en_memoria()
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
    ultimo = datos.order_by('-timestamp').first()
    actual = ultimo.humedad if ultimo else 0
    estadisticas['actual'] = actual
    return JsonResponse(estadisticas)


def pagina_estadisticas(request):
    return render(request, 'dashboard/estadisticas.html')

#------------------------------------------------------


def dashboard_estadisticas(request):
    if request.is_ajax() or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Obtener estadísticas del día actual
        hoy = now().date()
        stats = RegistroHumedad.objects.filter(fecha__date=hoy).aggregate(
            maximo=Max('humedad'),
           minimo=Min('humedad'),
           promedio=Avg('humedad'),
        )
        # Respuesta JSON para fetch
        return JsonResponse({
            'maximo': stats['maximo'] or 0,
            'minimo': stats['minimo'] or 0,
            'promedio': float(stats['promedio'] or 0),
        })
    else:
        # Renderiza plantilla HTML
        return render(request, 'dashboard/estadisticas.html')
