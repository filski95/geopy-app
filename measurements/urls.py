from django.urls import path

from . import views

app_name = "measurements"

urlpatterns = [
    path("", views.calculate_distance_view, name="measurements"),
]
