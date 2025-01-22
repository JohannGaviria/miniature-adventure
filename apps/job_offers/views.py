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
from apps.core.utils.validate_user_is_creator import validate_user_is_creator
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


# Endpoint para filtrar ofertas de trabajo
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def filter_job_offers(request):
    # Obtiene los parámetros de filtro de la solicitud
    filters = {
        'location__icontains': request.query_params.get('location'),
        'company__name__icontains': request.query_params.get('company'),
        'salary__gte': request.query_params.get('min_salary'),
        'salary__lte': request.query_params.get('max_salary'),
        'requirements__icontains': request.query_params.get('requirements'),
        'work_mode__icontains': request.query_params.get('work_mode'),
        'is_closed': request.query_params.get('is_closed'),
        'created_at__date': request.query_params.get('created_at'),
        'updated_at__date': request.query_params.get('updated_at')
    }

    # Elimina filtros con valores None
    filters = {key: value for key, value in filters.items() if value is not None}

    # Capitaliza el valor booleano de is_closed
    if 'is_closed' in filters:
        filters['is_closed'] = filters['is_closed'].capitalize()

    # Filtrar las ofertas de trabajo según los parámetros proporcionados
    job_offers = JobOffer.objects.filter(**filters).order_by('id')

    # Respuesta de error si no se encontraron ofertas de trabajo
    if not job_offers:
        return Response({
            'status': 'error',
            'message': 'No job offers found with the specified filters.'
        }, status=status.HTTP_404_NOT_FOUND)

    # Crea la paginación de los datos obtenidos
    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(job_offers, request)

    # Serializa los datos de las ofertas de trabajo
    job_offer_response_serializer = JobOfferResponseSerializer(paginated_queryset, many=True)

    # Obtiene la respuesta con los datos paginados
    response_data = paginator.get_paginated_response(job_offer_response_serializer.data)

    # Respuesta exitosa al obtener las ofertas de trabajo filtradas
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


# Endpoint para editar una oferta de trabajo
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_job_offer(request, job_offer_id):
    # Valida que el ID tenga el formato valido
    validation_response = validate_uuid(job_offer_id)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Valida que que el usuario sea tipo compañia
    validation_response = validate_user_type(request.user, 'company')

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
    
    # Valida que el usuario autenticado sea el creador de la oferta de trabajo
    validation_response = validate_user_is_creator(job_offer_data.company, request.user)
    
    # Verifica si hay errores en la validación
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Obtiene los datos enviados en la petición
    job_offer_validation_serializer = JobOfferValidationSerializer(job_offer_data, data=request.data, context={'request': request}, partial=True)

    # Obtiene la validación del serializer
    validation_error = serializer_validation(job_offer_validation_serializer)
    
    # Verifica la validación del serializer
    if validation_error:
        # Respuesta de error en la validación del serializer
        return validation_error

    # Verifica si 'title' está en los datos de la solicitud
    if 'title' in request.data:
        # Si 'title' está presente, entonces validar si la oferta está duplicada
        validation_error = check_duplicate_job_offer(request.data['title'], request.user.company)
        
        # Verifica si hay errores en la validación
        if validation_error:
            # Respuesta de error en la validación de duplicados
            return validation_error

    # Guarda la oferta de trabajo en la base de datos
    job_offer_validation_serializer.save()

    # Respuesta exitosa al editar la oferta de trabajo
    return Response({
        'status': 'success',
        'message': 'Job offer updated successfully.'
    }, status=status.HTTP_200_OK)
