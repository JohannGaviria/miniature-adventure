from django.urls import path
from . import views


urlpatterns = [
    path('postulations/postulate/<str:job_offer_id>', views.postulate_job_offer, name='postulate_job_offer'),
]
