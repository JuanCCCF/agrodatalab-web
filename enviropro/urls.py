from django.urls import path
from . import views

urlpatterns = [
    path("", views.registros_view, name="registros"),
    path("nuevo/", views.registro_create, name="registro_create"),
    path("editar/<int:pk>/", views.registro_update, name="registro_update"),
    path("eliminar/<int:pk>/", views.registro_delete, name="registro_delete"),
]