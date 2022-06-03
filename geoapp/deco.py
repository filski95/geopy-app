from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse


def restricted_access_decorator(allowed_groups=["admin"]):
    """argument = allowed groups to view this page"""

    def actual_decorator(view_function):
        """takes function to be decorated as argument"""

        def wrapper(request, *args, **kwargs):
            """arguments form function to be decorated"""
            user_groups = [*request.user.groups.all().values("name")]
            for pair in user_groups:
                for value in pair.values():
                    if value in allowed_groups:
                        return view_function(request, *args, **kwargs)

            return redirect(reverse("login"))

        return wrapper

    return actual_decorator
