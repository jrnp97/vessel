"""
Module to define api endpoints
"""

from rest_framework.routers import SimpleRouter

from fpso.api_v1.viewsets import VesselViewSet

router = SimpleRouter()
router.register(prefix=r'vessels', viewset=VesselViewSet, basename='vessel')

urlpatterns = router.urls
