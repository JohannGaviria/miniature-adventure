from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Company, Student
from apps.job_offers.models import JobOffer
from apps.postulations.models import Postulation
from rest_framework.authtoken.models import Token


class AcceptRejectPostulationTestCase(TestCase):
    """
    Test case para el endpoint de aceptación o rechazo de postulaciones a ofertas de trabajo.
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
        self.student_user = CustomUser.objects.create_user(
            username='TestStudent',
            first_name='TestFirstName',
            last_name='TestLastName',
            user_type='student',
            email='teststudent@email.com',
            password='TestPassword'
        )
        self.student = Student.objects.create(
            university='Test University',
            degree='Test Degree',
            major='Test Major',
            graduation_year=2025,
            professional_experience='Test Experience',
            about_me='Test About Me',
            user=self.student_user
        )
        self.postulation = Postulation.objects.create(
            student=self.student,
            job_offer=self.job_offer
        )
        self.url = reverse('accept_reject_postulation', kwargs={'job_offer_id': self.job_offer.id})


    def test_accept_postulation_successful(self):
        """
        Prueba de aceptación de postulación a oferta de trabajo exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se acepta correctamente una postulación a una oferta de trabajo.
        """
        data = [{'id': str(self.postulation.id), 'status': 'accept'}]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.postulation.refresh_from_db()
        self.assertEqual(self.postulation.status, 'accepted')


    def test_reject_postulation_successful(self):
        """
        Prueba de rechazo de postulación a oferta de trabajo exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se rechaza correctamente una postulación a una oferta de trabajo.
        """
        data = [{'id': str(self.postulation.id), 'status': 'reject'}]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.postulation.refresh_from_db()
        self.assertEqual(self.postulation.status, 'rejected')


    def test_accept_reject_postulation_invalid_uuid(self):
        """
        Prueba de aceptación o rechazo de postulación a oferta de trabajo con UUID inválido.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporciona un UUID inválido.
        """
        data = [{'id': 'invalid-uuid', 'status': 'accept'}]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_accept_reject_postulation_not_found(self):
        """
        Prueba de aceptación o rechazo de postulación a oferta de trabajo no encontrada.

        Verifica que el endpoint responda con un código de estado
        404 cuando no se encuentra la postulación.
        """
        data = [{'id': 'e23cbcc5-6a30-4008-bcef-4536414e744f', 'status': 'accept'}]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_accept_reject_postulation_non_company_user(self):
        """
        Prueba de aceptación o rechazo de postulación a oferta de trabajo con un usuario no compañía.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta aceptar o rechazar una postulación a una oferta de trabajo con un
        usuario que no es de tipo compañía.
        """
        self.user.user_type = 'student'
        self.user.save()
        data = [{'id': str(self.postulation.id), 'status': 'accept'}]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_accept_reject_postulation_invalid_action(self):
        """
        Prueba de aceptación o rechazo de postulación a oferta de trabajo con acción inválida.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporciona una acción inválida.
        """
        data = [{'id': str(self.postulation.id), 'status': 'invalid_action'}]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_accept_reject_postulation_not_creator(self):
        """
        Prueba de aceptación o rechazo de postulación a oferta de trabajo por un usuario que no es el creador.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta aceptar o rechazar una postulación a una oferta de trabajo por un
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
        Company.objects.create(
            name='Other Company',
            industry='Tech',
            location='Other Location',
            description='Other Description',
            user=other_user
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        data = [{'id': str(self.postulation.id), 'status': 'accept'}]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)



    def test_accept_reject_postulation_without_token(self):
        """
        Prueba de aceptación o rechazo de postulación a oferta de trabajo sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta aceptar o rechazar una postulación a una oferta de trabajo sin un
        token de autenticación.
        """
        self.client.credentials()
        data = [{'id': str(self.postulation.id), 'status': 'accept'}]
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
