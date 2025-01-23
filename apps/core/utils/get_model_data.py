from rest_framework.response import Response
from rest_framework import status

def get_model_data(model, field_name, field_value):
    """
    Obtiene los datos de un modelo basado en un campo y su valor.

    Args:
        model (Model): Modelo a consultar.
        field_name (str): Nombre del campo del modelo.
        field_value (str): Valor de búsqueda para el campo.
    
    Returns:
        data (Model): Datos del modelo si se encuentra.
        Response: Respuesta de error si no se encuentra el registro.
    """
    try:
        # Busca en el modelo el registro que coincide con el campo y valor proporcionados
        data = model.objects.get(**{field_name: field_value})
        return data
    except model.DoesNotExist:
        # Retorna una respuesta de error si no se encuentra el registro
        return Response({
            'status': 'error',
            'message': 'Data not found.'
        }, status=status.HTTP_404_NOT_FOUND)
