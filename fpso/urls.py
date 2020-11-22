"""
Module to define fpso app urls.
"""
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

app_name = 'fpso'
urlpatterns = [
    path('',
         TemplateView.as_view(
             template_name='fpso/index.html',
         ),
         name='index',
    ),
    path('api/v1/', include('fpso.api_v1.urls', namespace='fpso_api_v1'))
]
