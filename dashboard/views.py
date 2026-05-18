from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from enviropro.models import EnviroProRecord
from alerts.models import Alert, Recommendation
from django.db.models import Avg
import json
from django.core.serializers.json import DjangoJSONEncoder


"""
Módulo de vistas del Dashboard principal.

Este módulo gestiona la vista principal del sistema EnviroPro,
proporcionando un panel central de monitorización del estado
ambiental y operativo de la plataforma.

Su objetivo es ofrecer una visión global del sistema mediante:

- Estadísticas generales de los registros ambientales.
- Cálculo de medias de variables clave (humedad, temperatura,
  batería y panel solar).
- Análisis y conteo de alertas clasificadas por tipo.
- Visualización de la última recomendación generada.
- Preparación de datos para gráficas dinámicas con Chart.js.

El dashboard actúa como el punto central de control del sistema,
permitiendo a los usuarios autenticados consultar el estado
general de los sensores y las métricas ambientales en tiempo real.

El acceso a estas vistas está restringido a usuarios autenticados.
"""

# Dashboard principal
# Acceso solo permitido a usuarios autenticados
@login_required
def dashboard_view(request):

    # Obtener todos los registros ordenados por fecha
    registros = EnviroProRecord.objects.all().order_by("fecha")

    # Estadísticas básicas
    total_registros = registros.count()

    primera_lectura = registros.first()
    ultima_lectura = registros.last()

    # Cálculo de medias
    # "aggregate" permite calcular estadísticas en BD
    humedad_media = registros.aggregate(avg=Avg("humedad_media"))["avg"] or 0
    temperatura_media = registros.aggregate(avg=Avg("temp_suelo"))["avg"] or 0
    bateria_media = registros.aggregate(avg=Avg("bateria"))["avg"] or 0
    panel_media = registros.aggregate(avg=Avg("panel_solar"))["avg"] or 0

    # Conteo de alertas por tipo
    alertas_sequedad = Alert.objects.filter(tipo__icontains="sequedad").count()
    alertas_energia = Alert.objects.filter(tipo__icontains="energ").count()
    alertas_temp = Alert.objects.filter(tipo__icontains="temperatura").count()

    # Última recomendación generada
    ultima_recomendacion = Recommendation.objects.order_by("-id").first()

    # Datos para gráficas (chart.js)
    # Se convierten a listas para enviarlos al frontend
    fechas = list(registros.values_list("fecha", flat=True))
    humedad = list(registros.values_list("humedad_media", flat=True))
    temp = list(registros.values_list("temp_suelo", flat=True))
    bateria = list(registros.values_list("bateria", flat=True))

    # Contexto enviado a la plantilla
    context = {
        # Estadísticas generales
        "total_registros": total_registros,
        "primera_lectura": primera_lectura.fecha if primera_lectura else None,
        "ultima_lectura": ultima_lectura.fecha if ultima_lectura else None,

        # Medias ambientales
        "humedad_media": humedad_media,
        "temperatura_media": temperatura_media,
        "bateria_media": bateria_media,
        "panel_media": panel_media,

        # Alertas
        "alertas_sequedad": alertas_sequedad,
        "alertas_energia": alertas_energia,
        "alertas_temp": alertas_temp,

        # Recomendación
        "ultima_recomendacion": ultima_recomendacion,

        # Datos serializados para gráficas JS
        "fechas_json": json.dumps(fechas, cls=DjangoJSONEncoder),
        "humedad_json": json.dumps(humedad, cls=DjangoJSONEncoder),
        "temp_json": json.dumps(temp, cls=DjangoJSONEncoder),
        "bateria_json": json.dumps(bateria, cls=DjangoJSONEncoder),
    }

    return render(request, "dashboard/dashboard.html", context)

# Página about (acerca de)
# Vista informativa del proyecto
def about_view(request):
    return render(request, "dashboard/about.html")
