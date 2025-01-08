from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Company
from rest_framework.authtoken.models import Token


class GetCompanyDataTestCase(TestCase):
    """
    Test case para el endpoint de obtener datos de la compañia.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('get_company_data')
        self.user = CustomUser.objects.create_user(
            username='TestUsername',
            first_name='TestFirstName',
            last_name='TestLastName',
            user_type='company',
            email='test@email.com',
            password='TestPassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.company_data = Company.objects.create(
            name='Test Company Name',
            industry='technology',
            location='Test Location',
            description='Test Description',
            user=self.user
        )


    def test_get_company_data_successful(self):
        """
        Prueba de obtención de datos de la compañia exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se obtienen correctamente los datos de la compañia.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_get_company_data_non_company_user(self):
        """
        Prueba de obtención de datos de la compañia con un usuario no estudiante.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta obtener datos de la compañia con un
        usuario que no es de tipo compañia.
        """
        self.user.user_type = 'student'
        self.user.save()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_get_company_data_not_found(self):
        """
        Prueba de obtención de datos de la compañia no encontrados.

        Verifica que el endpoint responda con un código de estado
        404 cuando no se encuentran datos de la compañia para el usuario.
        """
        self.company_data.delete()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_get_company_data_without_token(self):
        """
        Prueba de obtención de datos de la compañia sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta obtener datos de la compañia sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
