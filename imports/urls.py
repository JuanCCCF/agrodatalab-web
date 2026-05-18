from django.urls import path
from . import views

urlpatterns = [
    path("", views.import_view, name="import_data"),
    path("reset/", views.reset_data, name="reset_data"),
    path("reset/confirm/", views.reset_import_confirm, name="reset_import_confirm")
]