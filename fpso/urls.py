"""
Module to define fpso app urls.
"""
from django.urls import path
from django.urls import include

urlpatterns = [
    path('api/v1/', include('fpso.api_v1.urls'))
]
