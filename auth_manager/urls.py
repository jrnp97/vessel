from django.urls import path
from django.urls import include

app_name = 'auth_manager'
urlpatterns = [
    path('api/v1/', include('auth_manager.api_v1.urls')),
]
