from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.job_offers.urls')),
    path('api/', include('apps.postulations.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
