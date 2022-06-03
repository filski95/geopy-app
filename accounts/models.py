from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    promotion = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["age"]

    def __str__(self) -> str:
        return self.username
