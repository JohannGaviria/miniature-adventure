from rest_framework.response import Response
from rest_framework import status


def validate_user_is_creator(element, user):
    """
    Valida que el usuario sea el creador del elemento.

    Args:
        element (Model): Elemento a validar.
        user (User): Usuario autenticado.
    
    Returns:
        Response: Respuesta de error si el usuario no es el creador.
        None: Si el usuario es el creador.
    """
    # Verifica que el usuario sea el creador
    if element.user != user:
        # Retorna un mensaje de error si el usuario no es el creador
        return Response({
            'status': 'error',
            'message': 'The user is not the creator.'
        }, status=status.HTTP_403_FORBIDDEN)
    # Retorna None si el usuario es el creador
    return None
