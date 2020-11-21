"""
Module to define models serializers for manage api display structure and logic.
"""
from rest_framework import serializers

from fpso.models import Vessel
from fpso.models import Equipment


class VesselSerializer(serializers.ModelSerializer):
    """ Class to manage api data structure """

    class Meta:
        model = Vessel
        fields = [
            'code',
            'created_at',
        ]


class EquipmentSerializer(serializers.ModelSerializer):
    """ Class to manage api data structure """
    code = serializers.CharField(
        max_length=50,
        allow_blank=False,
        trim_whitespace=True,
    )

    class Meta:
        model = Equipment
        fields = [
            'code',
            'name',
            'location',
            'vessel',
            'created_at',
        ]

    def active_inactive_equipment(self, code, vessel):
        if not isinstance(code, str) or not code:
            return None
        equipment = vessel.equipment.filter(code=code.strip(), active=False)
        if not equipment.exists():
            return None
        _id = equipment[0].id
        equipment.update(active=True)
        return self.__class__(Equipment.objects.get(id=_id))


class MassiveVesselEquipmentSerializer(serializers.Serializer):
    """ Serializer Object to Clean Equipment Code Array for bulk inactive """
    codes = serializers.ListField(
        child=serializers.CharField(
            max_length=50,
            allow_blank=False,
            trim_whitespace=True,
        ),
        required=True,
        allow_empty=False,
    )
