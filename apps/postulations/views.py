from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.core.utils.validate_uuid import validate_uuid
from apps.core.utils.validator_user_type import validate_user_type
from apps.core.utils.validate_user_profile import validate_user_profile
from apps.core.utils.get_model_data import get_model_data
from apps.core.utils.serializer_validation import serializer_validation
from apps.core.utils.validate_user_is_creator import validate_user_is_creator
from apps.core.utils.custom_pagination import CustomPageNumberPagination
from apps.job_offers.models import JobOffer
from .serializers import PostulationValidationSerializer, PostulationsResponseSerializer
from .models import Postulation
from config.settings.base import REST_FRAMEWORK


# Endpoint para la postulación a una oferta de trabajo
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def postulate_job_offer(request, job_offer_id):
    # Valida que el ID tenga el formato valido
    validation_response = validate_uuid(job_offer_id)

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Valida que el usuario autenticado sea de tipo estudiante
    validation_response = validate_user_type(request.user, 'student')

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Valida que el usuario autenticado tenga un perfil de estudiante asociado
    validation_response = validate_user_profile(request.user, 'student')

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Obtiene los datos de la oferta de trabajo
    job_offer_data = get_model_data(JobOffer, 'id', job_offer_id)

    # Verifica si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(job_offer_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return job_offer_data

    # Valida que la oferta de trabajo no este cerrada
    if job_offer_data.is_closed == True:
        # Respuesta de error al intentar postular a una oferta de trabajo cerrada
        return Response({
            'status': 'error',
            'message': 'The job offer is closed'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Valida que el usuario no haya postulado a la oferta de trabajo
    if Postulation.objects.filter(job_offer_id=job_offer_id, student=request.user.student).exists():
        # Respuesta de error al intentar postular a una oferta de trabajo a la que ya se postulo
        return Response({
            'status': 'error',
            'message': 'You have already applied to this job offer'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Obtiene los datos enviados en la peticion
    postulation_validation_serializer = PostulationValidationSerializer(data=request.data, context={'request': request, 'job_offer': job_offer_data})

    # Obtiene la validacion del serializer
    validation_error = serializer_validation(postulation_validation_serializer)

    # Verifica si hay errores en la validacion
    if validation_error:
        # Retorna la respuesta de error
        return validation_error

    # Guarda la postulacion a la oferta de trabajo
    postulation_validation_serializer.save()

    # Respuesta exitosa al crear la postulacion
    return Response({
        'status': 'success',
        'message': 'Postulation created successfully'
    }, status=status.HTTP_201_CREATED)


# Endpoint para retirar la postulación a una oferta de trabajo
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def withdraw_postulation(request, job_offer_id):
    # Valida que el ID tenga el formato valido
    validation_response = validate_uuid(job_offer_id)

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Valida que el usuario autenticado sea de tipo estudiante
    validation_response = validate_user_type(request.user, 'student')

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Valida que el usuario autenticado tenga un perfil de estudiante asociado
    validation_response = validate_user_profile(request.user, 'student')

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response
    
    # Obtiene los datos de la oferta de trabajo
    job_offer_data = get_model_data(JobOffer, 'id', job_offer_id)

    # Verifica si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(job_offer_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return job_offer_data

    # Valida que la oferta de trabajo no este cerrada
    if job_offer_data.is_closed == True:
        # Respuesta de error al intentar retirar la postulacion a una oferta de trabajo cerrada
        return Response({
            'status': 'error',
            'message': 'The job offer is closed'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Valida que el usuario haya postulado a la oferta de trabajo
    if not Postulation.objects.filter(job_offer_id=job_offer_id, student=request.user.student).exists():
        # Respuesta de error al intentar retirar la postulacion a una oferta de trabajo a la que no se ha postulado
        return Response({
            'status': 'error',
            'message': 'You have not applied to this job offer'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Elimina la postulacion a la oferta de trabajo
    Postulation.objects.filter(job_offer_id=job_offer_id, student=request.user.student).delete()

    # Respuesta exitosa al retirar la postulacion
    return Response({
        'status': 'success',
        'message': 'Postulation withdrawn successfully'
    }, status=status.HTTP_200_OK)


# Endpoint para obtener las postulaciones a una oferta de trabajo
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_postulations(request, job_offer_id):
    # Valida que el ID tenga el formato valido
    validation_response = validate_uuid(job_offer_id)

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # - Validar que el usuario autenticado sea de tipo compañia

    # Valida que el usuario autenticado sea de tipo compañia
    validation_response = validate_user_type(request.user, 'company')

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # - Validar que el usuario autenticado tenga un perfil de compañia asociado

    # Valida que el usuario autenticado tenga un perfil de compañia asociado
    validation_response = validate_user_profile(request.user, 'company')

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # - Obtener los datos de la oferta de trabajo

    # Obtiene los datos de la oferta de trabajo
    job_offer_data = get_model_data(JobOffer, 'id', job_offer_id)

    # Verifica si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(job_offer_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return job_offer_data

    # - Validar que la oferta de trabajo pertenezca a la compañia del usuario autenticado

    # Valida que la oferta de trabajo pertenezca a la compañia del usuario autenticado
    validation_response = validate_user_is_creator(job_offer_data.company, request.user)

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # - Obtener las postulaciones a la oferta de trabajo

    # Obtiene las postulaciones a la oferta de trabajo
    postulations = Postulation.objects.filter(job_offer=job_offer_id).order_by('id')

    # - Serializar los datos de las postulaciones

    # Serializa los datos de las postulaciones

    # Crea la paginacion de los datos obtenidos
    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(postulations, request)

    # Serializa los datos de las ofertas de trabajo
    postulation_response_serializer = PostulationsResponseSerializer(paginated_queryset, many=True)

    # Obtiene la respuesta con los datos paginados
    response_data = paginator.get_paginated_response(postulation_response_serializer.data)

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
            'postulations': response_data['results']
        }
    }, status=status.HTTP_200_OK)


# Endpoint para aceptar o rechazar una postulación a una oferta de trabajo
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def accept_reject_postulation(request, job_offer_id):
    # Valida que el ID de la oferta de trabajo tenga el formato valido
    validation_response = validate_uuid(job_offer_id)

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Valida que el usuario autenticado sea de tipo compañia
    validation_response = validate_user_type(request.user, 'company')

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Valida que el usuario autenticado tenga un perfil de compañia asociado
    validation_response = validate_user_profile(request.user, 'company')

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Obtiene los datos de la oferta de trabajo
    job_offer_data = get_model_data(JobOffer, 'id', job_offer_id)

    # Verifica si se obtuvo una respuesta de error en lugar de los datos
    if isinstance(job_offer_data, Response):
        # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
        return job_offer_data

    # Valida que la oferta de trabajo pertenezca a la compañia del usuario autenticado
    validation_response = validate_user_is_creator(job_offer_data.company, request.user)

    # Verifica si hay errores en la validacion
    if validation_response:
        # Retorna la respuesta de error
        return validation_response

    # Obtiene la lista de postulaciones de la solicitud
    postulations = request.data

    # Itera sobre cada postulación en la lista
    for postulation in postulations:
        # Valida que el ID de la postulación tenga el formato valido
        validation_response = validate_uuid(postulation.get('id'))

        # Verifica si hay errores en la validacion
        if validation_response:
            # Retorna la respuesta de error
            return validation_response

        # Obtiene los datos de la postulación
        postulation_data = get_model_data(Postulation, 'id', postulation.get('id'))

        # Verifica si se obtuvo una respuesta de error en lugar de los datos
        if isinstance(postulation_data, Response):
            # Si se obtuvo una respuesta de error, retornar directamente esa respuesta
            return postulation_data

        # Obtiene la acción (aceptar o rechazar) de la solicitud
        action = postulation.get('status')

        # Verifica que la acción sea válida
        if action not in ['accept', 'reject']:
            return Response({
                'status': 'error',
                'message': 'Invalid action. Action must be "accept" or "reject".'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Actualiza el estado de la postulación
        postulation_data.status = 'accepted' if action == 'accept' else 'rejected'
        postulation_data.save()

    # Respuesta exitosa al aceptar o rechazar las postulaciones
    return Response({
        'status': 'success',
        'message': 'Postulations status successfully applied.'
    }, status=status.HTTP_200_OK)
