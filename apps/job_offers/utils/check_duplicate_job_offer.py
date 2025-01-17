from rest_framework.response import Response
from rest_framework import status
from apps.job_offers.models import JobOffer


def check_duplicate_job_offer(title, user):
    """
    Chequea si ya existe una oferta de trabajo con el mismo título
    para el usuario actual.
    
    Args:
        title (str): Titulo de la oferta de trabajo.
        user (User): Usuario que intenta crear la oferta.

    Raises:
        ValidationError: Si ya existe una oferta similar para el usuario.
    """
    
    # Comprobamos si ya existe una oferta con el mismo título asociada al usuario
    if JobOffer.objects.filter(title=title, company=user).exists():
        return Response({
            'status': 'error',
            'message': 'There is already a job offer with a similar title for this user.'
        }, status=status.HTTP_400_BAD_REQUEST)
    return None
