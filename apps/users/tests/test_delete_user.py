from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from rest_framework.authtoken.models import Token


class DeleteUserTestCase(TestCase):
    """
    Test case para el endpoint de eliminación de usuario.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('delete_user')
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


    def test_delete_user_successful(self):
        """
        Prueba la eliminación exitosa de usuario.

        Verifica que el endpoint responda con un código de estado
        200 cuando el usuario está autenticado y se elimina el usuario.
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertFalse(CustomUser.objects.filter(email='test@email.com').exists())


    def test_delete_user_without_token(self):
        """
        Prueba la eliminación de usuario sin token.

        Verifica que el endpoint responda con un código de estado
        401 cuando no se proporciona un token de autenticación.
        """
        self.client.credentials()
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
