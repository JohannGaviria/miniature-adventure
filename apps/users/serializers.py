from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, Student


# Serializador para la validacion de los datos de usuario
class UserValidationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=CustomUser.USER_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'user_type']
    

    def validate_email(self, value):
        """
        Valida que el correo electronico sea unico.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(f"This email {value} is already in use.")
        return value
    

    def validate_password(self, value):
        """
        Valida que la contraseña sea segura.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)    
        return value
    

    def create(self, validated_data):
        """
        Crea un nuevo usuario con los datos validados.
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


# Serializador para la respuesta de usuario
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_type', 'date_joined', 'last_login']


# Serializador para la validacion de los datos de estudiante
class StudentValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        # Asigna el usuario autenticado al campo user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
