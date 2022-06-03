from textwrap import wrap

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from measurements.models import Measurement

from . import deco


def home_page_view(request):
    last_records_general = Measurement.objects.all().order_by("-id")[:10]
    context = {"last_records": last_records_general}

    return render(request, "geoapp/home.html", context=context)


@login_required
@deco.restricted_access_decorator(["admin"])
def surprise(request):
    """
    render template for restriced access page.
    no additional logic apart from decorators.
    """
    return render(request, "geoapp/surprise.html")
