from django.urls import path
from . import views


urlpatterns = [
    path('users/register', views.register, name='register'),
    path('users/login', views.login, name='login'),
    path('users/logout', views.logout, name='logout'),
    path('users/update', views.update_user, name='update_user'),
    path('users/delete', views.delete_user, name='delete_user'),
    path('users/student/add', views.add_student_data, name='add_student_data'),
    path('users/student/get', views.get_student_data, name='get_student_data'),
    path('users/student/update', views.update_student_data, name='update_student_data'),
    path('users/company/add', views.add_company_data, name='add_company_data'),
]