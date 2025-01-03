from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta


# Tests para el inicio de sesion del usuario
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')
        self.user = CustomUser.objects.create_user(
            username='TestUsername',
            first_name='TestFirstName',
            last_name='TestLastName',
            user_type='student',
            email='test@email.com',
            password='TestPassword'
        )
        self.data = {
            'email': 'test@email.com',
            'password': 'TestPassword'
        }

    def test_login_successful(self):
        """
        Prueba de inicio de sesión exitoso.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_login_invalid_email(self):
        """
        Prueba de inicio de sesión con correo electrónico incorrecto.
        """
        self.data['email'] = 'WrongEmail'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_login_invalid_password(self):
        """
        Prueba de inicio de sesión con contraseña incorrecta.
        """
        self.data['password'] = 'WrongPassword'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_login_account_locked(self):
        """
        Prueba de inicio de sesión con cuenta bloqueada tras tres intentos fallidos.
        """
        self.user.failed_login_attempts = 3
        self.user.last_failed_login = timezone.now()
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_login_reset_failed_attempts(self):
        """
        Prueba de restablecimiento de intentos fallidos tras inicio de sesión exitoso.
        """
        self.user.failed_login_attempts = 2
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 0)
