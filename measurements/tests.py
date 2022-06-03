import time
from http import client

from accounts.models import CustomUser
from django.test import RequestFactory, TestCase
from django.urls import reverse

from . import views
from .models import Measurement


class TestMeasurement(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="admin",
            age=25,
            promotion=False,
        )

        cls.user_promoted = CustomUser.objects.create_user(
            username="testuser2",
            email="test2@gmail.com",
            password="admin",
            age=25,
            promotion=True,
        )

        cls.record = (
            Measurement.objects.create(
                starting_location="Sosnowiec", destination="Bedzin", distance=50, user=cls.user
            ),
        )
        cls.factory = RequestFactory()

    def test_measurements_url(self):
        response = self.client.get("/measurements/")
        response_namespace = self.client.get(reverse("measurements:measurements"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_namespace.status_code, 200)

    def test_measurements_user_not_logged_in(self):
        response = self.client.get(reverse("measurements:measurements"))
        self.assertTemplateUsed("measurements/main.html")
        self.assertContains(response, "Please log in to use the app")

    def test_measurements_user_logged_in_free(self):
        # use of factory + user assigment to the request.
        request = self.factory.get("/measurements/")
        request.user = self.user
        response = views.calculate_distance_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Please log in to use the app")
        self.assertContains(response, "Calculate")
        self.assertContains(response, "Refresh")

    def test_measurements_free_user_logged_in_used_app(self):

        request = self.factory.post("/measurements/", {"starting_location": "Sosnowiec", "destination": "Bedzin"})
        request.user = self.user

        # expected delay >3 sec
        start = time.perf_counter()
        response = views.calculate_distance_view(request)
        total_time = time.perf_counter() - start

        self.assertContains(response, "Distance from Sosnowiec to Bedzin is")
        self.assertGreater(total_time, 4)

    def test_measurements_premium_user_logged_in_used_app(self):

        request = self.factory.post("/measurements/", {"starting_location": "Sosnowiec", "destination": "Maczki"})
        request.user = self.user_promoted

        # expected delay >3 sec
        start = time.perf_counter()
        response = views.calculate_distance_view(request)
        total_time = time.perf_counter() - start

        # check if records were saved to the db correctly
        recent_record = Measurement.objects.all().last()

        self.assertContains(response, "Distance from Sosnowiec to Maczki is")
        self.assertLess(total_time, 3)
        self.assertEqual(recent_record.destination, "Maczki")
        # check if user is being properly saved
        self.assertEqual(recent_record.user.username, "testuser2")
