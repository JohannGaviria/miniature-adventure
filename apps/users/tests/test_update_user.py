from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from rest_framework.authtoken.models import Token


class UpdateUserTestCase(TestCase):
    """
    Test case para el endpoint de actualización de datos de usuario.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('update_user')
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
        self.data = {
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName'
        }


    def test_update_user_successful(self):
        """
        Prueba de actualización de datos del usuario con éxito.

        Verifica que el endpoint responda con un código de estado
        200 cuando se proporcionan datos válidos de usuario y
        el usuario está autenticado.
        """
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_update_user_invalid_data(self):
        """
        Prueba de actualización de datos del usuario con datos no válidos.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporcionan datos no válidos de usuario.
        """
        invalid_data = {'email': 'invalidemail'}
        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_user_without_token(self):
        """
        Prueba de actualización de datos del usuario sin token.

        Verifica que el endpoint responda con un código de estado
        401 cuando no se proporciona un token de autenticación.
        """
        self.client.credentials()
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
