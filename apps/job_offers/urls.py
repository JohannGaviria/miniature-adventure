from django.urls import path
from . import views


urlpatterns = [
    path('job-offer/create', views.create_job_offer, name='create_job_offer'),
]
