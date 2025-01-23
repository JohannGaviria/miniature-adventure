from rest_framework.response import Response
from rest_framework import status


def serializer_validation(serializer):
    """
    Valida los datos enviados en el serializer.

    Args:
        serializer (Serializer): Serializer a validar.
    
    Returns:
        Response: Respuesta de error si los datos no son válidos.
    """
    # Valida los datos enviados
    if not serializer.is_valid():
        # Retorna un mensaje de error si los datos no son válidos
        return Response({
            'status': 'error',
            'message': 'Validation error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
