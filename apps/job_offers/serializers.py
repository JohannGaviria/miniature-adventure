from rest_framework import serializers
from .models import JobOffer
from apps.users.serializers import CompanyResponseSerializer


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
            read_only_fields (list): Campos de solo lectura.
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


class JobOfferResponseSerializer(serializers.ModelSerializer):
    """
    Serializador para la respuesta de los datos ofertas de trabajo.
    """
    company = CompanyResponseSerializer(read_only=True)
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (JobOffer): Modelo de oferta de trabajo.
            fields (list): Campos del serializador.
        """
        model = JobOffer
        fields = '__all__'
