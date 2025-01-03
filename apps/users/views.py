from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from apps.core.utils.serializer_validation import serializer_validation
from .serializers import UserValidationSerializer, UserResponseSerializer
from .models import CustomUser
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
        return Response(
            validation_error,
            status=status.HTTP_400_BAD_REQUEST
        )
    
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
