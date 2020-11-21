"""
Module to define api endpoint logic - viewsets -
"""
from django.http import QueryDict

from rest_framework import status
from rest_framework.decorators import action

from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import RetrieveModelMixin

from fpso.models import Vessel

from fpso.api_v1.serializers import VesselSerializer
from fpso.api_v1.serializers import EquipmentSerializer
from fpso.api_v1.serializers import MassiveVesselEquipmentSerializer


class EquipmentNestedViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    """ ViewSet to manage request process for use on equipment action with vessel_obj """
    vessel_obj = None
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        """ Override method to only return equipment of vessel specified. """
        return self.vessel_obj.equipment.filter(active=True)

    def insert_vessel_on_request_data(self, request):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['vessel'] = self.vessel_obj.id
            request.data._mutable = False
        else:
            request.data['vessel'] = self.vessel_obj.id

    def create(self, request, *args, **kwargs):
        """ Override method to set specified vessel on creation information """
        self.insert_vessel_on_request_data(request)
        serializer = self.get_serializer()
        equipment_serializer = serializer.active_inactive_equipment(
            code=request.data.get('code'),
            vessel=self.vessel_obj,
        )
        if equipment_serializer:
            return Response(equipment_serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        serializer = MassiveVesselEquipmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        codes = serializer.data['codes']
        self.vessel_obj.equipment.filter(code__in=codes).update(active=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VesselViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    """ Class to manage api request for manage vessel resource and its equipments """
    queryset = Vessel.objects.all()
    lookup_field = 'code'
    serializer_class = VesselSerializer

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def equipment(self, request, code=None):
        """ Method to allow manage equipment using nested hierarchy """
        view_set = EquipmentNestedViewSet(
            request=request,
            format_kwarg=None,
            vessel_obj=self.get_object()
        )
        methods = {
            'GET': 'list',
            'POST': 'create',
            'DELETE': 'destroy',
        }
        return getattr(view_set, methods[request.method])(request)
