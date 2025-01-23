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


# Define el modelo de estudiante
class Student(models.Model):
    university = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    graduation_year = models.IntegerField()
    professional_experience = models.TextField()
    cv = models.URLField(max_length=500, null=True, blank=True)
    about_me = models.TextField()
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


# Define el modelo de compañia
class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)