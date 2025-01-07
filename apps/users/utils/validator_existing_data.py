from rest_framework.response import Response
from rest_framework import status


def validate_existing_data(model, user):
    try:
        # Obtiene los datos del modelo
        model.objects.get(user=user)
        # Respuesta de error en la validación de los datos del usuario
        return Response({
            'status': 'errors',
            'message': 'Validation failed.',
            'errors': {
                'user_data': [
                    'User data already exists.'
                ]
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    except model.DoesNotExist:
        # Retorna None si los datos del modelo no existen
        return None