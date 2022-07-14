from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("user_detail/", views.user_view, name="user_detail"),
    path("promotion/", views.promotion_view, name="promotion"),
    path("toggle_promotion/", views.toggle_user_promotion, name="toggle"),
]
