from django.contrib import admin

# Register your models here.
from fpso.models import Vessel
from fpso.models import Equipment


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    pass


@admin.register(Equipment)
class EquipementAdmin(admin.ModelAdmin):
    pass

