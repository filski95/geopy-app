from .models import Measurement
from django import forms


class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ("starting_location", "destination")
