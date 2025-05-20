from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('grafico/', views.grafico_humedad, name='grafico_humedad'),
    path('indicador/', views.indicador_riesgo_humedad, name='indicador_riesgo'),
    path('historial/', views.historial_por_dia, name='historial_por_dia'),
    path('historial/<str:fecha>/', views.historial_detalle, name='historial_detalle'),
    path('api/estadisticas/', views.estadisticas_humedad, name='estadisticas_humedad'),
    path('estadisticas/', views.pagina_estadisticas, name='pagina_estadisticas'),
]
