from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Company
from apps.job_offers.models import JobOffer
from rest_framework.authtoken.models import Token


class FilterJobOffersTestCase(TestCase):
    """
    Test case para el endpoint de filtrado de ofertas de trabajo.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('filter_job_offers')
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


    def test_filter_job_offers_by_location(self):
        """
        Prueba de filtrado de ofertas de trabajo por ubicación.

        Verifica que el endpoint responda con un código de estado
        200 cuando se filtran correctamente las ofertas de trabajo por ubicación.
        """
        response = self.client.get(self.url, {'location': 'Test Location 1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']['job_offers']), 1)


    def test_filter_job_offers_by_company(self):
        """
        Prueba de filtrado de ofertas de trabajo por compañía.

        Verifica que el endpoint responda con un código de estado
        200 cuando se filtran correctamente las ofertas de trabajo por compañía.
        """
        response = self.client.get(self.url, {'company': 'Test Company'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']['job_offers']), 2)


    def test_filter_job_offers_by_salary_range(self):
        """
        Prueba de filtrado de ofertas de trabajo por rango de salario.

        Verifica que el endpoint responda con un código de estado
        200 cuando se filtran correctamente las ofertas de trabajo por rango de salario.
        """
        response = self.client.get(self.url, {'min_salary': 55000, 'max_salary': 65000}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']['job_offers']), 1)


    def test_filter_job_offers_by_requirements(self):
        """
        Prueba de filtrado de ofertas de trabajo por requisitos.

        Verifica que el endpoint responda con un código de estado
        200 cuando se filtran correctamente las ofertas de trabajo por requisitos.
        """
        response = self.client.get(self.url, {'requirements': 'Test Requirement 1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']['job_offers']), 1)


    def test_filter_job_offers_by_work_mode(self):
        """
        Prueba de filtrado de ofertas de trabajo por modo de trabajo.

        Verifica que el endpoint responda con un código de estado
        200 cuando se filtran correctamente las ofertas de trabajo por modo de trabajo.
        """
        response = self.client.get(self.url, {'work_mode': 'hybrid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']['job_offers']), 1)


    def test_filter_job_offers_by_is_closed(self):
        """
        Prueba de filtrado de ofertas de trabajo por estado de cierre.

        Verifica que el endpoint responda con un código de estado
        200 cuando se filtran correctamente las ofertas de trabajo por estado de cierre.
        """
        response = self.client.get(self.url, {'is_closed': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']['job_offers']), 2)


    def test_filter_job_offers_by_created_at(self):
        """
        Prueba de filtrado de ofertas de trabajo por fecha de creación.

        Verifica que el endpoint responda con un código de estado
        200 cuando se filtran correctamente las ofertas de trabajo por fecha de creación.
        """
        response = self.client.get(self.url, {'created_at': self.job_offer1.created_at.date()}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']['job_offers']), 2)


    def test_filter_job_offers_by_updated_at(self):
        """
        Prueba de filtrado de ofertas de trabajo por fecha de actualización.

        Verifica que el endpoint responda con un código de estado
        200 cuando se filtran correctamente las ofertas de trabajo por fecha de actualización.
        """
        response = self.client.get(self.url, {'updated_at': self.job_offer1.updated_at.date()}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']['job_offers']), 2)


    def test_filter_job_offers_without_token(self):
        """
        Prueba de filtrado de ofertas de trabajo sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta filtrar ofertas de trabajo sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.get(self.url, {'location': 'Test Location 1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
