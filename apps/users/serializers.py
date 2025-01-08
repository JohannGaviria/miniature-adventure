from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, Student


class UserValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validacion de los datos de usuario.
    """
    first_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=CustomUser.USER_CHOICES, required=True)

    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (CustomUser): Modelo de usuario personalizado.
            fields (list): Campos del serializador.
        """
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'user_type']
    

    def validate_email(self, value):
        """
        Valida que el correo electrónico no esté en uso.

        Args:
            value (str): Correo electrónico del usuario.
        
        Returns:
            str: Correo electrónico del usuario.
        
        Raises:
            serializers.ValidationError: Si el correo electrónico ya está en uso.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(f"This email {value} is already in use.")
        return value
    

    def validate_password(self, value):
        """
        Valida la contraseña del usuario.

        Args:
            value (str): Contraseña del usuario.
        
        Returns:
            str: Contraseña del usuario.
        
        Raises:
            serializers.ValidationError: Si la contraseña no cumple con las reglas de validación.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)    
        return value
    

    def create(self, validated_data):
        """
        Crea un nuevo usuario con los datos validados.

        Args:
            validated_data (dict): Datos validados del usuario.
        
        Returns:
            CustomUser: Nuevo usuario creado.
        """
        user = CustomUser(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserResponseSerializer(serializers.ModelSerializer):
    """
    Serializador para la respuesta de usuario.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (CustomUser): Modelo de usuario personalizado.
            fields (list): Campos del serializador.
        """
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_type', 'date_joined', 'last_login']


class StudentValidationSerializer(serializers.ModelSerializer):
    """
    Serializador para la validación de los datos del estudiante.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Student): Modelo de estudiante.
            fields (list): Campos del serializador.
            read_only_fields (list): Campos de solo lectura.
        """
        model = Student
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        """
        Crea un nuevo estudiante con los datos validados.

        Args:
            validated_data (dict): Datos validados del estudiante.
        
        Returns:
            Student: Nuevo estudiante creado.
        """
        # Asigna el usuario autenticado al campo user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class StudentResponseSerializer(serializers.ModelSerializer):
    """
    Serializador para la respuesta de los datos del estudiante.
    """
    class Meta:
        """
        Metadatos del serializador.

        Attributes:
            model (Student): Modelo de estudiante.
            fields (list): Campos del serializador.
        """
        model = Student
        fields = '__all__'
