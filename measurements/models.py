from accounts.models import CustomUser
from django.conf import settings
from django.db import models


class Measurement(models.Model):

    starting_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.TimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="measurements", blank=True, null=True, on_delete=models.SET_NULL
    )  # related name is used in serializers CustomUserSerializer (instead of measruement_set which is a default for reverse rel)

    def __str__(self) -> str:
        return f"Distance from {self.starting_location} to {self.destination} is {self.distance} km. "
