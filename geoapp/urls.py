from django.urls import path

from . import views

app_name = "geoapp"

urlpatterns = [
    path("", views.home_page_view, name="home"),
    path("top_secret/", views.surprise, name="surprise"),
]
