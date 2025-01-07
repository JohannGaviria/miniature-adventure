from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, Student
from rest_framework.authtoken.models import Token


class AddStudentDataTestCase(TestCase):
    """
    Test case para el endpoint de agregar datos del estudiante.
    """
    def setUp(self):
        """
        Configuración inicial de los casos de prueba.
        """
        self.client = APIClient()
        self.url = reverse('add_student_data')
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
        self.data = {
            'university': 'Test University',
            'degree': 'Test Degree',
            'major': 'Test Major',
            'graduation_year': 2025,
            'professional_experience': 'Test Experience',
            'about_me': 'Test About Me',
        }


    def test_add_student_data_successful(self):
        """
        Prueba la incorporación exitosa de datos de estudiantes.

        Verifica que el endpoint responda con un código de estado
        201 cuando se proporcionan datos válidos de estudiantes y
        el usuario está autenticado.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_add_student_data_invalid_data(self):
        """
        Prueba de agregar datos de estudiante con datos no válidos.

        Verifica que el endpoint responda con un código de estado
        400 cuando se proporcionan datos no válidos de estudiantes.
        """
        invalid_data = {'graduation_year': 'invalid_year'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
        

    def test_add_student_data_non_student_user(self):
        """
        Prueba de agregar datos de estudiante con un usuario no estudiante.

        Verifica que el endpoint responda con un código de estado
        403 cuando se intenta agregar datos de estudiantes con un
        usuario que no es de tipo estudiante.
        """
        self.user.user_type = 'company'
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_add_student_data_existing_data(self):
        """
        Prueba de agregar datos de estudiante con datos existentes.

        Verifica que el endpoint responda con un código de estado
        400 cuando se intenta agregar datos de estudiantes y ya
        existen datos de estudiantes para el usuario.
        """
        Student.objects.create(
            university='Test University',
            degree='Test Degree',
            major='Test Major',
            graduation_year=2025,
            professional_experience='Test Experience',
            about_me='Test About Me',
            user=self.user
        )
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_add_student_data_without_token(self):
        """
        Prueba de agregar datos de estudiante sin token de autenticación.

        Verifica que el endpoint responda con un código de estado
        401 cuando se intenta agregar datos de estudiantes sin un
        token de autenticación.
        """
        self.client.credentials()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
