from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Student
from rest_framework.authtoken.models import Token


class GetStudentDataTestCase(TestCase):
    """
    Test case para el endpoint de obtener datos del estudiante.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('get_student_data')
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
        self.student_data = Student.objects.create(
            university='Test University',
            degree='Test Degree',
            major='Test Major',
            graduation_year=2025,
            professional_experience='Test Experience',
            about_me='Test About Me',
            user=self.user
        )


    def test_get_student_data_successful(self):
        """
        Prueba de obtención de datos del estudiante exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se obtienen correctamente los datos del estudiante.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('data' in response.data)


    def test_get_student_data_non_student_user(self):
        """
        Prueba de obtención de datos del estudiante con un usuario no estudiante.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta obtener datos del estudiante con un
        usuario que no es de tipo estudiante.
        """
        self.user.user_type = 'company'
        self.user.save()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_get_student_data_not_found(self):
        """
        Prueba de obtención de datos del estudiante no encontrados.

        Verifica que el endpoint responda con un código de estado
        404 cuando no se encuentran datos del estudiante para el usuario.
        """
        self.student_data.delete()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_get_student_data_without_token(self):
        """
        Prueba de obtención de datos del estudiante sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta obtener datos del estudiante sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
