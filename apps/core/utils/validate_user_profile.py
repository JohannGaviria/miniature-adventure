from rest_framework.response import Response
from rest_framework import status


def validate_user_profile(request, type_user):
    """
    Valida que el usuario tenga un perfil asociado.
    
    Args:
        request (request): La solicitud del usuario.
        type_user (str): Tipo de usuario.
        
    Returns:
        Response: Respuesta con error si el perfil no existe.
        None: Si el usuario tiene un perfil asociado.
    """
    # Verifica si el usuario tiene un perfil de estudiante asociado
    if not hasattr(request, type_user):
        # Repuesta de error en la validación
        return Response({
            'status': 'error',
            'message': 'The user does not have a profile created.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # Retorna None si la validación es correcta
    return None
