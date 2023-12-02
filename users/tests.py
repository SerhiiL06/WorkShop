from django.test import TestCase
from .models import User


class RegisterTestCase(TestCase):
    def test_register(self):
        data = {
            "username": "test",
            "password1": "TestThis123",
            "password2": "TestThis123",
        }

        wrong_data = {
            "username": "test1",
            "password1": "TestThis123",
            "password2": "TestThis122",
        }

        path = "http://127.0.0.1:8000/accounts/users/register/"

        response = self.client.post(path=path, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

        wrong_response = self.client.post(path, data=wrong_data)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(wrong_response.status_code, 400)
