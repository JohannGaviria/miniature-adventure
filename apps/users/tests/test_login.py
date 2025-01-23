from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from django.utils import timezone


class LoginTestCase(TestCase):
    """
    Test case para el endpoint de inicio de sesión.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
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

        Verifica que el endpoint responda con un código de estado
        200 cuando se proporcionan credenciales válidas.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_login_invalid_email(self):
        """
        Prueba de inicio de sesión con correo electrónico incorrecto.

        Verifica que el endpoint responda con un código de estado
        401 cuando se proporciona un correo electrónico incorrecto.
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

        Verifica que el endpoint responda con un código de estado
        401 cuando se proporciona una contraseña incorrecta.
        """
        self.data['password'] = 'WrongPassword'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_login_account_locked(self):
        """
        Prueba de inicio de sesión con cuenta bloqueada.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta iniciar sesión con una cuenta
        bloqueada por exceso de intentos fallidos.
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
        Prueba de restablecimiento de intentos fallidos.

        Verifica que el contador de intentos fallidos se restablezca
        a 0 cuando se inicia sesión correctamente.
        """
        self.user.failed_login_attempts = 2
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 0)
