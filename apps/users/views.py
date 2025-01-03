from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.core.utils.serializer_validation import serializer_validation
from .serializers import UserValidationSerializer


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
