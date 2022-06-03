from django.contrib import admin

from .models import Measurement


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("starting_location", "destination", "distance", "created", "id", "user")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by("-id")


admin.site.register(Measurement, MeasurementAdmin)
