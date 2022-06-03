import logging
import time

from .models import Measurement


def slow_down_decorator(func):
    def wrapper(request, *args, **kwargs):
        # two conditions because it crashed when tried with if request.user.promotion == True in case of Anonymous User
        if request.user.username and request.user.promotion == True:
            return func(request, *args, **kwargs)
        else:
            delay = 3
            return func(request, delay, *args, **kwargs)

    return wrapper


def time_tracker_decorator(func):
    def wrapper(request, *args, **kwargs):
        start = time.perf_counter()
        deco_func = func(request, *args, **kwargs)
        total_time = round(time.perf_counter() - start, 2)

        last_record = Measurement.objects.all().last()
        logging.basicConfig(filename="distance_calculator.log", level=logging.INFO)
        logging.info(
            f"Location check with id {last_record.id} took {total_time} seconds. Starting location: {last_record.starting_location}, Destination: {last_record.destination}, User: {last_record.user}, Promoted: {last_record.user.promotion}"
        )

        return deco_func

    return wrapper
