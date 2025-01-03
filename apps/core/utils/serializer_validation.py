def serializer_validation(serializer):
    """
    Función para validar los datos de un serializador.
    """
    # Valida los datos enviados
    if not serializer.is_valid():
        # Retorna un mensaje de error si los datos no son válidos
        return {
            'status': 'error',
            'message': 'Validation error',
            'errors': serializer.errors
        }
