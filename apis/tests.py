import json

from accounts.models import CustomUser
from django.urls import reverse
from measurements.models import Measurement
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from .views import SingleMeasurementView


class ApiViewsTest(APITestCase):
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
        cls.factory = APIRequestFactory()
        cls.my_admin = CustomUser.objects.create_superuser(username="admin", password="adminadmin", age=27)

    def test_main_view_logged_out_user(self):
        response = self.client.get(reverse("apis:main_api_view"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # viewable by authenticated users
        self.assertContains(response, "users")
        self.assertContains(response, "measurements")

    #!tests of measurements model view
    def test_measurements_logged_out_user(self):
        response = self.client.get(reverse("apis:measurements_list"), follow=True)
        response_detail = self.client.get(reverse("apis:measurement-detail", args=[1]))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_detail.status_code, 403)

    def test_measurements_list_logged_in_user(self):
        """testing detail view for measurements_list with user logged in"""

        self.client.login(username="testuser", password="admin")
        response = self.client.get(reverse("apis:measurements_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.record.starting_location)
        self.assertContains(response, '"measurement_url":"http://testserver/api/measurements/1/"')
        self.assertContains(response, '"user":"testuser"')

    def test_measurements_detail_response(self):
        """testing detail view for measurement-detail with user logged in"""

        request = self.factory.get(reverse("apis:measurement-detail", args=["1"]))
        view = SingleMeasurementView.as_view()
        force_authenticate(request, user=self.user)
        response = view(request, pk="1")

        self.assertContains(response, '"measurement_url":"http://testserver/api/measurements/1/"')
        self.assertContains(response, '"starting_location":"Sosnowiec"')

    def test_measurements_detail_object_not_exist(self):

        self.client.login(username="testuser", password="admin")
        response = self.client.get(reverse("apis:measurement-detail", args=["30"]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #! tests of UserModel views
    def test_users_logged_out_user(self):
        """confirming that not logged in user wont see users api content"""

        response = self.client.get(reverse("apis:user_list"))
        response_detail = self.client.get(reverse("apis:customuser-detail", args=[1]))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_detail.status_code, 403)

    def test_users_logged_in_user_not_admin(self):
        """confirming that logged in user who is not admin wont see users' api content"""

        self.client.login(username="testuser", password="admin")
        response = self.client.get(reverse("apis:user_list"))
        response_detail = self.client.get(reverse("apis:customuser-detail", args=[1]))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_detail.status_code, 403)

    def test_users_list_logged_in_user_admin(self):
        """confirming that logged in user who is admin will see users' list api content"""

        self.client.login(username="admin", password="adminadmin")
        response = self.client.get(reverse("apis:user_list"))
        resp_content = json.loads(response.content)

        resp_content = resp_content["results"][0].get("measurements")
        # OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('measurements', ['http://testserver/api/measurements/1/']),
        expected_url = ["http://testserver/api/measurements/1/"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_content, expected_url)

    def test_users_detail_logged_in_user_admin(self):
        """confirming that logged in user who is admin will see users' list api content"""

        self.client.login(username="admin", password="adminadmin")
        response = self.client.get(reverse("apis:customuser-detail", args=[1]))
        resp_content = json.loads(response.content)

        resp_content = resp_content.get("measurements")
        # .{'id': 1, 'measurements': ['http://testserver/api/measurements/1/'], etc
        expected_url = ["http://testserver/api/measurements/1/"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_content, expected_url)
