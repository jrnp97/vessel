from django.urls import path

from rest_framework_simplejwt.views import token_verify
from rest_framework_simplejwt.views import token_refresh
from rest_framework_simplejwt.views import token_obtain_pair

urlpatterns = [
    path('token/', token_obtain_pair, name='jwt_auth'),
    path('token/verify/', token_verify, name='jwt_verify'),
    path('token/refresh/', token_refresh, name='jwt_refresh'),
]