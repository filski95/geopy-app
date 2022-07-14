from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "apis"
urlpatterns = [
    path("", views.api_root, name="main_api_view"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.SingleUserView.as_view(), name="customuser-detail"),
    path("measurements/", views.MeasurementsListView.as_view(), name="measurements_list"),
    path("measurements/<int:pk>/", views.SingleMeasurementView.as_view(), name="measurement-detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
