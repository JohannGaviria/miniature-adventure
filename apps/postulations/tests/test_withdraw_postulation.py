from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Student, Company
from apps.job_offers.models import JobOffer
from apps.postulations.models import Postulation
from rest_framework.authtoken.models import Token


class WithdrawPostulationTestCase(TestCase):
    """
    Test case para el endpoint de retiro de postulación a ofertas de trabajo.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='TestStudent',
            first_name='TestFirstName',
            last_name='TestLastName',
            user_type='student',
            email='teststudent@email.com',
            password='TestPassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.student = Student.objects.create(
            university='Test University',
            degree='Test Degree',
            major='Test Major',
            graduation_year=2025,
            professional_experience='Test Experience',
            about_me='Test About Me',
            user=self.user
        )
        self.company_user = CustomUser.objects.create_user(
            username='TestCompany',
            first_name='TestFirstName',
            last_name='TestLastName',
            user_type='company',
            email='testcompany@email.com',
            password='TestPassword'
        )
        self.company = Company.objects.create(
            name='Test Company',
            industry='Tech',
            location='Test Location',
            description='Test Description',
            user=self.company_user
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
        self.postulation = Postulation.objects.create(
            student=self.student,
            job_offer=self.job_offer
        )
        self.url = reverse('withdraw_postulation', kwargs={'job_offer_id': self.job_offer.id})


    def test_withdraw_postulation_successful(self):
        """
        Prueba de retiro de postulación a oferta de trabajo exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se retira correctamente la postulación a una oferta de trabajo.
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertFalse(Postulation.objects.filter(student=self.student, job_offer=self.job_offer).exists())


    def test_withdraw_postulation_invalid_uuid(self):
        """
        Prueba de retiro de postulación a oferta de trabajo con UUID inválido.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporciona un UUID inválido.
        """
        url = reverse('withdraw_postulation', kwargs={'job_offer_id': 'invalid-uuid'})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_withdraw_postulation_not_found(self):
        """
        Prueba de retiro de postulación a oferta de trabajo no encontrada.

        Verifica que el endpoint responda con un código de estado
        404 cuando no se encuentra la oferta de trabajo.
        """
        url = reverse('withdraw_postulation', kwargs={'job_offer_id': 'e23cbcc5-6a30-4008-bcef-4536414e744f'})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_withdraw_postulation_non_student_user(self):
        """
        Prueba de retiro de postulación a oferta de trabajo con un usuario no estudiante.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta retirar la postulación a una oferta de trabajo con un
        usuario que no es de tipo estudiante.
        """
        self.user.user_type = 'company'
        self.user.save()
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_withdraw_postulation_not_postulated(self):
        """
        Prueba de retiro de postulación a oferta de trabajo no postulada.

        Verifica que el endpoint responda con un código de estado
        400 cuando se intenta retirar la postulación a una oferta de trabajo a la que
        no se ha postulado anteriormente.
        """
        self.postulation.delete()
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_withdraw_postulation_closed_job_offer(self):
        """
        Prueba de retiro de postulación a oferta de trabajo cerrada.

        Verifica que el endpoint responda con un código de estado
        400 cuando se intenta retirar la postulación a una oferta de trabajo cerrada.
        """
        self.job_offer.is_closed = True
        self.job_offer.save()
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_withdraw_postulation_without_token(self):
        """
        Prueba de retiro de postulación a oferta de trabajo sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta retirar la postulación a una oferta de trabajo sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
