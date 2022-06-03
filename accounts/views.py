from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from measurements.models import Measurement

from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


def user_view(request):

    context = {}
    context["current_user_records"] = Measurement.objects.filter(user=request.user).order_by("-id")

    return render(request, "accounts/user_detail.html", context=context)


@login_required
def promotion_view(request):

    return render(request, "accounts/promotion.html")


def toggle_user_promotion(request):
    user = CustomUser.objects.get(username=request.user.username)
    user.promotion = not user.promotion
    print(user.promotion)
    user.save()
    return redirect("accounts:promotion")
