from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from apps.core.utils.serializer_validation import serializer_validation
from apps.core.utils.validate_user_is_creator import validate_user_is_creator
from apps.core.utils.get_model_data import get_model_data
from .serializers import (UserValidationSerializer, UserResponseSerializer,
                          StudentValidationSerializer, StudentResponseSerializer,
                          CompanyValidationSerializer, CompanyResponseSerializer)
from .models import CustomUser, Student, Company
from .utils.validator_users_type import validate_user_type
from .utils.validator_existing_data import validate_existing_data
from .utils.upload_file_cloudinary import upload_cv_to_cloudinary
from datetime import timedelta


# Endpoint para el registro de usuario
@api_view(['POST'])
def register(request):
    # Obtiene los datos enviados en la petición
    user_validation_serializer = UserValidationSerializer(data=request.data)

    # Obtiene la validación del serializer
    validation_error = serializer_validation(user_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return validation_error
    
    # Guarda el usuario en la base de datos
    user_validation_serializer.save()

    # Retorna un mensaje de éxito si el usuario se guardó correctamente
    return Response({
        'status': 'success',
        'message': 'User registered successfully'
    }, status=status.HTTP_201_CREATED)


# Endpoint para el inicio de sesión de usuario
@api_view(['POST'])
def login(request):
    # Obtiene los datos enviados en la petición
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        # Obtiene el usuario por el correo electrónico
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        # Retorna un mensaje de error por usuario no encontrado
        return Response({
            'status': 'errors',
            'message': 'Validation failed',
            'errors': {
                'email': [
                    'Email is incorrect'
                ]
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Verifica si la cuenta está bloqueada
    if user.failed_login_attempts >= 3 and user.last_failed_login and timezone.now() < user.last_failed_login + timedelta(minutes=15):
        # Retorna un mensaje de error por cuenta bloqueada
        return Response({
            'status': 'errors',
            'message': 'Account locked. Try again later.'
        }, status=status.HTTP_403_FORBIDDEN)

    # Verifica la contraseña del usuario
    if not user.check_password(password):
        # Incrementa el contador de intentos fallidos
        user.failed_login_attempts += 1
        user.last_failed_login = timezone.now()
        user.save()

        # Retorna un mensaje de error por contraseña incorrecta
        return Response({
            'status': 'errors',
            'message': 'Validation failed',
            'errors': {
                'password': [
                    'Password is incorrect'
                ]
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Restablece el contador de intentos fallidos en caso de éxito
    user.failed_login_attempts = 0
    user.save()

    # Crea o actualiza el token del usuario
    token, created = Token.objects.get_or_create(user=user)

    # Configura el tiempo de expiración del token
    token_expiration = timezone.now() + timedelta(days=3)

    # Serializa los datos del usuario
    user_response_serializer = UserResponseSerializer(user)

    # Retorna un mensaje de éxito si el usuario se logueó correctamente
    return Response({
        'status': 'success',
        'message': 'User logged in successfully.',
        'data': {
            'token': {
                'token_key': token.key,
                'token_expiration': token_expiration.isoformat()
            },
            'user': user_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint para el cierre de sesión de usuario
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # Obtener el usuario actual
    user = request.user

    # Actualizar los campos
    user.last_login = timezone.now()
    
    # Eliminar el token del usuario
    user.auth_token.delete()
    
    # Guardar el usuario
    user.save()
    
    # Respuesta de cierre de sesión exitoso
    return Response({
        'status': 'success',
        'message': 'User logged out successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint para actualizar los datos del usuario
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    # Obtiene los datos enviados en la petición
    user_validation_serializer = UserValidationSerializer(request.user, data=request.data, partial=True)

    # Obtiene la validación del serializer
    validation_error = serializer_validation(user_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return validation_error

    # Guarda los datos actualizados del usuario
    user_validation_serializer.save()

    # Elimina el token del usuario autenticado
    request.user.auth_token.delete()
    
    # Crea o actualiza el token del usuario
    token, created = Token.objects.get_or_create(user=request.user)

    # Configura el tiempo de expiración del token
    token_expiration = timezone.now() + timedelta(days=3)

    # Serializa los datos del usuario
    user_response_serializer = UserResponseSerializer(request.user)

    # Respuesta de éxito en la actualización de datos del usuario
    return Response({
        'status': 'success',
        'message': 'User data updated successfully.',
        'data': {
            'token': {
                'token_key': token.key,
                'token_expiration': token_expiration.isoformat()
            },
            'user': user_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint para eliminar el usuario
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
    # Elimina el token del usuario autenticado
    request.user.auth_token.delete()

    # Elimina el usuario autenticado
    request.user.delete()

    # Respuesta de eliminación exitoso
    return Response({
        'status': 'success',
        'message': 'User deleted successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint para agregar los datos del estudiante
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_student_data(request):
    # Valida que el usuario autenticado sea de tipo estudiante
    validation_response = validate_user_type(request.user, 'student')
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Valida que los datos del estudiante no existan
    validation_response = validate_existing_data(Student, request.user)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Obtiene el archivo de curriculum vitae
    cv_file = request.FILES.get('cv')

    # Verifica si se envió un archivo de curriculum vitae
    if cv_file:
        try:
            # Sube el archivo de curriculum vitae a Cloudinary
            cv_url = upload_cv_to_cloudinary(cv_file)
            # Asigna la URL del curriculum vitae a la petición
            request.data['cv'] = cv_url
        except Exception as e:
            # Retorna un mensaje de error al subir el archivo
            return Response({
                'status': 'error',
                'message': 'Error uploading file',
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Obtiene los datos enviados en la petición
    student_validation_serializer = StudentValidationSerializer(data=request.data, context={'request': request})
    
    # Obtiene la validación del serializer
    validation_error = serializer_validation(student_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return validation_error
    
    # Guarda los datos del estudiante en la base de datos
    student_validation_serializer.save()

    # Retorna un mensaje de exito al agregar los datos del estudiante
    return Response({
        'status': 'success',
        'message': 'Student data added successfully.',
    }, status=status.HTTP_201_CREATED)


# Endpoint para obtener los datos del estudiante
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_student_data(request):
    # Obtener los datos del estudiante
    student_data = get_model_data(Student, 'user', request.user)

    # Verificar si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(student_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return student_data

    # Valida que el usuario sea el estudiante
    validation_response = validate_user_is_creator(student_data, request.user)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Valida que el usuario autenticado sea de tipo estudiante
    validation_response = validate_user_type(request.user, 'student')
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Serializa los datos de respuesta
    student_response_serializer = StudentResponseSerializer(student_data)

    # Retorna un mensaje de exito al obtener los datos del estudiante
    return Response({
        'status': 'success',
        'message': 'Student data was successfully obtained.',
        'data': {
            'student': student_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint para actualizar los datos del estudiante
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_student_data(request):
    # Obtener los datos del estudiante
    student_data = get_model_data(Student, 'user', request.user)

    # Verificar si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(student_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return student_data

    # Valida que el usuario sea el estudiante
    validation_response = validate_user_is_creator(student_data, request.user)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Valida que el usuario autenticado sea de tipo estudiante
    validation_response = validate_user_type(request.user, 'student')
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Obtiene el archivo de curriculum vitae
    cv_file = request.FILES.get('cv')

    # Verifica si se envió un archivo de curriculum vitae
    if cv_file:
        try:
            # Sube el archivo de curriculum vitae a Cloudinary
            cv_url = upload_cv_to_cloudinary(cv_file)
            # Asigna la URL del curriculum vitae a la petición
            request.data['cv'] = cv_url
        except Exception as e:
            # Retorna un mensaje de error al subir el archivo
            return Response({
                'status': 'error',
                'message': 'Error uploading file',
                'errors': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Obtiene los datos enviados en la petición
    student_validation_serializer = StudentValidationSerializer(student_data, data=request.data, partial=True)
    
    # Obtiene la validación del serializer
    validation_error = serializer_validation(student_validation_serializer)
    
    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return validation_error
    
    # Guarda los datos actualizados del estudiante en la base de datos
    student_validation_serializer.save()

    # Retorna un mensaje de éxito al actualizar los datos del estudiante
    return Response({
        'status': 'success',
        'message': 'Student data updated successfully.'
    }, status=status.HTTP_200_OK)


# Endpoint para agregar los datos de la compañia
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_company_data(request):
    # Valida que el usuario autenticado sea de tipo compañia
    validation_response = validate_user_type(request.user, 'company')
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Valida que los datos de la compañia no existan
    validation_response = validate_existing_data(Company, request.user)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Obtiene los datos enviados en la petición
    company_validation_serializer = CompanyValidationSerializer(data=request.data, context={'request': request})
    
    # Obtiene la validación del serializer
    validation_error = serializer_validation(company_validation_serializer)

    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return validation_error
    
    # Guarda los datos de la compañia en la base de datos
    company_validation_serializer.save()

    # Retorna un mensaje de exito al agregar los datos del estudiante
    return Response({
        'status': 'success',
        'message': 'Company data added successfully.',
    }, status=status.HTTP_201_CREATED)


# Endpoint para obtener los datos de la compañia
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_company_data(request):
    # Obtener los datos de la compañia
    company_data = get_model_data(Company, 'user', request.user)

    # Verificar si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(company_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return company_data

    # Valida que el usuario sea el creador
    validation_response = validate_user_is_creator(company_data, request.user)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Valida que el usuario autenticado sea de tipo compañia
    validation_response = validate_user_type(request.user, 'company')
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Serializa los datos de respuesta
    company_response_serializer = CompanyResponseSerializer(company_data)

    # Retorna un mensaje de exito al obtener los datos de la compañia
    return Response({
        'status': 'success',
        'message': 'Company data was successfully obtained.',
        'data': {
            'company': company_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint para actualizar los datos de la compañia
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_company_data(request):
    # Obtener los datos de la compañia
    company_data = get_model_data(Company, 'user', request.user)

    # Verificar si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(company_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return company_data

    # Valida que el usuario sea el creador
    validation_response = validate_user_is_creator(company_data, request.user)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Valida que el usuario autenticado sea de tipo company
    validation_response = validate_user_type(request.user, 'company')
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Obtiene los datos enviados en la petición
    company_validation_serializer = CompanyValidationSerializer(company_data, data=request.data, partial=True)
    
    # Obtiene la validación del serializer
    validation_error = serializer_validation(company_validation_serializer)
    
    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return validation_error
    
    # Guarda los datos actualizados de la compañia en la base de datos
    company_validation_serializer.save()

    # Retorna un mensaje de éxito al actualizar los datos de la compañia
    return Response({
        'status': 'success',
        'message': 'Company data updated successfully.'
    }, status=status.HTTP_200_OK)
