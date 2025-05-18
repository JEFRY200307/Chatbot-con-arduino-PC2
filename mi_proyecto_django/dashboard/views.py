import io
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.conf import settings
import os
from django.shortcuts import render

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

def grafico_humedad(request):
    buffer = generar_grafico_humedad_en_memoria()
    return HttpResponse(buffer.getvalue(), content_type='image/png')

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

