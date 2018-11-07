from django.urls import path
from .views import RegisterUsers, RegisterAdminUsers

urlpatterns = [
    path('auth/register/', RegisterUsers.as_view(), name='register'),
    path('auth/register/admin/', RegisterAdminUsers.as_view(), name='admin'),
]
