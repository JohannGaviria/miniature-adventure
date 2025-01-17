from rest_framework import serializers
from .models import JobOffer


class JobOfferValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validacion de los datos de ofertas de trabajo
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (JobOffer): Modelo de oferta de trabajo.
            fields (list): Campos del serializador.
        """
        model = JobOffer
        fields = '__all__'
        read_only_fields = ['company']


    def create(self, validated_data):
        """
        Crea una nueva oferta de trabajo con los datos validados.

        Args:
            validated_data (dict): Datos validados de la oferta de trabajo.
        
        Returns:
            JobOffer: Nueva oferta de trabajo creada.
        """
        # Asigna el usuario autenticado al campo user
        validated_data['company'] = self.context['request'].user.company
        return super().create(validated_data)