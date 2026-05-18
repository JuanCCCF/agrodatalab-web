from django.shortcuts import render, redirect, get_object_or_404
from .models import EnviroProRecord
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import EnviroProRecord
from .forms import EnviroProRecordForm

"""
Módulo de vistas para la aplicación EnviroPro.

Este módulo gestiona los registros ambientales del sistema y proporciona
las operaciones CRUD (Crear, leer, editar y eliminar) necesarias para su
administración.

Funcionalidades principales:
- Listado de registros con paginación (10 registros por página).
- Creación de nuevos registros ambientales.
- Edición de registros existentes.
- Eliminación de registros con confirmación previa.

Todas las vistas están protegidas mediante autenticación, de forma que
únicamente los usuarios registrados pueden acceder y modificar los datos.

Este módulo forma parte del sistema de monitorización ambiental EnviroPro.
"""

# Listado de registros
# Muestra todos los registros ambientales almacenados con paginación para mejorar rendimiento y navegación.
# Acceso restringido a usuarios autenticados.
@login_required
def registros_view(request):

    registros_list = EnviroProRecord.objects.all().order_by("-fecha")

    paginator = Paginator(registros_list, 10)
    page_number = request.GET.get("page")
    registros = paginator.get_page(page_number)

    return render(request, "enviropro/registros.html", {
        "registros": registros
    })

# Crear registro
# Permite añadir manualmente un nuevo registro ambiental.
@login_required
def registro_create(request):

    form = EnviroProRecordForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("registros")

    return render(request, "enviropro/registro_form.html", {
        "form": form,
        "titulo": "Nuevo Registro"
    })

# Editar registro
# Permite modificar un registro existente.
@login_required
def registro_update(request, pk):

    registro = get_object_or_404(EnviroProRecord, pk=pk)

    form = EnviroProRecordForm(
        request.POST or None,
        instance=registro
    )

    if form.is_valid():
        form.save() 
        return redirect("registros")

    return render(request, "enviropro/registro_form.html", {
        "form": form,
        "titulo": "Editar Registro"
    })

# Eliminar registro
# Solicita confirmación antes de borrar un registro.
@login_required
def registro_delete(request, pk):

    registro = get_object_or_404(EnviroProRecord, pk=pk)

    if request.method == "POST":
        registro.delete()
        return redirect("registros")

    return render(request, "enviropro/registro_confirm_delete.html", {
        "registro": registro
    })
