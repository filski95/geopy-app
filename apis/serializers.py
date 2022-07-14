from accounts.models import CustomUser
from django.contrib.auth.models import Group
from measurements.models import Measurement
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    measurements = serializers.HyperlinkedRelatedField(many=True, view_name="apis:measurement-detail", read_only=True)
    user_url = serializers.HyperlinkedIdentityField(view_name="apis:customuser-detail")
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        exclude = ["password"]  # reveal everything but password


class MeasurementSerializer(serializers.ModelSerializer):
    measurement_url = serializers.HyperlinkedIdentityField(view_name="apis:measurement-detail")
    user = serializers.StringRelatedField()

    class Meta:
        model = Measurement
        fields = "__all__"
