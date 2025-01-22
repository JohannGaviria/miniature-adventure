from django.urls import path
from . import views


urlpatterns = [
    path('job_offers/create', views.create_job_offer, name='create_job_offer'),
    path('job_offers/get/<str:job_offer_id>', views.get_job_offer, name='get_job_offer'),
    path('job_offers/all', views.get_all_job_offers, name='get_all_job_offers'),
    path('job_offers/filter', views.filter_job_offers, name='filter_job_offers'),
    path('job_offers/update/<str:job_offer_id>', views.update_job_offer, name='update_job_offer'),
]
