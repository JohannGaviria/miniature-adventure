import uuid
from rest_framework.response import Response
from rest_framework import status


def validate_uuid(uuid_str):
    """
    Valida si una cadena es un UUID válido.

    Args:
        uuid_str (str): La cadena que se va a validar como UUID.

    Returns:
        Response: Respuesta con un error si no es un UUID válido, None si es válido.
    """
    try:
        uuid.UUID(uuid_str)
    except ValueError:
        return Response({
            'status': 'error',
            'message': f'"{uuid_str}" is not a valid UUID.'
        }, status=status.HTTP_400_BAD_REQUEST)
    return None
