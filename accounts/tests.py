from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import RequestFactory, TestCase
from django.urls import reverse
from measurements.models import Measurement

from . import views
from .models import CustomUser


class CustomUserModelTest(TestCase):
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

    def test_age_setting(self):

        with self.assertRaises(IntegrityError):
            wrong_user = CustomUser.objects.create_user(username="user", email="test@gmail.com", password="admin")
        with self.assertRaises(ValueError):
            wrong_user2 = CustomUser.objects.create_user(
                username="user",
                email="test@gmail.com",
                password="admin",
                age="twenyfive",
            )

    def test_correct_user_setup(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@gmail.com")
        self.assertEqual(self.user.age, 25)
        self.assertEqual(self.user.promotion, 0)  # false default

    def test_promotion_to_true(self):
        self.user.promotion = True
        self.assertEqual(self.user.promotion, 1)  # True

    def test_signup_view(self):
        response = self.client.get("/accounts/signup/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("accounts/registration/signup.html")

        self.response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_form_post(self):
        response = self.client.post(
            "/accounts/signup/",
            {
                "username": "filip",
                "age": 27,
                "password1": "lalalabababa123",
                "password2": "lalalabababa123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.all().last().username, "filip")

    def test_user_detail_url(self):

        request = self.factory.get("/accounts/user_detail/")
        request.user = self.user

        response = views.user_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "here are your last checks")
        self.assertContains(response, "Sosnowiec")
        self.assertTemplateUsed("accounts:user_detail.html")

    def test_promotion_page_free_user(self):
        # loging in instead of factory + user => otherwise cannot tets template
        self.client.login(username="testuser", password="admin")
        response = self.client.get("/accounts/promotion/")

        self.assertTemplateUsed("accounts/promotion.html")
        self.assertContains(response, "You have free account right now!")

    def test_toggle_user_promotion(self):
        request = self.factory.get(reverse("accounts:toggle"))
        request.user = self.user

        views.toggle_user_promotion(request)
        user_after_toggle = CustomUser.objects.all().last()
        self.assertEqual(user_after_toggle.promotion, True)
