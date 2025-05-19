from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('grafico/', views.grafico_humedad, name='grafico_humedad'),
    path('grafico_clasificacion/', views.grafico_clasificacion_humedad, name='grafico_clasificacion_humedad'),
]
