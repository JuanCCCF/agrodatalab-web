from django.urls import path
from . import views

urlpatterns = [
    path("", views.alerts_view, name="alerts"),
    path("create/", views.alert_create, name="alert_create"),
    path("edit/<int:pk>/", views.alert_update, name="alert_update"),
    path("delete/<int:pk>/", views.alert_delete, name="alert_delete"),
    path("recommendation/create/<int:alert_id>/", views.recommendation_create, name="reco_create"),
    path("recommendation/edit/<int:pk>/", views.recommendation_update, name="reco_update"),
    path("recommendation/review/<int:pk>/", views.recommendation_mark_reviewed, name="reco_mark_reviewed"),
]