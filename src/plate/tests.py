import re
import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from .validators import validate_amount_qs
from .services import generate_plate
from .utils import generate_plate_number
from .models import Plate, PlateArea


class ValidatorsTestCase(TestCase):

    def test_validate_amount_qs__is_zero(self):
        self.assertEqual(validate_amount_qs(0), 1)

    def test_validate_amount_qs__is_empty(self):
        self.assertEqual(validate_amount_qs(''), 1)

    def test_validate_amount_qs__is_not_digit(self):
        self.assertRaises(ValidationError, validate_amount_qs, amount='0.1')


class ServicesTestCase(TestCase):
    def test_generate_plate_length(self):
        self.assertEqual(2, len(generate_plate(plate_amount_qs=2)))

    def test_generate_plate_dict_keys(self):
        plate = generate_plate(1).pop()
        self.assertEqual(["plate", "area"], list(plate.keys()))


class UtilsTestCase(TestCase):
    def test_generate_plate_number__regex_match__correct(self):
        self.assertTrue(re.match(r"^[АВЕКМНОРСТУХ]{1}\d{3}[АВЕКМНОРСТУХ]{2}$", generate_plate_number()))

    def test_generate_plate_number__regex_match__incorrect(self):
        self.assertFalse(re.match(r"^[АВЕКМНОРСТУХ]{1}\d{3}[АВЕКМНОРСТУХ]{2}$", "В122В0"))


class PlateAPITestsCase(APITestCase):

    def test_generate_plate__token_not_provided(self):
        response = self.client.get('/plate/generate/')
        self.assertTrue(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_generate_plate__token_provided(self):
        User.objects.create_user(
            username="test_user",
            email="test_email@gmail.com",
            password="test_password",
        )
        access_token = self.client.post(
            "/api/token/",
            data={
                "username": "test_user",
                "password": "test_password"
            },
            format="json").json()["access"]

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = client.get('/plate/generate/')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.json()))

        response = client.get('/plate/generate/?amount=5')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(5, len(response.json()))

    def test_get_plate__token_provided(self):
        User.objects.create_user(
            username="test_user",
            email="test_email@gmail.com",
            password="test_password",
        )
        access_token = self.client.post(
            "/api/token/",
            data={
                "username": "test_user",
                "password": "test_password"
            },
            format="json").json()["access"]
        plate_area = PlateArea.objects.create(code="001", region="Test Region")
        plate = Plate.objects.create(plate_number="С111СС", plate_area=plate_area)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = client.get(f'/plate/get/{plate.pk}/')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json().get("plate_number"), plate.plate_number)

        qs_plate_response = client.get(f'/plate/get/?id={plate.pk}')
        self.assertEqual(status.HTTP_200_OK, qs_plate_response.status_code)
        self.assertEqual(qs_plate_response.json().get("plate_number"), plate.plate_number)

        not_exist_plate_response = client.get(f'/plate/get/{uuid.uuid4()}/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, not_exist_plate_response.status_code)

    def test_plate_add(self):
        User.objects.create_user(username="test_user", email="test_email@gmail.com", password="test_password")
        access_token = self.client.post(
            "/api/token/",
            data={
                "username": "test_user",
                "password": "test_password"
            },
            format="json").json()["access"]

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertFalse(Plate.objects.all().count())
        response = client.post('/plate/add/', data={"plate_number": "С111СС", "plate_area": "01"}, format="json")
        self.assertEqual(Plate.objects.all().count(), 1)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
