from django.db import models
from uuid import uuid4
from apps.users.models import Company


# Define el modelo de oferta de trabajo
class JobOffer(models.Model):
    WORK_MODE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=150)
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
