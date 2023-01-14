import uuid

from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict

from plate.utils import generate_plate_area, generate_plate_number

from .models import Plate
from .serializers import PlateReadSerializer
from .validators import validate_amount_qs


def generate_plate(plate_amount_qs: int | str) -> list[dict]:
    validated_amount = validate_amount_qs(plate_amount_qs)
    return [{"plate": generate_plate_number(), "area": generate_plate_area()} for _ in range(validated_amount)]


def get_plate(plate_id: uuid.UUID) -> ReturnDict:
    plate = get_object_or_404(Plate, pk=plate_id)
    return PlateReadSerializer(plate).data
