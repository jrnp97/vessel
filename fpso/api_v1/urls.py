"""
Module to define api endpoints
"""
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view

from fpso.api_v1.viewsets import VesselViewSet

router = SimpleRouter()
router.register(prefix=r'vessels', viewset=VesselViewSet, basename='vessel')

app_name = 'fpso_api_v1'
urlpatterns = [
    path(
        'docs/',
        TemplateView.as_view(
            template_name='redoc.html',
            extra_context={'schema_static': 'fpso/openapi-schema_v1.yml'}
        ),
        name='redoc',
    ),
]

urlpatterns.extend(router.urls)
