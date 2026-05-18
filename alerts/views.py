from django.shortcuts import render
from .models import Alert, Recommendation
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from .forms import AlertForm, RecommendationForm

"""
Módulo de gestión de Alertas y Recomendaciones.

Este módulo se encarga de la creación, visualización y administración
de las alertas generadas a partir de los datos ambientales del sistema,
así como de las recomendaciones asociadas a cada una de ellas.

Funcionalidades principales:
- Visualización de alertas generadas automáticamente por el sistema.
- Filtrado de alertas por variable ambiental (humedad, temperatura, batería).
- Paginación de resultados para mejorar el rendimiento.
- Creación, edición y eliminación de alertas manuales.
- Gestión de recomendaciones asociadas a cada alerta.
- Control del estado de revisión de las recomendaciones.

Las alertas representan eventos detectados en los datos ambientales
(sequedad, temperatura o energía). Por su parte, las recomendaciones
definen acciones o mejoras sugeridas para optimizar el funcionamiento
del sistema de sensores.

Este módulo complementa el dashboard principal, permitiendo la gestión
detallada de las incidencias detectadas automáticamente.
"""

# Listado de alertas creadas automáticamente
# Muestra todas las alertas con filtro por tipo y paginación para mejorar rendimiento.
def alerts_view(request):

    # Obtener filtro desde la URL, por ejemplo (?tipo=temperatura)
    tipo = request.GET.get("tipo")

    # Consulta principal ordenada por fecha descendente
    # prefetch_related evita consultas extra a BD
    alerts_list = (
        Alert.objects
        .prefetch_related("recomendaciones")
        .order_by("-fecha")
    )

    # Aplicar filtro según variable afectada
    if tipo:
        if tipo == "humedad":
            alerts_list = alerts_list.filter(variable_afectada="humedad")
        elif tipo == "temperatura":
            alerts_list = alerts_list.filter(variable_afectada="temperatura")
        elif tipo == "bateria":
            alerts_list = alerts_list.filter(variable_afectada="bateria")

    # Paginación (10 alertas por página)
    paginator = Paginator(alerts_list, 10)
    page = request.GET.get("page")
    alerts = paginator.get_page(page)

    return render(request, "alerts/alerts.html", {
        "alerts": alerts,
        "tipo_actual": tipo
    })

# Crear alerta manualmente
# Permite crear una alerta manual y redirige automáticamente a crear su recomendación.
def alert_create(request):

    form = AlertForm(request.POST or None)

    # Si el formulario es válido se guarda la alerta
    if form.is_valid():
        alert = form.save()

        # Tras crear la alerta se redirige automáticamente a crear recomendación
        return redirect("reco_create", alert.id)

    return render(request, "alerts/alert_form.html", {
        "form": form,
        "titulo": "Crear alerta"
    })

# Editar alerta
# Edita la alerta y gestiona automáticamente si debe editar o crear una recomendación.
def alert_update(request, pk):

    alert = get_object_or_404(Alert, pk=pk)

    # Formulario cargado con datos actuales
    form = AlertForm(request.POST or None, instance=alert)

    if form.is_valid():
        reco = alert.recomendaciones.first()
        
        # Si tiene recomendación --> editar
        if reco:
            return redirect("reco_update", reco.id)

        # Si no tiene recomendación --> crear
        return redirect("reco_create", alert.id)
    
    return render(request, "alerts/alert_form.html", {
        "form": form,
        "titulo": "Editar alerta"
    })

# Eliminar alerta
# Solicita confirmación antes de eliminar.
def alert_delete(request, pk):

    alert = get_object_or_404(Alert, pk=pk)

    # Solo elimina si el usuario confirma (POST)
    if request.method == "POST":
        alert.delete()
        return redirect("alerts")

    return render(request, "alerts/alert_delete.html", {
        "alert": alert
    })

# Crear recomendación
# Crea una recomendación asociada a una alerta.
def recommendation_create(request, alert_id):

    # Obtener alerta relacionada
    alert = get_object_or_404(Alert, id=alert_id)

    form = RecommendationForm(request.POST or None)

    if form.is_valid():
        reco = form.save(commit=False)
        reco.alerta = alert
        reco.save()

        return redirect("alerts")  # o dashboard

    return render(request, "alerts/recommendation_form.html", {
        "form": form,
        "alert": alert,
        "titulo": "Nueva recomendación"
    })

# Editar recomendación
# Permite modificar una recomendación existente.
def recommendation_update(request, pk):

    reco_update = get_object_or_404(Recommendation, pk=pk)

    form = RecommendationForm(request.POST or None, instance=reco_update)

    if form.is_valid():
        form.save()
        return redirect("alerts")

    return render(request, "alerts/recommendation_form.html", {
        "form": form,
        "alert": reco_update.alerta,
        "titulo": "Editar recomendación"
    })

# Marcar alerta como revisada
# Permite cambiar el estado de alerta a "revisada".
def recommendation_mark_reviewed(request, pk):
    reco = get_object_or_404(Recommendation, pk=pk)
    reco.estado = "revisada"
    reco.save()

    next_url = request.GET.get("next")

    if next_url:
        return redirect(next_url)

    return redirect("alerts")
