from django.urls import path
from . import views


urlpatterns = [
    path('job-offers/create', views.create_job_offer, name='create_job_offer'),
    path('job-offers/get/<str:job_offer_id>', views.get_job_offer, name='get_job_offer'),
]
