from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Plate, PlateArea
from .resources import PLATE_ACCESS_AREA


class PlateAddSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    plate_area = serializers.ChoiceField(
        choices=[(area["code"], area["region"]) for area in PLATE_ACCESS_AREA], write_only=True
    )

    class Meta:
        model = Plate
        fields = ("id", "plate_number", "plate_area")

    def create(self, validated_data):
        access_areas = list(filter(lambda item: item['code'] == f'{validated_data["plate_area"]}', PLATE_ACCESS_AREA))
        if not access_areas:
            raise ValidationError("Provide not supported access area")
        plate_area = access_areas.pop()
        validated_data["plate_area"], _ = PlateArea.objects.get_or_create(**plate_area)
        return super().create(validated_data)


class PlateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plate
        fields = "__all__"
        depth = 1
