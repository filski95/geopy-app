from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from measurements.models import Measurement


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "age")

    add_fieldsets = UserAdmin.add_fieldsets + (("Additional fields", {"fields": ("age",)}),)
    fieldsets = UserAdmin.fieldsets + (("Additional fields", {"fields": ("age",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
