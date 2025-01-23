from django.urls import path
from . import views


urlpatterns = [
    path('postulations/postulate/<str:job_offer_id>', views.postulate_job_offer, name='postulate_job_offer'),
    path('postulations/withdraw/<str:job_offer_id>', views.withdraw_postulation, name='withdraw_postulation'),
    path('postulations/get/<str:job_offer_id>', views.get_postulations, name='get_postulations'),
    path('postulations/accept_reject/<str:job_offer_id>', views.accept_reject_postulation, name='accept_reject_postulation'),
]
