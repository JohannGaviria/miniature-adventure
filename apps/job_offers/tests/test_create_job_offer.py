from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Company
from apps.job_offers.models import JobOffer
from rest_framework.authtoken.models import Token


class CreateJobOfferTestCase(TestCase):
    """
    Test case para el endpoint de creación de ofertas de trabajo.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('create_job_offer')
        self.user = CustomUser.objects.create_user(
            username='TestCompany',
            first_name='TestFirstName',
            last_name='TestLastName',
            user_type='company',
            email='testcompany@email.com',
            password='TestPassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.company = Company.objects.create(
            name='Test Company',
            industry='Tech',
            location='Test Location',
            description='Test Description',
            user=self.user
        )
        self.data = {
            'title': 'Test Job Offer',
            'description': 'Test Description',
            'requirements': 'Test Requirement',
            'location': 'Test Location',
            'salary': 50000,
            'work_mode': 'hybrid',
            'company': self.company.id
        }


    def test_create_job_offer_successful(self):
        """
        Prueba de creación de oferta de trabajo exitosa.

        Verifica que el endpoint responda con un código de estado
        201 cuando se proporciona una oferta de trabajo válida.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_create_job_offer_user_not_profile(self):
        """
        Prueba de creación de oferta de trabajo de un usuario que
        no tiene un perfil de compañia creado.

        Verifica que el endpoint responda con un código de estado
        400 cuando el usuario no tiene un perfil de compañia.
        """
        self.company.delete()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_create_job_offer_duplicate(self):
        """
        Prueba de creación de oferta de trabajo duplicada.

        Verifica que el endpoint responda con un código de estado
        400 cuando se intenta crear una oferta de trabajo duplicada.
        """
        self.client.post(self.url, self.data, format='json')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_create_job_offer_invalid_data(self):
        """
        Prueba de creación de oferta de trabajo con datos no válidos.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporcionan datos no válidos de la oferta de trabajo.
        """
        invalid_data = {'title': ''}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_create_job_offer_non_company_user(self):
        """
        Prueba de creación de oferta de trabajo con un usuario no compañía.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta crear una oferta de trabajo con un
        usuario que no es de tipo compañía.
        """
        self.user.user_type = 'student'
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_create_job_offer_without_token(self):
        """
        Prueba de creación de oferta de trabajo sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta crear una oferta de trabajo sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
