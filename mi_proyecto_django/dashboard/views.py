from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.http import JsonResponse
from .models import RegistroHumedad
from django.db.models import Avg, Max, Min
from django.utils.timezone import now

#----------------------------------------------------------------------
# Devuelve los últimos 60 registros de humedad en formato JSON (para gráfico en tiempo real)
def humedad_evolucion_json(request):
    datos = RegistroHumedad.objects.order_by('-timestamp')[:60][::-1]
    lista = [
        {"timestamp": r.timestamp.strftime("%H:%M:%S"), "humedad": r.humedad}
        for r in datos
    ]
    return JsonResponse(lista, safe=False)

#----------------------------------------------------------------------
# Devuelve el estado del sensor (conectado/desconectado)
def estado_sensor(request):
    ahora = timezone.now()
    conectado = RegistroHumedad.objects.filter(timestamp__gte=ahora - timedelta(seconds=10)).exists()
    return JsonResponse({'conectado': conectado})

#----------------------------------------------------------------------
# Devuelve el tiempo (en segundos) desde el último registro crítico (humedad > 80%)
def tiempo_desde_ultimo_critico(request):
    ultimo = RegistroHumedad.objects.filter(humedad__gt=80).order_by('-timestamp').first()
    if ultimo:
        ahora = timezone.now()
        delta = ahora - ultimo.timestamp
        segundos = int(delta.total_seconds())
    else:
        segundos = None
    return JsonResponse({'segundos_desde_critico': segundos})

#----------------------------------------------------------------------
# Devuelve el historial de humedad por día (para el botón de historial)
def historial_por_dia(request):
    fecha = request.GET.get('fecha')
    datos = []
    if fecha:
        datos = RegistroHumedad.objects.filter(timestamp__date=fecha).order_by('timestamp')
    return render(request, 'dashboard/historial.html', {'datos': datos, 'fecha': fecha})

#----------------------------------------------------------------------
# Vista principal del dashboard (todo en dashboard.html)
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

#----------------------------------------------------------------------
# Devuelve estadísticas generales de humedad (máximo, mínimo, promedio, actual)
def estadisticas_humedad(request):
    hoy = now().date()
    datos = RegistroHumedad.objects.filter(timestamp__date=hoy)
    estadisticas = datos.aggregate(
        promedio=Avg('humedad'),
        minimo=Min('humedad'),
        maximo=Max('humedad'),
    )
    ultimo = datos.order_by('-timestamp').first()
    actual = ultimo.humedad if ultimo else 0
    estadisticas['actual'] = actual
    return JsonResponse(estadisticas)