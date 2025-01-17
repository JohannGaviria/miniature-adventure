from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.core.utils.validator_user_type import validate_user_type
from apps.core.utils.serializer_validation import serializer_validation
from apps.core.utils.validate_user_profile import validate_user_profile
from .serializers import JobOfferValidationSerializer
from .models import JobOffer
from .utils.check_duplicate_job_offer import check_duplicate_job_offer
from apps.users.models import Company


# Endpoint para crear una oferta de trabajo
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_job_offer(request):
    # Valida que el usuario tenga un perfil de compañia asociado
    validation_response = validate_user_profile(request.user, 'company')

    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Valida que el usuario autenticado sea de tipo compañia
    validation_response = validate_user_type(request.user, 'company')
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Obtiene los datos enviados en la petición
    job_offer_validation_serializer = JobOfferValidationSerializer(data=request.data, context={'request': request})

    # Obtiene la validación del serializer
    validation_error = serializer_validation(job_offer_validation_serializer)
    
    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return validation_error

    # Valida si hay oferta duplicadas para el usuario
    validation_error = check_duplicate_job_offer(request.data['title'], request.user.company)

    # Verifica si hay errores en la validación
    if validation_error:
        # Respuesta de error en la validación
        return validation_error
    
    # Guarda la oferta de trabajo en la base de datos
    job_offer_validation_serializer.save()

    # Respuesta exitosa al crear la oferta de trabajo
    return Response({
        'status': 'success',
        'message': 'Job offer created successfully.',
    }, status=status.HTTP_201_CREATED)
