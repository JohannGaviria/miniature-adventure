from rest_framework.response import Response
from rest_framework import status


def validate_existing_data(model, user):
    """
    Validación de los datos existentes del usuario.

    Args:
        model (Model): Modelo a validar.
        user (User): Tipo de usuario a validar.
    
    Returns:
        Response: Respuesta de error si los datos del usuario ya existen.
        None: Si los datos del usuario no existen.
    """
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