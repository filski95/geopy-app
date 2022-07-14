from accounts.models import CustomUser
from measurements.models import Measurement
from numpy import generic
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import CustomUserSerializer, MeasurementSerializer

# Create your views here.

# main view of the API at api/
@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("apis:user_list", request=request, format=format),
            "measurements": reverse("apis:measurements_list", request=request, format=format),
        }
    )


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAdminUser,)


class SingleUserView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAdminUser,)


class MeasurementsListView(generics.ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SingleMeasurementView(generics.RetrieveAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = (permissions.IsAuthenticated,)
