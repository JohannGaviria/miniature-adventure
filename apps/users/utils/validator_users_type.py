from rest_framework.response import Response
from rest_framework import status


def validate_user_type(user, required_type):
    # Verifica si el tipo de usuario es correcto
    if user.user_type != required_type:
        # Respuesta de error en la validación del tipo de usuario
        return Response({
            'status': 'errors',
            'message': 'Validation failed.',
            'errors': {
                'user_type': [
                    'User type is invalid.'
                ]
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    # Retorna None si el tipo de usuario es correcto
    return None
