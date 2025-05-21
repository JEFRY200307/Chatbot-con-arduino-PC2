from django.urls import path
from . import views

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_view, name='dashboard'),
    path('humedad-evolucion-json/', views.humedad_evolucion_json, name='humedad_evolucion_json'),
    path('estadisticas-humedad/', views.estadisticas_humedad, name='estadisticas_humedad'),
    path('estado-sensor/', views.estado_sensor, name='estado_sensor'),
    path('tiempo-ultimo-critico/', views.tiempo_desde_ultimo_critico, name='tiempo_desde_ultimo_critico'),
    path('historial/', views.historial_por_dia, name='historial_por_dia'),
]