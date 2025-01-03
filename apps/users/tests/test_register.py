from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser


# Tests para el registro de usuario
class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        CustomUser.objects.create(
            username='TestExistingUsername',
            first_name='TestExistingFirstName',
            last_name='TestExistingLastName',
            user_type='student',
            email='testexisting@email.com',
            password='TestPassword'
        )
        self.data = {
            'username': 'TestUsername',
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'user_type': 'student',
            'email': 'test@email.com',
            'password': 'TestPassword',
        }


    def test_register_successful(self):
        """
        Prueba de registro de usuario exitoso.
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)


    def test_register_invalid_data(self):
        """
        Prueba de registro de usuario con datos inválidos.
        """
        invalid_data = {}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_register_existing_username(self):
        """
        Prueba de registro de usuario con nombre de usuario existente.
        """
        self.data['username'] = 'TestExistingUsername'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_register_existing_email(self):
        """
        Prueba de registro de usuario con correo electrónico existente.
        """
        self.data['email'] = 'testexisting@email.com'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_register_whit_invalid_email(self):
        """
        Prueba de registro de usuario con correo electrónico inválido.
        """
        self.data['email'] = 'testemail.com'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)

    
    def test_register_whit_weak_password(self):
        """
        Prueba de registro de usuario con contraseña debil.
        """
        self.data['password'] = '123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)


    def test_register_whit_invalid_user_type(self):
        """
        Prueba de registro de usuario con tipo de usuario inválido.
        """
        self.data['user_type'] = 'invalid'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in response.data)
        self.assertTrue('message' in response.data)
        self.assertTrue('errors' in response.data)
