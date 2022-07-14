import logging
import time

import folium
from django.shortcuts import get_object_or_404, render
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

from . import deco
from .forms import MeasurementModelForm
from .models import Measurement


@deco.time_tracker_decorator
@deco.slow_down_decorator
def calculate_distance_view(request, delay=None):
    form = MeasurementModelForm(request.POST)  #! create form from post data
    context = {"form": form}

    if request.method == "POST":
        if form.is_valid():
            if delay:
                time.sleep(delay)
            # getting info from a form
            instance = form.save(commit=False)
            st_points, d_points = _return_lat_lon(instance)
            instance.user = request.user
            instance.distance = _calculate_distance(st_points, d_points)
            instance.save()

            # preparing context to display.
            zoom = _get_zoom(instance.distance)
            context["map"] = _prepare_map(instance.starting_location, st_points, instance.destination, d_points, zoom)
            context["distance_message"] = get_object_or_404(Measurement, id=Measurement.objects.all().last().id)

    return render(request, "measurements/main.html", context=context)


#! utils functions used for creation of the map!
def _prepare_map(
    starting_location,
    starting_location_cords: tuple[float, float],
    destination,
    destination_cords: tuple[float, float],
    zoom,
) -> folium.Map:
    """prepare a map of cities indicated by the user - label with city name + a marker on coords"""

    m = folium.Map(width=1270, height=762, location=starting_location_cords, zoom_start=zoom, min_zoom=2)
    # adding marker
    folium.Marker(starting_location_cords, popup=starting_location, icon=folium.Icon(color="red")).add_to(m)
    folium.Marker(destination_cords, popup=destination, icon=folium.Icon(color="green")).add_to(m)
    folium.vector_layers.PolyLine((starting_location_cords, destination_cords)).add_to(m)

    m = m._repr_html_()
    return m


def _return_lat_lon(instance):
    """Instaace == Measurement object with "current_location" and "destination" provided by the user.
    -> data provided by the user should be used as arguments to geolocator.
    """
    geolocator = Nominatim(user_agent="measurements")

    cl_lat = geolocator.geocode(instance.starting_location).latitude
    cl_lon = geolocator.geocode(instance.starting_location).longitude
    d_lat = geolocator.geocode(instance.destination).latitude
    d_lon = geolocator.geocode(instance.destination).longitude

    return (cl_lat, cl_lon), (d_lat, d_lon)


def _calculate_distance(starting_location: tuple[float, float], destination: tuple[float, float]) -> float:
    """
     current_location[lat,long], destination[lat,lon]
    -> calculating distance between two points in kms roudned to 2 decimal places
    """
    result = round(geodesic(starting_location, destination).km, 2)
    return result


def _get_zoom(distance):
    if distance <= 100:
        return 10
    elif distance <= 1000:
        return 6
    elif distance <= 3000:
        return 4
    else:
        return 2
