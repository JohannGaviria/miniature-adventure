from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.core.utils.validator_user_type import validate_user_type
from apps.core.utils.serializer_validation import serializer_validation
from apps.core.utils.validate_user_profile import validate_user_profile
from apps.core.utils.get_model_data import get_model_data
from apps.core.utils.validate_uuid import validate_uuid
from apps.core.utils.custom_pagination import CustomPageNumberPagination
from .serializers import JobOfferValidationSerializer, JobOfferResponseSerializer
from .models import JobOffer
from .utils.check_duplicate_job_offer import check_duplicate_job_offer
from config.settings.base import REST_FRAMEWORK


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


# Endpoint para obtener una oferta de trabajo
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_job_offer(request, job_offer_id):
    # Valida que el ID tenga el formato valido
    validation_response = validate_uuid(job_offer_id)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Obtener los datos de la oferta de trabajo
    job_offer_data = get_model_data(JobOffer, 'id', job_offer_id)

    # Verifica si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(job_offer_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return job_offer_data

    # Serializar los datos de respuesta de la oferta de trabajo
    job_offer_response_serializer = JobOfferResponseSerializer(job_offer_data)

    # Respuesta exitosa al obtener la oferta de trabajo
    return Response({
        'status': 'success',
        'message': 'Job offer was successfully obtained.',
        'data': {
            'job_offer': job_offer_response_serializer.data
        }
    }, status=status.HTTP_200_OK)


# Endpoint para obtener todas las ofertas de trabajo
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_job_offers(request):
    # Obtener todas las ofertas de trabajo
    job_offers = JobOffer.objects.all().order_by('id')

    # Crea la paginacion de los datos obtenidos
    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(job_offers, request)

    # Serializa los datos de las ofertas de trabajo
    job_offer_response_serializer = JobOfferResponseSerializer(paginated_queryset, many=True)

    # Obtiene la respuesta con los datos paginados
    response_data = paginator.get_paginated_response(job_offer_response_serializer.data)

    # Respuesta exitosa al obtener las ofertas de trabajo
    return Response({
        'status': 'success',
        'message': 'The job offers were successfully obtained.',
        'data': {
            'page_info': {
                'count': response_data['count'],
                'page_size': int(request.query_params.get('page_size', REST_FRAMEWORK['PAGE_SIZE'])),
                'links': response_data['links']
            },
            'job_offers': response_data['results']
        }
    }, status=status.HTTP_200_OK)
