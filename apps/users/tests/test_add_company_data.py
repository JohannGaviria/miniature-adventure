from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Company
from rest_framework.authtoken.models import Token


class AddCompanyDataTestCase(TestCase):
    """
    Test case para el endpoint de agregar datos de la compañia.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('add_company_data')
        self.user = CustomUser.objects.create_user(
            username='TestUsername',
            first_name='TestFirstName',
            last_name='TestLastName',
            user_type='company',
            email='test@email.com',
            password='TestPassword',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data = {
            'name': 'Test Company Name',
            'industry': 'technology',
            'location': 'Test Location',
            'description': 'Test Description'
        }


    def test_add_company_data_successful(self):
        """
        Prueba la incorporación exitosa de datos de compañias.

        Verifica que el endpoint responda con un código de estado
        201 cuando se proporcionan datos válidos de compañia y
        el usuario está autenticado.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_add_company_data_invalid_data(self):
        """
        Prueba de agregar datos de compañia con datos no válidos.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporcionan datos no válidos de compañias.
        """
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
        

    def test_add_company_data_non_company_user(self):
        """
        Prueba de agregar datos de compañia con un usuario no compañia.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta agregar datos de compañias con un
        usuario que no es de tipo compañia.
        """
        self.user.user_type = 'student'
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_add_company_data_existing_data(self):
        """
        Prueba de agregar datos de compañia con datos existentes.

        Verifica que el endpoint responda con un código de estado
        400 cuando se intenta agregar datos de compañias y ya
        existen datos de compañias para el usuario.
        """
        Company.objects.create(
            name='Test Company Name',
            industry='technology',
            location='Test Location',
            description='Test Description',
            user=self.user
        )
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_add_company_data_without_token(self):
        """
        Prueba de agregar datos de compañia sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta agregar datos de compañias sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
