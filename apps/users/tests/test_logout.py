from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from rest_framework.authtoken.models import Token


class LogoutTestCase(TestCase):
    """
    Test case para el endpoint de cierre de sesión.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('logout')
        self.user = CustomUser.objects.create_user(
            username='TestUsername',
            first_name='TestFirstName',
            last_name='TestLastName',
            user_type='student',
            email='test@email.com',
            password='TestPassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_logout_successful(self):
        """
        Prueba de cierre de sesión exitoso.

        Verifica que el endpoint responda con un código de estado
        200 cuando el usuario está autenticado y se cierra la sesión.
        """
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_logout_without_token(self):
        """
        Prueba de cierre de sesión sin token.

        Verifica que el endpoint responda con un código de estado
        401 cuando no se proporciona un token de autenticación.
        """
        self.client.credentials()
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
