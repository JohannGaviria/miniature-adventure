from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Company
from apps.job_offers.models import JobOffer
from rest_framework.authtoken.models import Token


class GetAllJobOffersTestCase(TestCase):
    """
    Test case para el endpoint de obtención de todas las ofertas de trabajo.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('get_all_job_offers')
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
        self.job_offer1 = JobOffer.objects.create(
            title='Test Job Offer 1',
            description='Test Description 1',
            requirements='Test Requirement 1',
            location='Test Location 1',
            salary=50000,
            work_mode='hybrid',
            company=self.company
        )
        self.job_offer2 = JobOffer.objects.create(
            title='Test Job Offer 2',
            description='Test Description 2',
            requirements='Test Requirement 2',
            location='Test Location 2',
            salary=60000,
            work_mode='remote',
            company=self.company
        )


    def test_get_all_job_offers_successful(self):
        """
        Prueba de obtención de todas las ofertas de trabajo exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se obtienen correctamente todas las ofertas de trabajo.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']), 2)


    def test_get_all_job_offers_without_token(self):
        """
        Prueba de obtención de todas las ofertas de trabajo sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta obtener todas las ofertas de trabajo sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
