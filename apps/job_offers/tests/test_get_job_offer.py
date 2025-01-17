from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Company
from apps.job_offers.models import JobOffer
from rest_framework.authtoken.models import Token
from faker import Faker

fake = Faker()


class GetJobOfferTestCase(TestCase):
    """
    Test case para el endpoint de obtención de ofertas de trabajo.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
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
        self.job_offer = JobOffer.objects.create(
            title='Test Job Offer',
            description='Test Description',
            requirements='Test Requirement',
            location='Test Location',
            salary=50000,
            work_mode='hybrid',
            company=self.company
        )
        self.url = reverse('get_job_offer', kwargs={'job_offer_id': self.job_offer.id})


    def test_get_job_offer_successful(self):
        """
        Prueba de obtención de oferta de trabajo exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se obtiene correctamente la oferta de trabajo.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_get_job_offer_not_found(self):
        """
        Prueba de obtención de oferta de trabajo no encontrada.

        Verifica que el endpoint responda con un código de estado
        404 cuando no se encuentra la oferta de trabajo.
        """
        url = reverse('get_job_offer', kwargs={'job_offer_id': 'e23cbcc5-6a30-4008-bcef-4536414e744f'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_get_job_offer_invalid_uuid(self):
        """
        Prueba de obtención de oferta de trabajo con UUID inválido.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporciona un UUID inválido.
        """
        url = reverse('get_job_offer', kwargs={'job_offer_id': 'invalid-uuid'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_get_job_offer_without_token(self):
        """
        Prueba de obtención de oferta de trabajo sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta obtener una oferta de trabajo sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
