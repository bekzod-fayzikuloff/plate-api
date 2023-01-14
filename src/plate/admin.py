from django.contrib import admin

from .models import Plate, PlateArea


@admin.register(PlateArea)
class PlateAreaAdmin(admin.ModelAdmin):
    search_fields = ["code", "region"]


@admin.register(Plate)
class PlateAdmin(admin.ModelAdmin):
    list_filter = ["plate_area__region"]
    search_fields = ["plate_area__region", "plate_number"]
