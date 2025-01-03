from django.urls import path
from . import views


urlpatterns = [
    path('users/register', views.register, name='register'),
    path('users/login', views.login, name='login'),
    path('users/logout', views.logout, name='logout'),
    path('users/update', views.update_user, name='update_user'),
]