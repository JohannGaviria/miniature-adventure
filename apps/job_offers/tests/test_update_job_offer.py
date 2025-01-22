from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Company
from apps.job_offers.models import JobOffer
from rest_framework.authtoken.models import Token


class UpdateJobOfferTestCase(TestCase):
    """
    Test case para el endpoint de actualización de ofertas de trabajo.
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
        self.url = reverse('update_job_offer', kwargs={'job_offer_id': self.job_offer.id})
        self.data = {
            'title': 'Updated Job Offer',
            'description': 'Updated Description',
            'requirements': 'Updated Requirement',
            'location': 'Updated Location',
            'salary': 60000,
            'work_mode': 'remote'
        }


    def test_update_job_offer_successful(self):
        """
        Prueba de actualización de oferta de trabajo exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se actualiza correctamente la oferta de trabajo.
        """
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_job_offer_not_found(self):
        """
        Prueba de actualización de oferta de trabajo no encontrada.

        Verifica que el endpoint responda con un código de estado
        404 cuando no se encuentra la oferta de trabajo.
        """
        url = reverse('update_job_offer', kwargs={'job_offer_id': 'e23cbcc5-6a30-4008-bcef-4536414e744f'})
        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_job_offer_invalid_uuid(self):
        """
        Prueba de actualización de oferta de trabajo con UUID inválido.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporciona un UUID inválido.
        """
        url = reverse('update_job_offer', kwargs={'job_offer_id': 'invalid-uuid'})
        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_job_offer_non_company_user(self):
        """
        Prueba de actualización de oferta de trabajo con un usuario no compañía.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta actualizar una oferta de trabajo con un
        usuario que no es de tipo compañía.
        """
        self.user.user_type = 'student'
        self.user.save()
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_job_offer_not_creator(self):
        """
        Prueba de actualización de oferta de trabajo por un usuario que no es el creador.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta actualizar una oferta de trabajo por un
        usuario que no es el creador de la oferta.
        """
        other_user = CustomUser.objects.create_user(
            username='OtherCompany',
            first_name='OtherFirstName',
            last_name='OtherLastName',
            user_type='company',
            email='othercompany@email.com',
            password='OtherPassword'
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)

    
    def test_update_job_offer_invalid_data(self):
        """
        Prueba de actualización de oferta de trabajo con datos no válidos.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporcionan datos no válidos de la oferta de trabajo.
        """
        invalid_data = {'title': ''}
        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)

    
    def test_update_job_offer_duplicate(self):
        """
        Prueba de actualización de oferta de trabajo duplicada.

        Verifica que el endpoint responda con un código de estado
        400 cuando se intenta actualizar una oferta de trabajo con datos
        que ya existen en otra oferta de trabajo.
        """
        other_job_offer = JobOffer.objects.create(
            title='Other Job Offer',
            description='Other Description',
            requirements='Other Requirement',
            location='Other Location',
            salary=70000,
            work_mode='remote',
            company=self.company
        )
        self.data['title'] = other_job_offer.title
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_job_offer_without_token(self):
        """
        Prueba de actualización de oferta de trabajo sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta actualizar una oferta de trabajo sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
