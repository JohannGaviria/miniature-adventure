from rest_framework import serializers
from .models import Postulation


class PostulationValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validación de postulaciones.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Postulation): Modelo de postulación.
            fields (list): Campos del serializador.
            read_only_fields (list): Campos de solo lectura.
        """
        model = Postulation
        fields = '__all__'
        read_only_fields = ['student', 'job_offer']


    def create(self, validated_data):
        """
        Crea una nueva postulación con los datos validados.
        """
        # Asigna el usuario autenticado al campo estudiante
        validated_data['student'] = self.context['request'].user.student
        # Asigna la oferta de trabajo al campo oferta de trabajo
        validated_data['job_offer'] = self.context['job_offer']
        return super().create(validated_data)

