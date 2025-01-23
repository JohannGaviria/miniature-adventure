from rest_framework.response import Response
from rest_framework import status


def validate_user_type(user, required_type):
    """
    Valida que el tipo de usuario sea correcto.

    Args:
        user (User): Tipo de usuario a validar.
        required_type (str): Tipo de usuario requerido.
    
    Returns:
        Response: Respuesta de error si el tipo de usuario es incorrecto.
        None: Si el tipo de usuario es correcto.
    """
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
        }, status=status.HTTP_403_FORBIDDEN)
    # Retorna None si el tipo de usuario es correcto
    return None
