from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Student
from rest_framework.authtoken.models import Token


class UpdateStudentDataTestCase(TestCase):
    """
    Test case para el endpoint de actualizar datos del estudiante.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('update_student_data')
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
        self.data = {
            'university': 'Updated University',
            'degree': 'Updated Degree',
            'major': 'Updated Major',
            'graduation_year': 2026,
            'professional_experience': 'Updated Experience',
            'about_me': 'Updated About Me'
        }


    def test_update_student_data_successful(self):
        """
        Prueba de actualización de datos del estudiante exitosa.

        Verifica que el endpoint responda con un código de estado
        200 cuando se actualizan correctamente los datos del estudiante.
        """
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_student_data_invalid_data(self):
        """
        Prueba de actualización de datos del estudiante con datos no válidos.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporcionan datos no válidos de estudiantes.
        """
        invalid_data = {'graduation_year': 'invalid_year'}
        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_update_student_data_non_student_user(self):
        """
        Prueba de actualización de datos del estudiante con un usuario no estudiante.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta actualizar datos del estudiante con un
        usuario que no es de tipo estudiante.
        """
        self.user.user_type = 'company'
        self.user.save()
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_student_data_not_found(self):
        """
        Prueba de actualización de datos del estudiante no encontrados.

        Verifica que el endpoint responda con un código de estado
        404 cuando no se encuentran datos del estudiante para el usuario.
        """
        self.student_data.delete()
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_update_student_data_without_token(self):
        """
        Prueba de actualización de datos del estudiante sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta actualizar datos del estudiante sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
