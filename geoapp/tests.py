from typing import Tuple
from urllib import response

from accounts.models import CustomUser
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.test import RequestFactory, TestCase
from django.urls import reverse
from measurements.models import Measurement
from mixer.backend.django import mixer

from . import views


class TestGeoApp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="admin",
            age=25,
        )

        cls.record = Measurement.objects.create(
            starting_location="Sosnowiec", destination="Bedzin", distance=50, user=cls.user
        )

        cls.factory = RequestFactory()

    def test_home_page_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("geoapp/home.html")
        self.assertIsInstance(
            response.context["last_records"], QuerySet
        )  # useless because of the one with Measurement.?
        self.assertIsInstance(*response.context["last_records"], Measurement)
        self.assertContains(response, "Sosnowiec")
        self.assertContains(response, "Bedzin")
        self.assertNotContains(response, "Czeladz")

    def test_home_page_reverse(self):
        response = self.client.get(reverse("geoapp:home"))
        self.assertEqual(response.status_code, 200)

    def test_surprise_user_not_logged_in(self):
        # not logged in user -> login_required redirects to login page.
        response = self.client.get(reverse("geoapp:surprise"))
        response = self.client.get("/top_secret/")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("accounts/login.html")

    def test_surprise_logged_in_user_but_notadmin(self):
        # 2 decorators on surprise function 1. must be logged in + must be of a specific group (admin)
        # if either of the conditions not met => redirect to login.
        request = self.factory.get("/top_secret/")
        request.user = self.user

        response = views.surprise(request)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("accounts:login")
        self.assertTemplateNotUsed("geoapp/surprise.html")

    def test_surprise_logged_in_user_admin(self):
        request = self.factory.get("/top_secret/")
        request.user = self.user
        # https://mixer.readthedocs.io/en/latest/quickstart.html#base-usage
        # https://stackoverflow.com/questions/70687757/create-and-add-a-user-to-group-in-django-for-tests-purpose
        group = mixer.blend(Group, name="admin")
        request.user.groups.add(group)

        response = views.surprise(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("geoapp/surprise.html")
