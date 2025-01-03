from django.db import models
from django.contrib.auth.models import AbstractUser


# Define el modelo de usuario
class CustomUser(AbstractUser):
    USER_CHOICES = [
        ('student', 'Student'),
        ('company', 'Company')
    ]
    first_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=255, choices=USER_CHOICES)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
